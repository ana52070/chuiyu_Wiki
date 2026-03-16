---
author: lunar
date: 2026-03-16
description: claude code +AI coding plan
tags:
  - ai
---

## 导读

这篇文章想解决一个很现实的问题：**我想用 AI 帮我写代码，但我不想只在网页里聊天，我希望它能“进到项目里”读文件、跑命令、改代码，而且最好还能配合一套“先计划再动手”的工作方式。**

- 第 1 部分：Claude Code 是什么
- 第 2 部分：Claude Code 最基本怎么用（小白向）
- 第 3 部分：什么是 Coding Plan（国内语境里说的那个）
- 第 4 部分：Coding Plan/模型/套餐怎么选（不带货，给思路）
- 第 5 部分：Claude Code + Coding Plan 的配置教程（以 Anthropic 兼容接口为例）

文末我会把用到的资料来源列出来，方便你对照。


另外，你也可以通过观看B站视频来跟着操作，或者学习一些有关于ai coding等一系列知识。
【8分钟带你快速部署Claude Code(大学生向)】 https://www.bilibili.com/video/BV1SiA1zKEgS/?share_source=copy_web&vd_source=800b0cce2dee97823e91fad6181bdec5

【免费Claude Code，免费模型有满血版几成功力？ Claude Code高热度AI编程工具】 https://www.bilibili.com/video/BV1jGtEzNEAv/?share_source=copy_web&vd_source=800b0cce2dee97823e91fad6181bdec5

【最火AI编程Claude Code详细攻略，一期视频精通】 https://www.bilibili.com/video/BV1XGbazvEuh/?share_source=copy_web&vd_source=800b0cce2dee97823e91fad6181bdec5



## 1. 什么是 Claude Code

一句话：**Claude Code 是一个“跑在你电脑终端里的编程助手”。**

它跟网页里那种对话式 AI 最大的区别是：它不只是回答问题，它还能在你允许的范围内**读取你的代码仓库、编辑文件、运行命令**，并且能跨多个文件完成任务。

你可以把它想象成一个“很会写代码的同事”，你把项目目录给他看，他就能：

- 帮你理解项目结构（比如：入口在哪、模块怎么分）
- 帮你改代码（比如：修 bug、加功能）
- 帮你跑命令做验证（比如：npm test、pytest、go test、make）

它的入口通常是一个命令：

```bash
claude
```

然后你在里面用自然语言说需求，它会边做边问你要不要授权执行某些操作。

> 资料来源：Claude Code 官方概览页（Claude Code overview）

## 2. Claude Code 的基本用法（小白版）

下面按“从 0 到能用”走一遍。你不需要提前理解所有名词，照做就行。

### 2.1 安装（Windows / Linux：先装 Node.js，再用 npm 安装 Claude Code）

这一节只写 **Windows** 和 **Linux**，并且用“Node.js + npm”这种更常见的安装方式。

你可以把它理解成：先把“包管理工具”装好（npm），再用它把 Claude Code 这个程序装到全局。

#### 2.1.1 先安装 Node.js（建议 18+，优先选 LTS）

这一步的目标是：把 `node` 和 `npm` 装到电脑上。**npm 就像一个“应用商店/软件安装器”**，后面我们会用它来安装 Claude Code。

先给你一张“官方下载安装页”的样子，方便你对照：

![Node.js 下载页示意](/blog/ai/assets/nodejs-download-page.png)

下面分别写 Windows 和 Linux（尽量按“小白照着做就能成功”的方式写）。

**Windows 安装（推荐：MSI 安装包）**

1）打开 Node.js 官方下载页：

https://nodejs.org/en/download/

2）在页面上选择：

- 版本：尽量选 **LTS**（更稳定）
- 平台：Windows
- 架构：一般选 x64

3）下载后会得到一个 `.msi` 安装包，双击安装。

4）安装过程中保持默认选项即可。注意有一个选项类似 “**Automatically install the necessary tools**” 或 “安装额外工具”，不确定就先不要勾（小白也能正常用）。

5）安装完成后，打开 **PowerShell** 或 **CMD**，输入：

```bash
node -v
npm -v
```

能看到版本号就说明成功了。

如果你输入 `node -v` 提示找不到命令，最常见原因是：安装完终端没重开。把终端关掉重开再试一次。

**Linux 安装（两种常见方式，二选一）**

方式 A：用 nvm（更推荐，后面换版本很省心）

nvm 你可以理解成“Node.js 的版本管理器”，适合需要经常切换 Node 版本的人。Node.js 官网也给了 nvm 的安装方式。

