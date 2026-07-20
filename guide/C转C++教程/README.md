---
title: C++算法笔记1
author: claudecode(deepseekV4flash)
date: 2026-07-20 21:35:04
description: C++算法笔记1
tags:
  - Cpp算法
categories:
  - guide
  - C++算法入门
---

# C 转 C++ 教程

从 C 语言过渡到 C++ 的知识点梳理，面向有 C 基础的学习者。

## 目录结构

```
C转C++教程/
├── README.md
├── ch01-basics/          # 基本篇
│   ├── 01-使用C++刷算法的好处.md
│   ├── 02-using-namespace-std.md
│   ├── 03-cin和cout.md
│   ├── 04-头文件.md
│   ├── 05-变量声明.md
│   ├── 06-bool变量.md
│   ├── 07-const定义常量.md
│   ├── 08-string类.md
│   ├── 09-结构体.md
│   └── 10-引用和传值.md
├── ch02-stl/             # STL 篇
│   ├── 01-vector.md
│   ├── 02-set.md
│   ├── 03-map.md
│   ├── 04-stack.md
│   ├── 05-queue.md
│   └── 06-unordered-map和unordered-set.md
├── ch03-advanced/        # 进阶篇
│   ├── 01-bitset.md
│   ├── 02-sort函数.md
│   ├── 03-自定义cmp函数.md
│   └── 04-cctype头文件.md
└── ch04-cpp11/           # C++11 篇
    ├── 01-C++11简介.md
    ├── 02-auto声明.md
    ├── 03-基于范围的for循环.md
    ├── 04-to_string.md
    ├── 05-stoi-stod等转换函数.md
    └── 06-Dev-CPP使用C++11.md
```

## 章节导航

### 第 1 章：基本篇
C++ 基础语法入门，对比 C 语言的差异。

| 小节 | 内容 |
|------|------|
| [01 - 使用C++刷算法的好处](ch01-basics/01-使用C++刷算法的好处.md) | 兼容性、STL、string、性能权衡 |
| [02 - using namespace std](ch01-basics/02-using-namespace-std.md) | 命名空间的作用与使用 |
| [03 - cin 和 cout](ch01-basics/03-cin和cout.md) | C++ 风格的输入输出 |
| [04 - 头文件](ch01-basics/04-头文件.md) | C 与 C++ 头文件的对应关系 |
| [05 - 变量声明](ch01-basics/05-变量声明.md) | for 循环内声明变量 |
| [06 - bool 变量](ch01-basics/06-bool变量.md) | true/false 与数值转换 |
| [07 - const 定义常量](ch01-basics/07-const定义常量.md) | const 与 #define 对比 |
| [08 - string 类](ch01-basics/08-string类.md) | 定义、拼接、输入输出、常用方法 |
| [09 - 结构体](ch01-basics/09-结构体.md) | C++ 结构体可省略 struct |
| [10 - 引用和传值](ch01-basics/10-引用和传值.md) | 传值与传引用的区别 |

### 第 2 章：STL 篇
C++ 标准模板库的常用容器。

| 小节 | 内容 |
|------|------|
| [01 - vector](ch02-stl/01-vector.md) | 动态数组：创建、resize、push_back、迭代器 |
| [02 - set](ch02-stl/02-set.md) | 集合：自动排序、insert/find/erase |
| [03 - map](ch02-stl/03-map.md) | 键值对容器：添加、访问、遍历 |
| [04 - stack](ch02-stl/04-stack.md) | 栈：push/pop/top/size |
| [05 - queue](ch02-stl/05-queue.md) | 队列：push/pop/front/back/size |
| [06 - unordered_map 和 unordered_set](ch02-stl/06-unordered-map和unordered-set.md) | 无序版 map/set，超时场景替代 |

### 第 3 章：进阶篇
位运算、排序和字符处理工具。

| 小节 | 内容 |
|------|------|
| [01 - bitset](ch03-advanced/01-bitset.md) | 二进制位操作：set/flip/reset/to_ulong |
| [02 - sort 函数](ch03-advanced/02-sort函数.md) | 对数组/vector 排序 |
| [03 - 自定义 cmp 函数](ch03-advanced/03-自定义cmp函数.md) | 自定义排序规则 |
| [04 - cctype 头文件](ch03-advanced/04-cctype头文件.md) | 字符判断与转换函数 |

### 第 4 章：C++11 篇
C++11 新特性和实用函数。

| 小节 | 内容 |
|------|------|
| [01 - C++11 简介](ch04-cpp11/01-C++11简介.md) | C++11 总览 |
| [02 - auto 声明](ch04-cpp11/02-auto声明.md) | 类型推导，简化迭代器声明 |
| [03 - 基于范围的 for 循环](ch04-cpp11/03-基于范围的for循环.md) | 传值/传地址遍历容器 |
| [04 - to_string](ch04-cpp11/04-to_string.md) | 数字转字符串 |
| [05 - stoi/stod 等转换函数](ch04-cpp11/05-stoi-stod等转换函数.md) | 字符串转数值 |
| [06 - Dev C++ 使用 C++11](ch04-cpp11/06-Dev-CPP使用C++11.md) | 编译器设置方法 |

## 关于本教程

本教程来源于思维导图《C 转 C++》，旨在帮助有 C 语言基础的读者快速上手 C++。
