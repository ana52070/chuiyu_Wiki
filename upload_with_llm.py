import os
import subprocess
import sys
import datetime
import math
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 环境变量
load_dotenv()

# ================= 配置区域 =================
# 代理端口 (Clash常见端口 7890/7897)
PROXY_PORT = "7897" 
REMOTE_REPO = "origin"
BRANCH = "main"

# LLM 配置
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")

if not LLM_API_KEY:
    print("Error: LLM_API_KEY not found in .env.")
    print("Please set LLM_API_KEY, LLM_BASE_URL, LLM_MODEL in .env.")
    sys.exit(1)

client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)

# Token 限制配置
MAX_TOTAL_CHARS = 4000  # 发送给 LLM 的最大字符数

# 关注内容的白名单后缀 (只有这些文件会读取 Diff 内容)
TEXT_EXTENSIONS = {
    '.md', '.txt', '.markdown',           # 文档
    '.py', '.js', '.ts', '.jsx', '.tsx',  # 脚本
    '.vue', '.html', '.css', '.scss',     # 前端
    '.json', '.yaml', '.yml', '.toml',    # 配置
    '.sh', '.bat', '.gitignore'           # 其他文本
}
# ===========================================

def run_command(command, use_proxy=False, return_output=False):
    """运行系统命令，支持代理设置，强制使用UTF-8编码处理输出"""
    env = os.environ.copy()
    
    if use_proxy and PROXY_PORT:
        proxy_url = f"http://127.0.0.1:{PROXY_PORT}"
        env["http_proxy"] = proxy_url
        env["https_proxy"] = proxy_url
        env["ALL_PROXY"] = f"socks5://127.0.0.1:{PROXY_PORT}"

    # 设置 Python IO 编码
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,          
            encoding='utf-8',   
            errors='replace',   
            env=env
        )
        
        if return_output:
            return result.stdout.strip() if result.stdout else ""
            
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        if not return_output:
            print(f"❌ 命令执行错误: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ 系统错误: {e}")
        return False

def get_smart_diff():
    """
    智能获取 Diff 内容：
    1. 获取所有变动文件列表。
    2. 如果是白名单文件，读取 git diff 内容。
    3. 如果是资源文件，只记录文件名。
    4. 执行"保小压大"的截断策略。
    """
    # 获取暂存区的文件列表
    file_list_str = run_command("git diff --cached --name-only", return_output=True)
    if not file_list_str:
        return None
    
    files = file_list_str.split('\n')
    processed_diffs = []
    
    print(f"🔍 检测到 {len(files)} 个文件变化，正在分析...")

    # 1. 收集原始数据
    for file_path in files:
        if not file_path.strip(): continue
        
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in TEXT_EXTENSIONS:
            # 读取具体代码差异
            diff_content = run_command(f'git diff --cached "{file_path}"', return_output=True)
            if not diff_content:
                diff_content = f"[Changed] {file_path}"
            processed_diffs.append({
                "type": "text",
                "path": file_path,
                "content": diff_content,
                "length": len(diff_content)
            })
        else:
            # 非文本文件，只记录文件名
            msg = f"[Resource Updated] {file_path}"
            processed_diffs.append({
                "type": "resource",
                "path": file_path,
                "content": msg,
                "length": len(msg)
            })

    # 没有任何有效文件时提前返回
    if not processed_diffs:
        return None

    # 2. 智能截断逻辑 (Dynamic Average Truncation)
    total_len = sum(d['length'] for d in processed_diffs)
    
    if total_len <= MAX_TOTAL_CHARS:
        # 如果总长度未超限，直接合并返回
        final_output = "\n".join([d['content'] for d in processed_diffs])
    else:
        print(f"⚠️ Diff 总长 ({total_len}) 超过限制 ({MAX_TOTAL_CHARS})，执行智能压缩...")
        
        avg_quota = MAX_TOTAL_CHARS / len(processed_diffs)
        
        small_files = []
        large_files = []
        used_quota = 0
        
        for d in processed_diffs:
            if d['length'] <= avg_quota:
                small_files.append(d)
                used_quota += d['length']
            else:
                large_files.append(d)

        remaining_quota = MAX_TOTAL_CHARS - used_quota
        remaining_quota = max(remaining_quota, len(large_files) * 100) 
        
        large_file_quota = int(remaining_quota / len(large_files)) if large_files else 0
        
        final_parts = []
        
        for d in small_files:
            final_parts.append(d['content'])
            
        for d in large_files:
            half_quota = int(large_file_quota / 2) - 20
            content = d['content']
            truncated_content = (
                f"--- File: {d['path']} (Truncated) ---\n"
                f"{content[:half_quota]}\n"
                f"\n...[Skipped {len(content) - large_file_quota} chars]...\n"
                f"{content[-half_quota:]}\n"
            )
            final_parts.append(truncated_content)
            
        final_output = "\n".join(final_parts)

    return final_output

