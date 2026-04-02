---
author: lunar
date: 2026-04-02
description: Claude Code 每晚微学习计划首页，记录学习方式、文件结构与同步规则。
tags:
  - claude code
  - ai coding
  - learning
  - guide
---

# Claude Code 每晚微学习

这是一个长期、低阻力的 Claude Code 学习计划。

目标不是一次性啃完整本 PDF，而是每天晚上用 2~3 分钟吸收一个小知识点，慢慢建立起完整的 Claude Code 心智模型。

## 学习方式

- 每天晚上 21:30 由 OpenClaw 定时唤醒
- 当天现看上下文、现判断今晚最适合讲的内容
- 不预制整套课程，不机械切片
- 每次只发一个轻量知识点
- 发完后同步更新后台记录与整理版记录

## 文件说明

- `daily-learning-log.md`：面向阅读的整理版总记录
- `backend-log.md`：后台执行版记录，保留更原始的计划轨迹
- `daily/`：按天拆分的每日学习记录，文件名统一使用 `YYYY-MM-DD.md`

## 当前约定

- 时间：每天 21:30（Asia/Shanghai）
- 风格：带一点例子版
- 频率：每天都发
- 策略：动态选题，不预制整套内容

## 更新规则

仅在“当天确实发送了学习内容”之后，才同步更新 Wiki 记录。

更新完成后，按既定工作流执行：

```bash
python3 update_index_with_llm.py
python3 upload_with_llm.py
```
