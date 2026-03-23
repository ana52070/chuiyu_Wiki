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

### 🤖 AI 与大模型应用

- [Claude Code 从入门到生产：一文讲透安装、使用、MCP、SubAgent、Plugin 的实战指南](/pages/ea15bf)：完整转载并整理 Claude Code 实战指南，覆盖安装、终端交互、上下文管理、MCP、SubAgent、Plugin 等从入门到接近生产的完整路径。
- [claude code +AI coding plan](/pages/b8d11f)：介绍 Claude Code 终端编程助手的功能定位、基础用法及配合 Coding Plan 的工作流配置。
- [OpenClaw_CLI_命令行上手与常用命令速查](/pages/d8451b)：OpenClaw AI Agent Runtime 的快速上手指南，涵盖 CLI 安装与核心概念解析。
- [OpenClaw部署后权限配置与安全加固教程](/pages/2a0f3e)：OpenClaw 部署后的安全加固指南，涵盖文件权限、服务暴露防护及命令执行审批策略。
- [在国内网络环境下给OpenClaw运行环境配置全局代理](/pages/31a76d)：解决 OpenClaw 在国内网络环境下的访问问题，详解 HTTP 代理与 systemd 环境变量配置。
- [codex的使用笔记及心得](/pages/d509f7)：分享 Codex 使用笔记，重点讲解如何通过配置文件永久设置中文回复。
- [大语言模型培训课_ZXZC25](/blog/ai/大语言模型培训课_ZXZC25)：大语言模型入门培训笔记，涵盖模型选型、提示词技巧及 API 基础概念。
- [VScode使用AI编程教程](/blog/ai/VScode使用AI编程教程)：VScode 安装配置 CodeGeex 插件的图文教程，实现 AI 辅助编程与代码补全。
- [大语言模型通过MCP控制STM32](/blog/ai/大语言模型通过MCP控制STM32-支持Ollama、DeepSeek、openai等)：演示如何利用 MCP 协议让大语言模型控制 STM32 硬件，支持多种模型。
- [FunASR语音转文字本地部署、API接口教程](/blog/ai/FunASR语音转文字本地部署、API接口教程)：介绍阿里开源 FunASR 语音转文字模型的本地 Python 部署及 API 接口调用流程。
- [Sherpa-Onnx 语音实时识别 /RK3588部署](/blog/ai/Sherpa-Onnx_语音实时识别_RK3588部署)：在 RK3588 上部署 Sherpa-Onnx 实现实时语音识别，包含环境搭建与模型配置。
- [RK3588部署melo TTS模型附带NPU加速](/pages/aaf782)：在 RK3588 上部署 MeloTTS 文字转语音模型并利用 NPU 加速，实现高性能推理。

### 📟 嵌入式与边缘计算

- [RK3588从数据集到训练到部署YoloV8](/blog/yolo/RK3588从数据集到训练到部署YoloV8)：记录 RK3588 平台上 YoloV8 的环境配置、数据集准备到模型训练部署的全流程。
- [YoloV11的pt模型转rknn模型适用于RK3588等系列](/blog/yolo/YoloV11的pt模型转rknn模型适用于RK3588等系列)：介绍 YoloV11 环境搭建及将 pt 模型转换为 RKNN 格式以适配 RK3588 系列板卡的流程。
- [YoloV5的Onnx模型转RKNN模型(包成功，最详细)](/blog/yolo/YoloV5的Onnx模型转RKNN模型(包成功，最详细))：提供详细的 YoloV5 Onnx 模型转 RKNN 模型教程，包含环境搭建与常见报错解决。
- [Jetson Xavier Nx烧录刷机安装Ubuntu20.04系统及后续配置](/blog/Linux/Jetson_Xavier_Nx烧录刷机安装Ubuntu20.04系统及后续配置)：详解 Jetson Xavier NX 刷写 Ubuntu 20.04 系统流程及 eMMC 扩容避坑指南。
- [Ubuntu安装CH340驱动教程](/blog/Linux/Ubuntu安装CH340驱动教程)：讲解在 Ubuntu 22.04 下安装 CH340 驱动及排查设备识别问题的实操步骤。
- [ROS2串口通信-连接STM32等下位机](/blog/ROS2/ROS2串口通信-连接STM32等下位机串口模块调用)：ROS2 串口通信实战，讲解如何连接 STM32 等下位机并进行数据交互。
- [JY901-ROS2驱动代码](/blog/单片机/JY901-ROS2驱动代码)：分享 JY901 传感器的 ROS2 驱动代码移植与编译运行方法。
- [脉冲控制步进电机思路、STM32驱动步进电机代码分享](/blog/单片机/脉冲控制步进电机思路、STM32驱动步进电机代码分享)：解析脉冲控制步进电机原理，提供基于 STM32 PWM 与定时中断的驱动代码实现。
- [ModBusRTU通讯协议/STM32驱动步进电机驱动板](/blog/单片机/ModBusRTU通讯协议STM32驱动步进电机驱动板)：讲解 ModBus RTU 协议与 RS485 通讯基础，分享 STM32 控制步进电机驱动板的代码。
- [PAJ7620手势识别模块-STM32F103标准库](/blog/单片机/PAJ7620手势识别模块-STM32F103标准库)：PAJ7620 手势识别模块在 STM32F103 标准库下的移植教程与代码分享。

### 🛠️ 开发工具与环境

- [UV-python环境管理工具 入门教程](/blog/python/UV-python环境管理工具_入门教程)：介绍基于 Rust 编写的 UV 工具，对比传统工具解析其优势，提供快速上手安装指南。
- [Pytorch 手动安装教程 【超快|适用于国内没有源的方法】](/blog/yolo/Pytorch_手动安装教程_【超快适用于国内没有源的方法】)：分享一种利用 P2P 下载加手动 pip 安装 Pytorch 的方法，解决国内源缺失或速度慢的问题。
- [Git入门](/blog/tool/Git入门)：Git 版本控制入门教程，涵盖仓库初始化、配置查看及代码提交基础命令。
- [Nomachine-比VNC更稳定流畅的远程桌面软件](/blog/tool/Nomachine-比VNC更稳定流畅的远程桌面软件)：推荐 NoMachine 远程桌面软件，提供 Linux 环境下的安装与连接配置教程。
- [EMQX开源版安装指南：Linux/Windows全攻略](/blog/tool/EMQX开源版安装指南：LinuxWindows全攻略)：EMQX 开源版 MQTT 服务器在 Linux/Windows 平台的安装部署全攻略。
- [安卓开发 Gradle下载网络问题解决方法](/blog/other/安卓开发_Gradle下载网络问题解决方法)：解决安卓开发中 Gradle 下载慢或失败的问题，提供手动下载与镜像配置方案。

### 📂 其他项目与经验

- [Unity连接Python(Unity连接其它所有的通讯方案)](/blog/other/Unity连接Python(Unity连接其它所有的通讯方案))：通过 Socket 通信实现 Unity 与 Python 互联，进而扩展连接阿里云等更多服务的方案。
- [SolidWorks模型导入Unity教程](/blog/other/SolidWorks模型导入Unity教程)：详述 SolidWorks 模型导入 Unity 的两种路径，对比 Blender 与 3ds Max 方案的优劣。
- [经验分享](/pages/25d7b1)：面向大一新生的经验分享演讲稿，探讨 AI 时代的学习思维与项目实践心得。
- [备忘录](/pages/0bbee6)：记录杂项笔记与待办事项。

<!-- AI_CONTENT_END -->