```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash

# 不重启终端的情况下手动加载 nvm（照抄即可）
. "$HOME/.nvm/nvm.sh"

# 安装 Node.js（示例：安装 24，对应当前 LTS 大版本）
nvm install 24

# 验证
node -v
npm -v
```

方式 B：用系统包管理器（适合“我就想快点装上能用”）

不同发行版命令不一样。最稳的做法是：直接看 Node.js 官网的“Package manager”页面，按你的发行版选择命令：

https://nodejs.org/en/download/package-manager

装完后同样用下面两条验证：

```bash
node -v
npm -v
```

> 资料来源：Node.js 官方下载页与 Package manager 页面（文末也会列出）。

#### 2.1.2 用 npm 安装 Claude Code

在终端执行：

```bash
npm install -g @anthropic-ai/claude-code
```

装完后验证：

```bash
claude --version
```

> 提醒：官方文档里也说明“npm 安装需要 Node.js 18+”。另外不要用 `sudo npm install -g`，容易带来权限问题（后续卸载/更新也麻烦）。

#### 2.1.3 Windows 额外前置：Git for Windows 或 WSL

Windows 上运行 Claude Code，一般需要 **Git for Windows**（或使用 WSL）。如果你已经装了 Git，通常就够用。

> 资料来源：Claude Code 官方 Advanced setup（包含 npm 安装与 Windows 依赖说明）

### 2.2 在你的项目里启动（以及一个“新手会卡住”的点）

关键点只有一个：**在项目目录里启动**。比如你的项目在 `~/work/my-app`：

```bash
cd ~/work/my-app
claude
```

第一次启动时，Claude Code 通常会要求你登录/授权（会打开浏览器）。

这里要提前讲清楚一个现实情况：**如果你没有 Claude 的付费订阅或 Anthropic Console 账号，这一步可能走不通**，很多小白会直接卡在“登录/没权限/连不上”。

所以这篇文章后面才会讲“国内 Coding Plan（套餐 + 专属 API Key）”这种接入方式：你可以把 Claude Code 连接到一个第三方的模型服务上（只要它提供 Anthropic 兼容接口）。

如果你就是没有官方账号，建议你**先跳到第 5 节把第三方 Provider 配好**，再回来启动 `claude`，体验会顺很多。

### 2.3 你真正会用到的“斜杠命令”（在 Claude Code 里面输入）

很多新手一开始会以为“Claude Code 的命令”都是在终端里敲 `claude ...` 这种。

但你真正用得最多的，往往是**进入 Claude Code 之后**，在对话框里输入的那种 **`/xxx` 斜杠命令**。它们更像是“这个工具自带的快捷按钮”，用来做状态检查、切模型、清理对话、进入规划模式。

下面这几个是最常见、也最值得记住的：

```text
/init
```

让 Claude Code 在项目根目录生成一个 `CLAUDE.md`（或者类似的项目说明文件）。你可以把它当成“项目说明书 + 约定”，比如写：怎么启动、怎么跑测试、代码风格是什么。以后每次你用 Claude Code，它都会更懂你的项目。

```text
/status
```

查看当前会话的状态，比如：它现在用的是什么模型、连接的是哪家服务（Base URL）、有没有读到你的配置等。新手遇到“怎么感觉没生效”的问题，第一反应就先跑一下 `/status`。

```text
/model
```

切换模型。你可以理解成“同一个工具换不同的大脑”。写代码多的时候，有些模型更顺手；读长日志、做分析时，可能另一些更合适。

```text
/plan
```

进入规划模式（Plan mode）。这个模式下你可以要求它**先给方案、先拆步骤**，你确认后再改代码。对小白来说，它最大的价值是：把“AI 直接乱改一通”的风险降下来。

```text
/clear
```

清空当前对话历史，重新开始。你可以把它当成“把桌面收拾干净”。当你发现对话越聊越乱、它开始跑偏，就用这个。

```text
/compact
```

把当前对话压缩成摘要，节省上下文空间。简单说：把一堆聊天记录“打包成要点”，避免越聊越慢、越聊越贵。

如果你只想记一件事：**日常用 `/status` 看是否配置生效，用 `/model` 换模型，用 `/plan` 先规划，再让它动手。**

> 资料来源：Claude Code 官方 CLI reference（命令行相关）以及常见工具内置命令说明（不同版本可能略有差异，以实际界面为准）

## 3. 什么是 Coding Plan（国内语境里说的那个）

这里的 **Coding Plan** 不是“泛指一套工作流程”的意思。

