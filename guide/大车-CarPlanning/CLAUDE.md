# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

始终使用简体中文回复（Always respond in Chinese-simplified）。

## 这是什么

这是 **Chuiyu Wiki** 个人知识库（VitePress 站点）中的一个内容子目录，**不是软件工程项目本身**——它是一个机器人项目的中文技术文档集合。所有交付物都是带 YAML frontmatter 的 Markdown 文件，没有需要编译的源代码。

当前目录 `guide/大车-CarPlanning/` 记录「校园智巡」项目：基于 RTK + Livox Mid-360 激光融合的无图自主导航差速机器人（ROS2 Humble / Nav2 / robot_localization）。仓库根目录在 `../../`（`my-knowledge-base/`）。

## 内容结构与命名约定

- 文档按 `数字.标题.md` 顺序编号，构成主线开发路线（0 项目介绍 → 11 进度汇报）。
- `支线：N.标题.md`：与主线并行的硬件/环境搭建专题（Jetson 刷机、Docker、Mid-360、RTK、USB 串口绑定、电源）。
- `旧N.*.md`：已被取代的早期阶段文档，保留作存档，**不要当作当前方案修改**。
- `附录-*.md`：报错记录等横切参考。
- `assets/`：文档引用的图片，被构建与侧边栏忽略。

新增文档时沿用现有编号体系和中文文件名；正文用中文，技术术语/命令保留原文。

## Frontmatter（重要）

每个文档以 YAML frontmatter 开头。`categories`、`tags`、`permalink` 由 Teek 主题插件（`autoFrontmatter` + `sidebar: true`，见 `../../.vitepress/teekConfig.ts`）**自动生成**——新建文件时可只写 `title` 和 `date`，构建时会补全；不要手动维护侧边栏，它从目录结构自动派生。

## 命令（在仓库根目录 `../../` 运行）

```bash
npm install              # 安装依赖
npm run docs:dev         # 本地预览 (http://localhost:5173)
npm run docs:build       # 构建静态站点——用它验证 Markdown/构建错误
npm run docs:preview     # 预览构建产物
```

没有自动化测试套件（`npm test` 是占位符，直接报错退出）。验证文档改动的唯一方式是 `docs:dev` 或 `docs:build`。

## 提交与自动化

- 根目录 `upload_with_llm.py`（`python upload_with_llm.py`）会检测变更、调用 OpenRouter LLM 生成 commit message 并自动 add/commit/push，需要根目录 `.env` 中的 `OPENROUTER_API_KEY`。推送前应核对生成的提交信息。
- 历史提交混用 `Auto update: YYYY-MM-DD HH:MM:SS` 与 `docs:`/`fix:` 前缀两种风格。
