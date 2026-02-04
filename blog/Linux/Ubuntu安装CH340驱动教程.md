---
categories:
- Linux
date: 最新推荐文章于 2025-12-22
tags:
- Linux
title: Ubuntu安装CH340驱动教程
permalink: /blog/Linux/Ubuntu安装CH340驱动教程
---

# Ubuntu安装CH340驱动教程

> 原文链接：[Ubuntu安装CH340驱动教程](https://blog.csdn.net/chui_yu666/article/details/148385694)

### **Ubuntu22.04安装CH340驱动**

#### 3.1 用lsusb查看USB

  * 插上CH340之前



![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/efbfa66633474d52b09bc209b33fc607.png)

  * 插上CH340之后



![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e99b6f1750534d61878076581d2470cb.png)

输出中包含ID 1a86:7523 [QinHeng Electronics](<https://zhida.zhihu.com/search?content_id=251776544&content_type=Article&match_order=1&q=QinHeng+Electronics&zhida_source=entity>) CH340 serial converter的信息，这表明CH340设备已经被系统识别。

#### **3.2 查看USB转串口**
    
    
    ls -l /dev/ttyUSB0
    

/dev下没有该设备节点。

用[dmesg](<https://zhida.zhihu.com/search?content_id=251776544&content_type=Article&match_order=1&q=dmesg&zhida_source=entity>)命令查看：
    
    
    sudo dmesg | grep ch341
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/59f2f0c96bf54fdaa81ff64283d2c070.png)

ch341 uart转换器现在与ttyUSB0断开。

#### **3.3 升级驱动**

##### **一、安装 GCC 12 编译器**
    
    
    sudo apt-get update
    sudo apt-get install gcc-12 g++-12
    

##### **二、设置 GCC 12 为默认编译器**

使用 `update-alternatives` 命令配置系统默认编译器：
    
    
    # 添加gcc-12到备选列表
    sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 120 \
                             --slave /usr/bin/g++ g++ /usr/bin/g++-12 \
                             --slave /usr/bin/gcov gcov /usr/bin/gcov-12
    
    # 选择默认版本（会显示选项列表，选择gcc-12对应的编号）
    sudo update-alternatives --config gcc
    

[CH341SER_LINUX.ZIP - 南京沁恒微电子股份有限公司](<https://www.wch.cn/downloads/CH341SER_LINUX_ZIP.html>)

下载驱动后将其放入linux中。
    
    
    mkdir temp
    cd temp
    mkdir ch340
    

解压
    
    
    unzip CH341SER_LINUX.ZIP
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/982be83ead614a86964ffb00f4ef2765.png)

#### **3.4 编译安装CH340驱动**

切换到“driver”目录
    
    
    cd driver
    

使用“make”编译驱动程序，如果成功，将看到模块“ch341.ko”
    
    
    make
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/592f4dadeca64bb5af7970dc923c1c39.png)

键入“sudo make install”使驱动程序永久工作
    
    
    sudo make install
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/61532f4ac62a4211be411a39c8ce72f1.png)

重新插拔一次USB串口转换器  
用dmesg命令查看：
    
    
    sudo dmesg | grep ch341
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e2a6dc69f0b24cd991c68775d58150d3.png)

和 brltty程序冲突。  
卸载brltty程序  
brltty 是一款专为盲人设计的屏幕阅读器软件，它能够将文本输出转换为盲文点阵显示器上的触觉反馈。
    
    
    sudo apt autoremove --purge brltty
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/916b315f18a448d28220c0abd080939f.png)

再重新插拔一次USB串口转换器  
用dmesg命令查看：
    
    
    sudo dmesg | grep ch341-uart
    

ch341 uart转换器现在连接到ttyUSB0。

在/dev目录查看tty设备  
ls -l /dev/ttyUSB0

修改/dev/ ttyUSB0设备权限

sudo chmod 777 /dev/ttyUSB0

但是sudo dmesg | grep ch341-uart之后我实际跑不通。

此时的设备树上名称为：ttyCH341USB0

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d907ca29ab6547799be1f58bb93faf21.png)

