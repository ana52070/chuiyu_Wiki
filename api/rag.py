"""
rag.py - SiliconFlow 版本
向量检索 + DeepSeek/Qwen 生成回答
"""

import os
import requests

SUPABASE_URL    = os.environ["SUPABASE_URL"]
SUPABASE_KEY    = os.environ["SUPABASE_KEY"]
SILICONFLOW_KEY = os.environ["SILICONFLOW_KEY"]

EMBED_MODEL = "BAAI/bge-m3"
CHAT_MODEL  = "deepseek-ai/DeepSeek-V3"
TOP_K       = 5


def get_embedding(text: str) -> list[float]:
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
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()["data"][0]["embedding"]


def search_documents(query_embedding: list[float]) -> list[dict]:
    url = f"{SUPABASE_URL}/rest/v1/rpc/match_documents"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "query_embedding": query_embedding,
        "match_count": TOP_K,
        "match_threshold": 0.5,
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def generate_answer(question: str, contexts: list[dict]) -> str:
    if not contexts:
        return "我在知识库中没有找到相关内容，请尝试换个问法，或者这个话题还没有被记录进来。"

    context_text = "\n\n---\n\n".join([
        f"【来源：{c.get('file_path', '未知')}】\n{c['content']}"
        for c in contexts
    ])

    prompt = f"""你是吹雨的个人知识库助手，帮助主人检索和整理他的知识笔记。

下面是从知识库中检索到的相关内容：

{context_text}

---

请根据以上知识库内容，回答主人的问题。要求：
1. 回答要简洁、准确，直接基于知识库内容
2. 如果知识库内容不足以完整回答，请说明哪些部分有记录、哪些没有
3. 适当指出内容来源（哪个文章/笔记）
4. 用中文回答

主人的问题：{question}"""

    url = "https://api.siliconflow.cn/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {SILICONFLOW_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": CHAT_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.3,
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def query(question: str) -> str:
    try:
        embedding = get_embedding(question)
        contexts  = search_documents(embedding)
        return generate_answer(question, contexts)
    except Exception as e:
        return f"处理时出现错误：{str(e)}"