---
title: OpenClaw部署后权限配置与安全加固教程
author: lunar
date: 2026-03-04 08:00:00
description: OpenClaw 部署完成后的权限配置与安全加固：从最小权限、消息入口、Gateway 暴露、节点配对到命令执行审批
tags:
  - ai
  - openclaw
  - linux
  - security
permalink: /pages/2a0f3e
categories:
  - blog
  - ai
---

# OpenClaw 部署后权限配置与安全加固教程

OpenClaw 部署跑起来只是第一步，后面真正容易踩坑的是 **“权限开到哪里、怎么收口、怎么审计”**。

这篇文章按「**最小可用权限**」的思路，把常见的权限点拆成 5 块：

1. 文件/凭据权限（本机安全）
2. 消息入口权限（谁能找你、能做什么）
3. Gateway 暴露与反向代理（别把控制面板裸奔到公网）
4. Node/设备配对（让 OpenClaw 能触达设备能力）
5. 命令执行与审批（让 AI 能 `ls/git`，但不至于一把梭）

> 以下示例以 Ubuntu + systemd 安装的 OpenClaw 为例。

---

## 0）先跑一遍状态与安全审计

先看现状：

```bash
openclaw status
```

如果你看到类似：

- **CRITICAL Credentials dir is writable by others**
- **WARN State dir is group-writable**

说明你的 OpenClaw 状态目录/凭据目录权限太宽（例如 775），同机其他用户可能篡改凭据文件，这是最高优先级要修的。

---

## 1）修复本机目录权限（强烈建议立刻做）

把 OpenClaw 的状态目录和凭据目录收紧到仅当前用户可读写：

```bash
chmod 700 /home/ubuntu/.openclaw
chmod 700 /home/ubuntu/.openclaw/credentials
```

再检查：

```bash
openclaw status
```

确认 CRITICAL 已消失。

> 解释：`~/.openclaw/credentials` 里通常有渠道登录态、token 等敏感数据。目录可写=别人可以“投毒”放文件进去，后果比可读还严重。

---

## 2）消息入口权限：只让“可信的人”能对话

OpenClaw 的聊天通道（如 WhatsApp）建议默认走 allowlist：

- 只允许你的号码（或极少数号码）
- 群聊默认拒绝（除非你明确要在群里用）

你可以用配置文件（一般在 `~/.openclaw/openclaw.json`）控制，例如：

- `channels.whatsapp.dmPolicy: allowlist`
- `channels.whatsapp.allowFrom: ["+86..."]`
- `channels.whatsapp.groupPolicy: allowlist`

检查当前生效配置文件路径：

```bash
openclaw config file
```

> 思路：**先把“谁能跟 AI 说话”锁住**，再讨论“AI 能做什么”。否则你给了 AI 执行命令的权限，结果任何人都能通过消息入口驱动它，风险直接指数级上升。

---

## 3）Gateway 与 Control UI：默认只在本机回环，不要上公网

`openclaw status` 里会显示 Dashboard：

- `http://127.0.0.1:18789/`

一般建议：

- Gateway `bind=loopback`（仅本机访问）
- 如果一定要从局域网访问，也建议只对内网开放，并设置强 token
- 如果用 Nginx/Caddy 做反代，需要配置 **trusted proxy**，否则日志/来源识别会错，安全策略可能误判

安全审计里常见 WARN：

- **Reverse proxy headers are not trusted**

意思是：如果你把 UI 暴露给反代了，得把反代 IP 加入 `gateway.trustedProxies`（否则不要暴露，保持 loopback 最省心）。

---

## 4）Node / 设备配对：把“能控制的能力”隔离到节点侧

OpenClaw 通常分两层：

- **Gateway**：消息/调度/会话中枢
- **Node**：更靠近设备的能力（截图、屏幕、运行某些设备命令等，具体看你启用了哪些）

如果你要 OpenClaw 触达设备能力，需要启动并配对 Node：

```bash
openclaw node --help
openclaw nodes --help
openclaw devices --help
```

> 注意：不同版本/环境支持的 node 子命令略有差异，按 `--help` 为准。

### 节点命令的“收口”

在配置里通常会有类似：

- `gateway.nodes.denyCommands: [...]`

这是一层粗粒度的“禁用某些危险命令 ID”的措施。

安全审计里也经常提醒：

- **denyCommands 是按“命令名”精确匹配，不是按 shell 文本过滤**

所以不要把它当成“能拦住 rm -rf”那种 WAF；正确做法是：

- 从源头 **不给危险能力**（不允许某些 command IDs）
- 必要时 **要求审批**（见下一节）

---

## 5）命令执行（让 AI 能 `ls/git`）的正确打开方式：最小权限 + 审批

你想要的能力通常分 3 档：

### A. 只读（最安全）
- 允许 `ls`, `cat`, `rg`, `git status/diff/log`
- 只允许在指定目录（比如 wiki 仓库）

### B. 可写（中风险）
- 允许创建/编辑文件（用于写博客、改配置）
- 仍然限制目录范围

### C. 任意执行（高风险，不建议）
- 任意命令、任意目录
- 一旦消息入口被滥用，等于把终端交给了别人

我的建议：先从 **A/B** 开始，再逐步放开。

### 5.1 用 approvals 给“危险执行”加刹车

OpenClaw CLI 里有：

```bash
openclaw approvals --help
```

思路是：

- 对某些执行类动作启用“需要批准”
- 你在 Control UI（或 CLI）里点一下确认
- 平时正常 `ls/git diff` 不打扰你，危险动作才需要你拍板

### 5.2 用 sandbox 把执行环境隔离出来

如果你希望 AI 跑脚本/装依赖，但又不想污染系统，可以考虑：

```bash
openclaw sandbox --help
```

把执行放进隔离环境（容器/沙箱），能显著降低“误操作把系统搞坏”的概率。

---

## 推荐的一套“最小可用”白名单（适合写 wiki/查问题）

目录范围（只允许在）：

- `/home/ubuntu/project/chuiyu_Wiki`（你的 wiki 仓库）

命令白名单（先给这些足够）：

- 文件查看：`ls`, `find`, `cat`, `sed -n`, `head`, `tail`
- 搜索：`rg`（ripgrep）
- Git：`git status`, `git diff`, `git log`, `git show`

暂时不建议直接给：

- `sudo`
- `rm`, `chmod`, `chown`
- `curl | bash`、下载执行类

---

## 附：常用检查清单

- 入口：通道是否 allowlist？群聊是否默认拒绝？
- 本机：`~/.openclaw` 与 `~/.openclaw/credentials` 是否 700？
- UI：Dashboard 是否只在 127.0.0.1？
- 暴露：如果反代，是否正确配置 trusted proxies？
- 节点：node 是否启用？配对是否可撤销？命令是否收口？
- 执行：是否启用 approvals？是否限制目录与白名单？

---

## 写在最后

给 AI 开权限这件事，正确姿势不是“一次性开满”，而是：

- 先锁消息入口
- 再修本机权限
- 然后按任务逐步开放能力
- 能审批就审批，能隔离就隔离

你后续如果愿意，我也可以根据你当前 `~/.openclaw/openclaw.json` 的实际配置，帮你把“白名单目录 + 命令审批”落到可直接执行的一套配置（并且顺带把安全审计里的 WARN 都消掉）。
