---
categories:
- 单片机
date: 于 2025-06-12
tags:
- 单片机
title: JY901-ROS2驱动代码
permalink: /blog/单片机/JY901-ROS2驱动代码
---

# JY901-ROS2驱动代码

> 原文链接：[JY901-ROS2驱动代码](https://blog.csdn.net/chui_yu666/article/details/148605988)

## JY901-ROS2驱动代码

### 驱动包

该驱动代码修改自：
    
    
    https://github.com/ioio2995/witmotion_ros2
    
    
    
    git clone https://github.com/ana52070/jy901_for_ros2.git
    

下载后放入到自己的ubuntu中
    
    
    sudo apt-get install libasio-dev
    
    cd jy901_for_ros2
    
    colcon build
    
    source install/setup.bash
    
    ros2 launch witmotion_ros2 witmotion_launch.py
    

这样，雷达驱动就已经运行起来了。

如果报错，可以查看是否为配置不对：
    
    
     sudo vim src/witmotion_ros2/config/witmotion.yaml 
    
    
    
    witmotion_node:
      ros__parameters:
        port: /dev/ttyUSB1
        baud_rate: 115200 # baud
        update_rate: 50.0 # Hz
        topic_name: /witmotion
        frame_id: base_link
        imu_linear_acceleration_covariance: [0.0364, 0.0, 0.0, 0.0, 0.0048, 0.0, 0.0, 0.0, 0.0796]
        imu_angular_velocity_covariance: [0.0663, 0.0, 0.0, 0.0, 0.1453, 0.0, 0.0, 0.0, 0.0378]
        imu_orientation_covariance: [0.0479, 0.0, 0.0, 0.0, 0.0207, 0.0, 0.0, 0.0, 0.0041]
        imu_temperature_variance: 0.01829
        magnetometer_covariance: [0.000000187123, 0.0, 0.0, 0.0, 0.000000105373, 0.0, 0.0, 0.0, 0.000000165816]
        magnetometer_temperature_variance: 0.01829
        barometer_variance: 0.001
    

如果USB不对，请检查设备树中USB的名称，如果CH340未安装可参考：  
https://blog.csdn.net/chui_yu666/article/details/148385694?fromshare=blogdetail&sharetype=blogdetail&sharerId=148385694&sharerefer=PC&sharesource=chui_yu666&sharefrom=from_link

### RVIZ2查看

首先安装imu插件
    
    
    sudo apt install ros-ROS_DISTRO-rviz-imu-plugin
    

然后启动rviz
    
    
    rviz2
    

点击add

找到下面的imu

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/4d5266570f2740a586600ad6d6858ee8.png)

然后选择好对应的话题就可以了

最终效果：

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f31bc97d27ac49cdad5e511498985210.png)

