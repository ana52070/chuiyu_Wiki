---
title: 'carplanning_code'
date: '2026-03-23 13:57:06'
categories:
  - '软件项目'
tags:
  - 'GitHub'
permalink: '/projects/carplanning-code'
repo: 'ana52070/carplanning_code'
description: '暂无描述'
homepage: ''
stars: 1
language: 'Python'
license: ''
created_at: '2026-03-19T02:27:58Z'
updated_at: '2026-03-19T03:06:43Z'
topics:
  - '暂无'
---

# carplanning_code

- 仓库：[https://github.com/ana52070/carplanning_code](https://github.com/ana52070/carplanning_code)
- Star：1
- 主语言：Python
- README 来源：`README.md` (分支：`simulation`)

---

# campus_nav

基于 RTK 的校园无图自主导航系统（仿真阶段）

## 环境要求

- Ubuntu 22.04
- ROS2 Humble
- Gazebo Classic 11

## 依赖安装
```bash
sudo apt install -y \
  ros-humble-turtlebot3 \
  ros-humble-turtlebot3-simulations \
  ros-humble-turtlebot3-gazebo \
  ros-humble-robot-localization \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup
```

## 编译
```bash
cd ~/your_ws
colcon build --packages-select campus_nav
source install/setup.bash
```

## 启动
```bash
# 设置机器人型号
export TURTLEBOT3_MODEL=waffle

# 一键启动全部（仿真+定位+Nav2+Rviz）
ros2 launch campus_nav bringup.launch.py
```

等待约 10 秒所有节点启动完毕，在 Rviz 中点击 **Nav2 Goal** 设置目标点即可导航。

## 系统架构
```
GPS仿真插件 (/gps/fix)
    ↓
navsat_transform_node
    ↓
/odometry/gps ──┐
/odom          ─┼→ EKF → /odometry/filtered → map→odom TF
/imu           ─┘
                        ↓
/scan → Nav2 costmap → 路径规划 → /cmd_vel → 底盘
```

## 文件结构
```
campus_nav/
├── config/
│   ├── ekf.yaml          # EKF 融合参数
│   ├── navsat.yaml       # GPS 坐标转换参数
│   └── nav2_params.yaml  # Nav2 导航参数
├── launch/
│   ├── bringup.launch.py # 一键启动（推荐）
│   ├── sim.launch.py     # 仅启动仿真
│   ├── localization.launch.py
│   └── nav2.launch.py
├── urdf/
│   └── turtlebot3_waffle.urdf  # 加入GPS插件的URDF
├── models/
│   └── turtlebot3_waffle/
│       ├── model.sdf     # 加入GPS传感器的SDF
│       └── model.config
└── worlds/
    └── turtlebot3_world.world  # 设置天津坐标参考点的世界文件
```

## 硬件迁移计划

仿真阶段话题对应真实硬件：

| 仿真话题 | 真实硬件来源 |
|---------|------------|
| `/gps/fix` | UM982 RTK 驱动 |
| `/scan` | Mid-360 + pointcloud_to_laserscan |
| `/odom` | 底盘编码器驱动 |
| `/imu` | 底盘 IMU |
| `/cmd_vel` | 底盘驱动 |
