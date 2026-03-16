# OpenClaw CLI 命令行上手与常用命令速查（Mac / Linux）

> 参考来源：Kerry Zheng 的学习笔记《openclaw_command_tutorial》
> <https://github.com/Formyselfonly/openclaw_command_tutorial>
>
> 我在原文基础上做了：结构梳理 + 命令分组 + 常见坑点补充 + 我自己的使用建议（更贴近“日常用 OpenClaw 做事/排障”）。

---

## 0. OpenClaw 到底是什么（用一句话讲清楚）

OpenClaw 是一个 **AI Agent Runtime（智能体运行时）**：你把 LLM 当“大脑”，把 Skills/Tools 当“手脚”，OpenClaw Gateway 负责把二者接起来，并提供日志、配置、任务调度等运行支撑。

典型链路：

LLM → Agent → Skills(工具) → 真实动作（文件/浏览器/消息/设备/自动化…）

---

## 1. 安装（CLI）

### 1.1 brew（macOS / Linux）

```bash
brew install openclaw
openclaw --version
```

### 1.2 一键安装脚本（macOS / Linux）

```bash
curl -fsSL https://install.openclaw.ai | bash
openclaw --version
```

> 建议：安装后先跑一次 `openclaw --version`，确认 PATH 正常。

---

## 2. 第一次初始化（onboard）

```bash
openclaw onboard
```

如果你要装成系统后台服务（daemon），一般是：

```bash
openclaw onboard --install-daemon
```

我的建议：**学习阶段别急着 daemon**。前台跑最容易看日志、看报错、改完就重启，迭代速度快。

---

## 3. Gateway 的两种运行方式：前台 vs daemon

### 3.1 前台（学习/开发推荐）

```bash
openclaw gateway
# 或指定端口
openclaw gateway --port 18789
```

特点：终端关了就停；但调试最舒服。

### 3.2 daemon（生产/常驻）

适合：常驻服务器、树莓派、家里小主机等，追求稳定运行。

---

## 4. Daemon 常用命令（后台服务生命周期）

> 这套命令名在很多教程里最容易混淆：你要记住 **daemon 管“后台服务”**，而 **gateway 是“核心运行时进程”**。

```bash
openclaw daemon install
openclaw daemon start
openclaw daemon stop
openclaw daemon status
openclaw daemon restart
openclaw daemon uninstall
```

macOS 背后通常是 launchd；Linux 可能是 systemd（具体实现看 OpenClaw 版本）。

---

## 5. Gateway 管理（核心服务）

### 5.1 启动

```bash
openclaw gateway
openclaw gateway --port 18789
```

### 5.2 安装为 service

```bash
openclaw gateway install
```

### 5.3 停止

```bash
openclaw gateway stop
```

> 提醒：不同版本命令会有差异；如果你遇到子命令不存在，直接跑 `openclaw gateway --help` 以你本机输出为准。

---

## 6. Dashboard（UI）

Gateway 启动后通常访问：

- <http://127.0.0.1:18789>

也可以用：

```bash
openclaw dashboard
```

Dashboard 用来：看 Agent、看 Skills、看 logs、做调试。

---

## 7. 端口/进程排障（最常用的两招）

### 7.1 看端口是否在监听

```bash
lsof -i :18789
```

看到 `LISTEN` 基本就说明 Gateway 起来了。

### 7.2 端口占用 / 杀掉占用进程

```bash
lsof -i :18789
# 记住 PID
kill -9 <PID>
```

我的建议：
- 能优雅停就优雅停（daemon/gateway stop）
- `kill -9` 属于“最后手段”，但确实解决 80% 的“端口卡死”问题

---

## 8. Skills（工具系统）

### 8.1 查看已安装 skills

```bash
openclaw skills list
```

### 8.2 安装 skill

```bash
openclaw skills install browser
```

> 经验：新手最常踩的坑是“装了 skill 但没配置权限/能力”，导致工具调用失败。优先看 logs，再看 skill 的 SKILL.md / 配置项。

---

## 9. 配置（Config）

原文提到配置文件路径：

- `~/.openclaw/config.yaml`

常见修改方式：

```bash
openclaw configure
```

我的补充（更实用）：
- **先查 schema/字段含义**，再改（避免猜字段名）
- 改完一般需要重启 gateway/daemon
- 如果你在 OpenClaw 里跑多个 channel（WhatsApp/Telegram/Discord），配置变更更要谨慎：改坏了可能直接收不到消息

---

## 10. 日志（Logs）

```bash
openclaw logs
openclaw logs -f
```

排障优先级（我自己的习惯）：
1) 先 `-f` 看实时日志
2) 找到报错的 tool/skill/config 字段
3) 再去查对应文档/skill 说明

---

## 11. Doctor（诊断）

```bash
openclaw doctor
```

一般会检查：配置、skills、gateway、MCP 等。

---

## 12. 推荐学习路线（最省时间的顺序）

1) `openclaw gateway`
2) 打开 Dashboard 看状态
3) `openclaw skills list`
4) 装一个常用 skill（比如 browser/web_search）
5) 实际跑一个 agent 任务（比如“抓网页→总结→发消息”）

核心心法：**不要只看文档**，要“边跑边看边改”。

---

## 13. 我对 OpenClaw 的定位（个人看法）

- LangChain 更像“Agent Framework”（搭积木）
- OpenClaw 更像“Agent Runtime”（让积木稳定跑起来 + 对接真实世界）

如果你已经在折腾硬件/网关/ROS2/嵌入式自动化，OpenClaw 的价值很直接：
- 把“工具调用、权限、消息通道、定时任务”这些工程化问题收敛到一个统一运行时
- 你可以把精力花在 **Skill + 业务逻辑** 上，而不是每次都重写 glue code

---

## 14. 附：原文速查（命令清单）

```bash
openclaw gateway
openclaw dashboard
openclaw skills list
openclaw skills install <skill>
openclaw logs -f
openclaw doctor
openclaw daemon start|stop|status|restart
```

---

## 参考链接

- 原仓库：<https://github.com/Formyselfonly/openclaw_command_tutorial>
- OpenClaw Dashboard（默认）：<http://127.0.0.1:18789>
