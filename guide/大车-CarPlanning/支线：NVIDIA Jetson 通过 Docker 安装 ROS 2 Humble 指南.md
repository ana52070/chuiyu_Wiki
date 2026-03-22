---
author: chuiyu
date: 2026-03-22
description: 支线：NVIDIA Jetson 通过 Docker 安装 ROS 2 Humble 指南
tags:
  - 大车-CarPlanning
  - ROS2
  - Linux
---


> **适用平台**：NVIDIA Jetson Xavier NX / AGX Xavier / Orin 系列（JetPack 5.x，L4T R35.x）
> 
> **前置条件**：已通过 SDK Manager 刷好 JetPack 5.x 系统（Ubuntu 20.04），板卡可正常联网
> 
> **为什么用 Docker？** ROS 2 Humble 官方仅支持 Ubuntu 22.04，而 JetPack 5.x 的 Xavier 系列设备只能运行 Ubuntu 20.04。Docker 容器方案可以在不更换系统的前提下获得完整的 ROS 2 Humble 环境，同时保留 GPU 加速能力。

---

## 一、安装 Docker

JetPack 5.x 默认不一定预装 Docker，需要手动安装：

```bash
sudo apt update
sudo apt install -y docker.io
```

安装完成后启动 Docker 并设置开机自启：

```bash
sudo systemctl enable --now docker
```

将当前用户加入 `docker` 组，避免每次都要 `sudo`：

```bash
sudo usermod -aG docker $USER
```

**执行完后需要重新登录（或重启）才能生效。** 重新登录后验证：

```bash
docker info | grep -i runtime
```

此时输出中应该能看到 `runc`，但还没有 `nvidia`，下一步配置。

---

## 二、安装并配置 NVIDIA Container Runtime

### 2.1 安装 nvidia-container-runtime

```bash
sudo apt install -y nvidia-container-runtime
```

### 2.2 配置 Docker 使用 NVIDIA Runtime

编辑（或创建）Docker 的配置文件 `/etc/docker/daemon.json`：

```bash
sudo tee /etc/docker/daemon.json <<'EOF'
{
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    }
}
EOF
```

重启 Docker 使配置生效：

```bash
sudo systemctl restart docker
```

验证 NVIDIA Runtime 是否注册成功：

```bash
docker info | grep -i runtime
```

预期输出（应同时包含 `nvidia` 和 `runc`）：

```
 Runtimes: io.containerd.runc.v2 nvidia runc
 Default Runtime: runc
```

---

## 三、配置国内镜像加速（可选但推荐）

Docker Hub 在国内直连速度较慢，建议配置镜像加速器。编辑 `/etc/docker/daemon.json`，在已有配置基础上添加 `registry-mirrors` 字段：

```bash
sudo tee /etc/docker/daemon.json <<'EOF'
{
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    },
    "registry-mirrors": [
        "https://docker.1ms.run",
        "https://docker.xuanyuan.me"
    ]
}
EOF
```

重启 Docker：

```bash
sudo systemctl restart docker
```

> **注意**：国内镜像加速器的可用性经常变化。如果上述地址失效，可搜索"Docker 国内镜像加速 2026"获取最新可用地址，替换 `registry-mirrors` 数组中的 URL 即可。

---

## 四、确认 L4T 版本

在拉取镜像之前，需要确认你的 L4T 版本，以选择对应的镜像 tag：

```bash
cat /etc/nv_tegra_release
```

示例输出：

```
# R35 (release), REVISION: 6.4, GCID: 43803471, BOARD: t186ref, EABI: aarch64, ...
```

其中 `R35` 和 `REVISION: 6.4` 表示 L4T 版本为 **R35.6.4**。

也可以通过以下命令确认：

```bash
dpkg -l | grep nvidia-l4t-core
```

---

## 五、拉取 ROS 2 Humble 镜像

NVIDIA 的 Dustin Franklin 维护了一套 Jetson 专用的 ROS Docker 镜像，已集成 CUDA 支持。

### 5.1 选择镜像

