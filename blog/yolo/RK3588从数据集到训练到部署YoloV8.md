---
categories:
- yolo
date: 最新推荐文章于 2025-12-18
tags:
- yolo
title: RK3588从数据集到训练到部署YoloV8
permalink: /blog/yolo/RK3588从数据集到训练到部署YoloV8
---

# RK3588从数据集到训练到部署YoloV8

> 原文链接：[RK3588从数据集到训练到部署YoloV8](https://blog.csdn.net/chui_yu666/article/details/152815773)

### 环境配置

首先需要安装Conda、CUDA、Cudnn等工具，在此不过多赘述，主要讲解Python环境配置的相关参数
    
    
    Python版本：3.10
    
    Torch版本：1.13.1
    
    安装完成后还需要pip一下yolo的库：
    
    pip install ultralytics
    

### 数据库准备

数据库请自行准备，这里可以使用roboflow来进行数据库格式转换  
[roboflow](<https://app.roboflow.com/>)  
这里进入网站之后注册登录一下，然后新建工程  
![!\[\[Pasted image 20250818143655.png\]\]](https://i-blog.csdnimg.cn/direct/7062070b74a1430ba8e1af4d80d68df4.png)

然后上传自己的数据集  
![![](./assets/Pasted image 20250818143753.png)(https://i-blog.csdnimg.cn/direct/2d8649c86239412296c366514fd20f7f.png)

等待上传完毕  
![!\[\[Pasted image 20250818143809.png\]\]](https://i-blog.csdnimg.cn/direct/98454178dcca447ea605e68d333c36b3.png)

上传完毕后，点击Versions，然后后面的选项都默认即可  
![!\[\[Pasted image 20250818143856.png\]\]](https://i-blog.csdnimg.cn/direct/a9b4f0c8bf5f49a2b254a26200205905.png)

完成后点击创建  
![!\[\[Pasted image 20250818143917.png\]\]](https://i-blog.csdnimg.cn/direct/84920150f7fb43d8b427af3fa2ed6802.png)

创建完毕后，点击Download，选择YoloV8格式，  
![!\[\[Pasted image 20250818144012.png\]\]](https://i-blog.csdnimg.cn/direct/3e14ee6310e246229b5b5c0ad941f362.png)

这样，就拿到可以使用的数据集了。

### 模型训练

首先下载Yolov8：
    
    
    git clone https://github.com/Pertical/YOLOv8.git
    

然后在该项目中新建datasets文件夹，将上一步的数据集解压放入其中：  
![!\[\[Pasted image 20250818144540.png\]\]](https://i-blog.csdnimg.cn/direct/d779b0e089584c16b6563eda6aa25a6f.png)

随后，修改data.yaml
    
    
    train: /home/chuiyu/yolov8/ultralytics-main/datasets/data/train/images  #改为对应的绝对路径
    
    val: /home/chuiyu/yolov8/ultralytics-main/datasets/data/valid/images    #改为对应的绝对路径
    
    test: /home/chuiyu/yolov8/ultralytics-main/datasets/data/test/images    #改为对应的绝对路径
    
      
    
    nc: 1 #数据集种类数量
    
    names: ['0']  #数据集种类名称
    
      
    
    # roboflow:
    
    #   workspace: chuiyu
    
    #   project: yolo-38xf2
    
    #   version: 1
    
    #   license: CC BY 4.0
    
    #   url: https://universe.roboflow.com/chuiyu/yolo-38xf2/dataset/1
    

**最重要的一点** ：要改激活函数为ReLU，我们如果默认不改，则训练得到的PT模型的激活函数为SiLU，如下所示：  
![!\[\[Pasted image 20250818145220.png\]\]](https://i-blog.csdnimg.cn/direct/96f83c52c6eb4dd29773ce0a727fc429.png)

SiLU函数在PT模型中无任何问题，与ReLU函数的训练结果对比非常接近  
改激活函数流程如下：  
把ultralytics/nn/modules/conv.py中的Conv类进行修改，  
将default_act = nn.SiLU() # default activation改为  
default_act = nn.ReLU() # default activation

在项目根目录新建一个train.py
    
    
    from ultralytics import YOLO
    
      
    
    # 加载模型
    
    model = YOLO("yolov8n.yaml")  # 从头开始构建新模型
    
    model = YOLO("yolov8n.pt")  # 加载预训练模型（推荐用于训练）
    
      
    
    # Use the model
    
    results = model.train(data="datasets/data/data.yaml", epochs=300,batch=4)  # 训练模型
    
    # results = model.val()  # 在验证集上评估模型性能
    
    # results = model("https://ultralytics.com/images/bus.jpg")  # 预测图像
    
    # success = model.export(format="onnx")  # 将模型导出为 ONNX 格式
    
    

将yolov8n同样放入项目根目录(可去github上进行下载)  
随后即可运行train.py进行训练
    
    
    python3 train.py
    

### 测试验证

训练完成后，同样在根目录创建一个test.py用于测试验证
    
    
    from ultralytics import YOLO
    
      
    
    # 加载模型
    
    model = YOLO("/home/chuiyu/yolov8/ultralytics-main/runs/detect/train11/weights/best.pt")  # 将路径改为自己训练后的路径
    
      
      
    
    results = model("datasets/data/test/images")
    
    for result in results:
    
        result.save()
    

运行test.py，即可将测试集中的识别结果保存到根目录，可打开查看

### pt转onnx

在训练得到PT模型后，我们可以用netron软件打开模型，看一下结构

现在我们的激活函数已经为ReLU了。

pt转onnx我们需要使用另一个yolov8的工程，
    
    
    git clone https://github.com/airockchip/ultralytics_yolov8.git
    

将之前训练的.pt文件放入该项目的根目录  
同时在根目录新建一个requirements.txt
    
    
    # Ultralytics requirements
    # Usage: pip install -r requirements.txt
    
    # Base ----------------------------------------
    matplotlib>=3.2.2
    numpy>=1.22.2 # pinned by Snyk to avoid a vulnerability
    opencv-python>=4.6.0
    pillow>=7.1.2
    pyyaml>=5.3.1
    requests>=2.23.0
    scipy>=1.4.1
    # torch>=1.7.0
    # torchvision>=0.8.1
    tqdm>=4.64.0
    
    # Logging -------------------------------------
    # tensorboard>=2.13.0
    # dvclive>=2.12.0
    # clearml
    # comet
    
    # Plotting ------------------------------------
    pandas>=1.1.4
    seaborn>=0.11.0
    
    # Export --------------------------------------
    # coremltools>=7.0.b1  # CoreML export
    # onnx>=1.12.0  # ONNX export
    # onnxsim>=0.4.1  # ONNX simplifier
    # nvidia-pyindex  # TensorRT export
    # nvidia-tensorrt  # TensorRT export
    # scikit-learn==0.19.2  # CoreML quantization
    # tensorflow>=2.4.1  # TF exports (-cpu, -aarch64, -macos)
    # tflite-support
    # tensorflowjs>=3.9.0  # TF.js export
    # openvino-dev>=2023.0  # OpenVINO export
    
    # Extras --------------------------------------
    psutil  # system utilization
    py-cpuinfo  # display CPU info
    # thop>=0.1.1  # FLOPs computation
    # ipython  # interactive notebook
    # albumentations>=1.0.3  # training augmentations
    # pycocotools>=2.0.6  # COCO mAP
    # roboflow
    
    
    

然后下载依赖(同样使用之前的训练Yolov8的Python环境)
    
    
    pip install -r requirements.txt
    

完成后，修改**ultralytics_yolov8** 项目中的ultralytics/cfg/default.yaml，将其中的model参数路径改成你训练得到的的best.pt模型路径(记得使用绝对路径)  
![!\[\[Pasted image 20250818145810.png\]\]](https://i-blog.csdnimg.cn/direct/8418347f1aaa4d68ae04b3682890f05b.png)

回到刚才1中的ultralytics文件夹所在的路径下，依次执行如下两个命令：
    
    
    export PYTHONPATH=./
    python ./ultralytics/engine/exporter.py
    

结果如下所示，此时的.onnx就生成在了项目的根目录了。  
![!\[\[Pasted image 20250818145855.png\]\]](https://i-blog.csdnimg.cn/direct/07f3a891c71a46309ce979f9d6c7f609.png)  
再用netron打开我们的onnx模型，如下所示：  
![!\[\[Pasted image 20250818145950.png\]\]
!\[\[Pasted image 20250818145958.png\]\]](https://i-blog.csdnimg.cn/direct/2b769663d936413ba4ec923e655532c4.png)

注意！上图的三个红色方框非常重要，YOLOv8在RKNN转换过程中，是要有三个分支的，分别80×80检测头，40×40检测头，20×20检测头。每个检测头下，都有三个输出，分别是box边框输出，即图上的1×64×80×80；还有各类别输出，即1×4×80×80（这里的4就是指我在PT模型训练时的garbage.yaml文件中定义了4个类别），最后是综合置信度输出，即1×1×80×80。（其余检测头同理）

### onnx转rknn

这里我们另外创建Python环境
    
    
    conda create -n rknn210 python=3.8
    conda activate rknn210
    

现在需要用到rknn-toolkit2-2.1.0文件。  
进入rknn-toolkit2-2.1.0\rknn-toolkit2-2.1.0\rknn-toolkit2\packages文件夹下,安装依赖环境
    
    
    pip install -r requirements_cp38-2.1.0.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    
    pip install rknn_toolkit2-2.1.0+708089d1-cp38-cp38-linux_x86_64.whl
    
    

然后，我们的转rknn环境就配置完成了。

现在要进行模型转换,先进入rknn_model_zoo-2.1.0\examples\yolov8\python文件夹，先打开yolov8.py，进行适配参数修改：  
![!\[\[Pasted image 20250818150222.png\]\]](https://i-blog.csdnimg.cn/direct/31572bb4b7e44a62ae18b4e62499399a.png)

![!\[\[Pasted image 20250818150248.png\]\]](https://i-blog.csdnimg.cn/direct/7ca3cd5daf224c0d95dbb6efe319484d.png)

然后修改convert.py，如下所示：  
![!\[\[Pasted image 20250818150301.png\]\]](https://i-blog.csdnimg.cn/direct/8ebe82f9927c4937bed25d0ded177b9b.png)  
修改完成后，将我们之前得到的onnx模型复制到python文件夹下

运行转换命令
    
    
    python convert.py 模型文件名.onnx rk3588
    

可以看到，我们的模型转换并量化成功。

转换后的rknn模型已保存在model文件夹下。现在用netron打开我们的rknn模型，看一下结构：  
![!\[\[Pasted image 20250818150422.png\]\]](https://i-blog.csdnimg.cn/direct/a046b5c512004854be377b37861d806e.png)

这三个红框是和上面图中的三个红框对应的，所以若onnx没有所示的那三个框，则无法转换出适配官方部署文件的rknn模型。

### 模型部署

如果前面流程都已实现，模型的结构也没问题的话，则可以进行最后一步：模型端侧部署。  
我已经帮大家做好了所有的环境适配工作，科学上网后访问博主GitHub仓库:[YOLOv8_RK3588_object_detect](<https://github.com/A7bert777/YOLOv8_RK3588_object_detect>) 进行简单的路径修改就即可编译运行。
    
    
    git clone https://github.com/A7bert777/YOLOv8_RK3588_object_detect.git
    

git clone后把项目复制到开发板上，按如下流程操作：  
①：cd build，删除所有build文件夹下的内容  
②：cd src 修改main.cc，修改main函数中的如下三个内容：  
![!\[\[Pasted image 20250818150614.png\]\]](https://i-blog.csdnimg.cn/direct/eb1571f41d3d41f2b37edd46411851e3.png)

将这三个参数改成自己的绝对路径  
③：cd src 修改postprocess.cc下的txt标签的绝对路径：  
![!\[\[Pasted image 20250818150629.png\]\]](https://i-blog.csdnimg.cn/direct/fe25acf5ae264be49a5b025f5c13da92.png)

解释一下，这个标签路径中的内容如下所示：![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/32258086f1f843d7849df09ae143e23d.png)  
其实就是你在训练yolov8时在yaml配置文件中的那几个类别名  
④修改include/postprocess.h 中的宏 OBJ_CLASS_NUM

⑤：把你之前训练好并已转成RKNN格式的模型放到YOLOv8_RK3588_object_detect/model文件夹下，然后把你要检测的所有图片都放到YOLOv8_RK3588_object_detect/inputimage下。  
在运行程序后，生成的结果图片在YOLOv8_RK3588_object_detect/outputimage下

⑥：进入build文件夹进行编译
    
    
    cd build
    cmake ..
    make
    

然后就可以运行测试程序了：
    
    
    ./rknn_yolov8_demo
    

如果遇到了无法读取图片的报错：  
![!\[\[Pasted image 20250818150833.png\]\]](https://i-blog.csdnimg.cn/direct/3010bd6cd1d5403892d4812d24343929.png)

把main.cc中的ret = read_image_opencv(fullPath.c_str(), &src_image); 改为ret = read_image(fullPath.c_str(), &src_image);即可

### 参考资料

1.YoloV8模型训练：【【yolov8】2024,半小时速通yolov8，2024最新，windows,ubuntu,wsl】 https://www.bilibili.com/video/BV13H4y1G7DP/?share_source=copy_web&vd_source=800b0cce2dee97823e91fad6181bdec5

2.YoloV8模型转RKNN、部署：https://blog.csdn.net/A_l_b_ert/article/details/141610417?fromshare=blogdetail&sharetype=blogdetail&sharerId=141610417&sharerefer=PC&sharesource=chui_yu666&sharefrom=from_link

