---
title: EMQX开源版安装指南：Linux/Windows全攻略
date: 最新推荐文章于 2025-12-17
tags: [CSDN搬运]
---

# EMQX开源版安装指南：Linux/Windows全攻略

> 原文链接：[EMQX开源版安装指南：Linux/Windows全攻略](https://blog.csdn.net/chui_yu666/article/details/148051234)

## EMQX开源版安装教程-linux/windows

因最近自己需要使用MQTT，需要搭建一个MQTT服务器，所以想到了很久以前用到的EMQX。但是当时的EMQX使用的是开源版的，在官网可以直接下载。而现在再次打开官网时发现怎么也找不大开源版本了，所以便在网上找了很久资源，网上的安装教程都是之前的那种官网截图，所以自己找到了资源以后重新梳理一遍现在的EMQX开源版安装教程。

这里主要演示Linux版本，Windows版本可在这里下载到对应的安装包以后参考以前的资料进行安装及配置。

系统:Ubuntu 22.04LTS

### 下载

1.首先使用浏览器打开链接：  
https://www.emqx.com/zh/downloads/broker/

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/6960d4836c1d4c32967792b90947c003.png)

然后选择自己想要下载的版本，我这里以最新版5.8.6为例，点击5.8.6之后，按照自己的系统等信息选择对应的安装包

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/5df009b9e97348f9b277c6346db80c47.png)

例如我这里的系统是amd64的ubuntu22.04所以我选择了：

  * [emqx-5.8.6-ubuntu22.04-amd64.deb](<https://www.emqx.com/zh/downloads/broker/v5.8.6/emqx-5.8.6-ubuntu22.04-amd64.deb>)



![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/50022a2538aa4df3bcb651eb6529ed2f.png)

然后去到linux环境下：

使用指令wget + 粘贴
    
    
    wget https://www.emqx.com/zh/downloads/broker/v5.8.6/emqx-5.8.6-ubuntu22.04-amd64.deb
    

等待下载完成：

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/5ae1bf9b26a24fc4bebe05834a5ca24d.png)

### 2.安装

**1.安装依赖**
    
    
    sudo apt update
    sudo apt upgrade
    sudo apt install -y libssl-dev
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8089760184f74a3d8c65b20af4df22c5.png)

**2.安装deb包**

使用 `dpkg` 工具安装下载好的文件（需替换为实际下载路径）：
    
    
    sudo dpkg -i emqx-5.8.6-ubuntu22.04-amd64.deb
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9c8470161a284b6d902f2d6dd1f51366.png)

### 3.启动
    
    
    # 启动服务
    sudo systemctl start emqx
    
    # 检查服务状态（确保显示 "active (running)"）
    sudo systemctl status emqx
    

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/bd8bac4b99ca4262b433b7f91e40d2a6.png)

### 4\. 验证安装

访问 EMQ X 管理控制台（默认端口 `18083`）：

  * 浏览器输入：`http://localhost:18083`
  * 默认账号 / 密码：`admin/public`



![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/95da560a7bd146de81cf2b10489c91b1.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/de0c5119ede34954bf50b168d1f830a1.png)

#### **其他操作命令**

操作| 命令  
---|---  
停止服务| `sudo systemctl stop emqx`  
重启服务| `sudo systemctl restart emqx`  
开机自启| `sudo systemctl enable emqx`  
查看日志| `sudo journalctl -u emqx`  
  
  * 若需卸载，可运行：`sudo dpkg -r emqx`。



