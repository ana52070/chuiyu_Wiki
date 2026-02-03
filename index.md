---
# 使用官方的首页布局
layout: home

# 1️⃣ 首页大图文区域 (Hero Section)
hero:
  name: "Chuiyu Wiki" # 大标题
  text: "我的技术修炼之路" # 副标题
  tagline: "专注分享 Java 后端、AI 实战与嵌入式开发心得" # 标语
  
  # 首页大图 (Hero Image)
  # 你可以准备一张好看的大图（如 avatar.png），也放在 public 文件夹下
  image:
    src: /avatar.png # 图片路径
    alt: Chuiyu Wiki Logo # 图片描述

  # 操作按钮 (Actions)
  actions:
    - theme: brand # 主色按钮
      text: "开始阅读 🚀"
      link: /blog/ # 跳转到博客列表页
    - theme: alt # 次色按钮
      text: "GitHub 源码"
      link: https://github.com/你的用户名/你的仓库名

# 2️⃣ 特性卡片区域 (Features Section)
# 可以在这里列出你网站的几个主要亮点或板块
features:
  - title: ☕ Java后端技术栈
    details: 深入理解 Spring Boot、微服务架构、并发编程与性能调优。
    icon: ☕ # 可以是 Emoji，也可以是图片路径
  - title: 🤖 AI与深度学习
    details: 记录机器学习模型训练、YOLO目标检测、RKNN边缘计算部署实战。
    icon: 🤖
  - title: 💻 嵌入式与IoT
    details: 探索硬件开发乐趣，分享树莓派、ESP32等项目的折腾笔记。
    icon: 💻
---