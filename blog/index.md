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

## 🤖 人工智能与边缘计算
*前沿模型应用、RK3588 NPU加速与语音视觉实战*

*   **[RK3588部署melo TTS模型附带NPU加速](./ai/RK3588部署melo TTS模型附带NPU加速.md)**
    在RK3588开发板上部署MeloTTS语音合成模型，利用NPU实现约5倍速的推理加速。
*   **[大语言模型培训课_ZXZC25](./ai/大语言模型培训课_ZXZC25.md)**
    大语言模型基础入门，涵盖主流模型介绍、提示词工程技巧及API调用基础概念。
*   **[大语言模型通过MCP控制STM32-支持Ollama、DeepSeek、openai等](./ai/大语言模型通过MCP控制STM32-支持Ollama、DeepSeek、openai等.md)**
    探索通过MCP协议连接DeepSeek、Ollama等大语言模型，实现对STM32硬件设备的智能控制。
*   **[FunASR语音转文字本地部署、API接口教程](./ai/FunASR语音转文字本地部署、API接口教程.md)**
    阿里开源高精度语音识别模型FunASR的Python本地部署指南及API接口调用教程。
*   **[YoloV11的pt模型转rknn模型适用于RK3588等系列](./yolo/YoloV11的pt模型转rknn模型适用于RK3588等系列.md)**
    紧跟最新技术，详解YoloV11环境搭建及将pt模型转换为适配RK3588的rknn模型步骤。
*   **[Sherpa-Onnx 语音实时识别 /RK3588部署](./ai/Sherpa-Onnx_语音实时识别_RK3588部署.md)**
    基于Sherpa-Onnx框架在RK3588平台上实现高性能的离线实时语音识别部署。
*   **[YoloV5的Onnx模型转RKNN模型(包成功，最详细)](./yolo/YoloV5的Onnx模型转RKNN模型(包成功，最详细).md)**
    详细记录YoloV5模型经ONNX转换为RKNN格式的全过程，解决模型转换中的常见坑点。
*   **[RK3588从数据集到训练到部署YoloV8](./yolo/RK3588从数据集到训练到部署YoloV8.md)**
    全流程实战指南：涵盖自定义数据集准备、YoloV8模型训练及在RK3588平台上的最终部署。
*   **[VScode使用AI编程教程](./ai/VScode使用AI编程教程.md)**
    在VSCode中安装与配置CodeGeex插件，利用AI辅助代码编写、自动注释生成及智能问答。
*   **[Pytorch 手动安装教程 【超快|适用于国内没有源的方法】](./yolo/Pytorch_手动安装教程_【超快适用于国内没有源的方法】.md)**
    针对国内源缺失旧版本问题，提供利用P2P下载加速手动安装PyTorch的高效方法。

## 🛠️ 开发工具与环境搭建
*效率工具、Linux配置与版本控制*

*   **[Git入门](./tool/Git入门.md)**
    快速掌握Git版本控制核心命令，涵盖仓库初始化、配置、代码提交及缓存区管理。
*   **[Nomachine-比VNC更稳定流畅的远程桌面软件](./tool/Nomachine-比VNC更稳定流畅的远程桌面软件.md)**
    推荐比VNC更流畅的远程桌面软件Nomachine，附带Ubuntu与Windows端的安装连接教程。
*   **[UV-python环境管理工具 入门教程](./python/UV-python环境管理工具_入门教程.md)**
    介绍基于Rust编写的高性能Python包管理工具UV，体验比pip快10-100倍的环境管理效率。
*   **[Ubuntu安装CH340驱动教程](./Linux/Ubuntu安装CH340驱动教程.md)**
    解决Ubuntu 22.04系统下CH340串口驱动识别问题，提供详细的排查与安装步骤。
*   **[EMQX开源版安装指南：Linux/Windows全攻略](./tool/EMQX开源版安装指南：LinuxWindows全攻略.md)**
    针对Linux和Windows系统，提供EMQX开源版MQTT服务器的详细下载与安装指南。
*   **[安卓开发 Gradle下载网络问题解决方法](./other/安卓开发_Gradle下载网络问题解决方法.md)**
    解决Android Studio中Gradle下载缓慢问题，提供国内镜像源手动安装的快速解决方案。

## 🤖 嵌入式与机器人开发
*STM32控制、ROS2驱动与通信协议*

*   **[PAJ7620手势识别模块-STM32F103标准库](./单片机/PAJ7620手势识别模块-STM32F103标准库.md)**
    基于STM32F103标准库移植PAJ7620手势识别模块驱动，附带核心代码解析。
*   **[JY901-ROS2驱动代码](./单片机/JY901-ROS2驱动代码.md)**
    适配ROS2系统的JY901九轴传感器驱动代码分享，包含编译与运行配置说明。
*   **[ROS2串口通信-连接STM32等下位机/串口模块调用](./ROS2/ROS2串口通信-连接STM32等下位机串口模块调用.md)**
    在ROS2环境下使用Python实现串口通信，完成与STM32等下位机的数据交互。
*   **[ModBusRTU通讯协议/STM32驱动步进电机驱动板](./单片机/ModBusRTU通讯协议STM32驱动步进电机驱动板.md)**
    深入解析RS485与ModBus RTU协议，并演示STM32控制步进电机驱动板的实战应用。
*   **[脉冲控制步进电机思路、STM32驱动步进电机代码分享](./单片机/脉冲控制步进电机思路、STM32驱动步进电机代码分享.md)**
    分享利用STM32定时器中断与PWM脉冲控制步进电机的思路及底层驱动代码。

## 🌐 互联与图形技术
*Unity交互、跨平台通信与模型导入*

*   **[Unity连接Python(Unity连接其它所有的通讯方案)](./other/Unity连接Python(Unity连接其它所有的通讯方案).md)**
    构建Unity与Python的Socket通信桥梁，进而实现连接阿里云MQTT等万物互联方案。
*   **[SolidWorks模型导入Unity教程](./other/SolidWorks模型导入Unity教程.md)**
    详解如何通过Blender中转，将SolidWorks 3D装配体模型高效导入Unity进行交互开发。

## 📝 其他
*   **[备忘录](./备忘录.md)**
    记录日常开发中的杂项信息与临时笔记。

<!-- AI_CONTENT_END -->