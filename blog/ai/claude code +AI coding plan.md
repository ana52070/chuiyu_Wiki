---
author: chuiyu
date: 2026-03-16
description: claude code +AI coding plan
tags:
  - ai
---
# 导读

1.什么是claude code

2.claude code的基本用法

3.ai coding plan 介绍

4.常见coding plan推荐

5.claude code + coding plan 配置教程





# 1.什么是claude code



# 2.claude code的基本用法



# 3.ai coding plan 介绍



# 4.常见coding plan推荐



# 5.claude code + coding plan 配置教程

Coding Plan中的模型支持 Anthropic API 兼容接口，可以通过 Claude Code 调用。

## **安装与使用**

## 手动安装

## macOS/Linux

1.  安装或更新 [Node.js](https://nodejs.org/en/download/)（v18.0 或更高版本）。
    
2.  在终端中执行下列命令，安装 Claude Code。
    
    ```
    npm install -g @anthropic-ai/claude-code
    ```
    
3.  运行以下命令验证安装。若有版本号输出，则表示安装成功。
    
    ```
    claude --version
    ```
    

## Windows

在 Windows 上使用 Claude Code，需要安装 WSL 或 [Git for Windows](https://git-scm.com/install/windows)，然后在 WSL 或 Git Bash 中执行以下命令。

```
npm install -g @anthropic-ai/claude-code
```

> 详情可以参考Claude Code官方文档的[Windows安装教程](https://docs.anthropic.com/en/docs/claude-code/setup#windows-setup)。

## **Qwen Code 引导安装**

Claude Code 安装依赖于 Node.js 环境，手动安装可能会遇到环境配置问题。您可以使用 Qwen Code 来完成安装和验证。

1.  安装并配置 [Qwen Code](https://help.aliyun.com/zh/model-studio/qwen-code-coding-plan)。
    
2.  在终端输入以下命令启动 Qwen Code。
    
    ```
    qwen
    ```
    
3.  在 Qwen Code 对话框中输入以下指令。
    
    ## macOS/Linux
    
    ```
    请帮我安装 Claude Code。1. 前置条件：需要先安装 Node.js（v18.0 或更高版本）。2. 若已安装 Node.js，执行命令：npm install -g @anthropic-ai/claude-code，安装完成后执行 claude --version 验证安装是否成功。
    ```
    
    ## Windows
    
    ```
    请帮我安装 Claude Code。1. 前置条件：需要先安装 Node.js（v18.0 或更高版本）和 Git for Windows，如果没有安装请帮我安装。2. 若已满足前置条件，执行命令：npm install -g @anthropic-ai/claude-code，安装完成后执行 claude --version 验证安装是否成功。
    ```
    
4.  授权允许Qwen Code 执行命令，直至完成安装。
    
5.  输入/exit退出Qwen Code。
    
    ```
    /exit
    ```
    

### **在Claude Code配置Coding Plan**

在 Claude Code 中接入百炼 Coding Plan，需要配置以下信息：

1.  `ANTHROPIC_BASE_URL`：设置为 `https://coding.dashscope.aliyuncs.com/apps/anthropic`。
    
2.  `ANTHROPIC_AUTH_TOKEN`：设置为Coding Plan专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)。
    
3.  `ANTHROPIC_MODEL`：设置为 Coding Plan [支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan)。
    

## macOS/Linux

1.  创建并打开配置文件`~/.claude/settings.json`。
    
    > `~` 代表用户主目录。如果 `.claude` 目录不存在，需要先行创建。可在终端执行 `mkdir -p ~/.claude` 来创建。
    
    ```
    nano ~/.claude/settings.json
    ```
    
2.  编辑配置文件。将 YOUR\_API\_KEY 替换为 Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)。
    
    ```
    {    
        "env": {
            "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
            "ANTHROPIC_BASE_URL": "https://coding.dashscope.aliyuncs.com/apps/anthropic",
            "ANTHROPIC_MODEL": "qwen3.5-plus"
        }
    }
    ```
    
    保存配置文件，重新打开一个终端即可生效。
    
3.  编辑或新增 `~/.claude.json` 文件，将`hasCompletedOnboarding` 字段的值设置为 `true`并保存文件。
    
    ```
    {
      "hasCompletedOnboarding": true
    }
    ```
    
    > `hasCompletedOnboarding` 作为顶层字段，请勿嵌套于其他字段。
    
    该步骤可避免启动Claude Code时报错：`Unable to connect to Anthropic services`。
    

## Windows

1.  创建并打开配置文件`C:\Users\您的用户名\.claude\settings.json`。
    
    ## CMD
    
    1.  创建目录
        
        ```
        if not exist "%USERPROFILE%\.claude" mkdir "%USERPROFILE%\.claude"
        ```
        
    2.  创建并打开文件
        
        ```
        notepad "%USERPROFILE%\.claude\settings.json"
        ```
        
    
    ## PowerShell
    
    1.  创建目录
        
        ```
        mkdir -Force $HOME\.claude
        ```
        
    2.  创建并打开文件
        
        ```
        notepad $HOME\.claude\settings.json
        ```
        
    
2.  编辑配置文件。将 YOUR\_API\_KEY 替换为 Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)。
    
    ```
    {    
        "env": {
            "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
            "ANTHROPIC_BASE_URL": "https://coding.dashscope.aliyuncs.com/apps/anthropic",
            "ANTHROPIC_MODEL": "qwen3.5-plus"
        }
    }
    ```
    
    保存配置文件，重新打开一个终端即可生效。
    
3.  编辑或新增 `C:\Users\您的用户名\.claude.json` 文件，将`hasCompletedOnboarding` 字段的值设置为 `true`，并保存文件。
    
    ```
    {
      "hasCompletedOnboarding": true
    }
    ```
    

### **使用Claude Code**

1.  打开终端，并进入项目所在的目录。运行以下命令启动程序 Claude Code：
    
    ```
    cd path/to/your_project
    claude
    ```
    
2.  启动后，需要授权 Claude Code 执行文件。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0924991771/p1040228.png)
    
