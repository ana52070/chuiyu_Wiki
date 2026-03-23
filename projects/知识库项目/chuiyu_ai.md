---
title: 'chuiyu_ai'
date: '2026-03-23 14:00:58'
categories:
  - '软件项目'
tags:
  - 'GitHub'
permalink: '/projects/chuiyu-ai'
repo: 'ana52070/chuiyu_ai'
description: '基于微信聊天语料构建的「个性化回复生成」项目： 通过历史对话抽取你的回复风格，结合向量检索（RAG）与大模型生成，用于企业微信 webhook 自动回复。'
homepage: 'https://chuiyu-ai.vercel.app'
stars: 1
language: 'Python'
license: ''
created_at: '2026-03-02T16:36:07Z'
updated_at: '2026-03-02T17:37:45Z'
topics:
  - '暂无'
---

# chuiyu_ai

- 仓库：[https://github.com/ana52070/chuiyu_ai](https://github.com/ana52070/chuiyu_ai)
- Star：1
- 主语言：Python
- README 来源：`README.md` (分支：`main`)

---

# chuiyu_ai

基于微信聊天语料构建的「个性化回复生成」项目：  
通过历史对话抽取你的回复风格，结合向量检索（RAG）与大模型生成，用于企业微信 webhook 自动回复。

## 功能概览

- 微信导出聊天数据转换为训练/检索数据集
- 构建两类向量索引
- `style_index`：风格语料检索
- `reply_index`：历史回复示例检索
- 离线回放评估（多候选生成 + 规则打分）
- Vercel Serverless webhook 接入企业微信，在线回复

## 技术栈

- Python 3.10+
- Node.js 18+
- hnswlib / numpy / requests / openai / python-dotenv
- Vercel Functions（`api/webhook.js`）

## 项目结构

```text
.
├─ api/
│  └─ webhook.js                 # Vercel webhook 入口
├─ convert_wechat_export.py      # 微信导出数据 -> jsonl 数据集
├─ build_style_index.py          # 构建风格索引
├─ build_reply_index.py          # 构建回复示例索引
├─ npy_to_json.py                # 导出 reply vectors.json（供 JS 端检索）
├─ replay_rag.py                 # 离线回放评估
├─ llm_client.py                 # LLM/Embedding 统一调用
├─ scorer.py                     # 候选回复打分规则
├─ data_io.py                    # JSONL 读写
└─ upload_with_llm.py            # 可选：自动生成 commit message + push
```

## 快速开始

### 1. 安装依赖

Python 依赖（当前仓库未提供 `requirements.txt`，可先手动安装）：

```bash
pip install numpy hnswlib tqdm requests python-dotenv openai
```

Node 依赖：

```bash
npm install
```

### 2. 配置环境变量

在项目根目录创建 `.env`（请替换为你自己的值）：

```env
# Python 侧（llm_client.py / replay_rag.py / build_*）
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=your_api_key
CHAT_MODEL=gpt-4o-mini
EMBED_MODEL=text-embedding-3-small

# upload_with_llm.py（可与上面共用）
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini

# Vercel webhook（api/webhook.js）
WXWORK_CORP_ID=xxx
WXWORK_AGENT_ID=1000002
WXWORK_SECRET=xxx
WXWORK_TOKEN=xxx
WXWORK_AES_KEY=xxx
SILICONFLOW_KEY=xxx
VPS_PROXY_URL=http://your-proxy-host:8080
```

### 3. 数据处理

将微信导出的 JSON 转换为本项目数据格式：

```bash
python convert_wechat_export.py --input your_wechat_export.json --outdir . --gap 60 --max_context 12
```

会生成：

- `turn_pairs.jsonl`
- `user_bubbles.jsonl`
- `style_stats.json`

### 4. 构建索引

```bash
python build_style_index.py
python build_reply_index.py
python npy_to_json.py
```

预期产物：

- `style_index/hnsw.index`
- `style_index/meta.npy`
- `reply_index/hnsw.index`
- `reply_index/meta.npy`
- `reply_index/vectors.json`

### 5. 离线回放验证（可选）

```bash
python replay_rag.py
```

用于随机抽样对话，检查检索质量和生成风格一致性。

### 6. 部署到 Vercel

```bash
vercel
```

部署后将企业微信回调地址配置到 `api/webhook.js` 对应的路由（通常为 `/api/webhook`），并在 Vercel 项目中配置上述环境变量。

## 运行机制（简述）

1. 企业微信消息回调到 `/api/webhook`
2. 服务端验签并解密消息
3. 对用户消息做 embedding
4. 在 `reply_index/vectors.json` 中做本地相似检索
5. 将检索示例 + 对话上下文喂给模型生成短气泡回复
6. 质量过滤后按“类真人节奏”分条发送

## 开源建议

- 仓库已忽略 `.env`、`dataset.json`、`__pycache__`，但你仍应检查是否包含隐私聊天数据
- 建议在公开前移除或脱敏：
- `turn_pairs.jsonl`
- `user_bubbles.jsonl`
- `style_stats.json`
- 建议补充 `LICENSE`（如 MIT）以明确开源许可

## 免责声明

本项目仅用于技术研究与个人效率场景。请确保数据来源、隐私处理、消息自动化行为符合平台条款与当地法律法规。
