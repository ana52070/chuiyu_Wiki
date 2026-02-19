"""
index_wiki.py - SiliconFlow 版本
将仓库中所有 .md 文件向量化并存入 Supabase
用法: python index_wiki.py
"""

import os
import re
import time
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

# ── 配置 ──────────────────────────────────────────────
SUPABASE_URL    = os.environ["SUPABASE_URL"]
SUPABASE_KEY    = os.environ["SUPABASE_KEY"]
SILICONFLOW_KEY = os.environ["SILICONFLOW_KEY"]

INDEX_DIRS = ["blog", "guide", "projects"]

CHUNK_SIZE    = 800
CHUNK_OVERLAP = 100

EMBED_MODEL = "BAAI/bge-m3"
# ──────────────────────────────────────────────────────


def find_md_files(root: str = ".") -> list:
    files = []
    for d in INDEX_DIRS:
        dir_path = Path(root) / d
        if dir_path.exists():
            files.extend(dir_path.rglob("*.md"))
    return sorted(files)


def extract_frontmatter(content: str):
    meta = {}
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            fm = content[3:end].strip()
            for line in fm.splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    meta[k.strip()] = v.strip().strip('"').strip("'")
            content = content[end + 3:].strip()
    return meta, content


def split_chunks(text: str) -> list:
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        if end < len(text):
            last_para = chunk.rfind("\n\n")
            if last_para > CHUNK_SIZE // 2:
                end = start + last_para
                chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end - CHUNK_OVERLAP
    return [c for c in chunks if len(c) > 50]


def embed(text: str) -> Optional[list]:
    """调用 SiliconFlow Embedding API"""
    url = "https://api.siliconflow.cn/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {SILICONFLOW_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": EMBED_MODEL,
        "input": text[:2000],
        "encoding_format": "float",
    }
    for attempt in range(3):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            return resp.json()["data"][0]["embedding"]
        except Exception as e:
            print(f"  ⚠ Embedding 第 {attempt+1} 次失败: {e}")
            time.sleep(2 ** attempt)
    return None


def supabase_request(method: str, path: str, **kwargs):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    return requests.request(method, url, headers=headers, **kwargs)


def delete_file_chunks(file_path: str):
    supabase_request(
        "DELETE", f"documents?file_path=eq.{requests.utils.quote(file_path)}"
    )


def insert_chunks(rows: list):
    resp = supabase_request("POST", "documents", json=rows)
    if resp.status_code not in (200, 201):
        print(f"  ✗ 插入失败: {resp.text}")
    else:
        print(f"  ✓ 插入 {len(rows)} 个块")


def index_file(path: Path, repo_root: str = "."):
    rel_path = str(path.relative_to(repo_root))
    print(f"\n📄 {rel_path}")

    content = path.read_text(encoding="utf-8")
    meta, body = extract_frontmatter(content)

    body_clean = re.sub(r"```[\s\S]*?```", "", body)
    body_clean = re.sub(r"`[^`]+`", "", body_clean)
    body_clean = re.sub(r"!\[.*?\]\(.*?\)", "", body_clean)
    body_clean = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", body_clean)
    body_clean = re.sub(r"#{1,6}\s", "", body_clean)
    body_clean = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", body_clean)

    chunks = split_chunks(body_clean)
    if not chunks:
        print("  ⚠ 无有效内容，跳过")
        return

    delete_file_chunks(rel_path)

    rows = []
    for i, chunk in enumerate(chunks):
        print(f"  → 块 {i+1}/{len(chunks)} ({len(chunk)} 字符)", end=" ")
        embedding = embed(chunk)
        if embedding is None:
            print("❌ 跳过")
            continue
        rows.append({
            "file_path":   rel_path,
            "chunk_index": i,
            "content":     chunk,
            "embedding":   embedding,
            "metadata": {
                "title": meta.get("title", path.stem),
                "tags":  meta.get("tags", ""),
                "date":  meta.get("date", ""),
            },
        })
        print("✓")
        time.sleep(0.1)

    if rows:
        insert_chunks(rows)


def main():
    print("🚀 开始索引知识库...\n")
    md_files = find_md_files(".")
    print(f"共发现 {len(md_files)} 个 .md 文件")
    for path in md_files:
        index_file(path)
    print("\n\n✅ 索引完成！")


if __name__ == "__main__":
    main()