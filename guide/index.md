---
date: 2026-02-04 17:06:00
title: index
categories:
  - guide
sidebar: true
layout: doc
permalink: /pages/974787
---
# 📚 嵌入式全栈修炼手册

<!-- AI_CONTENT_START -->

- **Claude Code 微学习**
  - [backend-log](./claude-code/backend-log.md) — 记录 Claude Code 每晚微学习后台执行情况与同步状态。
  - [daily-learning-log](./claude-code/daily-learning-log.md) — 每日学习主题总索引，按时间回看核心一句话与对应页面。
  - [topics](./claude-code/topics.md) — 按主题沉淀可复用的知识点，如 `/permissions` 白名单的原理与边界。
  - [2026-04-08](./claude-code/daily/2026-04-08.md) — 详细讲解 `/permissions` 白名单：比 Auto 更细的一层权限控制。

- **C++算法入门（C 转 C++ 教程）**
  - [C++算法笔记1](./C转C++教程/README.md) — 从 C 过渡到 C++ 的知识点梳理，涵盖基本篇、STL 篇、进阶篇与 C++11 篇。
  - [使用C++刷算法的好处](./C转C++教程/ch01-basics/01-使用C++刷算法的好处.md) — 阐述 C++ 兼容 C、STL 丰富、字符串便捷等优势。
  - [using-namespace-std](./C转C++教程/ch01-basics/02-using-namespace-std.md) — 详解命名空间原理、`using namespace std` 的利弊与替代方案。
  - [cin和cout](./C转C++教程/ch01-basics/03-cin和cout.md) — 介绍 C++ 标准输入输出流的基本用法与性能优化技巧。
  - [头文件](./C转C++教程/ch01-basics/04-头文件.md) — 对比 C 头文件与 C++ 风格头文件，列出常用头文件对照表。
  - [变量声明](./C转C++教程/ch01-basics/05-变量声明.md) — 对比 C 与 C++ 的变量声明规则，强调 C++ 可随时声明的便利性。
  - [bool变量](./C转C++教程/ch01-basics/06-bool变量.md) — 介绍 C 中模拟布尔值的方式与 C++ 原生 `bool` 类型的使用。
  - [const定义常量](./C转C++教程/ch01-basics/07-const定义常量.md) — 讲解 `const` 的基本用法、编译时常量原理及其优势。
  - [string类](./C转C++教程/ch01-basics/08-string类.md) — 对比 C 风格字符串与 C++ `string` 类，展示运算符重载与成员函数的便捷。
  - [结构体](./C转C++教程/ch01-basics/09-结构体.md) — 对比 C 与 C++ 中结构体的定义与使用差异。
  - [引用和传值](./C转C++教程/ch01-basics/10-引用和传值.md) — 解释值传递与引用传递的原理与区别，并演示 `swap` 函数。
  - [章节小结](./C转C++教程/ch01-basics/99-章节小结.md) — 回顾第一章核心知识点：C++ 兼容性、命名空间、IO、头文件、变量声明、bool、const、string、结构体、引用。
  - [vector](./C转C++教程/ch02-stl/01-vector.md) — 详解动态数组 `vector` 的原理、创建方式与常用操作。
  - [set](./C转C++教程/ch02-stl/02-set.md) — 介绍有序集合 `set` 基于红黑树的实现、特性与适用场景。
  - [map](./C转C++教程/ch02-stl/03-map.md) — 讲解键值对容器 `map` 的原理、创建方式与常用操作。
  - [stack](./C转C++教程/ch02-stl/04-stack.md) — 说明栈容器适配器 `stack` 的先进后出特性与典型应用。
  - [queue](./C转C++教程/ch02-stl/05-queue.md) — 介绍队列与优先队列 `queue`/`priority_queue` 的原理与使用。
  - [unordered-map和unordered-set](./C转C++教程/ch02-stl/06-unordered-map和unordered-set.md) — 讲解基于哈希表的无序容器的原理、哈希冲突与性能对比。
  - [章节小结](./C转C++教程/ch02-stl/99-章节小结.md) — 总结 STL 六大容器的特性、时间复杂度与适用场景速查表。
  - [bitset](./C转C++教程/ch03-advanced/01-bitset.md) — 详解固定大小二进制位容器 `bitset` 的索引方向、成员函数与位运算操作。
  - [sort函数](./C转C++教程/ch03-advanced/02-sort函数.md) — 介绍 `std::sort` 的内省排序原理、原型与用法。
  - [自定义cmp函数](./C转C++教程/ch03-advanced/03-自定义cmp函数.md) — 讲解自定义比较函数实现降序、结构体排序等复杂排序规则。
  - [cctype头文件](./C转C++教程/ch03-advanced/04-cctype头文件.md) — 列举字符分类与转换函数，使用注意事项。
  - [章节小结](./C转C++教程/ch03-advanced/99-章节小结.md) — 回顾进阶章节：bitset、sort、自定义cmp、cctype 的核心要点。
  - [C++11简介](./C转C++教程/ch04-cpp11/01-C++11简介.md) — 概述 C++11 里程碑特性，介绍本章要学习的 auto、范围 for 等 6 个特性。
  - [auto声明](./C转C++教程/ch04-cpp11/02-auto声明.md) — 讲解 `auto` 类型推导原理、基本用法与配合范围 for 的最佳实践。
  - [基于范围的for循环](./C转C++教程/ch04-cpp11/03-基于范围的for循环.md) — 说明范围 for 循环的语法糖原理与三种遍历方式。
  - [to_string](./C转C++教程/ch04-cpp11/04-to_string.md) — 介绍 `to_string` 函数将数值转换为字符串的便捷性。
  - [stoi-stod等转换函数](./C转C++教程/ch04-cpp11/05-stoi-stod等转换函数.md) — 讲解字符串转数值的系列函数及其错误处理机制。
  - [Dev-CPP使用C++11](./C转C++教程/ch04-cpp11/06-Dev-CPP使用C++11.md) — 指导如何在 Dev C++ 中手动启用 C++11 标准。
  - [章节小结](./C转C++教程/ch04-cpp11/99-章节小结.md) — 总结 C++11 新特性章节的核心要点与速查表。