3.  输入`/status`确认模型、Base URL、API Key 是否配置正确。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0428202771/p1054776.png)
    
4.  在 Claude Code 中对话。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8292228671/p1040230.png)
    

### **切换模型**

1.  **启动 Claude Code 时切换**：在终端执行`claude --model <模型名称>`指定模型并启动 Claude Code，例如`claude --model qwen3-coder-next`。
    
2.  **会话期间**：在对话框输入`/model <模型名称>`命令切换模型，例如`/model qwen3-coder-next`。
    

### **常见命令**

| **命令** | **说明** | **示例** |
| --- | --- | --- |
| /init | 在项目根目录生成 CLAUDE.md 文件，用于定义项目级指令和上下文。 | /init |
| /status | 查看当前模型、API Key、Base URL 等配置状态。 | /status |
| /model <模型名称> | 切换模型。 | /model qwen3-coder-next |
| /clear | 清除对话历史，开始全新对话。 | /clear |
| /plan | 进入规划模式，仅分析和讨论方案，不修改代码。 | /plan |
| /compact | 压缩对话历史，释放上下文窗口空间。 | /compact |
| /config | 打开配置菜单，可设置语言、主题等。 | /config |

更多命令与用法详情，请参考 [Claude Code 官方文档](https://code.claude.com/docs/en/overview)。

## 能力扩展

Claude Code 支持通过 MCP 和 Skills 扩展自身能力，例如调用联网搜索获取实时信息、使用图片理解 Skill 分析图像内容等。详情请参考[最佳实践](https://help.aliyun.com/zh/model-studio/coding-plan-best-practices/)。

## **使用Claude Code IDE插件**

Claude Code IDE 插件支持在 VSCode、VSCode 系列 IDE（如 Cursor、Trae 等）、JetBrains 系列 IDE（如 IntelliJ IDEA、PyCharm 等）中使用。

## VS Code

1.  请先[在Claude Code配置Coding Plan](#15a5a014e5uy8)，Windows还需要安装 WSL 或 [Git for Windows](https://git-scm.com/install/windows)。
    
2.  打开VS Code，在扩展市场中搜索 `Claude Code for VS Code` 并安装。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9898540771/p1053283.png)
    
3.  安装完成后，重启 VSCode。单击右上角图标进入 Claude Code 开始对话。
    
    ![截屏2026-02-06 17](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9898540771/p1053286.png)
    
    若在对话时弹出 Anthropic 登录界面，说明尚未[在Claude Code配置Coding Plan](#15a5a014e5uy8)，请先完成配置。
    
    ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    
4.  切换模型：在对话框中输入`/`，选择 General config 进入设置页面，在Selected Model中选择[支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan-overview)，新建一个新窗口开始对话。
    
    ![截屏2026-02-06 17](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    

## JetBrains

1.  请先[安装 Claude Code](#9fc9401286mkk)，并[在Claude Code配置Coding Plan](#15a5a014e5uy8)。
    
2.  打开JetBrains（如 IntelliJ IDEA、PyCharm 等），在扩展市场中搜索 `Claude Code` 并安装。
    
    ![2026-02-25_16-27-56](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    
3.  安装后重启IDE，点击右上角图标即可使用，可通过`/model <模型名称>`命令切换模型。
    
    ![2026-02-25_16-40-33](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    
    若在对话时出现 `Not logged in. Please run /login`报错，说明尚未[在Claude Code配置Coding Plan](#15a5a014e5uy8)，请先完成配置。
    
    ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    

## 错误码

请参考[常见报错及解决方案](https://help.aliyun.com/zh/model-studio/coding-plan-faq#a9248c44029g6)。

## 常见问题

请参考[常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq)。

## **最佳实践**

##### **1\. 上下文管理**

-   **及时清理：** 使用 `/clear` 定期重置对话，防止旧的上下文干扰新任务并节省 Token。
    
-   **主动压缩**：使用 `/compact` 命令让 Claude 总结关键决策和修改的文件，保留核心记忆。
    
-   **明确指定文件：** 提问时使用 `@` 引用文件（如 `write a test for @auth.py`），避免模型无效扫描整个项目。
    
-   **善用子代理（Sub-agents）：** 对于大规模任务，让 Claude 启动子代理执行。子代理完成任务后返回精炼结论，保护主对话的上下文空间。
    

##### **2\. 先计划，再执行**

-   **启用 Plan 模式**：复杂任务前，先分析方案，不实际修改文件。
    
    -   快捷操作：连续按两次 `Shift + Tab` 进入 Plan Mode。
        
    -   提示词约束：提示词明确要求“先输出详细实施计划，经我确认后再修改文件”。
        
-   **降低试错成本**：确保逻辑闭环后再进行代码变更。
    

##### **3\. 沉淀项目核心知识**：编写 CLAUDE.md

-   **包含关键信息**：每次会话启动时自动加载CLAUDE.md，建议填入构建命令、代码规范及工作流等通用规则。
    
-   **动态维护**：内容应简短易读，仅记录广泛适用的全局约定，并随项目演进持续补充新规则。
    

##### **4\. 扩展能力： MCP 与 Skills**

-   [**MCP**](https://code.claude.com/docs/en/mcp)：安装成熟的 MCP Server，连接外部服务。例如：[添加联网搜索MCP](https://help.aliyun.com/zh/model-studio/web-search-for-coding-plan)。
    
-   [**Skills**](https://code.claude.com/docs/en/skills)：编写详细的 Skill 描述文案。Claude 决定是否调用该工具，取决于对该工具用途的定义。例如：[添加视觉理解能力Skill](https://help.aliyun.com/zh/model-studio/add-vision-skill)。
    
-   **Skills vs MCP**：Skills 教会 Claude “怎么做”（工作流知识），MCP 给 Claude“做的工具”（外部接口）。两者互补，Skills 也可集成外部接口。
    

##### **5\.** 自动化守护：Hooks

-   [**使用Hooks**](https://code.claude.com/docs/en/hooks)：Hooks 是确定性规则。它在 Claude 工作流的特定生命周期节点（如 PreToolUse 工具执行前校验等）自动运行本地脚本，确保关键校验或操作 100% 执行。
    
-   **配置方式**：
    
    1.  运行 `/hooks` 进行交互式配置。
        
    2.  直接编辑 `.claude/settings.json`。
        
    3.  让 Claude 帮你编写，如：“编写一个在每次文件编辑后运行 eslint 的 hook”。
        

##### **6\. 建立自检闭环**

-   **强制验证：** 要求 Claude 修改代码后，必须运行相关的测试用例（如 `pytest` 或 `npm test`）。
    
-   **定义成功标准：** “修改完成后，请确保编译通过，并且运行 `curl` 命令验证 API 返回值为 200”。
    
-   **视觉反馈：** 前端修改时，要求 Claude 截取浏览器截图来确认 UI 效果。