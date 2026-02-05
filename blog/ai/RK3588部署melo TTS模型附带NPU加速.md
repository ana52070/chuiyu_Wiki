---
date: 2026-02-05 14:51:44
title: RK3588部署melo TTS模型附带NPU加速
permalink: /pages/aaf782
categories:
  - blog
  - ai
---
# **环境**

LubanCat4 RK3588S

ubuntu22.04 LTS

Python3.10

相关来源链接：


[野火]嵌入式AI应用开发实战指南—基于LubanCat-RK系列板卡 文档](https://doc.embedfire.com/linux/rk356x/Ai/zh/latest/lubancat_ai/env/toolkit_lite2.html#id2)


[happyme531/MeloTTS-RKNN2 · HF Mirror](https://hf-mirror.com/happyme531/MeloTTS-RKNN2)


在RK3588上运行MeloTTS文字转语音模型!

- 推理速度(RK3588): 约5倍速
- 内存占用(RK3588): 约0.2GB

## 使用方法

1. 克隆或者下载此仓库到瑞芯微SoC的系统上.
    
2. 安装依赖
    

```bash
pip install -r requirements.txt
pip install rknn-toolkit-lite2
```

4. 运行

```bash
python melotts_rknn.py -s "你想要生成的文本"
```

## 已知问题

- 和原项目一样，Encoder部分并没有使用NPU加速，但是耗时不大，应该不会对推理速度有太大影响。