- **DDDMR Navigation 学习路线**
  - [DDDMR Navigation 学习 + 复现 + 实车部署 路线](./DDRMR_Navigation/DDDMR%20Navigation%20学习%20+%20复现%20+%20实车部署%20路线.md) — 针对有 ROS2 基础的学习者，规划 1–2 周从原理到实车部署的完整路线。

- **FreeRTOS**
  - [FreeRTOS操作系统移植教程-原理版](./FreeRTOS/FreeRTOS操作系统移植教程-原理版.md) — 从概念到实操，详细讲解 FreeRTOS 如何移植到 STM32F103 标准库工程。
  - [FreeRTOS操作系统移植教程-纯操作](./FreeRTOS/FreeRTOS操作系统移植教程-纯操作.md) — 仅保留操作步骤，快速指导 FreeRTOS 源码移植与配置。

- **Linux 系统裁剪**
  - [Linux系统裁剪-基础知识](./Linux系统裁剪/1.Linux系统裁剪-基础知识.md) — 介绍 Linux 系统构成（Uboot、内核、设备树、根文件系统）及裁剪本质。
  - [鲁班猫系统镜像裁剪实战](./Linux系统裁剪/2.鲁班猫系统镜像裁剪实战.md) — 基于 LubanCat_Gen_SDK 的鲁班猫系统镜像裁剪实战。