在国内很多教程/工具里，**Coding Plan 更像是一种“专门给 AI 编程工具用的 API 套餐服务”**：

- 你按月订阅（固定月费）
- 平台给你一个“专属 API Key”（相当于一把钥匙）
- 你把这把钥匙填到 Claude Code / Qwen Code 这类编程工具里
- 工具就能通过这个套餐去调用模型（通常是更适合写代码的那批模型）

如果你把 Claude Code 想成一台“电动螺丝刀”，那 Coding Plan 更像是“你办的一张电池年卡/月卡”：

- 没卡也能用？可以，但可能很贵/不稳定/或者根本没有权限
- 有卡之后，工具就能稳定地拿到“电”，你只管干活

以阿里云百炼的 Coding Plan 为例，它的页面会明确写：

- 它整合了多家模型（例如千问、GLM、Kimi、MiniMax 等）
- 提供固定月费、按配额限制请求次数
- **强调只允许在编程工具中交互式使用**，不允许你把套餐 Key 当普通 API 去写脚本批量调用

这也是为什么很多小白会选择“先装 Claude Code（工具本体），再用 Coding Plan 解决账号/成本/模型选择”的问题。

> 资料来源：阿里云百炼 Coding Plan 概述页（对套餐形态、模型支持、用量限制、使用范围有明确说明）

## 4. Coding Plan / 模型 / 套餐怎么选（给思路，不给答案）

Coding Plan 这事非常因人而异，所以这一节只给你一个**可操作的选择框架**。

### 4.1 先想清楚你要解决哪类任务

可以粗分三类：

第一类：日常小修小补
比如：改一个接口字段、修一个小 bug、加一个参数校验。特点是短、快、频繁。

第二类：中等规模的功能开发
比如：加一个登录流程、做一个配置页面、重构某个模块。特点是需要“持续多轮对话”，上下文比较长。

第三类：复杂工程任务
比如：跨模块重构、性能优化、协议适配、引入新框架。特点是步骤多、验证链路长，最需要 Plan。

你可以按自己的主要场景来选：你更在意“便宜”“稳定”“聪明”“长上下文”“工具调用能力”。优先级不同，选择自然不同。

### 4.2 模型选择的一个朴素原则

- 如果你主要写代码、改代码：优先选 **coder 类 / 编程优化** 的模型（或者官方明确适合 coding 的模型）。
- 如果你经常要读很长的日志/文档/多文件：优先选 **上下文更强** 的模型。
- 如果你预算敏感：就选 **更便宜但够用** 的模型，把“高端模型”留给难题。

你可以从一个“默认模型”开始用一周：统计一下你最常做的任务类型，再决定要不要升级。

### 4.3 套餐选择看三个指标

- 你一周大概会用多少次（轻度/中度/重度）
- 你的任务是不是经常很复杂（复杂任务一般更费额度/更费调用次数）
- 你是否接受按量计费的波动（有些人就喜欢“固定月费心里稳”）

> 资料来源：阿里云百炼 Coding Plan 概述页（包含支持模型、用量限制、以及“仅限在编程工具中使用”等注意事项）

### 4.4 国内 Coding Plan / 编程用 API 套餐购买入口（汇总）

不同平台的名字可能都叫“Coding Plan”，也可能不叫这个名字，但做的事情类似：给你一个专门面向编程工具的套餐/额度，让你把 Key 填进 Claude Code 之类的工具里用。

这里我只把**官方入口**列出来，方便你自己对比。

云厂商（通常更像“Coding Plan/订阅套餐”）：

- 阿里云百炼 Coding Plan（订阅/购买入口）：https://www.aliyun.com/benefit/scene/codingplan
- 腾讯云 Coding Plan（订阅/购买入口）：https://cloud.tencent.com/act/pro/codingplan
- 火山引擎（方舟）Coding Plan（活动/购买入口）：https://www.volcengine.com/activity/codingplan
- 百度智能云 Coding Plan（产品入口）：https://cloud.baidu.com/product/codingplan.html

模型厂商（不一定叫 Coding Plan，更多是“API 平台/充值/套餐”）：

- Kimi（月之暗面）开放平台（API/Key/计费入口）：https://platform.moonshot.cn/
- MiniMax Coding Plan（订阅入口）：https://platform.minimaxi.com/subscribe/coding-plan

> 小提示：如果你打开的是活动页或跳转页，建议从平台的“控制台/模型服务/计费”再确认一次，避免链接随活动结束失效。

## 5. Claude Code + Coding Plan 配置教程（Anthropic 兼容接口）

