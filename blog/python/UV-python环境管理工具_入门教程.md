---
categories:
- python
date: 最新推荐文章于 2026-01-05
tags:
- python
title: UV-python环境管理工具 入门教程
permalink: /blog/python/UV-python环境管理工具_入门教程
---

# UV-python环境管理工具 入门教程

> 原文链接：[UV-python环境管理工具 入门教程](https://blog.csdn.net/chui_yu666/article/details/148143137)

在学习使用 MCP 的时候接触到了 UV 这个环境管理工具，经过对比，发现它在诸多方面比 venv、conda 等工具更为出色，因此整理了这份简单的入门学习笔记，希望能帮助大家快速上手。

### 介绍

UV 是一款集 Python 版本管理、虚拟环境创建与管理、依赖安装等多功能于一体的轻量级工具，可类比为 “pyenv + virtualenv + pip-tools” 的组合。与传统工具不同，它使用 Rust 编写，这赋予了它卓越的性能，在处理依赖安装与解析时，速度可比 pip 快 10 - 100 倍 。

uv 的特点：

  1. 速度更快：相比 pip ，uv 采用 Rust 编写，性能更优。
  2. 支持 PEP 582：无需 virtualenv ，可以直接使用
  3. 兼容 pip ：支持 **pypackages** 进行管理。 requirements.txt 和 pyproject.toml 依赖管理。
  4. 替代 venv ：提供 uv venv 进行虚拟环境管理，比venv更轻量
  5. 跨平台：支持 Windows、macOS 和 Linux。



### 安装

##### 方法 1：pip

##### 使用 pip 安装（适用于已安装 pip 的系统）
    
    
     pip install uv
    

##### 方法 2：curl

##### 使用 curl 直接安装 如果你的系统没有 pip

直接运行：
    
    
    curl https://raw.githubusercontent.com/1stG/uv/master/installer.sh | bash
    

这会自动下载 uv 并安装到 /usr/local/bin 。

#### 方法 3：Windows 下的 PowerShell 安装

在 Windows 系统中，可通过 PowerShell 执行以下命令进行安装：
    
    
    irm https://raw.githubusercontent.com/1stG/uv/master/installer.ps1 | iex
    

安装完成后，可通过命令`uv --version`验证是否安装成功 。

### 换源

在 Windows 系统上修改 UV 的下载源，通过环境变量修改  
UV 提供了 UV_PYPI_INDEX_URL环境变量来设置默认的包索引源。

设置方法：  
打开 “此电脑” 或 “我的电脑”，右键点击选择 “属性”。  
在弹出的窗口中选择 “高级系统设置”。  
在 “系统属性” 窗口中，点击 “环境变量” 按钮。  
在 “系统变量” 或 “用户变量” 中点击 “新建”：  
变量名：UV_PYPI_INDEX_URL  
变量值：设置为你想要的镜像源地址，例如 https://pypi.tuna.tsinghua.edu.cn/simple。  
点击 “确定” 保存设置。

### 创建项目

笔者自己的理解：

​ 在传统的 venv、conda 等环境管理工具中，环境与项目相对独立，一个环境可运行多个项目代码（前提是环境匹配）。而 UV 通过在项目目录生成配置文件（`.uv`），实现环境与项目的便捷关联。默认情况下，进入项目目录时需手动激活环境，也可配置自动激活 。环境本质上是独立的，可在多个项目中复用。

因此，创建项目即创建环境。
    
    
    uv init project_name --python 3.12
    cd project_name
    

我们这里示例创建一个uv项目，名字叫uv_study:
    
    
    uv init uv_study --python 3.12
    cd uv_study
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9254028a45154030abd7bf17ca9570a2.png)

执行上述命令后，UV 会在当前目录下创建一个基于 Python 3.12 的虚拟环境，并生成`.uv`配置文件

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d62de66f778746669c963732775ca8ef.png)

这样，一个uv项目或者说一个uv环境就创建好了。

### 库管理

要想在这个环境中添加依赖库，只需要使用uv add命令即可。(当然得在对应的项目目录下)
    
    
    uv add package_name
    # 等效于pip install，但是比pip更快
    

例如，下图是uv初始环境：

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/40c7c5322a7649869748baea0455158f.png)

我们现在新安装一个requests库：
    
    
    uv add requests
    

安装完成后，uv会自动在pyproject.toml写入依赖，比传统的requirements.txt高效得多。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/52850d12a8614e488f0f47de78f57287.png)

当然也可以删除库：
    
    
    uv remove requests
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/482ba3857bce48758f9259ac6c75ee22.png)

### 运行项目

我们简单修改一下main.py运行测试一下：

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/a6be0b8f22364f35bd17ee0b89d600f9.png)

使用uv run即可
    
    
    uv run main.py
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/58b3b47e9e9d4c2db309dd170a5c217b.png)

### 使用别人的uv项目

我们这里先删除我们自己的venv环境：

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e890bc7c12cc4dfc873f64c8928e2e3d.png)

然后再重新导入这个uv项目，同步依赖，根据项目`pyproject.toml`文件安装所有声明的包：
    
    
    uv sync
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/79d61045a44446e9ae4abeaabbb6fe93.png)

如此，即可快速搭建与原作者一致的开发环境 。

