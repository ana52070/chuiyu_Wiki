---
title: Claude Code 从入门到生产：一文讲透安装、使用、MCP、SubAgent、Plugin 的实战指南
author: lunar
date: 2026-03-22 17:38:19
description: 很多人以为 Claude Code 只是一个会写代码的 AI，其实真正厉害的不是“生成代码”，而是它已经开始接管开发流程：改文件、跑命令、读设计稿、管上下文、做回滚、接 MCP、挂 SubAgent、装 Plugin。会让它写 Demo 的人很多，但能把它用进生产的人很少。这篇文章，就带你把 Claude Code 从“玩具”真正用成“生产力工具”。
tags:
  - ai
  - MCP
permalink: /pages/ea15bf
categories:
  - blog
  - ai
---

> 原文转载说明：本文基于公开可访问页面进行完整转载，并做了轻微排版整理，图片已本地化到仓库。
>
> 原文标题：Claude Code 从入门到生产：一文讲透安装、使用、MCP、SubAgent、Plugin 的实战指南
>
> 原文来源：CSDN / DreamMeng
>
> 原文链接：<https://blog.csdn.net/DreamMeng/article/details/159353229>

---

<div><p>2026年的春天，Claude Code 非常火🔥。</p>
<p></p>
<p><img alt="r/ClaudeAI - * Welcome to the Claude Code research preview! CLAUDE CODE Login successful. Press Enter to continue" src="/blog/ai/assets/csdn-159353229-01.jpeg"></p>
<p>很多人已经装上了，也体验过：让它写个页面、改几段代码、生成一个小工具，看起来都很惊艳。但真正的问题是：<strong>会让它写几段代码，不等于你真的掌握了 Claude Code。因为一旦你把它真正用进日常开发，就会立刻遇到一连串更实际的问题：</strong></p>
<p></p>
<p><img alt="" src="/blog/ai/assets/csdn-159353229-02.jpeg"></p>
<p>这些，才是 Claude Code 从“玩具”走向“生产工具”的关键。所以这篇文章不讲虚的，我直接按照一条完整的实战路径，把 Claude Code 从安装开始，一路讲到：</p>
<ul>
 <li>
  <p>基础交互</p></li>
 <li>
  <p>复杂任务处理</p></li>
 <li>
  <p>终端控制</p></li>
 <li>
  <p>回滚与上下文管理</p></li>
 <li>
  <p>图片与 Figma 设计稿还原</p></li>
 <li>
  <p>CLAUDE.md 项目记忆</p></li>
 <li>
  <p>Hook</p></li>
 <li>
  <p>Agent Skill</p></li>
 <li>
  <p>SubAgent</p></li>
 <li>
  <p>Plugin</p></li>
</ul>
<p>目标只有一个：</p>
<p><strong>让你只看这一篇文章，就能把 Claude Code 从入门一直用到接近生产环境。</strong></p>
<hr>
<h2>一、先装起来：Claude Code 的起点不是聊天，而是终端</h2>
<p>Claude Code 不是网页里的聊天机器人，它的核心使用方式是在终端里运行。<br>
  所以第一步不是“打开一个网页开始提问”，而是先把它安装到你的本机环境中。</p>
<p>通常安装流程是这样的：</p>
<ol>
 <li>
  <p>打开 Claude Code 官方安装页面。</p>
  <blockquote>
   <p>https://claude.com/product/claude-code</p>
  </blockquote>
  <p></p>
  <p><img alt="图片" src="/blog/ai/assets/csdn-159353229-03.png"></p>
  <p></p></li>
 <li>
  <p>复制页面给出的安装命令。</p>
  <ul>
   <li>
  </li></ul>
  <pre><code>curl -fsSL https://claude.ai/install.sh | bash</code></pre>
  <p>如果你不喜欢 <code>curl | bash</code> 这种方式，还有一个更“安全/规范”的替代方案。可以用：</p>
  <ul>
   <li>
  </li></ul>
  <pre><code>brew install --cask claude-code</code></pre>
  <p></p></li>
 <li>
  <p>回到终端，粘贴并执行。</p>
  <p></p>
  <p><img alt="图片" src="/blog/ai/assets/csdn-159353229-04.png"></p>
  <p></p></li>
 <li>
  <p>等待安装完成。</p>
  <p></p>
  <p><img alt="图片" src="/blog/ai/assets/csdn-159353229-05.png"></p>
  <p></p></li>
 <li>
  <p>之后你就可以在终端里直接输入 <code>claude</code> 启动它。</p>
  <p></p>
  <p><img alt="图片" src="/blog/ai/assets/csdn-159353229-06.png"></p>
  <p></p></li>
</ol>
<p>安装完成之后，Claude Code 的使用入口就是命令行。这一点非常重要，因为它决定了 Claude Code 后续的能力边界远远不只是“回答问题”，而是：</p>
<ul>
 <li>
  <p>进入你的项目目录</p></li>
 <li>
  <p>读写文件</p></li>
 <li>
  <p>执行命令</p></li>
 <li>
  <p>管理任务</p></li>
 <li>
  <p>接外部工具</p></li>
 <li>
  <p>维护会话与记忆</p></li>
</ul>
<p>也就是说，它更像一个运行在终端中的开发 Agent。</p>
<hr>
<h2>二、登录与授权：先让 Claude Code 拿到工作资格</h2>
<p>第一次启动 Claude Code 时，通常会要求你登录。如果没有自动提示，可以手动输入：/login 这样会主动触发登录流程。一般来说，Claude Code 的接入方式可以理解为两类：</p>
<h4>1）订阅账号登录：如果你本身已经有 Claude 的 Pro 或 Max 账号，通常可以直接走订阅授权方式。</h4>
<h4>2）API Key 登录：如果你走 API 模式，那就是按调用量计费。</h4>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-07.png"></p>
<p>完成授权后，Claude Code 就正式可用了。这里你要建立一个正确认知：</p>
<p><strong>Claude Code 的重点，不只是“模型本身”，而是“模型 + 终端 + 工具 + 工作流”。</strong></p>
<p>所以不要把它理解成另一个普通聊天框。它真正的价值，在于它能进入你的开发现场，替你执行一部分工作。</p>
<hr>
<h2>三、从一个最小实战开始：先让它做一个待办软件</h2>
<p>学一门工具，最好的方式不是先背命令，而是先做一个简单但完整的小任务。比如，你可以先新建一个目录：</p>
<pre>
</pre>
<ul>
 <li>
 </li><li>
