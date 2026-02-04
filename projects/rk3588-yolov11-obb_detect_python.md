---
title: rk3588-yolov11-obb_detect_python
date: 2026-02-04
author: ana52070
tags: [GitHub项目]
description: 暂无描述
---

# rk3588-yolov11-obb_detect_python

> 项目地址：[https://github.com/ana52070/rk3588-yolov11-obb_detect_python](https://github.com/ana52070/rk3588-yolov11-obb_detect_python)
> 
> 暂无描述

---

# YOLOv11-OBB RK3588 Python Demo

本项目提供了一套在 **Rockchip RK3588** 平台上使用 Python 和 **RKNN-Toolkit-Lite2** 部署 **YOLOv11 OBB (Oriented Bounding Box)** 旋转目标检测模型的示例代码。

项目充分利用了 RK3588 的 3 个 NPU 核心进行并发推理，支持单张图片、批量图片以及视频流的高效检测。

## ✨ 功能特性

*   **YOLOv11 OBB 支持**: 实现了针对旋转目标检测的后处理逻辑（DFL 解码 + 角度计算）。
*   **RK3588 3核并发**: 利用 RK3588 的 3 个 NPU 核心（Core 0, 1, 2）进行多线程并发推理，显著提升吞吐量。
*   **视频流处理**: 包含完整的视频推理管线（Reader -> Queue -> 3-Core Workers -> Queue -> Writer），并实现了**帧重排序**逻辑，确保输出视频帧顺序正确。
*   **开箱即用**: 提供了适配不同 Python 版本的 `rknn_toolkit_lite2` 安装包。

## 📂 目录结构

```text
.
├── inference_img.py        # 单线程、单核心图片推理示例（适合调试）
├── inference_3npu_img.py   # 多线程、3核心并发图片推理示例（高性能）
├── inference_mp4.py        # 多线程、3核心并发视频推理示例
├── inputimage/             # 输入图片目录
├── outputimage/            # 输出结果保存目录
├── rknnlite_packages/      # RKNN-Toolkit-Lite2 离线安装包 (Python 3.7 - 3.12)
├── librknnrt.so            # RKNN 运行时库
└── README.md               # 项目说明文档
```

## 🛠️ 环境依赖与安装

### 1. 硬件要求
*   Rockchip RK3588 开发板 (如 Orange Pi 5, Rock 5B, ITX-3588J 等)
*   系统: Ubuntu / Debian / RKNPU2 驱动已安装

### 2. 安装 Python 依赖
确保已安装 `opencv-python` 和 `numpy`：

```bash
pip install opencv-python numpy
```

### 3. 安装 RKNN-Toolkit-Lite2
本项目在 `rknnlite_packages/` 目录下提供了适配不同 Python 版本的 `.whl` 安装包。请根据您的 Python 版本选择安装：

```bash
# 例如，如果您使用的是 Python 3.9
pip install rknnlite_packages/rknn_toolkit_lite2-2.1.0-cp39-cp39-linux_aarch64.whl
```

## 🚀 快速开始

### ⚠️ 重要配置说明
在运行代码前，请务必打开对应的 `.py` 文件，修改 `RKNN_MODEL` 变量为您实际的模型路径：

```python
# 请修改为您自己的模型路径
RKNN_MODEL = '/path/to/your/yolov11_obb.rknn'
```

### 1. 单图推理 (Debug)
用于测试模型是否正常加载及后处理逻辑是否正确。

```bash
python inference_img.py
```
*   输入：`inputimage/` 目录下的图片
*   输出：`outputimage/` 目录下的 `final_*.jpg`

### 2. 多核并发图片推理 (High Performance)
使用 3 个线程同时调用 NPU 的 3 个核心处理图片文件夹。

```bash
python inference_3npu_img.py
```
*   输入：`inputimage/` 目录下的图片
*   输出：`outputimage/` 目录下的 `multi_*.jpg`

### 3. 视频推理
对视频文件进行多核加速推理，并保存结果视频。

```bash
# 请在 inference_mp4.py 中修改 VIDEO_PATH 和 OUTPUT_PATH
python inference_mp4.py
```

## 🧠 模型说明

本项目默认适配的 YOLOv11 OBB 模型参数如下（需与您的导出模型一致）：
*   **输入尺寸**: 1280 x 736
*   **量化类型**: INT8 (建议去头操作 `nohead` 以获得最佳性能)
*   **输出节点**: 3 个尺度的特征图 (Strides: 8, 16, 32)

如果您使用不同的输入尺寸或模型结构，请相应修改代码中的 `IMG_SIZE` 和 `post_process` 函数。

## 📝 常见问题

1.  **报错 `ImportError: librknnrt.so: cannot open shared object file`**
    *   请确保 `librknnrt.so` 在系统库路径中，或者将其所在目录添加到 `LD_LIBRARY_PATH`。
    *   本项目根目录已包含该文件，可以尝试：`export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)`

2.  **检测框乱飞或角度不对**
    *   检查 `post_process` 中的 `dfl_dist` 解码逻辑和 `angle` 计算公式是否与您的训练/导出配置一致。
    *   确认 `IMG_SIZE` 是否与模型输入严格匹配。

## 📄 License

MIT License
