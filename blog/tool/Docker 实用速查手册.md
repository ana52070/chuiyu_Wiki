---
author: claude
date: 2026-03-30
description: Docker 实用速查手册
tags:
  - Docker
---

> 写给「懂一点但记不住」的自己。每次忘了命令就来这里查。
> 
> 最后更新：2026-03-30

---

## 1. 镜像（Image）

镜像是容器的模板，类似于「系统安装盘」。

### 1.1 搜索 & 拉取

```bash
# 从 Docker Hub 搜索镜像
docker search ubuntu

# 拉取镜像（默认 latest 标签）
docker pull ubuntu:22.04

# 拉取 NVIDIA 官方 CUDA 镜像（常用于 GPU 开发）
docker pull nvcr.io/nvidia/cuda:11.8.0-devel-ubuntu22.04
```

### 1.2 查看本地镜像

```bash
# 列出所有本地镜像
docker images

# 只看镜像 ID
docker images -q

# 按名字过滤
docker images | grep ubuntu
```

### 1.3 删除镜像

```bash
# 删除指定镜像
docker rmi ubuntu:22.04

# 强制删除（即使有容器在用）
docker rmi -f ubuntu:22.04

# 删除所有没有被任何容器使用的「悬空镜像」（<none> 标签的那些）
docker image prune

# 删除所有未被使用的镜像（谨慎！）
docker image prune -a
```

### 1.4 构建镜像（Dockerfile）

```bash
# 在当前目录下根据 Dockerfile 构建镜像
docker build -t my-ros2:latest .

# 指定 Dockerfile 路径
docker build -t my-ros2:latest -f docker/Dockerfile.ros2 .

# 不使用缓存重新构建
docker build --no-cache -t my-ros2:latest .
```

#### 一个实用的 ROS 2 Dockerfile 示例

```dockerfile
FROM ubuntu:22.04

# 避免交互式安装卡住
ENV DEBIAN_FRONTEND=noninteractive

# 设置中文 locale（可选）
RUN apt-get update && apt-get install -y locales \
    && locale-gen zh_CN.UTF-8 \
    && update-locale LANG=zh_CN.UTF-8

# 安装 ROS 2 Humble
RUN apt-get update && apt-get install -y \
    software-properties-common curl \
    && add-apt-repository universe \
    && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
       -o /usr/share/keyrings/ros-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
       http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
       > /etc/apt/sources.list.d/ros2.list \
    && apt-get update && apt-get install -y ros-humble-desktop \
    && rm -rf /var/lib/apt/lists/*

# 自动 source ROS 2 环境
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc

WORKDIR /root/ros2_ws
CMD ["bash"]
```

### 1.5 导入导出镜像（离线传输）

```bash
# 导出镜像为 tar 文件（适合没有网络的机器之间传输）
docker save -o my-ros2.tar my-ros2:latest

# 从 tar 文件导入镜像
docker load -i my-ros2.tar
```

---

## 2. 容器（Container）

容器是镜像跑起来之后的实例，类似于「开机后的系统」。

### 2.1 创建 & 运行

```bash
# 最基本的运行：交互式启动并进入 bash
docker run -it ubuntu:22.04 bash

# 后台运行（-d = detach）
docker run -d --name my-container ubuntu:22.04 tail -f /dev/null
```

#### 你最常用的：带 GPU + 挂载目录 + 网络的完整启动命令

```bash
docker run -it \
    --name ros2-dev \
    --runtime nvidia \
    --gpus all \
    --network host \
    --privileged \
    -v /home/user/ros2_ws:/root/ros2_ws \
    -v /dev:/dev \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY=$DISPLAY \
    -e NVIDIA_VISIBLE_DEVICES=all \
    -e NVIDIA_DRIVER_CAPABILITIES=all \
    my-ros2:latest \
    bash
```

**各参数解释：**

|参数|作用|
|---|---|
|`--name ros2-dev`|给容器起个名字，后续操作方便|
|`--runtime nvidia`|使用 NVIDIA 容器运行时，挂载宿主机 CUDA|
|`--gpus all`|把所有 GPU 传入容器|
|`--network host`|直接使用宿主机网络（ROS 2 多节点通信必须）|
|`--privileged`|给容器完整权限（访问 /dev 下设备需要）|
|`-v 宿主机路径:容器路径`|目录挂载，容器内外共享文件|
|`-v /tmp/.X11-unix:...`|挂载 X11，容器内可以跑 GUI（如 RViz）|
|`-e DISPLAY=$DISPLAY`|传入显示环境变量|

> **提示：** 如果只需要特定 GPU，可以用 `--gpus '"device=0"'` 指定。

### 2.2 查看容器

```bash
# 查看正在运行的容器
docker ps

# 查看所有容器（包括已停止的）
docker ps -a

# 只看容器 ID
docker ps -aq

# 查看容器详细信息（排查问题用）
docker inspect ros2-dev

# 查看容器资源占用（CPU、内存、网络 IO）
docker stats

# 查看某个容器的资源占用
docker stats ros2-dev
```