镜像仓库地址：[dustynv/ros - Docker Hub](https://hub.docker.com/r/dustynv/ros/tags)

常用镜像 tag 对照：

|镜像 Tag|内容|体积|
|---|---|---|
|`humble-ros-base-l4t-r35.4.1`|ROS 2 Humble 基础包（无 GUI）|较小|
|`humble-desktop-l4t-r35.4.1`|含 rviz2、rqt 等桌面工具|较大（约 7GB+）|

> **关于 L4T 版本兼容性**：预构建镜像最高到 R35.4.1，但 R35.x 系列向下兼容，R35.4.1 的镜像可以在 R35.6.x 上正常运行。

### 5.2 拉取镜像

```bash
# 完整桌面版（含 rviz2、rqt 等 GUI 工具）
docker pull dustynv/ros:humble-desktop-l4t-r35.4.1

# 或者只拉基础版（体积更小，适合不需要 GUI 的场景）
docker pull dustynv/ros:humble-ros-base-l4t-r35.4.1
```

> **磁盘空间提醒**：desktop 版镜像解压后占用约 10GB 以上空间，请确保系统盘有足够的剩余空间。如果根分区在 eMMC（通常只有 16GB），建议先将系统迁移到外部 NVMe/SD 卡后再拉取。

---

## 六、启动容器

### 6.1 首次创建并运行容器

```bash
docker run --runtime nvidia -it \
    --name ros2_humble \
    --network=host \
    --privileged \
    -v /dev:/dev \
    -v ~/ros2_ws:/ros2_ws \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY=$DISPLAY \
    -e ROS_DOMAIN_ID=0 \
    dustynv/ros:humble-desktop-l4t-r35.4.1
```

### 6.2 启动参数详解

|参数|作用|
|---|---|
|`--runtime nvidia`|使用 NVIDIA 容器运行时，让容器能访问 GPU 和 CUDA。不加则容器内无法使用 GPU|
|`-it`|`-i`（保持标准输入打开）+ `-t`（分配伪终端），两者合用才能在容器内正常交互|
|`--name ros2_humble`|给容器命名，便于后续通过名称管理。不加则 Docker 会随机生成名称|
|`--network=host`|容器直接使用宿主机网络栈，不做网络隔离。**ROS 2 的 DDS 通信依赖组播发现机制，必须使用 host 网络**，否则多节点之间无法互相发现|
|`--privileged`|赋予容器几乎所有内核权限，允许访问宿主机设备。安全性有牺牲，但访问硬件设备时必须开启|
|`-v /dev:/dev`|将宿主机 `/dev` 挂载到容器内，使容器能访问串口（`/dev/ttyUSB0`、`/dev/ttyACM0`）、USB 摄像头（`/dev/video*`）、LiDAR 等硬件设备。需配合 `--privileged` 使用|
|`-v ~/ros2_ws:/ros2_ws`|将宿主机的工作空间目录挂载到容器内，**双向同步**——容器内编译的产物宿主机也能看到，宿主机上修改的代码容器内立刻生效。容器删除后数据不会丢失|
|`-v /tmp/.X11-unix:/tmp/.X11-unix`|挂载 X11 的 Unix socket，让容器内的 GUI 程序（rviz2、rqt 等）能通过宿主机的 X Server 显示窗口|
|`-e DISPLAY=$DISPLAY`|传递显示环境变量，告诉 GUI 程序往哪个显示器输出。如果 GUI 打不开，先在宿主机执行 `xhost +local:docker`|
|`-e ROS_DOMAIN_ID=0`|设置 ROS 2 的 Domain ID，相同 ID 的节点才能互相发现。默认为 0，多套 ROS 2 系统共存时用不同数字隔离|

### 6.3 验证环境

进入容器后：

```bash
# 镜像通常已自动 source，如果提示找不到 ros2 命令则手动执行
source /opt/ros/humble/setup.bash

# 验证 ROS 2 是否正常
ros2 topic list
```

预期输出：

```
/parameter_events
/rosout
```

看到以上输出即表示 ROS 2 Humble 环境已就绪。

---

## 七、日常使用

### 7.1 退出容器

在容器内输入 `exit` 或按 `Ctrl+D` 即可退出。由于创建时使用了 `--name` 且没有加 `--rm`，容器退出后不会被删除。

### 7.2 重新进入已有容器

```bash
docker start -ai ros2_humble
```

无需重新 `docker run`，之前在容器内安装的包和修改都还在。

### 7.3 在另一个终端进入同一容器

如果容器正在运行，想开第二个终端窗口：

```bash
docker exec -it ros2_humble bash
```

进入后记得 source ROS 2 环境：

```bash
source /opt/ros/humble/setup.bash
```

### 7.4 查看容器状态

```bash
# 查看正在运行的容器
docker ps

# 查看所有容器（包括已停止的）
docker ps -a
```

### 7.5 删除容器（谨慎操作）

```bash
docker rm ros2_humble
```

删除后容器内安装的包会丢失，但通过 `-v` 挂载的目录（如 `~/ros2_ws`）中的文件不受影响。

---

## 八、常见问题

### Q1: GUI 程序报错 `cannot open display`

在**宿主机**（不是容器内）执行：

```bash
xhost +local:docker
```

如果需要开机自动生效，可将此命令加入 `~/.bashrc`。

### Q2: 容器内看不到串口设备

确认启动时加了 `--privileged` 和 `-v /dev:/dev`。如果设备是在容器启动后才插入的，需要退出容器重新启动。

### Q3: ROS 2 节点之间无法通信

检查是否使用了 `--network=host`。另外确认所有节点的 `ROS_DOMAIN_ID` 一致。

### Q4: 拉取镜像速度很慢或超时

确认已配置国内镜像加速（见第三节）。如果加速器失效，可尝试更换其他加速地址。

### Q5: 磁盘空间不足

desktop 版镜像较大，如果根分区空间不够，可以考虑使用 `humble-ros-base` 版本，或将 Docker 数据目录迁移到外部存储。

---

## 参考资料

- [dustynv/ros Docker Hub](https://hub.docker.com/r/dustynv/ros/tags) — Jetson 专用 ROS 镜像仓库
- [dusty-nv/jetson-containers GitHub](https://github.com/dusty-nv/jetson-containers) — Jetson 容器构建工具
- [ROS 2 Humble 官方文档](https://docs.ros.org/en/humble/) — ROS 2 Humble 使用文档
- [NVIDIA JetPack 文档](https://docs.nvidia.com/jetson/jetpack/) — JetPack SDK 安装与配置