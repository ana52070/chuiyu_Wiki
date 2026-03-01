---
author: ana52070
categories:
- 软件项目
date: 2026-03-2
description: 暂无描述
tags:
- 软件项目
title: Flick - 桌面效率工具箱
permalink: /projects/软件项目/Flick - 桌面效率工具箱
---

> 项目地址：https://github.com/ana52070/Flick
> 
> Flick 是一个基于 .NET 8 和 WPF 构建的现代化 Windows 桌面效率工具。它集成了强大的剪贴板历史管理功能和多模型 AI 助手，旨在通过流畅的交互体验提升您的日常工作效率。

---



# Flick - 桌面效率工具箱

Flick 是一个基于 .NET 8 和 WPF 构建的现代化 Windows 桌面效率工具。它集成了强大的剪贴板历史管理功能和多模型 AI 助手，旨在通过流畅的交互体验提升您的日常工作效率。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![.NET](https://img.shields.io/badge/.NET-8.0-purple.svg)

## ✨ 主要功能

### 📋 智能剪贴板管理
不再丢失任何复制过的内容。Flick 在后台静默监听系统剪贴板，支持多种格式：
- **文本**: 自动保存并支持预览。
- **图片**: 自动保存图片到本地并生成缩略图，支持预览分辨率。
- **文件**: 记录复制的文件路径列表。
- **去重**: 智能识别重复内容，避免历史记录冗余。
- **持久化**: 使用 SQLite 本地数据库存储，重启后依然可用。

### 🤖 AI 助手集成
一键唤起 AI 助手，无缝集成主流大模型服务：
- **多模型支持**: 内置 **豆包**, **Gemini**, **Claude** 支持。
- **智能上下文**: 唤起 AI 时，Flick 会自动模拟 `Ctrl+C` 获取您当前选中的文本，并将其注入到 AI 对话框中，实现“即选即问”。
- **极速启动**: 采用 WebView2 预热机制，消除首次加载延迟，实现秒开体验。

### 🔒 隐私与安全
- **本地优先**: 所有剪贴板历史数据仅存储在您本地的 SQLite 数据库中 (`%APPDATA%\Flick\flick.db`)，绝不上传云端。
- **图片本地化**: 复制的图片资源安全地保存在本地应用数据目录中。

## 🛠️ 技术栈

- **核心框架**: .NET 8, WPF (Windows Presentation Foundation)
- **架构模式**: MVVM (Model-View-ViewModel)
- **依赖注入**: Microsoft.Extensions.DependencyInjection
- **数据存储**: Entity Framework Core + SQLite
- **Web 渲染**: Microsoft Edge WebView2
- **系统集成**: Win32 API (Hooks, Clipboard, Hotkeys)
- **日志系统**: Serilog

## 🚀 快速开始

### 环境要求
- Windows 10 或 Windows 11
- .NET 8 SDK

### 构建与运行

1. 克隆仓库：
   ```bash
   git clone https://github.com/yourusername/Flick.git
   cd Flick
   ```

2. 还原依赖并构建：
   ```bash
   dotnet restore
   dotnet build
   ```

3. 运行应用：
   ```bash
   cd src/Flick.App
   dotnet run
   ```

### 📦 发布构建

如果您需要生成可独立运行的 Windows x64 可执行文件（无需安装 .NET Runtime）：

```bash
dotnet publish src/Flick.App/Flick.App.csproj -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true -o ./publish/win-x64
```

构建完成后，您可以在 `publish/win-x64` 目录下找到 `Flick.exe`。

## ⌨️ 快捷键指南

Flick 旨在通过键盘操作最大化效率：

| 快捷键 | 功能 | 说明 |
| :--- | :--- | :--- |
| **Alt + V** | 剪贴板历史 | 打开剪贴板历史记录窗口，支持搜索和回车粘贴 |
| **Alt + 1** | 豆包 AI | 唤起豆包 AI 助手 (自动带入选中文字) |
| **Alt + 2** | Gemini AI | 唤起 Gemini AI 助手 (自动带入选中文字) |
| **Alt + 3** | Claude AI | 唤起 Claude AI 助手 (自动带入选中文字) |
| **Alt + Space** | 命令面板 | (开发中) 快速执行系统命令 |

## 📂 项目结构

```
src/
├── Flick.App/            # WPF 主应用程序 (UI, ViewModels, Views)
├── Flick.Core/           # 核心业务逻辑 (剪贴板监听, 业务处理)
├── Flick.Infrastructure/ # 基础设施层 (存储, 系统钩子, 日志, Win32 API)
└── Flick.Shared/         # 共享模型与接口
```

## 📄 许可证

本项目采用 [MIT 许可证](../../node_modules/glob/LICENSE.md) 开源。