这一节目标是：**让 Claude Code 不走默认的 Anthropic 官方通道，而是改走一个 Anthropic 兼容的第三方提供方**（例如某些 Coding Plan / 网关服务）。

你不需要理解“兼容接口”的所有细节，只要记住：

- Claude Code 本来要连一个“模型服务”
- 你把它的“服务器地址”和“钥匙”换成你自己的，它就会去你指定的地方请求模型

就像把手机地图的“导航服务商”从 A 换成 B，但你还是用同一个地图 App。

### 5.1 你需要准备的三样东西

1）Base URL（服务地址）
2）API Key（访问钥匙）
3）Model（模型名）

以阿里云百炼 Coding Plan 为例，它提供了专属 Base URL 和专属 API Key（通常 API Key 以特定前缀开头，页面也有提示）。

### 5.2 在 Claude Code 里设置环境变量（macOS/Linux）

Claude Code 支持在 `~/.claude/settings.json` 里写环境变量。你可以这样做：

1. 创建目录（如果没有）：

```bash
mkdir -p ~/.claude
```

2. 编辑 `~/.claude/settings.json`：

```bash
nano ~/.claude/settings.json
```

3. 写入类似这样的配置（把 `YOUR_API_KEY` 换成你自己的）：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
    "ANTHROPIC_BASE_URL": "https://coding.dashscope.aliyuncs.com/apps/anthropic",
    "ANTHROPIC_MODEL": "qwen3.5-plus"
  }
}
```

改完后，**重新打开一个终端** 再运行 `claude`，让环境变量生效。

### 5.3 避免首次启动时报连接错误（一个小坑）

有些情况下你会遇到类似“无法连接 Anthropic 服务”的报错。你可以创建或编辑 `~/.claude.json`，把 `hasCompletedOnboarding` 设置为 `true`：

```json
{
  "hasCompletedOnboarding": true
}
```

这更像是一个“我已经完成过新手引导”的标记，让它别在启动阶段卡住。

### 5.4 Windows 配置思路（简述）

Windows 的思路一样：找到用户目录下的 `.claude` 配置文件夹，创建 `settings.json`，写入同样的 `env` 配置。

另外，Windows 常见的坑是 Git Bash 路径。Claude Code 文档里给了一个环境变量 `CLAUDE_CODE_GIT_BASH_PATH`，当它找不到 Git Bash 时可以手动指定。

### 5.5 怎么验证你配对了（最简单的办法）

启动 Claude Code 后，你可以先做两件事：

- `claude --version`：确认 Claude Code 本体没问题
- 在 Claude Code 里运行 `/status`：看它显示的模型、Base URL 是否是你设置的

如果 `/status` 里显示的内容跟你配置一致，基本就说明“走通了”。

### 5.6 几张图片示例（你大概会看到什么界面）

第一次用这类工具，很多人会紧张：到底会不会乱改我文件？它怎么提示我授权？我怎么确认配置生效？

下面几张图来自公开文档页面（截图链接见文末资料来源），让你先对界面有个预期：

1）授权执行（Claude Code 需要你确认后才会跑命令/改文件）：

![Claude Code 授权提示示例](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0924991771/p1040228.png)

2）查看状态（确认模型、Base URL、Key 是否生效）：

![Claude Code /status 示例](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0428202771/p1054776.png)

3）开始对话的界面示意：

![Claude Code 对话界面示例](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8292228671/p1040230.png)

### 5.7 只提一嘴：IDE 插件

Claude Code 也有 VS Code / JetBrains 之类的插件形态，但我更推荐新手先把 **CLI 用顺**。原因很简单：CLI 更直接，排障更清楚，脚本化也更容易。

当你已经习惯了“先 Plan 再执行”的节奏，再去用插件，会更舒服。

## 资料来源

1. Claude Code overview（官方概览）：https://code.claude.com/docs/en/overview
2. Claude Code Advanced setup / 安装与系统要求（官方）：https://code.claude.com/docs/en/setup
3. Claude Code CLI reference（官方命令与参数）：https://code.claude.com/docs/en/cli-reference
4. Node.js 下载页（安装 Node.js / npm）：https://nodejs.org/en/download/
5. Node.js Package manager（各 Linux 发行版安装方式）：https://nodejs.org/en/download/package-manager
6. 阿里云百炼 Coding Plan 概述（支持模型、用量、使用限制等）：https://help.aliyun.com/zh/model-studio/coding-plan
7. 阿里云百炼 Qwen Code（文中提到的“在编程工具中接入 Coding Plan”的示例与配置思路）：https://help.aliyun.com/zh/model-studio/qwen-code-coding-plan