def generate_commit_message(diff_content):
    """Call ModelScope (OpenAI-compatible) API to generate Commit Message"""
    print("Requesting LLM to generate commit message...")

    system_prompt = (
        "You are a codebase maintainer. Generate a Commit Message based on the provided git diff.\n"
        "**Input Notes**:\n"
        "- The input may include code/doc changes.\n"
        "- The input may include `[Resource Updated] filename` for binary assets.\n"
        "- Long files may be truncated; infer intent from visible parts.\n\n"
        "**Output Requirements**:\n"
        "1. **Format**: Conventional Commits (e.g., `docs: update deploy guide`, `feat: add sync script`, `assets: add architecture image`).\n"
        "2. **Language**: Chinese.\n"
        "3. **Strategy**:\n"
        "   - If mainly docs, describe the updated knowledge points.\n"
        "   - If assets were added, mention them.\n"
        "   - Summarize into a single concise line; no Markdown code blocks."
    )

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Git Changes Summary:\n{diff_content}"}
            ],
            temperature=0.7,
        )

        print(f"DEBUG response: {response}")  # 加这一行

        if not response or not response.choices:
            print("LLM returned empty response.")
            return None

        content = response.choices[0].message.content
        if not content:
            print("LLM returned empty content.")
            return None

        message = content.strip().replace('`', '').strip('"').strip("'")
        print(f"LLM suggestion: {message}")
        return message

    except Exception as e:
        print(f"LLM request failed: {e}")
        return None
    

def git_sync():
    print("🚀 开始同步知识库...")
    
    # 1. Git Add
    print("Stage 1: 添加文件 (git add)...")
    if not run_command("git add ."): return

    # 2. 获取 Diff 并准备 Commit Message
    if len(sys.argv) > 1:
        commit_msg = sys.argv[1]
    else:
        # 使用新的智能 Diff 获取函数
        diff_output = get_smart_diff()
        
        if not diff_output:
            print("⚠️ 检测到暂存区为空 (没有文件变化)，跳过提交。")
            commit_msg = None
        else:
            commit_msg = generate_commit_message(diff_output)
            
            if not commit_msg:
                commit_msg = f"Auto update: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # 3. Git Commit
    if commit_msg:
        print(f"Stage 2: 提交更改 (git commit) -> '{commit_msg}'...")
        run_command(f'git commit -m "{commit_msg}"')
    else:
        print("Stage 2: 无需提交 (No changes).")

    # 4. Git Push
    print("Stage 3: 推送到云端 (git push)...")
    print("   Trying direct connection...")
    success = run_command(f"git push {REMOTE_REPO} {BRANCH}")
    
    if not success and PROXY_PORT:
        print("\n⚠️ 直连失败，尝试切换代理通道重试...")
        success = run_command(f"git push {REMOTE_REPO} {BRANCH}", use_proxy=True)
    
    if success:
        print("\n✅ 同步成功！你的知识库已更新。")
    else:
        print("\n❌ 同步失败，请检查网络或 Git 配置。")

if __name__ == "__main__":
    git_sync()