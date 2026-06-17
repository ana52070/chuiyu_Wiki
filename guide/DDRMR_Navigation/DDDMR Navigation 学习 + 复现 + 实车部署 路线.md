---
author: chuiyu
date: 2026-06-14
description: DDDMR Navigation 学习 + 复现 + 实车部署 路线
tags:
  - ROS2
  - ROS2项目
  - Mid360
---
## Context（为什么需要这份路线）

你想**系统学习并复现** DDDMR Navigation 这个 ROS2 Humble 3D 导航栈，
节奏为 **1–2 周**，以应用层为主、但要大致理解内部原理与代码框架。最终目标分三步走：

1. **学原理** → 2. **复现仿真** → 3. **部署到自己的差速车**（Xavier NX + Livox Mid360）。

硬件：笔记本 WSL2 + Docker Desktop，RTX4060 + R9-7945；嵌入式 Xavier NX + Mid360。

### 你的背景适配（基于简历，已校准）

计算机本科、强嵌入式 + 应用集成型选手，动手能力强。关键优势与对路线的影响：

| 你的优势                                             | 对路线的影响                                                            |
| ------------------------------------------------ | ----------------------------------------------------------------- |
| **C/C++ 熟练**                                     | 代码精读跳过语法讲解，直接读架构与算法，节奏加快                                          |
| **已做过 ROS2 + SLAM + 导航机器人**（国家级项目）               | 话题/服务/action/TF/launch 不复述；重点做 **2D Nav2 认知 → 3D 点云栈** 的迁移对照      |
| **YOLO + TensorRT + NPU 部署**（RK3588、YoloV8、RTSP） | lego_loam 的 **YOLO11+TRT 动态屏蔽** 是你的强项区，可深入；Xavier NX 的 TRT 部署对你不难 |
| **数学建模国一×2**                                     | 粒子滤波 / A* / MPC / GTSAM 位姿图优化 的数学**可展开细讲**，不必略过                   |
| **嵌入式 Linux / 交叉部署经验**                           | P3 实车（Xavier NX + l4t 镜像）阶段会很顺，可作为你的主战场                           |

> 一句话定位：你不是"导航新手"，而是"**对这套 3D 点云导航栈不熟、但底子很硬**"。
> 因此路线重心放在 **"这套栈相对 Nav2 的不同点 + 点云/位姿图/3D 代价地图的独有设计 + 实车迁移"**，
> 而不是 ROS2/C++/数学的基础铺垫。

> 注意：这是一份**学习路线 / 计划文档**，不是代码改动。执行阶段我会按本文件逐步带你跑命令、读代码、改配置。
> 关键发现：仓库自带一个**差速车 Gazebo 仿真**（[dddmr_x64_gazebo/src/diff_robot/](dddmr_x64_gazebo/src/diff_robot/)），
> 比 Go2 四足更接近你的目标平台，应优先用它复现。

---

## 总体策略：三阶段 + 1~2 周节奏

| 阶段             | 目标                     | 预计时间    | 产出                     |
| -------------- | ---------------------- | ------- | ---------------------- |
| **P0 环境**      | Docker 镜像 + 编译通过       | 0.5~1 天 | 能进容器、`colcon build` 成功 |
| **P1 跑通仿真**    | Go2/diff_robot 仿真导航跑起来 | 1~2 天   | RViz 里能设目标点、机器人自主到达    |
| **P2 原理+框架精读** | 按数据流读 7 个核心包           | 4~6 天   | 能讲清每个包干什么、改得动配置        |
| **P3 迁移差速车**   | Mid360 + 差速车配置 + 实车    | 3~5 天   | 自己机器人能建图+定位+导航         |

整个导航数据流（先建立全局认知，再钻细节）：
```
建图 lego_loam → 地图(PCD+位姿图) → 定位 mcl_3dl → map→odom TF
   → 感知 perception_3d(3D代价地图) → 全局规划 global_planner(点云A*)
   → 局部规划 local_planner(轨迹采样+MPC打分) → /cmd_vel
   → p2p_move_base(状态机编排全部)
```

---

## P0 — 环境准备（0.5~1 天）

