---
title: codex的使用笔记及心得
author: chuiyu
date: 2026-02-26 08:00:00
description: codex的使用笔记及心得
tags:
  - ai
permalink: /pages/d509f7
categories:
  - blog
  - ai
---
## 设置中文回复

默认 Codex 以英文回复，但国内用户更爱中文。临时命令如“用简体中文回复”有效，但重启失效。推荐使用 Codex 记忆文件 AGENTS.md 永久设置。

### 全局设置步骤：
1. 在终端执行：

```bash
   mkdir -p ~/.codex && printf 'Always respond in Chinese-simplified\n' > ~/.codex/AGENTS.md
```

2. 重启终端，运行 `codex`，输入查询如 “解释这个 Python 函数”，Codex 将始终用简体中文回应。


### 工作空间设置：

若只限当前项目，运行 `/init` 生成 AGENTS.md，然后编辑添加 “Always respond in Chinese-simplified”。

此配置提升 Codex 中文支持，让 AI 编程更亲切。测试：问 “如何优化 SQL 查询？”，回复将全中文。