

---
date: 2026-02-05 17:48:16
title: README
permalink: /pages/7670fd
categories:
  - 
---
# Chuiyu Wiki (Chuiyu's Knowledge Base)

<p align="center">
  <img src="/logo.jpg" alt="Logo" width="120" height="120" style="border-radius: 50%;">
</p>

<p align="center">
  <strong>Strive to shine brightly, rather than just be illuminated.</strong>
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

## 📖 Project Introduction

**Chuiyu Wiki** is a personal knowledge base and blog system built with [VitePress](https://vitepress.dev/). It documents my accumulated insights and experiences throughout my learning and development journey, covering technical notes and practical projects in areas such as embedded development, artificial intelligence, Linux systems, and ROS2.

This project uses the [vitepress-theme-teek](https://github.com/Kele-Bingtang/vitepress-theme-teek) theme, featuring a clean and elegant interface with support for various custom configurations.

## 🚀 Content Overview

The knowledge base is primarily organized into the following sections:

*   **✍️ Blog Posts (`/blog/`)**: Sharing technical insights, tutorials, and reflections.
    *   Microcontroller Development (STM32, Sensor Drivers, etc.)
    *   AI Large Model Applications (LLM, Speech Recognition, TTS)
    *   Linux Administration & Tool Usage
    *   Other Interesting Technical Explorations
*   **📚 Study Notes (`/guide/`)**: Systematic learning materials and tutorials.
    *   Embedded Linux Fundamentals
    *   Advanced C++ (C++17, Basics)
    *   ROS2 Robot Operating System
    *   Getting Started with STM32 Microcontrollers
    *   Linux System Customization
*   **🛠️ Project Logs (`/projects/`)**: Showcases of open-source projects I've contributed to or developed.
    *   Embedded Linux Projects (AI Tracking, YOLO, Web Control)
    *   Microcontroller Projects (FreeRTOS, MCP Control)
    *   Software Projects

## ✨ Features

*   **Automated Deployment**: Integrated with the `upload_with_llm.py` script, which leverages an LLM to automatically generate commit messages and sync to GitHub.
*   **Modern Theme**: Utilizes the Teek theme, supporting dark mode, dynamic banners, and article categories/tags.
*   **Full-Text Search**: Built-in local search functionality for quick knowledge retrieval.
*   **Responsive Design**: Fully optimized for both desktop and mobile reading experiences.

## 🛠️ Running Locally

If you want to run the project locally or contribute code, please follow these steps:

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/ana52070/chuiyu_Wiki.git
    cd chuiyu_Wiki
    ```

2.  **Install Dependencies**
    ```bash
    npm install
    ```

3.  **Start the Development Server**
    ```bash
    npm run docs:dev
    ```
    Once started, visit `http://localhost:5173` to preview the site.

4.  **Build Static Files**
    ```bash
    npm run docs:build
    ```

## 🤖 Automated Sync Script

This project includes a Python script `upload_with_llm.py` designed to streamline the Git commit workflow:

*   Automatically detects file changes.
*   Uses the OpenRouter API (Gemini/DeepSeek, etc.) to intelligently generate commit messages.
*   Automatically handles the Git Add, Commit, and Push workflow.
*   Supports network proxy configuration to ensure connection stability.

**Usage:**
```bash
python upload_with_llm.py
```
*(Requires configuring `OPENROUTER_API_KEY` in the `.env` file)*

## 🤝 External Links

*   [GitHub Profile](https://github.com/ana52070)
*   [Bilibili Profile](https://space.bilibili.com/166842001)
*   [CSDN Profile](https://blog.csdn.net/chui_yu666)

## 📄 License

This project is licensed under the [ISC License](LICENSE).

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/ana52070">Chuiyu</a>
</p>
