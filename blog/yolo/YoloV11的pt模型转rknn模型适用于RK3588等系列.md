---
title: YoloV11的pt模型转rknn模型适用于RK3588等系列
date: 于 2026-01-12
tags: [CSDN搬运]
---

# YoloV11的pt模型转rknn模型适用于RK3588等系列

> 原文链接：[YoloV11的pt模型转rknn模型适用于RK3588等系列](https://blog.csdn.net/chui_yu666/article/details/156868279)

### YoloV11环境搭建

下载源码
    
    
    git clone https://github.com/ultralytics/ultralytics.git
    
    mv ultralytics yolov11
    
    cd yolov11/
    
    

搭建python环境(以conda为例)
    
    
    #创建conda环境
    conda create --name yolov11 python==3.10
    #激活
    conda activate yolov11
    
    #安装torch cuda版本
    pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
    
    
    
    

新建requirements.txt
    
    
    sudo vim requirements.txt
    
    
    
    #requirements.txt
    # YOLOv11 官方依赖（仅保留核心必要包，避免冲突）
    
    ultralytics>=8.2.0  # 包含 YOLOv11，直接安装官方最新版
    
    numpy>=1.21.6
    
    opencv-python>=4.6.0
    
    pillow>=9.1.0
    
    

安装依赖
    
    
    pip install -r requirememts.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    

新建环境测试脚本：test_env.py
    
    
    from ultralytics import YOLO
    import os
    # 加载 YOLOv11 官方预训练模型（自动下载，首次运行可能需要1-2分钟）
    model = YOLO('yolov11n.pt')  # 'yolov11n.pt' 是轻量版，适合快速验证；需要高精度可换 'yolov11x.pt'
    
    # 测试模型（用一张示例图，在线拉取测试图）
    
    results = model('https://ultralytics.com/images/zidane.jpg')  # 在线拉取测试图
    
    # 保存检测结果图片（关键修改：无界面环境用 save() 替代 show()）
    # 创建输出目录（避免报错）
    output_dir = 'yolo_detection_results'
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存标注后的图片（文件名：detection_result.jpg，保存到创建的目录中）
    save_path = os.path.join(output_dir, 'detection_result.jpg')
    
    results[0].save(save_path)  # 保存图片到本地
    
    
    print(f"检测完成！结果图片已保存至：{save_path}")
    
    

在官方github(https://github.com/ultralytics/ultralytics.git)中下载yolov11n.pt模型，放入到yolov11目录下：
    
    
    wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d025efc0c0e44ce6852ddc9cccdfaf7a.png)

完成后，运行测试环境代码：
    
    
    python3 test_env.py
    

如果成功弹出识别图片的话，则说明环境配置成功。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/014304ac90d0444fb2d92eb6bc2a3c48.png)

### Pt格式转rknn格式

首先需要安装rknn-toolkit2,可以直接去rknn-toolkit2的github中单独下载对应的requirements.txt和whl：  
[rknn-toolkit2/rknn-toolkit2/packages/arm64 at master · airockchip/rknn-toolkit2](<https://github.com/airockchip/rknn-toolkit2/tree/master/rknn-toolkit2/packages/arm64>)  
![!\[\[Pasted image 20260112151714.png\]\]](https://i-blog.csdnimg.cn/direct/4bfc9edd9d0642c7933e22260181ad47.png)
    
    
    #下载对应的requirements.txt和whl
    
    #安装requirements.txt
    pip install -r requirements_cp310-2.1.0.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    
    #安装rknn-toolkit2的whl
    pip install rknn_toolkit2-2.1.0+708089d1-cp310-cp310-linux_x86_64.whl
    
    

模型转换
    
    
    # Export a YOLO11n PyTorch model to RKNN format # 'name' can be one of rk3588, rk3576, rk3566, rk3568, rk3562, rv1103, rv1106, rv1103b, rv1106b, rk2118, rv1126b 
    
    yolo export model=yolo11n.pt format=rknn name=rk3588 # creates'/yolo11n_rknn_model'
    

导出参数  
![!\[\[Pasted image 20260112141016.png\]\]](https://i-blog.csdnimg.cn/direct/835bd9cedb5d43c4aa6fce2aba63ac92.png)

转换成功后，会输出保存的结果：  
![!\[\[Pasted image 20260112153411.png\]\]](https://i-blog.csdnimg.cn/direct/2044129eeadf4c949f281caa25e8498f.png)

然后我们可以在对应的路径下拿到模型rknn文件和其对应的metadata.yaml  
![!\[\[Pasted image 20260112153447.png\]\]](https://i-blog.csdnimg.cn/direct/a824b67710f543d9b9e7ea68107371eb.png)

至此，yolov11的pt转rknn完成。