> 全部在 WSL2 内执行；RTX4060 可用 CUDA 镜像跑 YOLO，但**入门先用 CPU 镜像 `dddmr:x64` 足够**。

1. 读总览，建立心智模型：
   - [dddmr_navigation/README.md](dddmr_navigation/README.md) — 它解决 Nav2 的哪些局限
   - [dddmr_navigation/src/dddmr_beginner_guide/README_CN.md](dddmr_navigation/src/dddmr_beginner_guide/README_CN.md) — 中文快速上手
2. 构建镜像（host 上跑一次，选 `x64` 与 `x64_gz`）：
   ```bash
   cd dddmr_navigation/dddmr_docker/docker_file && ./build.bash
   ```
   产出镜像：`dddmr:x64`（CPU 导航）、`dddmr_gz:x64`（Gazebo）。
3. WSLg 图形检查：确认 `echo $DISPLAY` 有值（RViz/Gazebo 要用 X11，run 脚本已挂 `/tmp`、`/dev`、`--network=host`）。
4. 下载 demo 地图：
   ```bash
   cd dddmr_navigation/src/dddmr_beginner_guide && ./download_files.bash   # 下到 ~/dddmr_bags
   ```
5. 进容器编译（symlink 安装，改 YAML 不用重编）：
   ```bash
   ./run_x64_navigation.bash                 # 启动并进入 dddmr:x64 容器
   source /opt/ros/humble/setup.bash
   cd /root/dddmr_navigation
   colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
   source install/setup.bash
   ```

**P0 验收**：`colcon build` 全绿，`ros2 pkg list | grep dddmr` 能看到包。

---

## P1 — 跑通仿真 demo（1~2 天）

需要**两个容器**（Gazebo 一个、导航栈一个）。先用官方 Go2 demo 把链路跑通，再切 diff_robot。

### 1A. Go2 四足 demo（先验证链路）
```bash
# 终端1（Gazebo 容器）：./run_x64_gazebo.bash 进入后
ros2 launch go2_config gz_lidar_odom.launch.py
# 终端2（导航容器）：source install/setup.bash 后
ros2 launch p2p_move_base go2_localization.launch
```
- 启动文件：[go2_localization.launch](dddmr_navigation/src/dddmr_p2p_move_base/launch/go2_localization.launch)
  会拉起 mcl_feature(lego_loam) / mcl_3dl / global_planner / p2p_move_base / rviz2。
- 在 RViz 用 **3D Initial Pose** 给初始位姿，再用 **3D Goal Pose** 工具设目标点。

### 1B. 切到差速车仿真（更贴近你的目标）
- 差速车仿真启动：
  [diff_robot_gazebo.launch.py](dddmr_x64_gazebo/src/diff_robot/diff_robot_gazebo/launch/diff_robot_gazebo.launch.py)
- 它发布 `/velodyne_points`(PointCloud2)、`/odom`、订阅 `/cmd_vel`，`base_link` 为基座，与导航栈接口一致。
- 这一步主要练：**话题/TF 对接** 和 **看 `ros2 topic echo / rqt_graph / tf2 view_frames`**。

**P1 验收**：能在 RViz 设目标点，机器人自主规划路径并到达；理解每个话题谁发谁收（用 `ros2 node info`、`rqt_graph` 验证）。

---

## P2 — 原理 + 代码框架精读（4~6 天）

**读法**：每个包都先看 `xxx_node.cpp`（入口，几十行）→ 主类头文件 → 核心 `.cpp`。
配合官方各包 README（每个包都有完整 demo 文档）。按数据流顺序读。

> **针对你的读法**：你已有 ROS2/SLAM 项目经验，重点不是"这是什么"，而是**"它和 Nav2 / 你做过的 2D 导航差在哪"**。
> 每读一个包，问自己三个问题：① 输入/输出点云或话题是什么？② 为什么要做成 3D 点云 / 位姿图，而不是 2D 栅格？
> ③ 这块的数学（A*/MPC/粒子滤波/GTSAM）核心思想是什么？数学你底子够，**遇到想深挖的随时叫我展开推导**。