### 2.3 启动 / 停止 / 重启

```bash
# 启动一个已经停止的容器
docker start ros2-dev

# 以交互模式启动（直接进入终端）
docker start -ai ros2-dev

# 停止容器（发送 SIGTERM，优雅关闭）
docker stop ros2-dev

# 强制杀掉（发送 SIGKILL，立即终止）
docker kill ros2-dev

# 重启
docker restart ros2-dev
```

### 2.4 进入正在运行的容器

```bash
# 最常用：进入容器的 bash 终端
docker exec -it ros2-dev bash

# 以 root 用户进入（如果容器默认是非 root 用户）
docker exec -it --user root ros2-dev bash

# 在容器内执行一条命令（不进入终端）
docker exec ros2-dev ls /root/ros2_ws
```

> **`exec` vs `attach` 的区别：**
> 
> - `docker exec -it ... bash` → 新开一个终端进去，退出不影响容器
> - `docker attach ...` → 连接到容器的主进程，`Ctrl+C` 可能会把容器干掉
> 
> **建议一律用 `exec`。**

### 2.5 删除容器

```bash
# 删除已停止的容器
docker rm ros2-dev

# 强制删除（即使正在运行）
docker rm -f ros2-dev

# 删除所有已停止的容器
docker container prune

# 核弹级别：删除所有容器（慎用！）
docker rm -f $(docker ps -aq)
```

### 2.6 容器日志

```bash
# 查看容器日志
docker logs ros2-dev

# 实时跟踪日志（类似 tail -f）
docker logs -f ros2-dev

# 只看最后 50 行
docker logs --tail 50 ros2-dev

# 带时间戳
docker logs -t ros2-dev
```

### 2.7 文件拷贝

```bash
# 宿主机 → 容器
docker cp ./my_package ros2-dev:/root/ros2_ws/src/

# 容器 → 宿主机
docker cp ros2-dev:/root/ros2_ws/build/log.txt ./
```

### 2.8 将容器保存为新镜像

```bash
# 容器里装了一堆东西，想保存下来
docker commit ros2-dev my-ros2:with-nav2

# 带提交信息
docker commit -m "安装了 Nav2 和 LIO-SAM 依赖" ros2-dev my-ros2:with-nav2
```

> **注意：** `docker commit` 适合临时保存，正式项目建议用 Dockerfile 管理，这样可复现。

---

## 3. 数据卷（Volume）

数据卷是 Docker 管理的持久化存储，容器删了数据还在。

```bash
# 创建数据卷
docker volume create ros2-data

# 查看所有数据卷
docker volume ls

# 查看数据卷详情（可以看到在宿主机上的实际路径）
docker volume inspect ros2-data

# 使用数据卷启动容器
docker run -it -v ros2-data:/root/ros2_ws/data my-ros2:latest bash

# 删除数据卷
docker volume rm ros2-data

# 删除所有没有被容器使用的数据卷
docker volume prune
```

**`-v` 挂载的两种方式对比：**

|方式|示例|特点|
|---|---|---|
|绑定挂载（Bind Mount）|`-v /home/user/ws:/root/ws`|直接映射宿主机目录，开发时用|
|命名卷（Named Volume）|`-v my-vol:/root/data`|Docker 管理，适合持久化数据库等|

---

## 4. 网络（Network）

```bash
# 查看所有 Docker 网络
docker network ls

# 创建自定义网络
docker network create my-net

# 让容器加入自定义网络
docker run -it --network my-net --name node1 ubuntu:22.04 bash

# 查看某个网络的详情（看哪些容器在里面）
docker network inspect my-net

# 删除网络
docker network rm my-net
```

**常用网络模式：**

|模式|说明|使用场景|
|---|---|---|
|`--network host`|容器直接用宿主机网络栈|ROS 2 多机通信、需要局域网广播|
|`--network bridge`（默认）|容器有独立 IP，通过端口映射访问|一般 Web 服务|
|`--network none`|无网络|安全隔离场景|

> **ROS 2 场景建议：** 一律用 `--network host`，省去 DDS 发现的麻烦。

---

## 5. Docker Compose

Compose 用于定义和管理多容器应用。一个 `docker-compose.yml` 搞定所有容器的配置。

### 5.1 基本命令

```bash
# 启动所有服务（后台运行）
docker compose up -d

# 启动并重新构建镜像
docker compose up -d --build

# 查看运行中的服务
docker compose ps

# 查看日志
docker compose logs

# 实时跟踪某个服务的日志
docker compose logs -f ros2-nav

# 停止所有服务
docker compose down

# 停止并删除数据卷（数据库数据会丢！慎用）
docker compose down -v

# 重启某个服务
docker compose restart ros2-nav

# 进入某个服务的终端
docker compose exec ros2-nav bash
```