</li></ul>
<pre><code>mkdir my-todo</code><code>cd my-todo</code></pre>
<p></p>
<p>然后启动 Claude Code：</p>
<pre>
</pre>
<ul>
 <li>
</li></ul>
<pre><code>claude</code></pre>
<p></p>
<p>进入之后，直接给它一个清晰需求：</p>
<blockquote>
 <p>给我做一个待办软件，使用 HTML 实现</p>
</blockquote>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-08.png"></p>
<p>这时 Claude Code 会开始分析你的需求，并尝试创建文件，比如 <code>index.html</code>。</p>
<p>但这里它不会一上来就直接改，而是会先问你：</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-09.png"></p>
<ul>
 <li>
  <p>是否允许本次创建文件？</p></li>
 <li>
  <p>是否允许本次会话期间后续所有编辑自动通过？</p></li>
 <li>
  <p>或者拒绝这次修改？</p></li>
</ul>
<p>这一刻，你就正式接触到了 Claude Code 的核心机制之一：</p>
<p><strong>模式与权限控制。</strong></p>
<hr>
<h2>四、三种模式一定要分清：默认模式、自动模式、规划模式</h2>
<p>Claude Code 最容易让新手混乱的地方，就是模式切换。但其实它的逻辑并不复杂，只要你把这三种模式理解透了，后面很多行为你就看得懂了。通过 <strong>Shift + Tab</strong>，你可以在不同模式之间切换。</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-10.png"></p>
<h3>1）默认模式：最适合第一次进项目</h3>
<p>默认模式下，Claude Code 每次创建文件、修改文件，都会先征求你的同意。</p>
<p>这种模式的特点是：</p>
<ul>
 <li>
  <p>安全</p></li>
 <li>
  <p>可控</p></li>
 <li>
  <p>不容易误改</p></li>
 <li>
  <p>适合陌生项目</p></li>
</ul>
<p>适合什么时候用？</p>
<ul>
 <li>
  <p>第一次进入一个项目</p></li>
 <li>
  <p>不确定 Claude Code 会改哪里</p></li>
 <li>
  <p>改的是比较重要的代码</p></li>
 <li>
  <p>你想先观察它的行为</p></li>
</ul>
<p>缺点也很明显：如果任务比较长，它会频繁打断你，让你一次次确认。</p>
<hr>
<h3>2）自动模式：文件层面最省心</h3>
<p>如果你开启自动模式，那么 Claude Code 后续在当前会话中对文件的创建和编辑，就不再反复询问你了。这时候它可以连续完成很多事情，比如：</p>
<ul>
 <li>
  <p>拆分文件</p></li>
 <li>
  <p>写多个模块</p></li>
 <li>
  <p>重构目录</p></li>
 <li>
  <p>连续改代码</p></li>
</ul>
<p>适合什么时候用？</p>
<ul>
 <li>
  <p>你已经明确任务目标</p></li>
 <li>
  <p>目录可控</p></li>
 <li>
  <p>本地实验项目</p></li>
 <li>
  <p>想快速推进开发</p></li>
</ul>
<p>但要注意：自动模式只代表“文件编辑自动通过”，不代表它执行所有终端命令也自动通过。这一点很多人会误解，后面讲终端权限时你就会明白。</p>
<hr>
<h3>3）规划模式（Plan Mode）：复杂任务先讨论，不直接开改</h3>
<p>规划模式是 Claude Code 非常强的一个能力。开启后，它不会直接修改文件，而是先帮你：</p>
<ul>
 <li>
  <p>理解目标</p></li>
 <li>
  <p>拆分步骤</p></li>
 <li>
  <p>设计目录结构</p></li>
 <li>
  <p>说明实施方案</p></li>
 <li>
  <p>给出执行计划</p></li>
</ul>
<p>这个模式非常适合：</p>
<ul>
 <li>
  <p>架构重构</p></li>
 <li>
  <p>技术栈迁移</p></li>
 <li>
  <p>复杂页面改造</p></li>
 <li>
  <p>大模块新增</p></li>
 <li>
  <p>需求还没完全想清楚的时候</p></li>
</ul>
<p>比如你已经有了一个单文件 <code>index.html</code> 的待办应用，但你觉得这种结构不适合继续扩展，想改造成：</p>
<ul>
 <li>
  <p>React + TypeScript + Vite</p></li>
</ul>
<p>这时，不要直接说“给我重构”。更推荐的方式是先切到规划模式，然后输入：</p>
<blockquote>
 <p>请将当前待办应用重构为 React + TypeScript + Vite 项目，保留现有功能，并保持 UI 风格一致。</p>
</blockquote>
<p>如果还想补充要求，可以继续增加，比如：</p>
<ul>
 <li>
  <p>给每个待办事项增加优先级</p></li>
 <li>
  <p>分为高、中、低</p></li>
 <li>
  <p>用不同颜色区分</p></li>
</ul>
<p>在规划模式下，Claude Code 会先产出一份方案。<br>
  这份方案里通常会包括：</p>
<ul>
 <li>
  <p>改造目标</p></li>
 <li>
  <p>推荐目录结构</p></li>
 <li>
  <p>需要新增哪些文件</p></li>
 <li>
  <p>原功能如何迁移</p></li>
 <li>
  <p>状态管理怎么做</p></li>
 <li>
  <p>可能需要的测试点</p></li>
</ul>
<p>然后它会问你：</p>
<ul>
 <li>
  <p>直接执行计划</p></li>
 <li>
  <p>执行但保留谨慎权限</p></li>
 <li>
  <p>继续修改计划</p></li>
</ul>
<p>这就是 Claude Code 非常像“工程搭档”的地方。不是一上来就写，而是先和你把方案对齐。</p>
<hr>
<h2>五、在 Claude Code 里直接执行终端命令：这是它和普通聊天工具最大的区别之一</h2>
<p>很多 AI 编程工具会生成代码，但是否能真正进入你的开发过程，关键要看它能不能操作终端。在 Claude Code 里，你可以输入 ! 号进入 Bash 模式并执行命令。比如你已经让它生成了 <code>index.html</code>，现在想直接打开这个文件看效果，就不一定非要去文件管理器手工双击。</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-11.png"></p>
<pre>
</pre>
<ul>
 <li>
