# Chuiyu Wiki (吹雨的知识库)

<p align="center">
  <img src="public/logo.jpg" alt="Logo" width="120" height="120" style="border-radius: 50%;">
</p>

<p align="center">
  <strong>要努力去发光,而不是被照亮</strong>
</p>

<p align="center">
  <a href="https://github.com/ana52070/chuiyu_Wiki">
    <img src="https://img.shields.io/github/stars/ana52070/chuiyu_Wiki?style=social" alt="GitHub stars">
  </a>
  <a href="https://github.com/ana52070/chuiyu_Wiki/fork">
    <img src="https://img.shields.io/github/forks/ana52070/chuiyu_Wiki?style=social" alt="GitHub forks">
  </a>
  <a href="https://github.com/ana52070/chuiyu_Wiki/issues">
    <img src="https://img.shields.io/github/issues/ana52070/chuiyu_Wiki" alt="GitHub issues">
  </a>
  <a href="https://github.com/ana52070/chuiyu_Wiki/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/ana52070/chuiyu_Wiki" alt="License">
  </a>
</p>

---

## 📖 项目简介

**Chuiyu Wiki** 是一个基于 [VitePress](https://vitepress.dev/) 构建的个人知识库与博客系统。这里记录了我在学习和开发过程中的点滴积累，涵盖了嵌入式开发、人工智能、Linux 系统、ROS2 等多个领域的技术笔记与项目实战。

本项目采用了 [vitepress-theme-teek](https://github.com/teek-theme/vitepress-theme-teek) 主题，界面简洁美观，支持多种自定义配置。

## 🚀 内容概览

知识库主要包含以下几个板块：

*   **✍️ 博客文章 (`/blog/`)**: 分享技术心得、教程和随笔。
    *   单片机开发 (STM32, 传感器驱动等)
    *   AI 大模型应用 (LLM, 语音识别, TTS)
    *   Linux 运维与工具使用
    *   其他有趣的技术探索
*   **📚 学习笔记 (`/guide/`)**: 系统性的学习资料和教程。
    *   嵌入式 Linux 基础
    *   C++ 进阶 (C++17, 基础)
    *   ROS2 机器人操作系统
    *   STM32 单片机入门
    *   Linux 系统裁剪
*   **🛠️ 项目记录 (`/projects/`)**: 个人参与或开发的开源项目展示。
    *   嵌入式 Linux 项目 (AI 跟踪, YOLO, Web 控制)
    *   单片机项目 (FreeRTOS, MCP 控制)
    *   软件项目

## ✨ 特性

*   **自动化部署**: 集成 `upload_with_llm.py` 脚本，利用 LLM 自动生成 Commit Message 并同步到 GitHub。
*   **现代化主题**: 使用 Teek 主题，支持暗黑模式、动态 Banner、文章分类与标签。
*   **全文搜索**: 内置本地搜索功能，快速定位知识点。
*   **响应式设计**: 完美适配桌面端与移动端阅读体验。

## 🛠️ 本地运行

如果你想在本地运行或贡献代码，请按照以下步骤操作：

1.  **克隆仓库**
    ```bash
    git clone https://github.com/ana52070/chuiyu_Wiki.git
    cd chuiyu_Wiki
    ```

2.  **安装依赖**
    ```bash
    npm install
    ```

3.  **启动开发服务器**
    ```bash
    npm run docs:dev
    ```
    启动后，访问 `http://localhost:5173` 即可预览。

4.  **构建静态文件**
    ```bash
    npm run docs:build
    ```

## 🤖 自动化同步脚本

本项目包含一个 Python 脚本 `upload_with_llm.py`，用于简化 Git 提交流程：

*   自动检测文件变更。
*   使用 OpenRouter API (Gemini/DeepSeek 等) 智能生成 Commit Message。
*   自动处理 Git Add, Commit, Push 流程。
*   支持网络代理配置，确保连接稳定性。

**使用方法:**
```bash
python upload_with_llm.py
```
*(需配置 `.env` 文件中的 `OPENROUTER_API_KEY`)*

## 🤝 友情链接

*   [Github 个人主页](https://github.com/ana52070)
*   [B站 个人主页](https://space.bilibili.com/166842001)
*   [CSDN 个人主页](https://blog.csdn.net/chui_yu666)

## 📄 许可证

本项目采用 [ISC License](LICENSE) 许可证。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/ana52070">Chuiyu</a>
</p>