- **ROS2**
  - [引言](./ROS2/1.CLI/0.引言.md) — ROS2 CLI 部分学习导航，已更新完毕。
  - [配置环境](./ROS2/1.CLI/1.配置环境.md) — 配置 ROS2 环境变量与检查 ROS_DOMAIN_ID。
  - [使用turtlesim、ros2和rqt](./ROS2/1.CLI/2.使用turtlesim、ros2和rqt.md) — 安装 turtlesim 并体验 ROS2 基本命令与 rqt 图形界面。
  - [理解节点](./ROS2/1.CLI/3.理解节点.md) — 理解 ROS2 节点概念，使用 `ros2 node` 命令。
  - [理解话题](./ROS2/1.CLI/4.理解话题.md) — 理解话题通信机制，使用 `rqt_graph` 可视化节点话题。
  - [了解服务](./ROS2/1.CLI/5.了解服务.md) — 理解服务调用-响应模型，与话题的区别。
  - [理解参数](./ROS2/1.CLI/6.理解参数.md) — 理解节点参数，使用 `ros2 param` 命令。
  - [理解行为](./ROS2/1.CLI/7.理解行为.md) — 理解动作通信：目标、反馈、结果，以及可取消特性。
  - [使用rqt_console查看日志](./ROS2/1.CLI/8.使用rqt_console查看日志.md) — 使用图形工具查看和过滤日志消息。
  - [启动节点](./ROS2/1.CLI/9.启动节点.md) — 使用启动文件同时启动多个节点。
  - [录制和回放数据](./ROS2/1.CLI/10.录制和回放数据.md) — 录制和回放 ROS2 话题数据（暂略）。
  - [引言（客户端）](./ROS2/2.客户端/0.引言.md) — 客户端部分学习导航，已更新部分章节。
  - [什么是ROS 2包？](./ROS2/2.客户端/1.什么是ROS%202包？.md) — 介绍 ROS2 包的构成与文件结构。
  - [使用colcon 构建软件包](./ROS2/2.客户端/1.使用colcon%20构建软件包.md) — 安装 colcon 并创建第一个工作空间。
  - [创建一个工作空间](./ROS2/2.客户端/2.创建一个工作空间.md) — 详细步骤创建 ROS2 工作空间并克隆示例仓库。
  - [创建软件包](./ROS2/2.客户端/3.创建软件包.md) — 创建 ROS2 软件包（内容待补充）。

- **STM32 单片机**
  - [STM32简介](./STM32单片机/【1-1】STM32简介.md) — 介绍 STM32、ARM 架构、F103C8T6 资源与命名规则。
  - [软件安装](./STM32单片机/【2-1】软件安装.md) — 提供 Keil 与 STLINK 驱动安装说明。
  - [新建工程](./STM32单片机/【2-2】新建工程.md) — 讲解 STM32 开发方式（寄存器/标准库/HAL）并点亮第一个 LED。
  - [GPIO输出](./STM32单片机/【3-1】GPIO输出.md) — 总结 GPIO 操作三步法：开启时钟、初始化结构体、调用输出函数。
  - [LED&流水灯&蜂鸣器](./STM32单片机/【3-2】LED&流水灯&蜂鸣器.md) — 实现 LED 闪烁、流水灯与蜂鸣器控制，附常用 GPIO 输出函数。
  - [GPIO输入](./STM32单片机/【3-3】GPIO输入.md) — 学习按键与传感器模块的硬件电路及输入模式配置。
  - [按键控制LED&光敏控制蜂鸣](./STM32单片机/【3-4】按键控制LED&光敏控制蜂鸣.md) — 模块化编程实现按键控制 LED 与光敏传感器控制蜂鸣器。
  - [OLED调试工具](./STM32单片机/【4-1】OLED调试工具.md) — 介绍 OLED 屏幕作为调试工具，对比 I2C/SPI 通信方式。
  - [OLED显示屏](./STM32单片机/【4-2】OLED显示屏.md) — 接线与程序实例，展示 OLED 显示字符、数字、十六进制等。
  - [EXTI外部中断](./STM32单片机/【5-1】EXTI外部中断.md) — 详解外部中断配置步骤：RCC、GPIO、AFIO、EXTI、NVIC。
  - [红外传感&旋转编码计次](./STM32单片机/【5-2】红外传感&旋转编码计次.md) — 使用外部中断实现红外传感器计次与旋转编码器计数。
  - [定时器](./STM32单片机/【6-0】定时器.md) — 概述定时器四大功能：定时中断、输出比较、输入捕获、编码器接口。
  - [TIM定时中断](./STM32单片机/【6-1】TIM定时中断.md) — 讲解定时器基本原理、类型与基本定时器配置。
  - [定时中断&内外时钟源选择](./STM32单片机/【6-2】定时中断&内外时钟源选择.md) — 定时中断初始化步骤与内外时钟源选择。
  - [TIM输出比较](./STM32单片机/【6-3】TIM输出比较.md) — 详解输出比较模块用于产生 PWM 波形，驱动电机。
  - [流水灯&舵机电机驱动](./STM32单片机/【6-4】流水灯&舵机电机驱动.md) — 使用 PWM 实现 LED 流水灯、舵机与直流电机驱动。
  - [TIM输入捕获](./STM32单片机/【6-5】TIM输入捕获.md) — 理解输入捕获概念，用于测量频率与占空比。
  - [输入捕获测频率&PWMI测频率占空比](./STM32单片机/【6-6】输入捕获测频率&PWMI测频率占空比.md) — 使用输入捕获与 PWMI 模式测量频率和占空比，附相关库函数。
  - [ADC数模转换器](./STM32单片机/【7-1】ADC数模转换器.md) — 介绍 ADC 作用、逐次逼近型原理与 STM32 内部 ADC。
  - [AD单通道&多通道](./STM32单片机/【7-2】AD单通道&多通道.md) — 配置 ADC 单通道与多通道转换，附相关库函数。
  - [USART串口协议](./STM32单片机/【9-1】USART串口协议.md) — 讲解通信接口分类（双工、时钟、电平）与串口通信基础。
  - [USART串口外设](./STM32单片机/【9-2】USART串口外设.md) — 分析 USART 框图与基本结构，解释发送/接收数据流程。
  - [串口发送&串口接收](./STM32单片机/【9-3】串口发送&串口接收.md) — 实现串口发送与接收，附相关函数说明。
  - [USART串口数据包](./STM32单片机/【9-4】USART串口数据包.md) — 制定 HEX 与文本数据包格式，讨论收发流程。
  - [串口收发HEX&文本数据包](./STM32单片机/【9-5】串口收发HEX&文本数据包.md) — 实例代码实现串口收发 HEX 与文本数据包。
  - [FlyMcu & STLINK Utility](./STM32单片机/【9-6】FlyMcu%20&%20STLINK%20Utility.md) — 使用 FlyMcu 串口下载与 STLINK Utility 烧录程序。
  - [其他模块驱动学习](./STM32单片机/【番外】其他模块驱动学习.md) — 学习 NRF24L01 无线模块的引脚定义、工作原理与配置流程。

