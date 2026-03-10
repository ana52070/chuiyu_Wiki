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

### 人工智能与应用

- [codex的使用笔记及心得](./ai/codex的使用笔记及心得.md)：介绍如何配置 AGENTS.md 文件让 Codex 永久使用简体中文回复，提升 AI 编程体验。
- [FunASR语音转文字本地部署、API接口教程](/blog/ai/FunASR语音转文字本地部署、API接口教程)：阿里开源 FunASR 语音识别模型的 Python 本地部署与环境配置指南。
- [OpenClaw部署后权限配置与安全加固教程](./ai/OpenClaw部署后权限配置与安全加固教程.md)：详解 OpenClaw 部署后的安全策略，涵盖文件权限、消息入口及命令执行审批等关键配置。
- [RK3588部署melo TTS模型附带NPU加速](/pages/aaf782)：在 RK3588 开发板上部署 MeloTTS 语音合成模型，利用 NPU 加速实现约 5 倍速推理。
- [Sherpa-Onnx 语音实时识别 /RK3588部署](/blog/ai/Sherpa-Onnx_语音实时识别_RK3588部署)：RK3588 平台部署 Sherpa-Onnx 实现实时语音识别的详细步骤与环境配置。
- [VScode使用AI编程教程](/blog/ai/VScode使用AI编程教程)：演示在 VScode 中安装 CodeGeex 插件实现 AI 实时代码补全与辅助编程。
- [在国内网络环境下给OpenClaw运行环境配置全局代理](./ai/在国内网络环境下给OpenClaw运行环境配置全局代理.md)：解决 OpenClaw 在国内网络环境下的访问限制，为 systemd 服务配置 HTTP/HTTPS 全局代理。
- [大语言模型培训课_ZXZC25](/blog/ai/大语言模型培训课_ZXZC25)：涵盖大语言模型基础原理、常用提示词技巧及 API 调用的入门培训笔记。
- [大语言模型通过MCP控制STM32-支持Ollama、DeepSeek、openai等](/blog/ai/大语言模型通过MCP控制STM32-支持Ollama、DeepSeek、openai等)：利用 MCP 协议打通大模型与 STM32 硬件的控制链路，支持多种模型后端。

### 嵌入式与硬件开发

- [JY901-ROS2驱动代码](/blog/单片机/JY901-ROS2驱动代码)：JY901 惯性测量单元的 ROS2 驱动包编译、配置与使用指南。
- [ModBusRTU通讯协议/STM32驱动步进电机驱动板](/blog/单片机/ModBusRTU通讯协议STM32驱动步进电机驱动板)：介绍 RS485 与 ModBus 协议基础，并提供 STM32 驱动步进电机的代码实现。
- [PAJ7620手势识别模块-STM32F103标准库](/blog/单片机/PAJ7620手势识别模块-STM32F103标准库)：PAJ7620 手势识别模块在 STM32F103 上的标准库驱动移植与代码分享。
- [脉冲控制步进电机思路、STM32驱动步进电机代码分享](/blog/单片机/脉冲控制步进电机思路、STM32驱动步进电机代码分享)：讲解利用 PWM 和定时中断控制步进电机的思路，并分享 STM32 具体实现代码。
- [ROS2串口通信-连接STM32等下位机/串口模块调用](/blog/ROS2/ROS2串口通信-连接STM32等下位机串口模块调用)：指导在 ROS2 环境下开启串口并与 STM32 等下位机进行通讯测试。
- [Pytorch 手动安装教程 【超快|适用于国内没有源的方法】](/blog/yolo/Pytorch_手动安装教程_【超快适用于国内没有源的方法】)：针对国内源版本缺失问题，提供 Pytorch 手动下载 whl 包并安装的加速方案。
- [RK3588从数据集到训练到部署YoloV8](/blog/yolo/RK3588从数据集到训练到部署YoloV8)：记录 RK3588 平台上 YoloV8 的完整开发流程，涵盖环境配置、数据集准备及模型训练。
- [YoloV11的pt模型转rknn模型适用于RK3588等系列](/blog/yolo/YoloV11的pt模型转rknn模型适用于RK3588等系列)：指导如何将 YoloV11 pt 模型转换为适配 RK3588 NPU 的 rknn 模型。
- [YoloV5的Onnx模型转RKNN模型(包成功，最详细)](/blog/yolo/YoloV5的Onnx模型转RKNN模型(包成功，最详细))：详解 YoloV5 Onnx 模型转 RKNN 模型的全过程，包含 Docker 环境配置与常见报错解决。

### 开发工具与环境

- [Ubuntu安装CH340驱动教程](/blog/Linux/Ubuntu安装CH340驱动教程)：解决 Ubuntu 22.04 下 CH340 驱动识别问题，包含设备查看及驱动排查步骤。
- [UV-python环境管理工具 入门教程](/blog/python/UV-python环境管理工具_入门教程)：介绍基于 Rust 编写的 UV Python 环境管理工具，对比 venv/conda 具有更快的速度和兼容性。
- [EMQX开源版安装指南：Linux/Windows全攻略](/blog/tool/EMQX开源版安装指南：LinuxWindows全攻略)：提供 EMQX 开源版 MQTT 服务器的下载与安装指南，涵盖 Linux (Ubuntu) 环境下的详细配置流程。
- [Git入门](/blog/tool/Git入门)：Git 版本控制基础教程，涵盖代码仓库初始化、配置及代码提交的基础命令操作。
- [Nomachine-比VNC更稳定流畅的远程桌面软件](/blog/tool/Nomachine-比VNC更稳定流畅的远程桌面软件)：介绍 NoMachine 远程桌面软件的安装与连接过程，体验比 VNC 更流畅稳定的远程操作。

### 其他项目与教程

- [备忘录](/pages/0bbee6)：记录杂项内容与临时笔记。
- [SolidWorks模型导入Unity教程](/blog/other/SolidWorks模型导入Unity教程)：汇总两种将 SolidWorks 3D 模型导入 Unity 的方法，对比 Blender 与 3DMax 中转方案的优缺点。
- [Unity连接Python(Unity连接其它所有的通讯方案)](/blog/other/Unity连接Python(Unity连接其它所有的通讯方案))：提出 Unity 通过 Socket 连接 Python 再连接阿里云的间接通讯方案，解决数字孪生项目中的连接难题。
- [安卓开发 Gradle下载网络问题解决方法](/blog/other/安卓开发_Gradle下载网络问题解决方法)：解决安卓开发中 Gradle 下载慢或失败的问题，提供手动下载并替换文件的详细解决步骤。

<!-- AI_CONTENT_END -->