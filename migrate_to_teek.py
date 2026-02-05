import os
import re
import yaml
import time
from datetime import datetime

# 目标文件夹列表
TARGET_DIRS = ["blog", "guide", "projects"]

def get_file_creation_time(file_path):
    """获取文件的创建时间并格式化为 Teek 要求的字符串"""
    stat = os.stat(file_path)
    # 优先取创建时间，如果系统不支持则取修改时间
    ctime = getattr(stat, 'st_birthtime', stat.st_mtime)
    return datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')

def fix_frontmatter():
    print("🚀 开始为 Teek 主题深度重构文章头部信息...")
    
    for root_dir in TARGET_DIRS:
        if not os.path.exists(root_dir):
            continue
            
        for root, dirs, files in os.walk(root_dir):
            # 排除 assets 目录
            if 'assets' in dirs:
                dirs.remove('assets')
            
            for file in files:
                if not file.endswith(".md") or file == "index.md": # 排除首页
                    continue
                
                file_path = os.path.join(root, file)
                
                # 计算分类：以父目录名作为分类
                parent_folder = os.path.basename(root)
                category = parent_folder if parent_folder not in TARGET_DIRS else "随笔"

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 分离 Frontmatter
                match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
                
                fm = {}
                body = content
                
                if match:
                    fm_text = match.group(1)
                    body = match.group(2)
                    try:
                        fm = yaml.safe_load(fm_text) or {}
                    except Exception as e:
                        print(f"⚠️ 解析错误 {file}: {e}")
                else:
                    # 如果没有头部，body 就是全部内容
                    body = content

                # --- 开始深度重构 ---
                
                # 1. 标题 (Title)
                if 'title' not in fm:
                    fm['title'] = file.replace('.md', '')

                # 2. 日期 (Date) - Teek 排序的核心
                if 'date' not in fm:
                    fm['date'] = get_file_creation_time(file_path)

                # 3. 永久链接 (Permalink)
                # 格式：/目录/文件名（去后缀）
                if 'permalink' not in fm:
                    rel_path = os.path.relpath(file_path, os.getcwd()).replace('\\', '/')
                    fm['permalink'] = '/' + rel_path.replace('.md', '')

                # 4. 分类与标签 (Categories & Tags)
                # 强制覆盖为列表格式，确保 Teek 侧边栏能识别
                fm['categories'] = [category]
                fm['tags'] = [category] # 默认将分类也作为标签，你可以手动修改

                # 5. 清理多余字段 (可选，如果想删除旧脚本留下的其他垃圾字段可以加在这里)
                # fm.pop('old_tag', None) 

                # 重新生成 Frontmatter
                # sort_keys=False 保证字段顺序不会乱
                new_fm = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)
                new_content = f"---\n{new_fm}---\n{body}"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ 已适配: {file_path} -> 分类: {category}")

    print("\n🎉 适配完成！现在运行 npm run docs:dev，你应该能看到文章出现在分类和归档里了。")

if __name__ == "__main__":
    try:
        fix_frontmatter()
    except ImportError:
        print("❌ 请先运行: pip install pyyaml")