### 5.2 一个实际的 docker-compose.yml 示例

场景：ROS 2 导航节点 + 单独的数据库记录轨迹

```yaml
version: "3.8"

services:
  ros2-nav:
    image: my-ros2:with-nav2
    container_name: ros2-nav
    runtime: nvidia            # GPU 支持
    network_mode: host         # ROS 2 通信需要
    privileged: true
    environment:
      - DISPLAY=${DISPLAY}
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=all
    volumes:
      - /home/user/ros2_ws:/root/ros2_ws
      - /dev:/dev
      - /tmp/.X11-unix:/tmp/.X11-unix
    command: >
      bash -c "source /opt/ros/humble/setup.bash &&
               source /root/ros2_ws/install/setup.bash &&
               ros2 launch campus_nav navigation.launch.py"
    restart: unless-stopped    # 崩溃自动重启

  postgres:
    image: postgres:15
    container_name: trajectory-db
    environment:
      POSTGRES_USER: ros
      POSTGRES_PASSWORD: ros123
      POSTGRES_DB: trajectories
    volumes:
      - pg-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

volumes:
  pg-data:                     # 命名卷，数据持久化
```

### 5.3 环境变量管理

```bash
# 方式 1：在 docker-compose.yml 同目录放一个 .env 文件
# .env 文件内容：
# DISPLAY=:1
# POSTGRES_PASSWORD=ros123

# 方式 2：命令行指定
docker compose --env-file ./custom.env up -d
```

---

## 6. 系统清理

Docker 用久了会积累大量无用数据，定期清理很有必要。

```bash
# 查看 Docker 磁盘占用
docker system df

# 详细版本
docker system df -v

# 一键清理所有未使用的资源（镜像、容器、网络、构建缓存）
# ⚠️ 会删掉所有停止的容器和未使用的镜像
docker system prune

# 加上数据卷也一起清（数据会丢，三思！）
docker system prune --volumes

# 只清理构建缓存
docker builder prune
```

---

## 7. 常见问题速查

### 7.1 容器里 GUI 打不开（RViz / Gazebo）

```bash
# 在宿主机上先允许 X11 连接
xhost +local:docker

# 然后确保容器启动时带了这两个参数：
# -v /tmp/.X11-unix:/tmp/.X11-unix
# -e DISPLAY=$DISPLAY
```

### 7.2 容器里没有 GPU / nvidia-smi 报错

```bash
# 检查宿主机 nvidia-container-toolkit 是否安装
dpkg -l | grep nvidia-container-toolkit

# 没装的话：
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### 7.3 容器里访问串口 / USB 设备

```bash
# 方式 1：挂载具体设备
docker run -it --device /dev/ttyUSB0 my-ros2:latest bash

# 方式 2：直接 --privileged + 挂载 /dev（简单粗暴）
docker run -it --privileged -v /dev:/dev my-ros2:latest bash
```

### 7.4 容器内 apt 速度慢

```bash
# 进入容器后换源
sed -i 's|archive.ubuntu.com|mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list
apt-get update
```

或者在 Dockerfile 里直接写好：

```dockerfile
RUN sed -i 's|archive.ubuntu.com|mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list
```

### 7.5 想让容器开机自启

```bash
# 创建容器时加 --restart 策略
docker run -d --restart unless-stopped --name ros2-dev my-ros2:latest

# 给已有容器补上
docker update --restart unless-stopped ros2-dev
```

|策略|说明|
|---|---|
|`no`|默认，不自动重启|
|`on-failure`|非正常退出时重启|
|`unless-stopped`|除非手动 stop，否则一直重启（推荐）|
|`always`|无论什么情况都重启|

---

## 附：命令速查表

| 操作         | 命令                                    |
| ---------- | ------------------------------------- |
| 拉取镜像       | `docker pull ubuntu:22.04`            |
| 查看镜像       | `docker images`                       |
| 删除镜像       | `docker rmi <镜像名>`                    |
| 运行容器       | `docker run -it --name xxx <镜像> bash` |
| 查看容器       | `docker ps -a`                        |
| 启动已停止的容器   | `docker start -ai <容器名>`              |
| 进入运行中容器    | `docker exec -it <容器名> bash`          |
| 停止容器       | `docker stop <容器名>`                   |
| 删除容器       | `docker rm <容器名>`                     |
| 查看日志       | `docker logs -f <容器名>`                |
| 文件拷贝       | `docker cp 源路径 目标路径`                  |
| 容器保存为镜像    | `docker commit <容器名> <新镜像名>`          |
| 镜像导出       | `docker save -o file.tar <镜像名>`       |
| 镜像导入       | `docker load -i file.tar`             |
| Compose 启动 | `docker compose up -d`                |
| Compose 停止 | `docker compose down`                 |
| Compose 进入 | `docker compose exec <服务名> bash`      |
| 查看磁盘占用     | `docker system df`                    |
| 一键清理       | `docker system prune`                 |
