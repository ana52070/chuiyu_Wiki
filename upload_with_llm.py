import os
import subprocess
import sys
import datetime
import requests
from dotenv import load_dotenv

# 加载 .env 环境变量
load_dotenv()

# ================= 配置区域 =================
# 代理端口 (Clash常见端口 7890/7897)
PROXY_PORT = "7897" 
REMOTE_REPO = "origin"
BRANCH = "main"

# LLM 配置
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-lite-preview-02-05:free")
MAX_DIFF_LENGTH = 4000  # 截断长度，防止超出 Token 限制
# ===========================================

def get_proxy_config():
    """生成 requests 库需要的代理字典"""
    if PROXY_PORT:
        proxy_url = f"http://127.0.0.1:{PROXY_PORT}"
        return {
            "http": proxy_url,
            "https": proxy_url
        }
    return None

def run_command(command, use_proxy=False, return_output=False):
    """运行系统命令，支持代理设置，强制使用UTF-8编码处理输出"""
    env = os.environ.copy()
    
    if use_proxy and PROXY_PORT:
        proxy_url = f"http://127.0.0.1:{PROXY_PORT}"
        # print(f"🔌 使用代理: {proxy_url}")
        env["http_proxy"] = proxy_url
        env["https_proxy"] = proxy_url
        env["ALL_PROXY"] = f"socks5://127.0.0.1:{PROXY_PORT}"

    # 设置 Python IO 编码，防止 Windows 下打印报错
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,          # 以文本形式处理
            encoding='utf-8',   # 关键修改：强制使用 UTF-8 解码
            errors='replace',   # 关键修改：遇到无法解码的字符用 ? 代替，防止崩溃
            env=env
        )
        
        if return_output:
            # 确保返回的是字符串，防止 None
            return result.stdout.strip() if result.stdout else ""
            
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        # 命令执行失败（比如 git 报错）
        if not return_output:
            print(f"❌ 命令执行错误: {e.stderr}")
        return False
    except Exception as e:
        # 其他 Python 层面错误（比如之前遇到的解码错误，虽然上面修复了，但保留作为兜底）
        print(f"❌ 系统错误: {e}")
        return False

def generate_commit_message(diff_content):
    """调用 OpenRouter API 生成 Commit Message"""
    if not OPENROUTER_API_KEY:
        print("⚠️ 未检测到 OPENROUTER_API_KEY，将使用默认时间戳信息。")
        return None

    print("🤖 正在请求 LLM 生成提交描述...")

    # 截断处理
    if len(diff_content) > MAX_DIFF_LENGTH:
        print(f"⚠️ Diff 内容过长 ({len(diff_content)} 字符)，已截断至前 {MAX_DIFF_LENGTH} 字符...")
        diff_content = diff_content[:MAX_DIFF_LENGTH] + "\n...[Diff Truncated]..."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost", # OpenRouter 要求字段
    }

    # 提示词工程：强制要求 Conventional Commits 格式
    system_prompt = (
        "你是一个代码提交专家。请根据提供的 git diff 内容生成一个简洁的 Git Commit Message。\n"
        "要求：\n"
        "1. 使用标准 Conventional Commits 格式 (例如: feat: ..., fix: ..., docs: ...)。\n"
        "2. 使用中文。\n"
        "3. 即使有多个更改，也请总结为一个主要的一句话标题，不要分行，不要使用 Markdown 代码块。\n"
        "4. 语气客观、直接。"
    )

    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Git Diff Content:\n{diff_content}"}
        ]
    }

    try:
        # 使用 requests 调用，并应用代理配置
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=data,
            headers=headers,
            proxies=get_proxy_config(), # 这里让 API 请求也走代理
            timeout=30 # 防止请求卡死
        )
        response.raise_for_status()
        result = response.json()
        
        message = result['choices'][0]['message']['content'].strip()
        # 清理可能产生的额外引号或反引号
        message = message.replace('`', '').strip('"').strip("'")
        print(f"✨ LLM 生成建议: {message}")
        return message

    except Exception as e:
        print(f"⚠️ LLM 生成失败: {e}")
        return None

def git_sync():
    print("🚀 开始同步知识库...")
    
    # 1. Git Add
    print("Stage 1: 添加文件 (git add)...")
    if not run_command("git add ."): return

    # 2. 获取 Diff 并准备 Commit Message
    # 优先检查是否有命令行参数传入
    if len(sys.argv) > 1:
        commit_msg = sys.argv[1]
    else:
        # 获取暂存区的差异 (git diff --cached)
        # 注意：此时文件已经 add 了，所以要用 --cached 才能看到差异
        diff_output = run_command("git diff --cached", return_output=True)
        
        if not diff_output:
            print("⚠️ 检测到暂存区为空 (没有文件变化)，跳过提交。")
            # 也可以选择在这里直接 push，防止本地落后
            commit_msg = None
        else:
            # 尝试使用 LLM 生成
            commit_msg = generate_commit_message(diff_output)
            
            # 如果 LLM 失败，回退到时间戳
            if not commit_msg:
                commit_msg = f"Auto update: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # 3. Git Commit
    if commit_msg:
        print(f"Stage 2: 提交更改 (git commit) -> '{commit_msg}'...")
        # 使用双引号包裹 message 防止 shell 错误
        run_command(f'git commit -m "{commit_msg}"')
    else:
        print("Stage 2: 无需提交 (No changes).")

    # 4. Git Push
    print("Stage 3: 推送到云端 (git push)...")
    
    # 先尝试直连
    print("   Trying direct connection...")
    success = run_command(f"git push {REMOTE_REPO} {BRANCH}")
    
    # 如果直连失败且配置了代理，尝试走代理
    if not success and PROXY_PORT:
        print("\n⚠️ 直连失败，尝试切换代理通道重试...")
        success = run_command(f"git push {REMOTE_REPO} {BRANCH}", use_proxy=True)
    
    if success:
        print("\n✅ 同步成功！你的知识库已更新。")
    else:
        print("\n❌ 同步失败，请检查网络或 Git 配置。")

if __name__ == "__main__":
    git_sync()