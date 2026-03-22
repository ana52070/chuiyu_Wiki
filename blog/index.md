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

- [claude code +AI coding plan](./pages/b8d11f)：介绍 Claude Code 终端编程助手的配置与使用，结合 Coding Plan 实现“先计划再动手”的 AI 编程工作流。
- [OpenClaw_CLI_命令行上手与常用命令速查](./pages/d8451b)：OpenClaw AI Agent Runtime 的 CLI 安装指南与常用命令速查，帮助快速上手智能体开发。
- [OpenClaw部署后权限配置与安全加固教程](./pages/2a0f3e)：OpenClaw 部署后的安全指南，涵盖目录权限、消息入口、Gateway 暴露及命令执行审批等加固措施。
- [在国内网络环境下给OpenClaw运行环境配置全局代理](./pages/31a76d)：解决 OpenClaw 在国内网络环境下的访问问题，配置 HTTP/HTTPS 代理及 systemd 环境变量。
- [codex的使用笔记及心得](./pages/d509f7)：分享 OpenAI Codex 的使用心得，重点介绍如何通过 AGENTS.md 文件设置中文回复。
- [大语言模型通过MCP控制STM32-支持Ollama、DeepSeek、openai等](./blog/ai/大语言模型通过MCP控制STM32-支持Ollama、DeepSeek、openai等)：利用 MCP 协议，通过 Ollama、DeepSeek 等大模型控制 STM32 硬件，实现 AI 与嵌入式设备的交互。
- [RK3588部署melo TTS模型附带NPU加速](./pages/aaf782)：在 RK3588 上部署 MeloTTS 文字转语音模型，利用 NPU 加速实现约 5 倍速推理。
- [Sherpa-Onnx 语音实时识别 /RK3588部署](./blog/ai/Sherpa-Onnx_语音实时识别_RK3588部署)：在 RK3588 开发板上部署 Sherpa-Onnx，实现基于新一代 Kaldi 的本地实时语音识别。
- [FunASR语音转文字本地部署、API接口教程](./blog/ai/FunASR语音转文字本地部署、API接口教程)：阿里开源 FunASR 语音识别模型的本地 Python 部署流程，支持高精度快速转写。
- [VScode使用AI编程教程](./blog/ai/VScode使用AI编程教程)：在 VScode 中安装配置 CodeGeex 插件，实现 AI 实时补全代码、自动注释等功能。
- [大语言模型培训课_ZXZC25](./blog/ai/大语言模型培训课_ZXZC25)：大模型基础入门培训笔记，涵盖常用模型介绍、提示词技巧及 API 调用原理。

### YOLO 与计算机视觉

- [RK3588从数据集到训练到部署YoloV8](./blog/yolo/RK3588从数据集到训练到部署YoloV8)：从环境配置、数据集准备到模型训练，全流程讲解如何在 RK3588 上部署 YoloV8。
- [YoloV11的pt模型转rknn模型适用于RK3588等系列](./blog/yolo/YoloV11的pt模型转rknn模型适用于RK3588等系列)：指导如何将 YoloV11 的 pt 模型转换为适用于 RK3588 等 Rockchip 芯片的 rknn 模型。
- [YoloV5的Onnx模型转RKNN模型(包成功，最详细)](./blog/yolo/YoloV5的Onnx模型转RKNN模型(包成功，最详细))：详细记录在 Ubuntu 20.04 下使用 Docker 将 YoloV5 Onnx 模型转换为 RKNN 模型的过程，包含踩坑点。
- [Pytorch 手动安装教程 【超快适用于国内没有源的方法】](./blog/yolo/Pytorch_手动安装教程_【超快适用于国内没有源的方法】)：解决国内源 Pytorch 版本缺失或下载慢的问题，提供手动下载 whl 包并 pip 安装的加速方案。

### 嵌入式与 Linux 系统

- [Jetson Xavier Nx烧录刷机安装Ubuntu20.04系统及后续配置](./blog/Linux/Jetson_Xavier_Nx烧录刷机安装Ubuntu20.04系统及后续配置)：详解 Jetson Xavier NX (eMMC版) 刷写 JetPack 5/Ubuntu 20.04 及系统扩容迁移 SSD 的完整流程。
- [Ubuntu安装CH340驱动教程](./blog/Linux/Ubuntu安装CH340驱动教程)：Ubuntu 22.04 系统下 CH340 驱动的安装与排查指南，解决 USB 转串口设备识别问题。
- [ROS2串口通信-连接STM32等下位机/串口模块调用](./blog/ROS2/ROS2串口通信-连接STM32等下位机串口模块调用)：ROS2 串口通信实战，演示如何连接 STM32 等下位机并进行数据交互。
- [JY901-ROS2驱动代码](./blog/单片机/JY901-ROS2驱动代码)：维特智能 JY901 惯性导航模块的 ROS2 驱动包使用教程，包含安装与配置方法。

### 单片机与硬件控制

- [脉冲控制步进电机思路、STM32驱动步进电机代码分享](./blog/单片机/脉冲控制步进电机思路、STM32驱动步进电机代码分享)：基于 STM32 的步进电机控制方案，结合 PWM 输出与定时中断实现伪开环位置控制。
- [ModBusRTU通讯协议/STM32驱动步进电机驱动板](./blog/单片机/ModBusRTU通讯协议STM32驱动步进电机驱动板)：解析 ModBus RTU 协议，并提供 STM32 通过 RS485 控制步进电机驱动板的代码实现。
- [PAJ7620手势识别模块-STM32F103标准库](./blog/单片机/PAJ7620手势识别模块-STM32F103标准库)：PAJ7620 手势识别模块的 STM32F103 标准库移植教程，包含核心驱动代码分享。

### 开发工具与环境

- [UV-python环境管理工具 入门教程](./blog/python/UV-python环境管理工具_入门教程)：介绍一款基于 Rust 编写、比 pip 快 10-100 倍的 Python 环境管理工具 UV 的安装与使用。
- [EMQX开源版安装指南：Linux/Windows全攻略](./blog/tool/EMQX开源版安装指南：LinuxWindows全攻略)：MQTT 服务器 EMQX 开源版的详细安装指南，覆盖 Linux 与 Windows 平台。
- [Nomachine-比VNC更稳定流畅的远程桌面软件](./blog/tool/Nomachine-比VNC更稳定流畅的远程桌面软件)：介绍 Nomachine 远程桌面软件在 Linux (Ubuntu) 下的安装与连接配置，体验比 VNC 更流畅的操作。
- [Git入门](./blog/tool/Git入门)：Git 版本控制基础教程，涵盖仓库初始化、配置及代码提交等常用命令。
- [安卓开发 Gradle下载网络问题解决方法](./blog/other/安卓开发_Gradle下载网络问题解决方法)：解决安卓开发中 Gradle 下载慢或失败的问题，提供手动下载与配置的加速方案。
- [Unity连接Python(Unity连接其它所有的通讯方案)](./blog/other/Unity连接Python(Unity连接其它所有的通讯方案))：利用 Socket 通信实现 Unity 与 Python 的互联，进而通过 Python 桥接阿里云 MQTT 等外部服务。
- [SolidWorks模型导入Unity教程](./blog/other/SolidWorks模型导入Unity教程)：详解两种将 SolidWorks 3D 模型导入 Unity 的方法（Blender 转换与 3DMax 转换），解决材质丢失问题。

### 其他与随笔

- [经验分享](./pages/25d7b1)：大一新生分享会演讲稿，探讨 AI 时代的学习思维与工具箱建立。
- [备忘录](./pages/0bbee6)：记录杂项内容，用于备忘。

<!-- AI_CONTENT_END -->