</li></ul>
<pre><code>open index.html</code></pre>
<p>如果你想查看当前目录下的文件，也可以执行：</p>
<pre>
</pre>
<ul>
 <li>
</li></ul>
<pre><code>ls</code></pre>
<p>如果要安装依赖，可以运行：</p>
<pre>
</pre>
<ul>
 <li>
</li></ul>
<pre><code>npm install</code></pre>
<p>如果要启动开发服务，可以运行：</p>
<pre>
</pre>
<ul>
 <li>
</li></ul>
<pre><code>npm  run dev</code></pre>
<p>这意味着 Claude Code 不是只会“说怎么做”，而是已经开始具备“帮你做”的能力了。</p>
<p>过去我们的工作流是：</p>
<ul>
 <li>
  <p>问 AI</p></li>
 <li>
  <p>复制代码</p></li>
 <li>
  <p>自己粘贴</p></li>
 <li>
  <p>自己保存</p></li>
 <li>
  <p>自己开终端</p></li>
 <li>
  <p>自己运行</p></li>
 <li>
  <p>出错再回来问</p></li>
</ul>
<p>现在它可以逐步把这些动作串起来。</p>
<p>所以你要明白：<br><strong>Claude Code 的真正威力，不是生成一段代码，而是能帮你推进整个开发链路。</strong></p>
<hr>
<h2>六、为什么自动模式下它还会向你确认命令？因为文件编辑和终端命令不是一个风险等级</h2>
<p>这里是 Claude Code 很多人第一次使用时会困惑的地方。你明明已经打开了自动模式，为什么它在执行某些命令时还是会停下来问你？原因很简单：</p>
<p><strong>Claude Code 认为执行终端命令，比修改文件更危险。</strong></p>
<p>比如：</p>
<ul>
 <li>
  <p>创建目录</p></li>
 <li>
  <p>安装依赖</p></li>
 <li>
  <p>删除内容</p></li>
 <li>
  <p>启动脚本</p></li>
 <li>
  <p>修改某些环境结构</p></li>
</ul>
<p>这些动作可能会对整个项目甚至本机环境产生影响。所以即使你在自动模式下，它对于命令层面的行为仍然会比较谨慎。这是合理的，因为：</p>
<ul>
 <li>
  <p>改一个文件，影响通常局部可控；</p></li>
 <li>
  <p>执行一个命令，影响可能是全局的。</p></li>
</ul>
<p>所以文件权限自动放开，不代表命令权限也自动放开。</p>
<hr>
<h2>七、最高权限模式：<code>dangerously-skip-permissions</code> 到底能不能用？</h2>
<p>如果你觉得每次执行命令都要确认太麻烦，那么 Claude Code 提供了一个更彻底的方式：</p>
<p>启动时直接加上这个参数：</p>
<pre>
</pre>
<ul>
 <li>
</li></ul>
<pre><code>claude --dangerously-skip-permissions</code></pre>
<p></p>
<p>一旦这样启动，Claude Code 基本就进入了“权限绕过”状态。它执行各种终端命令时，不会再频繁要求你确认。听上去是不是很爽？</p>
<p>是的，它确实能大幅提高效率。特别是在这种场景下非常好用：</p>
<ul>
 <li>
  <p>本地实验项目</p></li>
 <li>
  <p>个人 Demo</p></li>
 <li>
  <p>你新建的空目录</p></li>
 <li>
  <p>完全可控的沙盒环境</p></li>
</ul>
<p>但这个选项名字里为什么直接写着 <code>dangerously</code>？因为它确实危险。开启后，你相当于把终端里的很多主动权直接交给了 Claude Code。理论上，它就具备了执行下列操作的可能：</p>
<ul>
 <li>
  <p>删除文件</p></li>
 <li>
  <p>改动目录</p></li>
 <li>
  <p>安装或卸载依赖</p></li>
 <li>
  <p>执行各种 Shell 命令</p></li>
</ul>
<p>所以我的建议很明确：</p>
<table>
 <tbody>
  <tr>
   <th>
    <p>可以考虑开启的场景:</p></th>
   <th>
    <p>不建议开启的场景</p></th>
  </tr>
  <tr>
   <td>
    <ul>
     <li>
      <p>你自己本地的测试项目</p></li>
     <li>
      <p>没有重要数据的新目录</p></li>
     <li>
      <p>想追求极致效率的个人环境</p></li>
    </ul>
    <p></p>
    <p></p></td>
   <td>
    <ul>
     <li>
      <p>公司代码仓库</p></li>
     <li>
      <p>生产项目</p></li>
     <li>
      <p>含敏感配置的目录</p></li>
     <li>
      <p>共享机器</p></li>
     <li>
      <p>你根本不了解结构的旧项目</p></li>
    </ul></td>
  </tr>
 </tbody>
</table>
<p>一句话总结：这是一个效率开关，也是一个风险开关。<br>
  能不能开，不看你胆子大不大，而看你的环境是不是足够可控。</p>
<hr>
<h2>八、让它帮你重构架构：从 HTML 单文件升级到 React + TypeScript + Vite</h2>
<p>我们继续顺着待办应用这个例子往下走。</p>
<p>如果 Claude Code 初始生成的是一个单文件 HTML 应用，那么它很适合快速验证想法，但不适合长期维护。<br>
  因为代码全写在一个文件里，项目稍微复杂一点，就会变得很难改。</p>
<p>这时你就可以进入规划模式，提出结构升级需求。</p>
<p>比如：</p>
<blockquote>
 <p>请把当前待办应用重构成 React + TypeScript + Vite 项目，保留所有现有功能，界面风格保持一致。</p>
</blockquote>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-12.png"></p>
<p>如果你还想加新功能，也可以在同一轮需求里补进去，比如：</p>
<blockquote>
 <p>每个待办项要有优先级，高、中、低三档，并且用不同颜色区分。</p>
</blockquote>
<p>Claude Code 会先给你一份计划。</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-13.png"></p>
<p>如果你觉得还不够完整，可以继续补要求，让它重新整理计划。只有当你对方案满意了，再让它真正执行。这一点要养成习惯：</p>
<p><strong>小活儿直接做，大活儿先出计划。</strong></p>
<p>很多人觉得 AI 最大的问题是“写出来的东西不稳定”，但其实很多不稳定，不是模型不行，而是你没让它先把方案想清楚。</p>
<hr>
<h2>九、自己启动开发服务器：但要小心，服务一跑起来，Claude Code 可能会被阻塞</h2>
<p>当 Claude Code 完成了前端项目的创建后，通常你会想跑起来看看效果。</p>
<p>这时你可以执行：</p>
<pre>
</pre>
<ul>
 <li>