### Day 1 — 地基 + 感知
- **dddmr_sys_core**：[base_p2p_local_planner.h](dddmr_navigation/src/dddmr_sys_core/include/dddmr_sys_core/base_p2p_local_planner.h)
  + [dddmr_enum_states.h](dddmr_navigation/src/dddmr_sys_core/include/dddmr_sys_core/dddmr_enum_states.h) — 编排器与规划器的「契约」+ 状态枚举。
- **perception_3d**（插件式 3D 代价地图，~4.9k 行）：
  入口 `src/perception_3d_node.cpp` → `include/perception_3d/perception_3d_ros.h` →
  插件基类 `sensor.h` → 看一个具体插件 [plugins/multilayer_spinning_lidar.cpp](dddmr_navigation/src/dddmr_perception_3d/plugins/multilayer_spinning_lidar.cpp)（最大、最关键）。
  概念：static/dynamic graph、marking/clearing、SpeedLimit/NoEntry 区域。

### Day 2 — 建图 lego_loam（3D LiDAR SLAM，~5.9k 行）
- 入口 `src/lego_loam_node.cpp`（44 行，3 节点流水线，用 Channel<> 做节点间 IPC）。
- 流水线：`imageProjection.cpp`(点云→距离图像、地面/物体分割) →
  `featureAssociation.cpp`(提取角点/平面特征) → `mapOptimization.cpp`(2049 行，GTSAM 位姿图优化 + 回环)。
- **YOLO11+TensorRT 屏蔽动态人体（你的强项区，建议深入）**：相关代码
  [dddmr_trt/](dddmr_navigation/src/dddmr_trt/)（TRT 封装）+ lego_loam 里 `yolo_ros2_image_sub.cpp`、
  config 里 `trt_model_path` 开关。RTX4060 上可直接玩；这套也是后面 Xavier NX 部署 TRT 的预演。

### Day 3 — 定位 mcl_3dl（3D 粒子滤波，~2.2k 行）
- 入口 `mcl_3dl_node.cpp` → `mcl_3dl.h` → `mcl_3dl.cpp`(927 行)。
- 概念：粒子滤波模板 `pf.h`、运动模型（**DifferentialDrive** 差速模型，正合你用）、
  似然测量模型 `lidar_measurement_model_likelihood.cpp`、子地图按搜索半径加载 `sub_maps.cpp`。

### Day 4 — 全局规划 global_planner（点云 A*）
- 入口 `global_planner_node.cpp` → `global_planner.h`(action server) →
  [a_star_on_pc.cpp](dddmr_navigation/src/dddmr_global_planner/src/a_star_on_pc.cpp)（点云上跑 A*，用 nanoflann KD-tree 做近邻）。
- 概念：在 3D 地面点云上建图搜索、转弯惩罚 `turning_weight`。

### Day 5 — 局部规划 local_planner（轨迹采样 + MPC 打分，~4.5k 行）
- 入口 `local_planner_node.cpp` → `local_planner.h/.cpp`（采样→打分→选最优）。
- 两套插件体系：
  - **trajectory_generators**：`dd_simple_trajectory_generator_theory.cpp`（**差速直行**）、
    `dd_rotate_inplace_theory.cpp`（原地转）。
  - **mpc_critics**：`collision_model` / `pure_pursuit_model` / `toward_global_plan_model` /
    `shortest_angle_model` / `stick_path_model` / `twirling_model`。
  - **recovery_behaviors**：`rotate_inplace_behavior`。

### Day 6 — 编排 p2p_move_base（状态机，~1.1k 行）
- 入口 `p2p_move_base_node.cpp` → `p2p_move_base.h/.cpp`(705 行) → 状态机 `p2p_fsm.cpp`。
- 概念：action server（PToP 目标）、PLAN→CONTROL→RECOVERY→SUCCEEDED/FAILED 流转、起步航向对齐。

**P2 验收**：能画出完整数据流图、说清每个包的输入/输出话题与职责；能定位「改速度上限 / 改机器人尺寸」要动哪个 YAML 段。

---

## P3 — 迁移到差速车（Mid360 + Xavier NX，3~5 天）

核心是**复制一份配置并替换硬件相关参数**，无需改 C++ 源码。

### 3.1 复制并改导航配置
基于 [go2_localization.yaml](dddmr_navigation/src/dddmr_p2p_move_base/config/go2_localization.yaml) 复制一份 `mycar_localization.yaml`，重点改：