- **大车-CarPlanning（校园智巡）**
  - [项目介绍](./大车-CarPlanning/0.项目介绍.md) — 项目概述：基于 RTK 与激光融合的无图自主导航机器人。
  - [TODO清单](./大车-CarPlanning/1.TODO清单.md) — 新旧技术路线切换后的详细 TODO 清单与阶段划分。
  - [Nav2无图导航仿真搭建](./大车-CarPlanning/2.Nav2无图导航仿真搭建.md) — 在 ROS2 Humble 仿真中搭建无图导航，EKF + Nav2 完整流程。
  - [融入RTK-GPS插件进行仿真](./大车-CarPlanning/3.融入RTK-GPS插件进行仿真.md) — 在仿真中加入 GPS 定位链路，实现 map 与 UTM 对齐。
  - [功能包整合与 GitHub 管理](./大车-CarPlanning/4.功能包整合与%20GitHub%20管理.md) — 将所有配置整合进标准 ROS2 功能包，便于 git 管理。
  - [小车3D建模](./大车-CarPlanning/5.小车3D建模.md) — 使用 SolidWorks 进行小车 3D 建模，模型已上传 GitHub。
  - [仿真迁移实物](./大车-CarPlanning/6.仿真迁移实物.md) — 将仿真环境移植到实物硬件（底盘驱动、雷达、EKF 定位）。
  - [驱动层运行系统报告](./大车-CarPlanning/7.驱动层运行系统报告.md) — Xavier NX 驱动层运行状态报告，含 CPU/内存占用与风险评估。
  - [中期审视项目-拆分](./大车-CarPlanning/8.中期审视项目-拆分.md) — 项目功能模块任务拆分文档，供成员认领。
  - [ROS2 Humble 跨设备 DDS 组播通信配置指南](./大车-CarPlanning/9.ROS2%20Humble%20跨设备%20DDS%20组播通信配置指南.md) — 配置 WSL2 与 Jetson 间 DDS 通信，实现远程 RViz 可视化。
  - [校园智巡 Nav Console — 部署与启动手册](./大车-CarPlanning/10.校园智巡%20Nav%20Console%20—%20部署与启动手册.md) — Web 控制台部署与启动手册，覆盖 Xavier NX 与开发电脑。
  - [校园智巡 — 近一周进度汇报（2026-06-02）](./大车-CarPlanning/11.校园智巡%20—%20近一周进度汇报.md) — 汇报 USB 串口固定绑定与跨设备 DDS 通信配置成果。
  - [校园智巡 — 近一周进度汇报（2026-06-16）](./大车-CarPlanning/12.校园智巡%20—%20近一周进度汇报.md) — 汇报 3D 打印连接件散热隔离、上下层控制对齐与实车测试结果。
  - [项目概述：RTK + LiDAR 里程计无地图自主导航系统（v2）](./大车-CarPlanning/13.项目概述：RTK%20+%20LiDAR%20里程计无地图自主导航系统（v2）.md) — v2 架构引入 FAST-LIO2 替代轮式里程计，CPU 迁移至 Intel N100。
  - [FAST-LIO2 详解：在校园智巡项目中的角色](./大车-CarPlanning/14.FAST-LIO2%20详解：在校园智巡项目中的角色.md) — 深入讲解 FAST-LIO2 原理、与轮式里程计对比、方案选型理由。
  - [任务计划：校园智巡 v2 升级路线图](./大车-CarPlanning/15.任务计划：校园智巡%20v2%20升级路线图.md) — 分阶段任务计划，从 N100 环境搭建到收尾优化。
  - [FASTLIO2_ROS2 实战使用指南](./大车-CarPlanning/16.FASTLIO2_ROS2%20实战使用指南.md) — 针对校园智巡 v2 的 FASTLIO2 配置修改与实战指南。
  - [支线：0.Jetson Xavier Nx烧录刷机安装Ubuntu20.04系统及后续配置](./大车-CarPlanning/支线：0.Jetson%20Xavier%20Nx烧录刷机安装Ubuntu20.04系统及后续配置.md) — 转载整理 Jetson Xavier NX 刷机、系统扩容与基础配置。
  - [支线：1.NVIDIA Jetson 通过自建 Ubuntu 22.04 Docker 镜像安装 ROS 2 Humble](./大车-CarPlanning/支线：1.NVIDIA%20Jetson%20通过自建%20Ubuntu%2022.04%20Docker%20镜像安装%20ROS%202%20Humble.md) — 在 Jetson 上自建 Docker 镜像安装 ROS2 Humble，对比 dustynv 方案。
  - [支线：2.MID-360雷达环境搭建](./大车-CarPlanning/支线：2.MID-360雷达环境搭建.md) — 完整链路：网口配置、上位机确认、驱动安装、Fast-LIO 建图。
  - [支线：3.电源规划](./大车-CarPlanning/支线：3.电源规划.md) — 用电设备清单与供电方案（4S LiPo 14.8V 7000mAh）。
  - [支线：4.UM982 RTK GPS ROS2 驱动部署文档](./大车-CarPlanning/支线：4.UM982%20RTK%20GPS%20ROS2%20驱动部署文档.md) — 在 Jetson Docker 中部署 UM982 GPS 驱动，发布 /gps/fix 话题。
  - [支线：5.Jetson Xavier NX — USB 串口设备固定绑定指南](./大车-CarPlanning/支线：5.Jetson%20Xavier%20NX%20—%20USB%20串口设备固定绑定指南.md) — 通过 udev 规则固定 USB 串口设备符号链接，解决编号漂移。
  - [支线：6.FASTLIO2_ROS2 完整部署教程](./大车-CarPlanning/支线：6.FASTLIO2_ROS2%20完整部署教程.md) — 在 Ubuntu 22.04 原生系统上部署 FASTLIO2_ROS2 的完整步骤。
  - [附录-运行中遇到的报错记录](./大车-CarPlanning/附录-运行中遇到的报错记录.md) — 记录 WSL2 下 ROS2 topic list 无反应等常见报错及解决方案。
  - [旧2.第一阶段 车辆与物理环境](./大车-CarPlanning/旧2.第一阶段%20车辆与物理环境.md) — （已归档）早期阿克曼模型获取与 Gazebo 测试。
  - [旧3.第二阶段 LIO-SAM 适配](./大车-CarPlanning/旧3.第二阶段%20LIO-SAM%20适配.md) — （已归档）LIO-SAM 环境搭建与编译。
  - [旧4.第三阶段 Mid360插件替换](./大车-CarPlanning/旧4.第三阶段%20Mid360插件替换.md) — （已归档）Livox-SDK2 与 livox_ros_driver2 编译安装。