</li></ul>
<pre><code>npm run dev</code></pre>
<p></p>
<p>如果项目正常，终端通常会输出本地访问地址。你点开链接，就能看到页面效果。但这里有一个必须理解的点：</p>
<p><strong>当前终端一旦被开发服务占住，Claude Code 就没法继续正常处理你的新输入。</strong></p>
<p>因为 <code>npm run dev</code> 这类命令通常是持续运行的。它会一直监听文件变化、持续占用前台终端。所以如果你在同一个会话里还想继续让 Claude Code 改代码、回答问题、追加功能，就必须把这个服务放到后台。</p>
<hr>
<h2>十、后台任务管理：让服务继续跑，同时你还能继续和 Claude Code 协作</h2>
<p>如果前端服务正在运行，而你又想继续和 Claude Code 对话，这时最好的做法是把当前任务放到后台。</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-14.png"></p>
<p>放到后台之后，会发生两件事：</p>
<h4>第一，开发服务不会停</h4>
<p>你的页面依然可以访问，热更新通常也还能工作。</p>
<h4>第二，Claude Code 恢复响应</h4>
<p>你可以继续给它提需求、让它修改代码。</p>
<p>随后你还可以查看当前后台任务列表。在任务列表里，通常能看到类似 <code>npm run dev</code> 这样的服务正在后台运行。如果后面你想结束这个服务，也可以在任务管理界面中停止它。这套机制在实际开发里非常重要，因为真实工作不是“写完代码就结束”，而是：</p>
<ul>
 <li>
  <p>启服务</p></li>
 <li>
  <p>看页面</p></li>
 <li>
  <p>发现问题</p></li>
 <li>
  <p>改代码</p></li>
 <li>
  <p>再看效果</p></li>
 <li>
  <p>再继续改</p></li>
</ul>
<p>Claude Code 能管理后台任务，就意味着它开始真正接近开发现场，而不是只做静态回答。</p>
<hr>
<h2>十一、追加功能后发现做错了怎么办？用 Rewind 回滚</h2>
<p>假设你现在已经把待办应用跑起来了，接着你又让 Claude Code 帮你加了一个“中英文切换”的功能。它确实加上去了，右上角还多了语言切换。但你用着用着突然发现：</p>
<p>“等等，我的用户本来就都看得懂中文，我做这个功能干什么？”</p>
<p>这时候最理性的做法不是继续补丁式修改，而是直接回滚。Claude Code 提供了回滚能力。它会记录你在不同请求节点上的变更点，你可以回到其中某一个版本。</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-15.png"></p>
<p>回滚时通常会有几种选择：</p>
<ul>
 <li>
  <p>同时回滚代码和会话</p></li>
 <li>
  <p>只回滚代码</p></li>
 <li>
  <p>只回滚会话</p></li>
 <li>
  <p>放弃回滚</p></li>
</ul>
<p>如果你的目标是“撤销这个功能，回到功能添加前的状态”，那最稳妥的做法通常是把代码和会话一起回退。这样一来，不只是文件内容回去，连当前对话的上下文也会同步回到那个节点，更不容易让 Claude Code 后续继续沿着错误方向往下走。</p>
<hr>
<h2>十二、但一定要记住：Claude Code 的回滚不是 Git</h2>
<p>这里必须单独提醒一下。</p>
<p>Claude Code 的回滚很好用，但你不能把它当成完整的版本控制系统。</p>
<p>因为它更擅长撤销“它自己写入的内容”，但对那些通过终端命令产生的副作用，它未必能完整恢复。例如：</p>
<ul>
 <li>
  <p>你执行了 <code>mkdir</code></p></li>
 <li>
  <p>你执行了 <code>npm install</code></p></li>
 <li>
  <p>你生成了某些构建文件</p></li>
 <li>
  <p>你安装了依赖包</p></li>
</ul>
<p>这些内容，有时候不会随着 Claude Code 的回滚一起彻底消失。所以回滚之后，如果你发现目录里还有很多残留文件，不要惊讶。这不是一定出 Bug，而是 Claude Code 的回滚边界本来就和 Git 不一样。</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-16.png"></p>
<p>所以我的建议是：</p>
<h4>Claude Code 的 Rewind 适合做什么？</h4>
<ul>
 <li>
  <p>快速撤销最近几轮错误尝试</p></li>
 <li>
  <p>回到某个会话节点重新开始</p></li>
 <li>
  <p>撤回一次不满意的功能改动</p></li>
</ul>
<h4>不适合做什么？</h4>
<ul>
 <li>
  <p>替代 Git 分支管理</p></li>
 <li>
  <p>替代正式版本控制</p></li>
 <li>
  <p>处理复杂工程的精确回滚</p>
  <p></p></li>
</ul>
<p>真正重要的项目，Git 还是必需的。</p>
<hr>
<h2>十三、如果你不满意它做的页面，直接给它看图</h2>
<p>很多时候，纯文字描述 UI 是不够的。你说“高级一点”，它理解的是一种高级；你说“现代一点”，它可能还是给你一个很典型的 AI Demo 风格页面。这时候怎么办？最直接的方式，就是把设计稿图片给 Claude Code。</p>
<p>操作方式通常有两种：</p>
<h4>方法一：直接拖拽图片到 Claude Code</h4>
<p>你把 PNG 图片直接拖进去，它就能识别这是图像输入。</p>
<h4>方法二：复制图片后粘贴</h4>
<p>这里有一个细节要注意：<br>
  在 Claude Code 里粘贴图片时，用的是 <strong>Ctrl + V</strong>。即使你在 macOS 上，也不是 Command + V。</p>
<p>图片给进去之后，你就可以直接下指令：</p>
<blockquote>
 <p>请根据这张设计稿修改当前页面。</p>
</blockquote>
<p>这时候 Claude Code 会尝试根据图片中的布局、颜色、层次来调整页面。</p>
<p>这种方式已经很好用了，特别适合：</p>
<ul>
 <li>
  <p>快速做近似还原</p></li>
 <li>
  <p>调整视觉方向</p></li>
 <li>
  <p>让 AI 更接近你的审美预期</p></li>