- **Lidar 规格（`lego_loam_ip.laser`）→ 按 Mid360 改**（参考
  [loam_bag_mid360_config.yaml](dddmr_navigation/src/dddmr_lego_loam/lego_loam_bor/config/loam_bag_mid360_config.yaml)）：
  ```yaml
  num_vertical_scans: 32
  num_horizontal_scans: 1000
  vertical_angle_bottom: -7.0      # Mid360 竖直 FOV
  vertical_angle_top: 52.0
  stitcher_num: 3                  # 关键！非旋转/非重复扫描雷达用 2~4（旋转雷达=0）
  odom_type: "wheel_odometry"      # 差速车有轮速里程计就用它
  ```
- **机器人足迹立方体（cuboid，8 顶点）** 按实车尺寸量取改写（flb/frb/flt/frt/blb/brb/blt/brt）。
- **速度/角速度上限**（`local_planner` / `trajectory_generators`：`max_vel_x`、`max_vel_theta`、`wheel_diameter`）。
- **地图路径**（`sub_maps.pose_graph_dir`）指向你自己建的图目录。
- **话题 remap**：把 `/lslidar_point_cloud`→你的 Mid360 点云话题（launch 文件里改 remap）。

### 3.2 实车接口要求（你的差速车必须提供）
- `/cmd_vel`（geometry_msgs/Twist，linear.x + angular.z）
- `/odom`（nav_msgs/Odometry，`odom→base_link` TF，≥10Hz）
- Mid360 点云（sensor_msgs/PointCloud2）
- TF 树：`map→odom→base_link→{mid360_link, base_footprint}`（静态 TF 按 CAD/实测发布）

### 3.3 建图 → 定位 → 导航（实车流程）
```bash
# 建图（在线）：ros2 launch lego_loam_bor lego_loam.launch   → 存出 PCD 地图
# 或离线从 bag：ros2 launch lego_loam_bor lego_loam_bag.launch
# 定位+导航：     ros2 launch p2p_move_base p2p_move_base_localization.launch
```
Xavier NX 上用 `dddmr:l4t_r36` 镜像（`build.bash` 选 l4t）。

**P3 验收**：实车能建出地图 PCD、MCL 定位收敛（map→odom 稳定）、RViz 设点能自主导航。

---

## 学习方法建议（贯穿全程）

- **边跑边读**：每读一个包，就在仿真里 `ros2 topic echo` 它的输入输出、用 RViz 看可视化，把代码和现象对上。
- **善用 `--symlink-install`**：改 YAML 立即生效，适合做「改参数看效果」的实验。
- **不必逐行抠数学**：A*/MPC/粒子滤波 先理解「输入→输出→为什么」，数学细节按需深入（符合你应用层为主的定位）。
- **遇到卡点随时问我**：包括编译报错、WSLg 黑屏、TF 不通、Mid360 点云对接等，我可以带你逐个排查。

---

## 验证 / 里程碑清单

- [ ] P0：镜像构建成功 + `colcon build` 全绿
- [ ] P1：Go2 demo 在 RViz 能设点自主导航；diff_robot 仿真话题/TF 对通
- [ ] P2：能口述完整数据流 + 每个包职责；能改一处配置并观察到效果
- [ ] P3：Mid360 + 差速车配置完成；实车建图/定位/导航跑通

---

## 节奏建议（基于你的背景，1~2 周可达）

- **第 1 周**：P0（0.5 天）+ P1（1.5 天）+ P2 前半（感知/建图/定位，约 3 天）。周末能在仿真里设点导航 + 看懂前 4 个包。
- **第 2 周**：P2 后半（全局/局部/编排，约 2 天）+ P3（Mid360 配置 + Xavier NX 部署 + 实车建图导航，约 3 天）。
- **你的主战场在 P3**：嵌入式部署是你强项，预留更多时间打磨实车（TF 标定、Mid360 点云对接、TRT 在 NX 上跑通）。
- **可选加深**（数学建模国一，余力可挖）：GTSAM 位姿图优化的因子图推导、MCL 粒子重采样、MPC critic 加权打分——这些都可叫我单独展开。
