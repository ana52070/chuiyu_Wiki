---
author: ana52070
categories:
- 嵌入式Linux项目
date: 2026-01-28
description: 暂无描述
tags:
- 嵌入式Linux项目
title: web_onvif_modbus
permalink: /projects/嵌入式Linux项目/web_onvif_modbus
---

# web_onvif_modbus

> 项目地址：[https://github.com/ana52070/web_onvif_modbus](https://github.com/ana52070/web_onvif_modbus)
> 
> 暂无描述

---

# Web Onvif Modbus Control System

  

这是一个基于 C 语言开发的嵌入式综合控制系统，集成了轻量级 Web 服务器、Onvif 摄像头 PTZ 控制以及 Modbus TCP 主站通信功能。该项目旨在提供一个通过 Web 界面管理网络摄像头和工业 Modbus 设备的统一解决方案。

  

## 🚀 主要功能

  

### 1. Web 服务器 (Webserver)

- **轻量级 HTTP 服务**：基于 Socket 实现的多线程 Web 服务器。

- **RESTful API 支持**：提供 HTTP 接口用于前端交互。

  - 云台控制 (`deal_move`, `deal_preset`)

  - 自动追踪配置 (`deal_trackcfg`)

  - 网络参数配置 (`deal_ipcfg`)

- **静态资源服务**：支持 HTML、CSS、JS 及图片资源的访问。

- **JSON 数据处理**：使用 cJSON 库进行数据解析与封装。

  

### 2. Onvif 摄像头控制 (Onvif)

- **PTZ 控制**：通过 gSOAP 生成的 Onvif 协议栈控制摄像头。

- **功能支持**：

  - 摄像头初始化与发现

  - 云台移动控制 (Pan/Tilt/Zoom)

  - 预置位 (Preset) 调用与管理

- **多摄管理**：支持同时管理多个摄像头实例。

  

### 3. Modbus TCP 主站 (ModbusTCP)

- **主站通信**：实现了 Modbus TCP 客户端功能，可连接远程从站设备。

- **数据读写**：

  - 支持读取线圈 (Coils) 和寄存器 (Registers)。

  - 支持多种数据类型（位、字节、16位整数、32位整数）。

- **稳定性设计**：包含连接超时、重试机制及通信延时控制。

  

### 4. 系统命令执行 (Command)

- **脚本调用**：支持通过 C 代码调用 Shell 脚本。

- **系统管理**：包含网络配置 (`ipset.sh`)、系统重启 (`reboot.sh`) 等功能。

  

## 📂 目录结构

  

```

.

├── main.c                  # 主程序入口，负责线程创建与调度

├── Makefile                # 项目构建文件

├── Webserver/              # Web 服务器模块

│   ├── Code/               # HTTP 协议处理、API 接口实现

│   ├── Config/             # 配置文件 (json)

│   └── HTML/               # 前端静态资源文件

├── Onvif/                  # Onvif 协议模块

│   ├── Code/               # 摄像头管理与 PTZ 控制逻辑

│   └── PTZBinding.nsmap    # gSOAP 命名空间映射

├── ModbusTCP/              # Modbus TCP 模块

│   └── Code/               # Modbus 主站协议栈实现

└── Command/                # 系统命令模块

    ├── Code/               # 命令执行接口

    └── Sh/                 # Shell 脚本文件

```

  

## 🛠️ 编译与运行

  

### 依赖项

- **GCC**: C 语言编译器

- **Make**: 构建工具

- **Pthread**: POSIX 线程库

- **cJSON**: JSON 解析库 (位于 `../../../arm_libs_build/cJSON/`，需根据实际环境调整路径)

- **gSOAP**: 用于 Onvif 协议支持

  

### 编译

在项目根目录下执行 `make` 命令：

  

```bash

make

```

  

这将生成可执行文件 `onvif_total_project`。

  

### 运行

```bash

./onvif_total_project

```

  

程序启动后将开启以下服务：

- **Web Server**: 默认监听端口 `8080` (可在 `main.c` 或头文件中修改 `SERVER_PORT`)。

- **Onvif Task**: 初始化摄像头并准备接收控制指令。

- **Modbus Task**: (默认注释，需在 `main.c` 中取消注释开启) 连接 Modbus 从站。

  

## ⚙️ 配置说明

  

- **Web 端口**: 在 `main.c` 中 `task_webserver` 函数内设置。

- **Modbus 目标**: 在 `main.c` 或 `ModbusTCP/Code/modbusTcp_master.c` 中配置 `MODBUS_SERVER_IP` 和端口。

- **摄像头参数**: 在 `Onvif/Code/camera_config.h` 或初始化代码中配置摄像头 IP 和认证信息。

  

## 📝 许可证

[License Information Here]