</ul>
<p>但要坦白说，单靠图片还原通常还不够精确。因为图片只能提供视觉结果，无法天然提供：</p>
<ul>
 <li>
  <p>精确间距</p></li>
 <li>
  <p>字体样式规范</p></li>
 <li>
  <p>组件结构</p></li>
 <li>
  <p>设计系统信息</p></li>
</ul>
<p>想做到更准，就要上 MCP。</p>
<hr>
<h2>十四、MCP 到底是什么？</h2>
<h2>一句话理解：让 Claude Code 不只是“看见”，而是真正“读取外部世界”</h2>
<p>很多人第一次接触 MCP，会觉得这个词很抽象。</p>
<p>你可以先这样理解：</p>
<p><strong>MCP 是让大模型连接外部工具和外部上下文的一种标准方式。</strong></p>
<p>在 Claude Code 的场景里，它的意义就是：</p>
<ul>
 <li>
  <p>不再只靠你手工描述</p></li>
 <li>
  <p>不再只靠一张截图猜</p></li>
 <li>
  <p>而是让 Claude Code 直接去读取工具中的结构化信息</p>
  <p></p></li>
</ul>
<p>这就是为什么用 MCP 接 Figma，会比单纯给截图更强。因为它拿到的不只是“长什么样”，还包括：</p>
<ul>
 <li>
  <p>设计上下文</p></li>
 <li>
  <p>组件信息</p></li>
 <li>
  <p>字体与间距</p></li>
 <li>
  <p>样式规则</p></li>
 <li>
  <p>布局关系</p>
  <p></p></li>
</ul>
<p>这就从“凭感觉还原”升级成了“依据结构化设计信息还原”。</p>
<hr>
<h2>十五、如何安装 Figma 的 MCP Server，并让 Claude Code 读取设计稿</h2>
<p>如果你想让 Claude Code 更精准地还原 Figma 设计稿，一般做法是安装对应的 Figma MCP Server。操作思路通常是：</p>
<ol>
 <li>
  <p>按照 Figma MCP Server 的安装方式，在终端执行安装命令。</p>
  <pre><code>claude mcp add --transport http figma https://mcp.figma.com/mcp</code></pre></li>
 <li>安装完成后，重新启动 Claude Code。</li>
 <li>
  <p>使用 /resume 回到当前会话。也可以用 claude -c。</p></li>
 <li>
  <p>在 Claude Code 里查看当前 MCP 工具。</p>
  <p>/mcp</p></li>
 <li>
  <p>找到 Figma 相关工具并完成授权。</p>
  <p></p>
  <p><img alt="图片" src="/blog/ai/assets/csdn-159353229-17.png"></p>
  <p></p></li>
 <li>
  <p>然后把 Figma 设计稿链接交给 Claude Code。</p></li>
</ol>
<p>完成这些后，你就可以直接对 Claude Code 说：</p>
<blockquote>
 <p>请修改当前页面，使它与这个 Figma 设计稿保持一致。</p>
</blockquote>
<p>并把设计链接一起提供给它。</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-18.png"></p>
<p>接下来，Claude Code 会尝试调用对应的 MCP 工具，例如：</p>
<ul>
 <li>
  <p>获取 design context</p></li>
 <li>
  <p>获取设计截图</p></li>
 <li>
  <p>获取组件信息</p></li>
</ul>
<p>当这些信息拿到之后，它就能依据更完整的设计上下文去改代码。这种方式的还原效果，通常会明显优于单纯凭一张 PNG 图片硬猜。</p>
<p>当然，也别神化它。它依然可能会在个别细节上出现：</p>
<ul>
 <li>
  <p>某些值没算对</p></li>
 <li>
  <p>某些字段是 undefined</p></li>
 <li>
  <p>某些布局还得你手工微调</p></li>
</ul>
<p>但总体方向通常会更准，尤其对间距、风格、层次感的把握会更好。</p>
<hr>
<h2>十六、安装完 MCP 后会话没了怎么办？用 Resume 恢复</h2>
<p>有时你为了安装 MCP Server，需要先退出 Claude Code。装完之后再进来，很多人第一反应是：</p>
<p>“我之前那段对话是不是丢了？”</p>
<p>其实未必。Claude Code 支持恢复历史会话。常见思路有两种：</p>
<h4>方式一：手动恢复</h4>
<p>进入 Claude Code 后，执行恢复会话命令，然后从历史列表中选择你刚才那个会话。</p>
<h4>方式二：启动时直接继续上次会话</h4>
<p>在启动 Claude Code 时，加一个 continue 参数，让它直接恢复最近一次会话。</p>
<p>这样做的好处非常明显：</p>
<ul>
 <li>
  <p>不用重新讲项目背景</p></li>
 <li>
  <p>不用重新解释你刚才做到哪一步</p></li>
 <li>
  <p>不用重新把需求从头输入一遍</p></li>
</ul>
<p>这会让 Claude Code 更像一个持续协作对象，而不是一次性问答工具。</p>
<hr>
<h2>十七、上下文太长怎么办？学会用 Compact 和 Clear</h2>
<p>当你和 Claude Code 互动得越来越多，它的上下文会不断累积：</p>
<ul>
 <li>
  <p>你提了很多需求</p></li>
 <li>
  <p>它写了很多代码</p></li>
 <li>
  <p>跑了很多命令</p></li>
 <li>
  <p>调了很多工具</p></li>
 <li>
  <p>还读了图片和 MCP</p></li>
</ul>
<p>如果不处理，这会带来几个问题：</p>
<ul>
 <li>
  <p>响应变慢</p></li>
 <li>
  <p>成本变高</p></li>
 <li>
  <p>容易抓不住重点</p></li>
 <li>
  <p>记忆越来越乱</p></li>
</ul>
<p>所以一定要学会上下文管理。</p>
<hr>
<h3>1）/compact：保留重点，压缩无关噪音</h3>
<p>当你觉得当前会话已经很长，但项目还要继续做下去，这时最推荐用的是压缩。压缩的作用不是“忘掉一切”，而是：</p>
<ul>
 <li>
  <p>把核心需求留下来</p></li>
 <li>
  <p>把关键信息提炼出来</p></li>
 <li>
  <p>把那些冗长日志、中间过程、重复记录压缩掉</p></li>
