---
date: 2026-02-04 09:16:38
title: index
categories:
  - blog
sidebar: true
layout: doc
permalink: /pages/d81aa7
---
# 博客文章 📝
这里记录了我的所有技术文章。
请点击左侧菜单查看具体内容。

<!-- AI_CONTENT_START -->

### AI 与大模型应用

- [claude code +AI coding plan.md](./ai/claude code +AI coding plan.md)  
  介绍 Claude Code 终端编程助手的使用方法及其与 Coding Plan 的结合配置教程，旨在解决 AI 编程“落地难”的问题。

- [OpenClaw_CLI_命令行上手与常用命令速查.md](./ai/OpenClaw_CLI_命令行上手与常用命令速查.md)  
  OpenClaw AI Agent Runtime 的 CLI 安装、初始化及常用命令速查指南，帮助快速上手智能体运行环境。

- [OpenClaw部署后权限配置与安全加固教程.md](./ai/OpenClaw部署后权限配置与安全加固教程.md)  
  OpenClaw 部署后的安全加固指南，涵盖文件权限、消息入口及命令执行审批等关键配置。

- [在国内网络环境下给OpenClaw运行环境配置全局代理.md](./ai/在国内网络环境下给OpenClaw运行环境配置全局代理.md)  
  解决 OpenClaw 在国内网络环境下的访问问题，配置 HTTP 代理及 systemd 服务环境变量。

- [codex的使用笔记及心得.md](./ai/codex的使用笔记及心得.md)  
  分享 Codex 使用心得，重点介绍如何通过 AGENTS.md 文件配置永久中文回复。

- [RK3588部署melo TTS模型附带NPU加速.md](./ai/RK3588部署melo TTS模型附带NPU加速.md)  
  在 RK3588 上部署 MeloTTS 文字转语音模型，实现 NPU 加速与低内存占用运行。

- [大语言模型培训课_ZXZC25.md](./ai/大语言模型培训课_ZXZC25.md)  
  大语言模型基础概念介绍、常用提示词技巧及 API 调用原理解析。

- [大语言模型通过MCP控制STM32-支持Ollama、DeepSeek、openai等.md](./ai/大语言模型通过MCP控制STM32-支持Ollama、DeepSeek、openai等.md)  
  利用 MCP 协议实现大语言模型对 STM32 硬件的控制，支持多种主流模型。

- [FunASR语音转文字本地部署、API接口教程.md](./ai/FunASR语音转文字本地部署、API接口教程.md)  
  阿里开源 FunASR 语音识别模型的本地 Python 部署流程及 API 接口调用教程。

- [Sherpa-Onnx_语音实时识别_RK3588部署.md](./ai/Sherpa-Onnx_语音实时识别_RK3588部署.md)  
  在 RK3588 平台上部署 Sherpa-Onnx 实现实时语音识别的安装与配置教程。

- [VScode使用AI编程教程.md](./ai/VScode使用AI编程教程.md)  
  图文演示如何在 VScode 中安装并使用 CodeGeex 插件实现 AI 辅助编程。

### YOLO 与视觉部署

- [YoloV11的pt模型转rknn模型适用于RK3588等系列.md](./yolo/YoloV11的pt模型转rknn模型适用于RK3588等系列.md)  
  指导如何在 RK3588 平台上搭建环境并将 YoloV11 模型转换为 RKNN 格式进行部署。

- [YoloV5的Onnx模型转RKNN模型(包成功，最详细).md](./yolo/YoloV5的Onnx模型转RKNN模型(包成功，最详细).md)  
  基于 Docker 环境，详细讲解 YoloV5 Onnx 模型转 RKNN 模型的步骤与常见问题处理。

- [RK3588从数据集到训练到部署YoloV8.md](./yolo/RK3588从数据集到训练到部署YoloV8.md)  
  涵盖从环境配置、数据集准备到模型训练的 RK3588 YoloV8 完整部署流程。

- [Pytorch_手动安装教程_【超快适用于国内没有源的方法】.md](./yolo/Pytorch_手动安装教程_【超快适用于国内没有源的方法】.md)  
  针对国内源资源缺失问题，提供一种利用 P2P 下载和手动 pip 安装 Pytorch 的快速解决方案。

### 嵌入式与单片机

- [PAJ7620手势识别模块-STM32F103标准库.md](./单片机/PAJ7620手势识别模块-STM32F103标准库.md)  
  PAJ7620 手势识别模块的 STM32F103 标准库移植与驱动代码分享。

- [JY901-ROS2驱动代码.md](./单片机/JY901-ROS2驱动代码.md)  
  维特智能 JY901 传感器在 ROS2 环境下的驱动包安装、编译及运行指南。

- [ROS2串口通信-连接STM32等下位机串口模块调用.md](./ROS2/ROS2串口通信-连接STM32等下位机串口模块调用.md)  
  讲解 ROS2 环境下如何进行串口通信配置，实现与 STM32 等下位机的数据交互。

- [ModBusRTU通讯协议STM32驱动步进电机驱动板.md](./单片机/ModBusRTU通讯协议STM32驱动步进电机驱动板.md)  
  介绍 RS485 与 ModBus RTU 协议，并提供 STM32 控制步进电机驱动板的实现代码。

- [脉冲控制步进电机思路、STM32驱动步进电机代码分享.md](./单片机/脉冲控制步进电机思路、STM32驱动步进电机代码分享.md)  
  讲解利用 PWM 和定时中断控制步进电机的思路，并提供 STM32 驱动代码。

### 工具与环境配置

- [Git入门.md](./tool/Git入门.md)  
  Git 版本控制的基础入门教程，包含仓库初始化、配置及代码提交等常用命令。

- [Nomachine-比VNC更稳定流畅的远程桌面软件.md](./tool/Nomachine-比VNC更稳定流畅的远程桌面软件.md)  
  介绍 Nomachine 远程桌面软件在 Linux 环境下的安装与连接配置，对比 VNC 更流畅。

- [UV-python环境管理工具_入门教程.md](./python/UV-python环境管理工具_入门教程.md)  
  介绍 UV 这款集版本管理、环境创建于一体的轻量级 Python 工具，对比传统工具具有显著性能优势。

- [Ubuntu安装CH340驱动教程.md](./Linux/Ubuntu安装CH340驱动教程.md)  
  详细记录了在 Ubuntu 22.04 系统上识别、安装及验证 CH340 串口驱动的全过程。

- [EMQX开源版安装指南：LinuxWindows全攻略.md](./tool/EMQX开源版安装指南：LinuxWindows全攻略.md)  
  EMQX 开源版消息代理在 Linux 和 Windows 系统上的详细下载与安装部署指南。

### 其他技术分享

- [Unity连接Python(Unity连接其它所有的通讯方案).md](./other/Unity连接Python(Unity连接其它所有的通讯方案).md)  
  利用 Socket 通信实现 Unity 与 Python 的互联，进而打通 Unity 与阿里云等外部服务的连接。

- [SolidWorks模型导入Unity教程.md](./other/SolidWorks模型导入Unity教程.md)  
  详解两种将 SolidWorks 3D 模型导入 Unity 的方法，包含材质保留与格式转换技巧。

- [安卓开发_Gradle下载网络问题解决方法.md](./other/安卓开发_Gradle下载网络问题解决方法.md)  
  解决安卓开发中 Gradle 下载慢或失败的问题，提供手动下载配置的解决方案。

<!-- AI_CONTENT_END -->