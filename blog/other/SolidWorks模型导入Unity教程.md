---
categories:
- other
date: 于 2025-03-02
tags:
- other
title: SolidWorks模型导入Unity教程
permalink: /blog/other/SolidWorks模型导入Unity教程
---

# SolidWorks模型导入Unity教程

> 原文链接：[SolidWorks模型导入Unity教程](https://blog.csdn.net/chui_yu666/article/details/145968550)

## 前言

由于项目需求，要将SolidWorks中绘制的3D装配体模型导入到Unity当中，但在网上并未找到比较好的图文模型，对于此需求都只是提一嘴而已。因此这里将自己找到的教程进行汇总解析。

SW导入Unity有两种方法，其中两种方法都需要到另外的第三款软件。这里先介绍第一种方法，后续会更新第二种方法。

第一种方法是使用Blender软件进行STL转FBX，优点是Blender软件小，导入简单，缺点是会丢失材质颜色，适用于不需要颜色的情况

第二种方法是使用3Dmax，优点是不会丢失材质和颜色，缺点是麻烦，3Dmax的软件较大。

## 第一种方法：Blender

对于Blender、SolidWorks、Unity的下载工作这里就不介绍了，有需要的可自行上网查找方法。

### SolidWorks导出STL

#### 0.装配体导出为单个STL的准备工作

首先，如果你需要导入的最终的模型是一个单一零件的话，那么就可以跳过这一步。如果是装配体的话，则需要进行这一步操作。

sw装配体直接转换成[stl](<https://so.csdn.net/so/search?q=stl&spm=1001.2101.3001.7020> "stl")文件，会生成贼多的小stl文件

有一个办法，把装配体.sldasm文件打开然后转换成.sldprt文件（就是普通零件格式），再把.sldprt文件转换成.stl文件，就是一个整体stl

首先打开装配体文件![](https://i-blog.csdnimg.cn/direct/a31009d4ee6f4794ab458373870758c6.png)

然后将其另存为.sldprt文件（就是普通零件格式）

![](https://i-blog.csdnimg.cn/direct/9a05f5bb85eb4bcb9dd06f8e22577664.png)![](https://i-blog.csdnimg.cn/direct/0478499058594cf9abbb0b53de87868a.png)

保存![](https://i-blog.csdnimg.cn/direct/24af2cec22f44bd491d456699c8e7e74.png)

然后打开这个另存为的.sldprt文件进行下一步的导出STL操作。

#### 1.导出STL![](https://i-blog.csdnimg.cn/direct/a81e27d0ca8a440abdf290d01a8397b5.png)

导出为STL并保存![](https://i-blog.csdnimg.cn/direct/07c941a6f3544bba98f7378d1c261d64.png)

### Blender导出FBX

打开Blender![](https://i-blog.csdnimg.cn/direct/abdcbda455924cf6a41b727b8ddc7dab.png)

然后删除常规自动生成的正方体![](https://i-blog.csdnimg.cn/direct/8de5292073f544f88a56d8ec056e3303.png)

然后导入刚刚生成的STL文件![](https://i-blog.csdnimg.cn/direct/edc9a9a3def648d9b0d33841f667789f.png)![](https://i-blog.csdnimg.cn/direct/90976c9437f14a919da0acacdcb30b86.png)

紧接着就可以直接导出为FBX格式了： ![](https://i-blog.csdnimg.cn/direct/e8469461301744d196b867eb66ca70ae.png)

选择导出网格，导出![](https://i-blog.csdnimg.cn/direct/8d0699717963446da7d29f0d9c784923.png)

### Unity导入FBX

首先打开Unity工程，再打开刚刚导出的FBX文件![](https://i-blog.csdnimg.cn/direct/a66bc813a82b4fd08e26c5f4da2fe038.png)

然后直接将FBX文件使用鼠标拖入到Unity当中![](https://i-blog.csdnimg.cn/direct/f0f02ec416ed428082ad5dc5a31cabc9.png)

再把模型拖入到场景中![](https://i-blog.csdnimg.cn/direct/8abf1d658f4d41ee988fdccba54decbb.png)

最后，调整一下模型的方向![](https://i-blog.csdnimg.cn/direct/eaf8083e6ae147789d572071a32d34c0.png)

这样，从SolidWorks导入模型到Unity当中就成功了。

## 第二种方法：3Dmax(推荐)

### SolidWorks导出Step

首先打开装配体/零件文件![](https://i-blog.csdnimg.cn/direct/92bc7f214d244678b13872b3deef7ce0.png)

然后将其另存为.step

注意有两个.step，选择下面那个214![](https://i-blog.csdnimg.cn/direct/c2fc7863f80045c1b4344f606195bc93.png)

然后点击选项，将配置改为和我的一样的： ![](https://i-blog.csdnimg.cn/direct/e2ea4f10989c444184e88cf94381dc4f.png)![](https://i-blog.csdnimg.cn/direct/ac71c78562fa4665a58241bbf3db1925.png)

### 3Dmax导出

打开3Dmax![](https://i-blog.csdnimg.cn/direct/cfe03cdb978b4ba29257902eb24d0ae7.png)

首先设置单位为mm![](https://i-blog.csdnimg.cn/direct/c140c4bf000f471cab6dacbd4f2bed42.png)![](https://i-blog.csdnimg.cn/direct/c64eb6dcdde048f893df1af8308f9fe3.png)

然后导入刚刚生成的STEP文件![](https://i-blog.csdnimg.cn/direct/afcca7e08dc247e6aea3224253f09730.png)![](https://i-blog.csdnimg.cn/direct/825fa54cfac14d39b61ae9cf0450a3a1.png)

配置改为和我一样的： ![](https://i-blog.csdnimg.cn/direct/b96cf4d120de461d9a41a14c17790f72.png)

模型较大的话可能会有点卡有加载现象，稍等即可：![](https://i-blog.csdnimg.cn/direct/b04c256f88bf4d5eb15edf32b536bb79.png)![](https://i-blog.csdnimg.cn/direct/cf512c600b6f48efb6cbe845d49dcbca.png)

然后进行导出FBX操作：![](https://i-blog.csdnimg.cn/direct/51679fd99ec04544b8ec875fc691f97a.png)![](https://i-blog.csdnimg.cn/direct/72b40179ad1a4658b4519ab65d273a0a.png)![](https://i-blog.csdnimg.cn/direct/b09bf96675474d2f8a4c95b8fcc99360.png)

到这里导出就完成了。

### Unity导入FBX

首先打开Unity工程和刚刚导出的fbx文件![](https://i-blog.csdnimg.cn/direct/f33a88384fb1438abb59f687145cb96f.png)

然后直接将fbx文件拖入至unity工程中即可![](https://i-blog.csdnimg.cn/direct/c8ea83e31a7c4d4abc8d2b3c66332ff8.png)