- **嵌入式 Linux 基础**
  - [前言](./嵌入式LInux基础/1.前言.md) — 学习笔记开篇，介绍基于 i.MX6ULL 的嵌入式 Linux 学习路线。
  - [如何学习Linux开发](./嵌入式LInux基础/2.如何学习Linux开发.md) — 提供嵌入式 Linux 学习路线图。
  - [i.MX系列芯片简介](./嵌入式LInux基础/3.i.MX系列芯片简介.md) — 介绍 i.MX 系列、ARM 架构与 Cortex-A7 内核。
  - [Linux系统简介](./嵌入式LInux基础/4.Linux系统简介.md) — 讲解 Linux 起源、主要构成与发行版本。
  - [虚拟机安装Ubuntu系统](./嵌入式LInux基础/5.虚拟机安装Ubuntu系统.md) — 指导虚拟机安装 Ubuntu 并设置共享文件夹。
  - [Linux文件目录](./嵌入式LInux基础/6.Linux文件目录.md) — 介绍 Linux 目录层次标准与各目录用途。
  - [用户管理与文件权限](./嵌入式LInux基础/7.用户管理与文件权限.md) — 讲解 Linux 用户管理、passwd/group/shadow 文件与文件权限。
  - [Linux命令行](./嵌入式LInux基础/8-10.Linux命令行.md) — 介绍 Shell 概念、命令格式与常用命令（man、ls 等）。
  - [使用编辑器](./嵌入式LInux基础/11.使用编辑器.md) — 介绍 gedit 与 vi/vim 编辑器的使用。
  - [运行开发板与串口终端登录](./嵌入式LInux基础/12.运行开发板与串口终端登录.md) — 指导开发板启动与串口终端登录。
  - [查看开发板系统信息](./嵌入式LInux基础/13.查看开发板系统信息.md) — 通过 /proc 文件系统查看 CPU、内核版本等信息。
  - [命令行点灯和检测按键](./嵌入式LInux基础/14.命令行点灯和检测按键.md) — 通过 /sys 文件系统控制 LED 灯与检测按键。
  - [使用脚本测试硬件](./嵌入式LInux基础/15.使用脚本测试硬件.md) — 使用 fire-config 与测试脚本验证板载外设功能。
  - [认识系统镜像和固件](./嵌入式LInux基础/16.认识系统镜像和固件.md) — 介绍镜像文件格式与野火 Debian 镜像版本。
  - [烧录Debian镜像至SD卡](./嵌入式LInux基础/17.烧录Debian镜像至SD卡.md) — 使用 Etcher 烧录 Debian 镜像至 SD 卡并启动。
  - [fire-config工具简介](./嵌入式LInux基础/18.fire-config工具简介.md) — 介绍野火开发板系统配置工具 fire-config 的使用。
  - [项目资料下载-git](./嵌入式LInux基础/19.项目资料下载-git.md) — 使用 Git 从 GitHub/Gitee 下载项目资料。
  - [挂载NFS网络文件系统](./嵌入式LInux基础/20.挂载NFS网络文件系统.md) — 搭建 NFS 环境实现主机与开发板文件共享。
  - [GCC和Hello World](./嵌入式LInux基础/21.GCC和Hello%20World.md) — 讲解 GCC 编译工具链与 Hello World 的编译运行过程。
  - [ARM-GCC和开发板的HelloWorld](./嵌入式LInux基础/22.ARM-GCC和开发板的HelloWorld.md) — 交叉编译 Hello World 并在 ARM 开发板上运行。
  - [Linux系统下的Hello World](./嵌入式LInux基础/23.%20Linux系统下的Hello%20World.md) — 深入分析 Linux 下 Hello World 的运行机制，对比裸机开发。
  - [Makefile简介](./嵌入式LInux基础/24.%20Makefile简介.md) — 介绍 Makefile 的作用、依赖关系与基本概念。
  - [使用Makefile控制编译](./嵌入式LInux基础/25.%20使用Makefile控制编译.md) — 通过示例学习 Makefile 的基础语法与规则。
  - [文件操作与系统调用](./嵌入式LInux基础/26.%20文件操作与系统调用.md) — 讲解文件系统概念、C 标准库与系统调用的关系。

<!-- AI_CONTENT_END -->
