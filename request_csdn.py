import requests
from bs4 import BeautifulSoup
import html2text
import os
import time
import re

# ================= 配置区域 =================
CSDN_ID = "chui_yu666"  # 你的 CSDN ID
TARGET_DIR = "./blog"   # 文章保存目录
# ===========================================

# 伪装成浏览器，防止被反爬
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_article_list(user_id):
    """获取用户所有文章链接"""
    links = []
    page = 1
    print(f"🕷️ 开始扫描用户 {user_id} 的文章列表...")
    
    while True:
        url = f"https://blog.csdn.net/{user_id}/article/list/{page}"
        try:
            resp = requests.get(url, headers=HEADERS)
            if resp.status_code != 200:
                break
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            article_list = soup.find_all('div', class_='article-item-box')
            
            if not article_list:
                break # 没有更多文章了
            
            found_new = False
            for item in article_list:
                link_tag = item.find('a')
                if link_tag:
                    href = link_tag['href']
                    # 过滤掉非文章链接
                    if "/article/details/" in href:
                        links.append(href)
                        found_new = True
            
            if not found_new:
                break
                
            print(f"   已扫描第 {page} 页，累计发现 {len(links)} 篇文章")
            page += 1
            time.sleep(10) # 礼貌爬虫，歇一秒
            
        except Exception as e:
            print(f"❌ 扫描列表出错: {e}")
            break
            
    # 去重
    return list(set(links))

def parse_article(url):
    """解析单篇文章内容"""
    try:
        resp = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # 1. 获取标题
        title_tag = soup.find('h1', id='articleContentId')
        title = title_tag.get_text().strip() if title_tag else "无标题文章"
        
        # 2. 获取发布时间
        date_tag = soup.find('span', class_='time')
        date = date_tag.get_text().strip() if date_tag else ""
        # 简单处理日期格式，只取 YYYY-MM-DD
        if " " in date:
            date = date.split(" ")[0]
            
        # 3. 获取正文 HTML
        content_div = soup.find('div', id='content_views')
        if not content_div:
            return None
            
        # 4. 转换为 Markdown
        # 配置 html2text
        converter = html2text.HTML2Text()
        converter.ignore_links = False
        converter.ignore_images = False
        converter.body_width = 0 # 不自动换行
        converter.protect_links = True
        
        markdown_content = converter.handle(str(content_div))
        
        return {
            "title": title,
            "date": date,
            "content": markdown_content,
            "url": url
        }
    except Exception as e:
        print(f"❌ 解析文章失败 {url}: {e}")
        return None

def save_to_markdown(data):
    """保存为 MD 文件"""
    # 清理文件名中的非法字符
    safe_title = re.sub(r'[\\/*?:"<>|]', "", data['title'])
    safe_title = safe_title.replace(" ", "_") # 空格转下划线
    
    filename = f"{safe_title}.md"
    filepath = os.path.join(TARGET_DIR, filename)
    
    # 构建 Frontmatter (VitePress 需要的头部)
    frontmatter = f"""---
title: {data['title']}
date: {data['date']}
tags: [CSDN搬运]
---

# {data['title']}

> 原文链接：[{data['title']}]({data['url']})

{data['content']}
"""
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
    
    print(f"✅ 已保存: {filename}")

def main():
    # 1. 确保目录存在
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        
    # 2. 获取所有链接
    article_links = get_article_list(CSDN_ID)
    print(f"📊 总共找到 {len(article_links)} 篇文章，准备开始搬运...\n")
    
    # 3. 遍历下载
    for i, link in enumerate(article_links):
        print(f"[{i+1}/{len(article_links)}] 正在处理: {link}")
        article_data = parse_article(link)
        if article_data:
            save_to_markdown(article_data)
            time.sleep(15) # 每篇文章间隔 1.5 秒，防止 IP 被封
            
    print("\n🎉 全部搬运完成！快去运行 npm run docs:dev 看看效果吧！")

if __name__ == "__main__":
    main()