---
title: 安卓开发 Gradle下载网络问题解决方法
date: 最新推荐文章于 2025-02-26
tags: [CSDN搬运]
---

# 安卓开发 Gradle下载网络问题解决方法

> 原文链接：[安卓开发 Gradle下载网络问题解决方法](https://blog.csdn.net/chui_yu666/article/details/145516497)

## 

在进行安卓开发时检测会遇到Gradle包下载不了的问题，因此在这里建议手动下载，速度会快非常多，再也不用担心Gradle的问题了。具体操作方法如下：

### 1.确定下载gradle包版本，一般来说以报错为准：

![](https://i-blog.csdnimg.cn/direct/58aad4d33e4d4a3095d4452517641708.png)

### 2.去国内镜像网站下载对应的Gradle包：

网站链接：[Index of /gradle/](<https://mirrors.cloud.tencent.com/gradle/> "Index of /gradle/")

![img](https://i-blog.csdnimg.cn/blog_migrate/9bb32f5886e60405ad6b55b42e32a93d.png)

不需要慢慢翻，直接Ctrl+F搜索就行：![](https://i-blog.csdnimg.cn/direct/c6b8293e7efa4817abace14a00cdebcb.png)

下载

![](https://i-blog.csdnimg.cn/direct/ee41db319cab40b5b4dfd2242114e076.png)

下载完成后，将该压缩包移动至：
    
    
     C:\Users\用户名\.gradle\wrapper\dists

注意，将用户名替换为自己的用户名，例如我的为：
    
    
     C:\Users\ting_yu\.gradle\wrapper\dists

![](https://i-blog.csdnimg.cn/direct/8b873995005740a69e9956aacc6b33cf.png)

找到刚刚要下载的包的文件夹，进去之后再进入一个随机编码的文件夹内，例如我的为：
    
    
     C:\Users\ting_yu\.gradle\wrapper\dists\gradle-7.2-bin\2dnblmf4td7x66yl1d74lt32g![](https://i-blog.csdnimg.cn/direct/0bf9e661e9e049a0923085e96a3e6d4d.png)

将压缩包放置在此，并解压，结果如下图：

![](https://i-blog.csdnimg.cn/direct/96619a4afad64bab9d22cfc106dbb73c.png)

### 3.重新编译

![](https://i-blog.csdnimg.cn/direct/2264f1b081a045c8a4aa691c2033e5dc.png)

这样，手动安装Gradle就完成了

