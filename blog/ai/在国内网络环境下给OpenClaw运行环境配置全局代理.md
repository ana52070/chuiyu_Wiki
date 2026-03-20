---
title: 在国内网络环境下给OpenClaw运行环境配置全局代理
author: lunar
date: 2026-03-04 08:00:00
description: 在国内网络环境下给 OpenClaw 运行环境配置全局代理（HTTP/HTTPS + systemd）
tags:
  - ai
  - openclaw
  - linux
  - proxy
permalink: /pages/31a76d
categories:
  - blog
  - ai
---

# 在国内网络环境下给 OpenClaw 运行环境配置全局代理

> 目的：解决 **OpenClaw（Node.js 常驻进程 + systemd 服务）在国内网络环境下无法正常访问部分网络服务** 的问题。
>
> 参考来源：<https://blog.newnaw.com/?p=1599>

## 背景与思路

OpenClaw 属于 **Node.js 运行时 + 常驻后台服务** 的形态。很多时候你在终端里手动 `curl` 能走代理，并不代表 systemd 启动的服务（比如 openclaw-gateway）也能继承到代理环境变量。

所以这里分两步：

1. 先准备一个 **本机可用的 HTTP 代理**（很多程序不直接支持 SOCKS5，只认 HTTP）。
2. 再把 HTTP/HTTPS 代理 **写到系统与 systemd 的环境变量** 里，确保：
   - 终端命令默认走代理
   - systemd system 级服务走代理
   - systemd user 级服务走代理（OpenClaw gateway 通常跑在这里）

> 提醒：请在遵守法律法规与网络策略的前提下使用。

---

## 1）准备本地 HTTP 代理（示例端口）

文章给的示例：本机同时提供

- SOCKS5：`127.0.0.1:10808`
- HTTP：`127.0.0.1:10809`

（具体代理软件/协议不展开，这里只记录“如何让 OpenClaw 和系统服务使用它”。）

### 验证本地 HTTP 代理可用

能返回公网 IP 说明 OK：

```bash
curl -x http://127.0.0.1:10809 https://httpbin.org/ip
```

---

## 2）配置系统级 HTTP/HTTPS 代理

### 2.1 让终端命令默认走代理（/etc/environment）

备份并编辑：

```bash
sudo cp /etc/environment /etc/environment.bak.$(date +%F_%H%M%S)
sudo vim /etc/environment
```

建议整段覆盖写入（按你的端口调整）：

```bash
ALL_PROXY=http://127.0.0.1:10809
all_proxy=http://127.0.0.1:10809
HTTP_PROXY=http://127.0.0.1:10809
http_proxy=http://127.0.0.1:10809
HTTPS_PROXY=http://127.0.0.1:10809
https_proxy=http://127.0.0.1:10809
NO_PROXY=localhost,127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,169.254.0.0/16,.local,.lan
no_proxy=localhost,127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,169.254.0.0/16,.local,.lan
```

让当前 shell 立刻生效：

```bash
set -a
. /etc/environment
set +a
env | grep -i proxy
```

验证能访问外网（示例用 Google；你也可以换成其它站点）：

```bash
curl -I -L --connect-timeout 5 --max-time 10 https://www.google.com
```

### 2.2 让 systemd（system 级服务）继承代理

创建 drop-in：

```bash
sudo mkdir -p /etc/systemd/system.conf.d
sudo vim /etc/systemd/system.conf.d/10-proxy.conf
```

写入（注意这里是 DefaultEnvironment，且要用引号包住每个 kv）：

```ini
[Manager]
DefaultEnvironment="ALL_PROXY=http://127.0.0.1:10809" "all_proxy=http://127.0.0.1:10809" "HTTP_PROXY=http://127.0.0.1:10809" "http_proxy=http://127.0.0.1:10809" "HTTPS_PROXY=http://127.0.0.1:10809" "https_proxy=http://127.0.0.1:10809" "NO_PROXY=localhost,127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,169.254.0.0/16,.local,.lan" "no_proxy=localhost,127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,169.254.0.0/16,.local,.lan"
```

让 systemd 重新执行自身加载配置：

```bash
sudo systemctl daemon-reexec
```

### 2.3 让 systemd --user（用户服务）继承代理

OpenClaw 的 gateway 常驻进程很多情况下是 **user service**，所以还要给 user systemd 配。

创建用户环境文件：

```bash
mkdir -p ~/.config/environment.d
vim ~/.config/environment.d/10-proxy.conf
```

写入：

```bash
ALL_PROXY=http://127.0.0.1:10809
all_proxy=http://127.0.0.1:10809
HTTP_PROXY=http://127.0.0.1:10809
http_proxy=http://127.0.0.1:10809
HTTPS_PROXY=http://127.0.0.1:10809
https_proxy=http://127.0.0.1:10809
NO_PROXY=localhost,127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,169.254.0.0/16,.local,.lan
no_proxy=localhost,127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,169.254.0.0/16,.local,.lan
```

让 user systemd 重新加载：

```bash
systemctl --user daemon-reexec
```

验证 user systemd 环境里确实有代理：

```bash
systemctl --user show-environment | grep -i proxy
```

最后重启 OpenClaw gateway 并检查状态：

```bash
systemctl --user restart openclaw-gateway.service
openclaw status
```

---

## 写在最后

原文提到：上述步骤主要由 AI 生成，作者做了整理与验证；并且一个很现实的点是——这些配置其实也可以交给 OpenClaw 自己去完成（前提是它有足够的执行权限与安全边界）。
