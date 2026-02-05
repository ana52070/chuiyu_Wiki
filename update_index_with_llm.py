import os
import glob
import re
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

# 配置信息
API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL")
MODEL = os.getenv("LLM_MODEL")

# 检查配置
if not API_KEY:
    print("❌ 错误: 未在 .env 文件中找到 LLM_API_KEY。")
    print("请确保已创建 .env 文件并配置了 LLM_API_KEY, LLM_BASE_URL, LLM_MODEL。")
    exit(1)

# 初始化 OpenAI 客户端
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def get_directory_content(directory, line_limit=50):
    """
    读取指定目录下的所有 .md 文件（排除 index.md），提取前 N 行内容。
    """
    files_data = []
    # 递归查找所有 .md 文件
    search_pattern = os.path.join(directory, "**", "*.md")
    files = glob.glob(search_pattern, recursive=True)
    
    print(f"📂 正在扫描 {directory} 目录...")
    
    for file_path in files:
        # 排除 index.md 自身
        if os.path.basename(file_path).lower() == "index.md":
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # 读取前 N 行
                lines = [next(f) for _ in range(line_limit)]
                content = "".join(lines)
                
                # 获取相对路径，用于生成链接
                # 在 Windows 上，路径分隔符可能是 \，需要统一为 /
                rel_path = os.path.relpath(file_path, directory).replace("\\", "/")
                
                files_data.append(f"--- 文件名: {rel_path} ---\n{content}\n--- 文件结束 ---\n")
                print(f"  ✅ 读取: {rel_path}")
        except StopIteration:
            # 文件行数少于 limit，读取全部
             with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                rel_path = os.path.relpath(file_path, directory).replace("\\", "/")
                files_data.append(f"--- 文件名: {rel_path} ---\n{content}\n--- 文件结束 ---\n")
                print(f"  ✅ 读取: {rel_path}")
        except Exception as e:
            print(f"  ⚠️ 无法读取 {file_path}: {e}")

    return "\n".join(files_data)

def generate_summary(content, section_name):
    """
    调用 LLM 生成总结内容。
    """
    print(f"🤖 正在请求 AI 生成 {section_name} 的导读...")
    
    prompt = f"""
    你是一个专业的知识库管理员。请根据以下提供的 Markdown 文件内容片段（包含 Frontmatter 和正文前几行），为 "{section_name}" 板块生成一个**带简介的导读列表**。

    **要求：**
    1.  **格式**：使用 Markdown 列表格式。
    2.  **内容**：每一项包含文章标题（带链接）和一句话的简短摘要（基于文件内容总结）。
    3.  **链接**：链接地址必须使用提供的相对路径（例如 `[标题](./相对路径)`）。
    4.  **风格**：简洁、专业、吸引人。
    5.  **排序**：如果能从内容中判断出重要性或时间，按推荐顺序排列；否则按逻辑分类排列。
    6.  **输出限制**：只输出 Markdown 内容，不要包含 "好的"、"这是结果" 等废话。

    **待处理文件内容：**
    {content}
    """

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "你是一个帮助整理知识库索引的 AI 助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ AI 请求失败: {e}")
        return None

def update_index_file(directory, new_content):
    """
    更新 index.md 文件中的 AI 内容区域。
    """
    index_path = os.path.join(directory, "index.md")
    
    if not os.path.exists(index_path):
        print(f"❌ 错误: 找不到 {index_path}")
        return

    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        # 定义标记
        start_marker = "<!-- AI_CONTENT_START -->"
        end_marker = "<!-- AI_CONTENT_END -->"

        # 使用正则表达式查找标记区域
        pattern = re.compile(f"({re.escape(start_marker)})(.*?)({re.escape(end_marker)})", re.DOTALL)
        
        if not pattern.search(original_content):
            print(f"❌ 错误: 在 {index_path} 中未找到标记区域。")
            print(f"请确保文件中包含 {start_marker} 和 {end_marker}")
            return

        # 替换内容
        updated_content = pattern.sub(f"\\1\n\n{new_content}\n\n\\3", original_content)

        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
            
        print(f"✨ 成功更新 {index_path}")

    except Exception as e:
        print(f"❌ 更新文件失败: {e}")

def main():
    print("========================================")
    print("   📚 知识库索引自动更新助手 (AI Powered)")
    print("========================================")
    
    options = {
        "1": "blog",
        "2": "guide",
        "3": "projects"
    }
    
    print("请选择要更新的目录：")
    for key, value in options.items():
        print(f"  [{key}] {value}")
    
    choice = input("\n请输入选项 (1-3): ").strip()
    
    if choice not in options:
        print("❌ 无效选项，程序退出。")
        return

    target_dir = options[choice]
    
    # 1. 获取目录内容
    files_content = get_directory_content(target_dir, line_limit=50)
    
    if not files_content:
        print("⚠️ 该目录下没有找到有效的 .md 文件。")
        return

    # 2. 生成总结
    ai_summary = generate_summary(files_content, target_dir)
    
    if ai_summary:
        # 3. 更新 index.md
        update_index_file(target_dir, ai_summary)
        print("\n✅ 任务完成！")

if __name__ == "__main__":
    main()