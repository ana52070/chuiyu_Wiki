---
categories:
- yolo
date: 最新推荐文章于 2025-12-31
tags:
- yolo
title: YoloV5的Onnx模型转RKNN模型(包成功，最详细)
permalink: /blog/yolo/YoloV5的Onnx模型转RKNN模型(包成功，最详细)
---

# YoloV5的Onnx模型转RKNN模型(包成功，最详细)

> 原文链接：[YoloV5的Onnx模型转RKNN模型(包成功，最详细)](https://blog.csdn.net/chui_yu666/article/details/146968079)

## 前言

下面是前期准备：

1.环境

Ubuntu20.04 LTS

存储：建议100G以上(我感觉50G左右可能够)

2.文件

rknn-toolkit2-1.4.0.zip(下载链接见4.其它)

onnx模型(算子集版本小于等于 12,具体原因详见4.其它中的3.1报错提示)

验证图片

模型的类别

3.方式

本博客使用VMware虚拟机以及VMware共享文件夹实现虚拟机和主机之间的互传文件。

这里放一下配置方法链接：

[主机与VMware虚拟机共享文件夹：解决虚拟机找不到共享文件夹问题 - 知乎](<https://zhuanlan.zhihu.com/p/650638983>)

## 1.安装docker
    
    
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get remove docker docker-engine docker.io containerd runc
    sudo apt-get install ca-certificates curl gnupg lsb-release
    # 添加密钥
    curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
    # 添加软件源
    sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
    
    sudo apt-get install docker-ce docker-ce-cli containerd.io
    sudo usermod -aG docker chs(换成你自己的用户名)
    sudo reboot
    sudo systemctl start docker
    sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
    service docker restart
    sudo docker run hello-world
    sudo docker version
    sudo docker images
    

注意：  
运行docker的helloworld时
    
    
    sudo docker run hello-world
    

如果显示helloworld则代表docker的环境正常，但如果提示：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9b4d633d16be4a14a8811926cac4070d.png)

属于正常现象，docker会有问题连接不上，国内全面禁止了docker本源及镜像源，用科学

不过不运行helloworld不影响rknn的转换，略过即可，只要后面的版本等信息输出正常就行：

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/6d9ce5b17a404e72b2c25977c2a1dfdc.png)

和我的截图差不多就行，不要有报错一般就代表安装成功了。

## 2.进入docker镜像

首先回到主目录
    
    
    cd ~/
    

创建一个rknn文件夹
    
    
    mkdir rknn
    

rknn-toolkit2-1.4.0.zip复制到rknn文件夹下

因为我这里是使用共享文件夹所以就当把rknn-toolkit2-1.4.0.zip复制到windows的对应目录后直接cp了：
    
    
    cp /mnt/hgfs/Ubuntu20.04/rknn-toolkit2-1.4.0.zip rknn-toolkit2-1.4.0.zip
    

然后解压这个文件夹
    
    
    unzip rknn-toolkit2-1.4.0.zip
    

再将onnx模型放入rknn-toolkit2-1.4.0/examples文件夹
    
    
    cd rknn
    cp /mnt/hgfs/Ubuntu20.04/best.onnx best.onnx
    cp best.onnx rknn-toolkit2-1.4.0/examples/best.onnx
    

然后将docker的镜像放到~/
    
    
     cp rknn-toolkit2-1.4.0/docker/rknn-toolkit2-1.4.0-cp38-docker.tar.gz ~/rknn-toolkit2-1.4.0-cp38-docker.tar.gz
    

开启docker服务
    
    
    sudo systemctl start docker
    

加载docker镜像，需要等一小会
    
    
    docker load --input rknn-toolkit2-1.4.0-cp38-docker.tar.gz
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/43eab1499d564c8c969889c0ab1bd951.png)

运行docker镜像
    
    
    docker run -t -i --privileged -v /dev/bus/usb:/dev/bus/usb -v ~/rknn/rknn-toolkit2-1.4.0/examples:/examples rknn-toolkit2:1.4.0-cp38 /bin/bash
    

如若运行成功，你就会成功进入docker镜像中，此时你将会变为root用户
    
    
    ls
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e34a6425f66042a8906e8cb550765481.png)

进入examples文件夹查看一下我们的onnx模型在不在
    
    
    cd examples/
    ls
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/442c1519b6ac486d8b783b4748e4a280.png)

