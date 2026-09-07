如果你现在是在刚安装好的 **WSL2 Ubuntu 22.04** 里面，我建议直接在 Ubuntu 中安装 **Miniconda**。

你可以先确认自己是在 Ubuntu 终端：

```
cat /etc/os-release
```

看到 `Ubuntu 22.04` 就可以继续。

### 1. 下载 Miniconda

对于普通 Intel/AMD Windows 电脑上的 WSL2，一般是 `x86_64`：

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

如果提示：

```
wget: command not found
```

先安装：

```
sudo apt update
sudo apt install wget -y
```

然后重新下载。

### 2. 运行安装程序

```
bash Miniconda3-latest-Linux-x86_64.sh
```

接下来会进入安装流程。

首先会看到许可证：

```
Welcome to Miniconda3 ...

In order to continue the installation process,
please review the license agreement.
Please, press ENTER to continue
```

按：

```
Enter
```

然后不断按 Enter 往下翻，最后会问是否接受：

```
Do you accept the license terms? [yes|no]
```

输入：

```
yes
```

### 3. 选择安装位置

接下来一般会出现：

```
Miniconda3 will now be installed into this location:

/home/chuiyu/miniconda3

- Press ENTER to confirm the location
- Press CTRL-C to abort the installation
- Or specify a different location below
```

这里**直接按 Enter**，使用默认位置即可。

也就是安装到：

```
~/miniconda3
```

不要为了方便装到 `/mnt/c/...` 之类的 Windows 目录。WSL 下直接放 Linux 文件系统更合适。

### 4. 初始化 Conda

安装快结束的时候通常会问：

```
Do you wish to update your shell profile to automatically initialize conda?
[yes|no]
```

这里输入：

```
yes
```

然后：

```
source ~/.bashrc
```

此时终端前面一般会出现：

```
(base) chuiyu@xxx:~$
```

说明 Conda 已经生效。

检查：

```
conda --version
```

例如：

```
conda 25.x.x
```

### 5. 创建一个 Python 环境

例如你后面要折腾 YOLO，可以先创建 Python 3.10 环境：

```
conda create -n my_yolov8 python=3.10 -y
```

进入环境：

```
conda activate my_yolov8
```

然后检查：

```
python --version
```

应该类似：

```
Python 3.10.x
```

查看所有环境：

```
conda env list
```

你可以把它理解成：

```
WSL2
└── Ubuntu 22.04
    │
    └── Miniconda
        │
        ├── base
        │
        ├── my_yolov8
        │   └── Python 3.10
        │
        ├── yolov5
        │   └── Python 3.9
        │
        └── 以后其他项目的环境
```

**最核心的几个 Conda 命令**先记这几个就够：

```
# 创建环境
conda create -n 环境名 python=3.10

# 进入环境
conda activate 环境名

# 退出环境
conda deactivate

# 查看所有环境
conda env list

# 删除环境
conda remove -n 环境名 --all
```