</ul>
<p>这样 Claude Code 后面还能继续工作，但负担会小很多。Ctrl + o 可以查看压缩后的上下文内容。</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-19.png"></p>
<p>这非常适合：</p>
<ul>
 <li>
  <p>一个功能做完，要继续做下一个功能</p></li>
 <li>
  <p>会话很长，但项目背景还要保留</p></li>
 <li>
  <p>想降低上下文噪音</p></li>
</ul>
<hr>
<h3>2）/clear：彻底清空上下文</h3>
<p>如果你接下来要做的是另一个完全无关的任务，那就没必要背着旧上下文继续走。这时候可以直接清空。适合这种情况：</p>
<ul>
 <li>
  <p>这个项目先不做了</p></li>
 <li>
  <p>接下来换成另一个目录、另一类任务</p></li>
 <li>
  <p>旧上下文继续保留反而容易干扰判断</p></li>
</ul>
<p>一句话总结：</p>
<ul>
 <li><strong>还在同一个项目里继续推进：优先 <code>compact</code></strong></li>
 <li><strong>准备换任务、换上下文：再考虑 <code>clear</code></strong>
  <p></p></li>
</ul>
<p>未来会不会高效使用 AI，核心能力之一就是：你会不会管理上下文。</p>
<hr>
<h2>十八、CLAUDE.md：把“口头提醒”升级成“项目记忆”</h2>
<p>很多人用 Claude Code，会不断重复说这些话：</p>
<ul>
 <li>
  <p>这个项目用 React + TypeScript</p></li>
 <li>
  <p>不允许动 API 层</p></li>
 <li>
  <p>样式统一用 Tailwind</p></li>
 <li>
  <p>输出说明用中文</p></li>
 <li>
  <p>不要随便改目录结构</p></li>
 <li>
  <p>变更前先给计划</p></li>
 <li>
  <p>回答要简洁</p></li>
</ul>
<p>如果这些都靠每次口头说，那太低效了。Claude Code 提供了一种更稳定的办法：<br><strong>项目记忆文件 <code>CLAUDE.md</code>。</strong></p>
<p>你可以让 Claude Code 帮你初始化一份 <code>CLAUDE.md</code>，然后你自己继续补充内容。</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-20.png"></p>
<p>这个文件非常适合放：</p>
<ul>
 <li>
  <p>项目背景</p></li>
 <li>
  <p>技术栈</p></li>
 <li>
  <p>目录约束</p></li>
 <li>
  <p>开发规范</p></li>
 <li>
  <p>输出语言</p></li>
 <li>
  <p>风格偏好</p></li>
 <li>
  <p>注意事项</p></li>
</ul>
<p>例如你完全可以写：</p>
<ul>
 <li>
  <p>本项目使用 React + TypeScript + Vite</p></li>
 <li>
  <p>所有新增组件放入 <code>src/components</code></p></li>
 <li>
  <p>不允许直接修改 <code>api</code> 目录</p></li>
 <li>
  <p>所有回答以中文输出</p></li>
 <li>
  <p>需要先给出改造思路再动手</p></li>
 <li>
  <p>样式优先保持现有视觉风格</p></li>
</ul>
<p>这样 Claude Code 每次进入这个项目时，就会读取这些规则。</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-21.jpeg"></p>
<p>它的本质，就是把你和 AI 之间那些反复重复的口头约定，固化成项目级长期记忆。</p>
<hr>
<h2>十九、项目级记忆和用户级记忆要分开理解</h2>
<p>通常这类记忆 /memory 会有两层：</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-22.png"></p>
<h4>1）项目级 ./CLAUDE.md</h4>
<p>只对当前项目生效。适合写这个项目自己的规则。</p>
<h4>2）用户级 ~/.claude/CLAUDE.md</h4>
<p>对你这个用户整体生效。适合写你个人长期不变的偏好。</p>
<table>
 <tbody>
  <tr>
   <td>
    <p>项目级适合写</p></td>
   <td>
    <p>用户级适合写</p></td>
  </tr>
  <tr>
   <td>
    <ul>
     <li>
      <p>技术栈</p></li>
     <li>
      <p>目录结构要求</p></li>
     <li>
      <p>项目特定约束</p></li>
     <li>
      <p>输出规范</p></li>
    </ul></td>
   <td>
    <ul>
     <li>
      <p>你偏爱中文回复</p></li>
     <li>
      <p>你喜欢先给方案再执行</p></li>
     <li>
      <p>你喜欢精简还是详细风格</p></li>
     <li>
      <p>你常用的编码习惯</p></li>
    </ul></td>
  </tr>
 </tbody>
</table>
<p>这两层分清之后，Claude Code 的记忆会更稳定，也更不容易混乱。</p>
<hr>
<h2>二十、Hook：把重复动作自动化</h2>
<p>接下来开始进入高级玩法。</p>
<p>1. Hook 是什么？</p>
<p>你可以把它理解成：当 Claude Code 完成某个动作时，自动触发你预先定义的一段逻辑。最典型的场景，就是代码格式化。</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-23.png"></p>
<p>比如你不想每次都手工运行格式化工具。那么就可以配置一个 Hook：只要 Claude Code 刚刚创建或编辑了文件，就自动执行一次格式化。这个逻辑非常适合做成 Hook。</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-24.png"></p>
<h3>2. Hook 适合干什么？</h3>
<p>除了格式化，它还很适合自动做这些事：</p>
<ul>
 <li>
  <p>运行 prettier</p></li>
 <li>
  <p>运行 lint</p></li>
 <li>
  <p>自动补充文件头</p></li>
 <li>
  <p>执行测试</p></li>
 <li>
  <p>生成日志</p></li>
 <li>
  <p>发送通知</p></li>
 <li>
  <p>校验命名规则</p></li>
</ul>
<p>它的本质是：</p>
<p><strong>把“每次都得手动做的事”变成自动执行的流程。</strong></p>
<p>当团队里很多规范总是靠“记得做一下”维持时，Hook 的价值就非常大。因为一旦靠人记忆，迟早会漏。</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-25.png"></p>
<h3>3. Hook 的思维方式</h3>
<p>你在设计 Hook 时，其实只需要想清楚三件事：</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-26.png"></p>
<p>你一旦按这个思路去理解，Hook 就不再是一个抽象概念，而是一个很实用的自动化入口。</p>
<hr>
<h2>二十一、Agent Skill：把常用套路沉淀成随时可调用的能力</h2>
<p>有些任务不是很复杂，但重复频率很高，而且每次格式都差不多。例如：</p>
<ul>
 <li>
  <p>每日总结</p></li>
 <li>
  <p>周报</p></li>
 <li>
  <p>会议纪要</p></li>
 <li>
  <p>发布说明</p></li>
 <li>
  <p>Bug 报告</p></li>
 <li>
  <p>Code Review 模板</p></li>
 <li>
  <p>PR 描述</p></li>
