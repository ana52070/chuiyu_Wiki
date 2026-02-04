import requests
import os
import re
import time

# ================= 配置区域 =================
GITHUB_USER = "ana52070"  # 你的 GitHub 用户名
TARGET_DIR = "./projects" # 保存目录
# ===========================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/vnd.github.v3+json",

}

def get_repos():
    """获取用户的所有原创仓库列表"""
    print(f"🔍 正在连接 GitHub API 获取 {GITHUB_USER} 的仓库列表...")
    repos = []
    page = 1
    
    while True:
        # 每页获取 100 个仓库（GitHub API 限制）
        url = f"https://api.github.com/users/{GITHUB_USER}/repos?type=owner&sort=updated&per_page=100&page={page}"
        try:
            resp = requests.get(url, headers=HEADERS)
            if resp.status_code != 200:
                print(f"❌ 获取列表失败: {resp.status_code} - {resp.text}")
                break
            
            data = resp.json()
            if not data:
                break
                
            for repo in data:
                # 再次确认不是 Fork 的项目
                if not repo.get('fork', False):
                    repos.append(repo)
            
            if len(data) < 100:
                break # 已经拿完所有页了
            page += 1
            
        except Exception as e:
            print(f"❌ 网络错误: {e}")
            break
            
    print(f"✅ 共发现 {len(repos)} 个原创仓库。")
    return repos

def fetch_readme(repo):
    """获取单个仓库的 README 内容"""
    default_branch = repo.get('default_branch', 'main')
    repo_name = repo['name']
    
    # 尝试常见的 README 文件名
    filenames = ['README.md', 'readme.md', 'README.MD']
    
    for fname in filenames:
        # 使用 raw.githubusercontent.com 直接获取原始内容
        raw_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{repo_name}/{default_branch}/{fname}"
        resp = requests.get(raw_url, headers=HEADERS)
        
        if resp.status_code == 200:
            return resp.text, default_branch
            
    return None, None

def process_content(content, repo_name, branch):
    """
    核心功能：正则替换相对路径
    1. 图片 ![]() -> 指向 raw.githubusercontent (直接显示图)
    2. 链接 []()  -> 指向 github.com/blob (点击跳转到 GitHub 查看文件)
    """
    base_raw_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{repo_name}/{branch}/"
    base_blob_url = f"https://github.com/{GITHUB_USER}/{repo_name}/blob/{branch}/"

    def replace_link(match):
        text = match.group(1)
        link = match.group(2)
        
        # 如果已经是 http 开头，或者是锚点(#)，或者是邮件(mailto)，则不修改
        if link.startswith(('http', 'https', '#', 'mailto:')):
            return match.group(0)
        
        # 判断是图片还是普通链接
        is_image = match.group(0).startswith('!')
        
        # 清理路径开头可能的 ./
        clean_link = link.lstrip('./')
        
        if is_image:
            # 图片使用 Raw 链接
            new_url = base_raw_url + clean_link
            return f"![{text}]({new_url})"
        else:
            # 普通文件链接使用 Blob 链接 (网页浏览视图)
            new_url = base_blob_url + clean_link
            return f"[{text}]({new_url})"

    # 正则替换 Markdown 链接格式 [text](link) 和 ![text](link)
    # 注意：这个正则比较简单，处理不了特别复杂的嵌套括号，但对 README 够用了
    new_content = re.sub(r'(!?\[.*?\])\((.*?)\)', replace_link, content)
    return new_content

def save_readme(repo, content, branch):
    """保存为本地 Markdown 文件"""
    repo_name = repo['name']
    desc = repo.get('description') or "暂无描述"
    updated_at = repo.get('updated_at', '').split('T')[0]
    
    # 处理内容中的相对链接
    processed_content = process_content(content, repo_name, branch)
    
    # 构建 Frontmatter
    frontmatter = f"""---
title: {repo_name}
date: {updated_at}
author: {GITHUB_USER}
tags: [GitHub项目]
description: {desc}
---

# {repo_name}

> 项目地址：[{repo['html_url']}]({repo['html_url']})
> 
> {desc}

---

{processed_content}
"""
    
    file_path = os.path.join(TARGET_DIR, f"{repo_name}.md")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
    print(f"💾 已保存: {repo_name}.md")

def main():
    # 1. 创建目录
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"📁 创建目录: {TARGET_DIR}")

    # 2. 获取列表
    repos = get_repos()
    
    # 3. 遍历下载
    print("🚀 开始批量拉取 README...")
    success_count = 0
    
    for repo in repos:
        print(f"   正在处理: {repo['name']} ...")
        content, branch = fetch_readme(repo)
        
        if content:
            save_readme(repo, content, branch)
            success_count += 1
        else:
            print(f"   ⚠️ 跳过: {repo['name']} (未找到 README)")
        
        time.sleep(5) # 礼貌爬虫
        
    print(f"\n🎉 全部完成！成功拉取 {success_count} 个项目的文档。")
    print("👉 别忘了检查 .vitepress/config.mts 里的 sidebar 配置，确保 projects 目录能显示出来！")

if __name__ == "__main__":
    main()