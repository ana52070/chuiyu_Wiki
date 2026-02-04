---
title: Pytorch 手动安装教程 【超快|适用于国内没有源的方法】
date: 已于 2025-02-08
tags: [CSDN搬运]
---

# Pytorch 手动安装教程 【超快|适用于国内没有源的方法】

> 原文链接：[Pytorch 手动安装教程 【超快|适用于国内没有源的方法】](https://blog.csdn.net/chui_yu666/article/details/145516315)

## 0.起因

本人在学习yolov5的时候，因为v5所需要的torch版本较低，楼主需要安装pytorch1.8.1的版本，但国内的清华源、阿里源等都没有这么低的版本的资源了，因此只能使用torch官方的源来安装，可官方源非常慢而且经常会断连。无奈之下只能寻找其它安装方案，因此便有了手动安装的方案。

这个方案是使用迅雷的p2p下载+手动pip安装，速度比直接使用国内源还快，不过就是稍微麻烦了一点点。

## 1.确定需要下载的torch版本

这里以torch1.8.1为例：

![](https://i-blog.csdnimg.cn/direct/665fe2c05fd44d71894cd30ca616c4b8.png)

一般安装方法：
    
    
     pip install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html

使用官方源安装，但是速度非常慢而且会断连因此不推荐。

![](https://i-blog.csdnimg.cn/direct/abd69db2ee984870b33d2bb9a471f2d8.png)这里就确定了torch版本以及下载地址。

## 2.找到需要下载的whl的直链地址

[download.pytorch.org/whl/torch_stable.html](<https://download.pytorch.org/whl/torch_stable.html> "download.pytorch.org/whl/torch_stable.html")

去上面这个链接里，找到需要下载的包，这个包在上面官方源下载的时候有提到名字：

![](https://i-blog.csdnimg.cn/direct/33b3e61915224b5f8130100617256dcb.png)

然后去网站里搜索这个名字，使用Ctrl+F搜索即可：

![](https://i-blog.csdnimg.cn/direct/60abcd534caa4688a3d0046d821cae25.png)

然后鼠标右击复制链接：

![](https://i-blog.csdnimg.cn/direct/291a651105224db7a0861ac6cf84654e.png)

## 3.使用迅雷P2P下载

迅雷下载链接，安装教程这里就省略了，注意安装完成以后的exe文件在：
    
    
     选择的安装地址\Thunder\Program\Thunder.exe

通过网盘分享的文件：迅雷v11.1.12.1692.rar 链接: [百度网盘 请输入提取码](<https://pan.baidu.com/s/19ErAI87te8I6BgYoqARIKg?pwd=7tyf> "百度网盘 请输入提取码") 提取码: 7tyf

注意：不要使用官方版，官方版限不限速不说，楼主亲测会阻止下载torch包，提示非法，估计是因为torch包的官方源在国外吧。

打开迅雷，点击新建：

![](https://i-blog.csdnimg.cn/direct/017e778bf824425fb55d6c3aaca4f9ae.png)

把刚才的链接粘贴过来，然后点击确定： ![](https://i-blog.csdnimg.cn/direct/9a08cd58bef540d899733810a0554a89.png)

选择下载地址，然后点击立即下载。![](https://i-blog.csdnimg.cn/direct/32c321ebd4e548ffb29d8f749d99e7cf.png)

这样，迅雷就会开始下载了，网速越快，下载越快，根本不限速，而且P2P的方式比传统下载方式会快很多。

![](https://i-blog.csdnimg.cn/direct/3dcf872322e248f8ba904db1c7541424.png)

下载完成后，在命令行里输入：
    
    
     pip install 要安装的包的路径

例如我这里是：
    
    
     pip install D:\下载\torch-1.8.1+cu111-cp38-cp38-win_amd64.whl![](https://i-blog.csdnimg.cn/direct/4b4fb96cd15d40abaafed2063ac2e150.png)

然后，pip就会自己安装并且检查没有安装的依赖了。![](https://i-blog.csdnimg.cn/direct/003db67521654818bcc6844c322fa730.png)

到这里，torch就安装完毕了，剩下的torchaudio、torchvision包都不算很大，如果嫌麻烦的话可以直接使用官方下载的命令来继续安装了，如果想更快的话就使用同样的方式找到需要安装的torchaudio、torchvision的具体包名使用迅雷下载后手动安装。不过在这里还是建议直接使用官方源来直装会方便很多。
    
    
     pip install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html

这样，pip会自动检查已安装的包和未安装的包，未安装的包会自动安装。![](https://i-blog.csdnimg.cn/direct/59cd1f825ece44c699e410b60593f752.png)

## 4.检查是否安装完成

进入python环境，运行以下代码，若成功导入torch，显示torch版本以及是否支持cuda为True则安装成功。
    
    
     import torch
     ​
     # 查看torch版本
     print("PyTorch版本:", torch.__version__)
     ​
     # 检查是否支持CUDA
     if torch.cuda.is_available():
         print("CUDA可用")
         print("CUDA版本:", torch.version.cuda)
         print("可用的GPU数量:", torch.cuda.device_count())
         print("当前使用的GPU设备索引:", torch.cuda.current_device())
         print("GPU设备名称:", torch.cuda.get_device_name(torch.cuda.current_device()))
     else:
         print("CUDA不可用")

我这里直接用命令行了： ![](https://i-blog.csdnimg.cn/direct/d9d2e49938f64421ba5751515a19002e.png)

至此，Pytorch手动安装完成。

参考链接：  
[如何下载torch1.8.1和cu111_torch==1.8.1+cu111-CSDN博客](<https://blog.csdn.net/qq_51907153/article/details/142819451> "如何下载torch1.8.1和cu111_torch==1.8.1+cu111-CSDN博客")