</ul>
<p>如果你每次都重新写要求，太浪费了。这时候最适合用 Agent Skill。</p>
<p>你可以把它理解成：一份给 Claude Code 看的能力说明书。它通常包含两部分：</p>
<h4>第一部分：元信息</h4>
<ul>
 <li>
  <p>名称</p></li>
 <li>
  <p>描述</p></li>
 <li>
  <p>什么时候适合调用</p></li>
</ul>
<h4>第二部分：具体要求</h4>
<ul>
 <li>
  <p>输出格式</p></li>
 <li>
  <p>固定结构</p></li>
 <li>
  <p>语气要求</p></li>
 <li>
  <p>需要包含哪些信息</p></li>
</ul>
<hr>
<h3>举个最典型的例子：日报 Skill</h3>
<p>假设你每天都想让 Claude Code 按固定格式帮你写日报，那你就可以创建一个类似 <code>daily-report</code> 的 Skill。</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-27.png"></p>
<p>里面规定：</p>
<ul>
 <li>
  <p>必须包含日期</p></li>
 <li>
  <p>必须有开发摘要</p></li>
 <li>
  <p>必须有开发详情</p></li>
 <li>
  <p>必须有问题与阻塞</p></li>
 <li>
  <p>必须有明日计划</p></li>
</ul>
<p>以后当你输入：</p>
<blockquote>
 <p>写一份今日开发总结</p>
</blockquote>
<p>Claude Code 就可能自动识别并调用这个 Skill。或者你也可以主动调用它。这样你的日报输出就能长期保持同样结构，而不必每天都重复解释一次。</p>
<p>这就是 Skill 最适合的场景：高频、固定套路、对格式要求强。</p>
<hr>
<h2>二十二、SubAgent：不是模板，而是“分身”</h2>
<p>很多人学到这里，会觉得：</p>
<p>“Skill 已经很强了，那为什么还要 SubAgent？”</p>
<p>因为这两者根本不是一个层级的东西。</p>
<ul>
 <li>
  <p>Skill 更像是“给主助手加了一套固定写法”。</p></li>
 <li>
  <p>而 SubAgent 更像是“给主助手配了一个专门干某类活的分身”。</p></li>
</ul>
<p>这就是本质区别。</p>
<hr>
<h3>1. SubAgent 适合什么场景？</h3>
<p>适合这些任务：</p>
<ul>
 <li>
  <p>代码审核</p></li>
 <li>
  <p>大型目录分析</p></li>
 <li>
  <p>安全检查</p></li>
 <li>
  <p>文档巡检</p></li>
 <li>
  <p>架构审查</p></li>
 <li>
  <p>风险评估</p></li>
</ul>
<p>这些任务通常有个共同特点：</p>
<ul>
 <li>
  <p>中间过程很多</p></li>
 <li>
  <p>可能要读大量代码</p></li>
 <li>
  <p>需要独立分析</p></li>
 <li>
  <p>不希望把主会话塞得很脏</p></li>
</ul>
<p>这时就很适合交给 SubAgent。</p>
<hr>
<h3>2. 你可以如何理解 SubAgent？</h3>
<p>你可以这样想：</p>
<p>主会话是你当前坐在桌前的主工程师。<br>
  SubAgent 是你临时叫来的某个专项顾问。</p>
<p>比如你说：</p>
<blockquote>
 <p>帮我做一次代码审核</p>
</blockquote>
<p>这时候主 Agent 不一定自己亲自去啃所有文件，而是把任务交给一个“代码审核专员”去做。</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-28.png"></p>
<p>这个专员：</p>
<ul>
 <li>
  <p>有自己的任务边界</p></li>
 <li>
  <p>有自己的行为规则</p></li>
 <li>
  <p>有自己的上下文</p></li>
 <li>
  <p>有自己的工具权限</p></li>
</ul>
<p>它干完活之后，只把最终审核结果汇报回来。这样，主会话就不会被一堆中间分析过程撑爆。</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-29.png"></p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-30.png"></p>
<h2>二十三、Skill 和 SubAgent 的区别，一定要彻底弄懂</h2>
<p>这是 Claude Code 里最容易混淆、但又最关键的点之一。</p>
<table>
 <tbody>
  <tr>
   <th>
    <p></p></th>
   <th>
    <p>Agent Skill</p></th>
   <th>
    <p>SubAgent</p></th>
  </tr>
  <tr>
   <td>
    <p>特点：</p></td>
   <td>
    <ul>
     <li>
      <p>共享主会话上下文</p></li>
     <li>
      <p>继承你当前对话里的背景</p></li>
     <li>
      <p>过程也会进入当前上下文</p></li>
     <li>
      <p>适合轻量、格式化、高频任务</p></li>
    </ul></td>
   <td>
    <ul>
     <li>
      <p>有独立上下文</p></li>
     <li>
      <p>中间过程不污染主会话</p></li>
     <li>
      <p>适合重分析任务</p></li>
     <li>
      <p>适合处理大量内容</p></li>
    </ul></td>
  </tr>
  <tr>
   <td>
    <p>比如：</p></td>
   <td>
    <ul>
     <li>
      <p>日报</p></li>
     <li>
      <p>周报</p></li>
     <li>
      <p>当前任务总结</p></li>
     <li>
      <p>会议纪要</p></li>
    </ul></td>
   <td>
    <ul>
     <li>
      <p>大项目代码审核</p></li>
     <li>
      <p>风险检查</p></li>
     <li>
      <p>大规模文档扫描</p></li>
     <li>
      <p>深度架构分析</p></li>
    </ul></td>
  </tr>
 </tbody>
</table>
<p>一句话记住：Skill 是套路。SubAgent 是分身。</p>
<p>再具体一点：</p>
<ul>
 <li>
  <p>你想让 Claude Code 用固定格式做事，用 Skill。</p></li>
 <li>
  <p>你想让 Claude Code 派一个独立代理去做重任务，用 SubAgent。</p></li>