正常，进入onnx的yolov5文件夹
    
    
    cd onnx/yolov5/
    

将其放入onnx的yolov5文件夹
    
    
     cp /examples/best.onnx best.onnx
     ls
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/82ce6dab16ed4affb763444b0a0fa112.png)

## 3.生成RKNN模型

首先将验证图片放入该文件夹，这里我们需要新建一个终端(不要关闭之前的终端)

然后将我们的一张验证图片放进来
    
    
    docker cp /mnt/hgfs/Ubuntu20.04/test.jpg infallible_sanderson:/examples/onnx/yolov5/test.jpg
    

这里解释一下：/mnt/hgfs/Ubuntu20.04/test.jpg 外部的图片

infallible_sanderson docker镜像名字，可用docker ps -a 指令查询

/examples/onnx/yolov5/test.jpg 要复制到的路径

回到最开始的那个终端

查看图片是否被复制进来
    
    
    ls
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0b048313f27c441792fe6e5898f48a56.png)

然后我们复制一份dataset.txt
    
    
    cp dataset.txt mydataset.txt
    

再编辑
    
    
    vim mydataset.txt
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/cc5dc337b2fa44328218f0e1e313897f.png)

点击i

然后将名称修改为我们刚复制进来的图片文件名

然后按esc

输入英文冒号:

输入wq，按回车保存

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/cc6747a9f3e549c1bbe7e800ea2e44ef.png)

再复制一份test.py后编辑
    
    
    cp test.py mytest.py
    vim mytest.py
    

ps:我这里中途换了一个onnx模型和图片，以jzl.onnx和jzl.jpg为例

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/b261f0a1100041fc90c25fd6d596ab79.png)

然后翻到最后

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e4426bb78e004e92a11b185ed5d6b0f7.png)

最后esc

英文冒号：

wq

回车

此时就可以开始运行代码开始转换了：
    
    
    python mytest.py
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/05f0dd7549b84f9fb6831eb890dd22a6.png)

等待几秒就好

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3002fc038f3544a6a0305f8aacc2febb.png)

然后查看一下是否导出成功
    
    
    ls
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ca3b8680ab244c479d3ae7b3a33b3945.png)

看起来像是成功了，我们将rknn模型和out.jpg拿出来

切换回到终端2，复制图片和模型文件
    
    
    docker cp infallible_sanderson:/examples/onnx/yolov5/out.jpg /mnt/hgfs/Ubuntu20.04/out.jpg
    Successfully copied 108kB to /mnt/hgfs/Ubuntu20.04/out.jpg
    
    
    docker cp infallible_sanderson:/examples/onnx/yolov5/jzl.rknn  /mnt/hgfs/Ubuntu20.04/jzl.rknn
    Successfully copied 8.45MB to /mnt/hgfs/Ubuntu20.04/jzl.rknn
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e11d9804f3f04a0bb4743d329dcd72a1.png)

回到windows对应的共享文件夹打开

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/a9689eff903242c3ba230dfd2897e630.png)

打开out.jpg看看

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/c610b6e443d04450a3ffd23bfa09b622.png)

效果不错，成功了

## 4.其它

#### 1.参考链接

【04 rk3568 yolov5 生成rknn文件】 https://www.bilibili.com/video/BV1Cz421k75D/?share_source=copy_web&vd_source=800b0cce2dee97823e91fad6181bdec5

#### 2.下载链接

##### 1.rknn-toolkit2-1.4.0.zip

链接: https://pan.baidu.com/s/1NM27wWLNjZkPaOzzoXfgKA?pwd=c6ad 提取码: c6ad 复制这段内容后打开百度网盘手机App，操作更方便哦

##### 2.Ubuntu20.04系统镜像

https://mirrors.tuna.tsinghua.edu.cn/ubuntu-releases/20.04/

#### 3.可能报错情况：

##### 3.1：onnx版本太高

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/843b15e0cce44147be548bc49e170e94.png)

需注意在使用yolo导出onnx模型的时候，在export.py中的opset属性要写12，写13会导致这里导出rknn报错

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/fafeafe111ce4b5f8ceeb60c2cea2b1d.png)

##### 3.2模型运行的输入纬度3维与实际要求4维，纬度不符的错误

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ef9f5531789e46ea9768bf840ff8b521.png)

此问题尚未解决，原因未知，但最后生成了RKNN文件，是否能用尚未测试。