</ul>
<p>只要把这点记住，后面很多高级玩法你都会顺很多。</p>
<hr>
<h2>二十四、Plugin：把 Skill、SubAgent、Hook 等能力打包成一键安装包</h2>
<p>如果说 Skill、Hook、SubAgent 还是单个能力组件，那么 Plugin 就是把这些组件打包起来，做成一个能力安装包。</p>
<p>你可以把 Plugin 理解成：Claude Code 的能力整合包。</p>
<p>安装一个 Plugin，可能就相当于一次性装上了：</p>
<ul>
 <li>
  <p>一个 Skill</p></li>
 <li>
  <p>一个 Hook</p></li>
 <li>
  <p>一个 SubAgent</p></li>
 <li>
  <p>一组配置</p></li>
 <li>
  <p>甚至一些外部工具接入规则</p></li>
</ul>
<hr>
<h3>1. Plugin 的价值在哪里？</h3>
<p>它最大的价值不是给个人玩，而是给团队复用。比如一个团队里，已经沉淀出一套成熟的前端设计工作流：</p>
<ul>
 <li>
  <p>有固定的界面规范</p></li>
 <li>
  <p>有常用的提示模板</p></li>
 <li>
  <p>有统一的样式策略</p></li>
 <li>
  <p>有审核要求</p></li>
</ul>
<p>如果这些东西都靠口口相传，很容易失真。<br>
  但如果能打成 Plugin，团队成员装上就能直接用，效率会高很多。</p>
<hr>
<h3>2. 前端设计类 Plugin 为什么特别值得关注？</h3>
<p>因为 AI 生成前端页面时，经常会出现一种“很像 AI 做的页面”的感觉。</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-31.png"></p>
<p>比如：</p>
<ul>
 <li>
  <p>配色套路化</p></li>
 <li>
  <p>布局审美雷同</p></li>
 <li>
  <p>交互缺乏层次</p></li>
 <li>
  <p>有种熟悉的模板味</p></li>
</ul>
<p>而一些专门的前端设计类 Plugin，目标就是改善这种共性，让 Claude Code 在做页面时更贴近成熟设计规范，而不是只会输出那种标准化 AI Demo 风格。</p>
<p>所以如果你是做前端的，或者你经常让 Claude Code 出页面，Plugin 这条线非常值得深入研究。</p>
<hr>
<h2>二十五、真正想把 Claude Code 用进生产，建议你这样落地</h2>
<p>讲到这里，能力很多了。但真正能不能用起来，关键还是看你的使用策略。这里给你几个最实用的落地建议。</p>
<hr>
<h3>建议 1：小任务直接做，大任务先 Plan Mode</h3>
<p>不要所有任务都一句话扔给 Claude Code 开干。正确做法是：</p>
<ul>
 <li>
  <p>小改动、单功能、单文件：直接做</p></li>
 <li>
  <p>重构、迁移、新架构、大功能：先出计划</p></li>
</ul>
<p>这会明显降低返工率。</p>
<hr>
<h3>建议 2：把 <code>dangerously-skip-permissions</code> 当作实验环境加速器，不要当默认配置</h3>
<p>它确实很爽，但不该在所有环境无脑开启。只在这些地方考虑用：</p>
<ul>
 <li>
  <p>本地实验目录</p></li>
 <li>
  <p>新建 Demo</p></li>
 <li>
  <p>可随时删除的沙盒项目</p></li>
</ul>
<p>不要在这些地方轻易开：</p>
<ul>
 <li>
  <p>公司项目</p></li>
 <li>
  <p>老仓库</p></li>
 <li>
  <p>敏感代码库</p></li>
 <li>
  <p>有配置和密钥的目录</p></li>
</ul>
<hr>
<h3>建议 3：尽早写好 <code>CLAUDE.md</code></h3>
<p>很多人不是不会用 Claude Code，而是不会给它稳定上下文。把这些信息尽早写进去：</p>
<ul>
 <li>
  <p>技术栈</p></li>
 <li>
  <p>目录约束</p></li>
 <li>
  <p>输出语言</p></li>
 <li>
  <p>项目背景</p></li>
 <li>
  <p>风格偏好</p></li>
 <li>
  <p>不能碰的地方</p></li>
 <li>
  <p>修改前必须先做什么</p></li>
</ul>
<p>这是提升稳定性的关键动作之一。</p>
<hr>
<h3>建议 4：重复性输出用 Skill，重分析任务用 SubAgent</h3>
<p>这个判断一定要形成肌肉记忆：</p>
<ul>
 <li>
  <p>高频格式任务 → Skill</p></li>
 <li>
  <p>深度分析任务 → SubAgent</p></li>
</ul>
<p>一旦选对，Claude Code 会好用很多。</p>
<hr>
<h3>建议 5：真正想做设计还原，尽量接 MCP</h3>
<p>文字描述 UI，通常不够准；<br>
  只看截图，通常不够细；<br>
  能接结构化设计信息，才更接近工程可用。</p>
<p>所以如果你们本来就在用 Figma，尽快研究 MCP，会非常值。</p>
<hr>
<h3>建议 6：回滚只是应急，Git 仍然是正式版本控制核心</h3>
<p>Claude Code 可以帮你快速撤销错误方向，但不要因为它有 Rewind，就忽略 Git。真正重要的项目，一定要继续保留：</p>
<ul>
 <li>
  <p>分支</p></li>
 <li>
  <p>提交记录</p></li>
 <li>
  <p>回滚点</p></li>
 <li>
  <p>可审计变更</p></li>
</ul>
<p>Claude Code 是开发搭档，不是版本治理系统。</p>
<hr>
<h2>二十六、结语：Claude Code 的真正门槛，不在命令，而在工作流</h2>
<p>很多人第一次看 Claude Code，会被它“能写代码”吸引。但用久了你会发现，它真正厉害的地方，从来不是“生成一段代码”。而是它正在逐步提供一整套开发 Agent 工作流能力：</p>
<p></p>
<p><img alt="图片" src="/blog/ai/assets/csdn-159353229-32.png"></p>
<ul></ul>
<p>这些能力组合在一起，Claude Code 就不再只是一个代码助手，而更像一个可以被你逐步驯化、配置、扩展、沉淀的开发系统。所以学 Claude Code，真正要学的不是几个命令，而是这件事：</p>
<p><strong>你如何设计自己的 AI 开发工作流。</strong></p>
<p>这才是它从“好玩”走向“好用”，再走向“生产可落地”的关键。</p></div>
