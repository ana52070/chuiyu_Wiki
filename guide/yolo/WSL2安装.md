可以。Windows 10/11 下安装 **WSL2 + Ubuntu 22.04**，推荐直接用微软现在提供的 `wsl` 命令，比较省事。

### 1. 先检查 WSL

以**管理员身份**打开 PowerShell：

```
wsl --status
```

再看看当前已经安装了什么：

```
wsl -l -v
```

如果提示没有安装 WSL，直接：

```
wsl --install
```

执行完成后如果提示重启，就**重启电脑**。

---

### 2. 查看可以安装哪些 Ubuntu

重启后打开 PowerShell：

```
wsl --list --online
```

一般会看到类似：

```
NAME                            FRIENDLY NAME
Ubuntu                          Ubuntu
Ubuntu-22.04                    Ubuntu 22.04 LTS
Ubuntu-24.04                    Ubuntu 24.04 LTS
...
```

你要的是 **Ubuntu 22.04**，所以执行：

```
wsl --install -d Ubuntu-22.04
```

等待下载安装。

---

### 3. 第一次进入 Ubuntu

安装完成后执行：

```
wsl -d Ubuntu-22.04
```

第一次启动会让你创建 Linux 用户，例如：

```
Enter new UNIX username: chuiyu
New password:
Retype new password:
```

注意输入密码时**屏幕不会显示任何字符**，这是 Linux 正常行为，直接输入然后回车。

---

### 4. 确认是不是 WSL2

回到 PowerShell：

```
wsl -l -v
```

理想情况：

```
  NAME            STATE           VERSION
* Ubuntu-22.04    Running         2
```

关键看最后：

```
VERSION
2
```

这就说明你安装的是 **WSL2**。

如果显示 `1`，执行：

```
wsl --set-version Ubuntu-22.04 2
```

另外建议直接把以后新安装的 Linux 默认设置成 WSL2：

```
wsl --set-default-version 2
```

---

### 5. 进入 Ubuntu 后更新软件

进入：

```
wsl -d Ubuntu-22.04
```

然后 Ubuntu 里面执行：

```
sudo apt update
sudo apt upgrade -y
```

检查系统：

```
cat /etc/os-release
```

应该能看到：

```
NAME="Ubuntu"
VERSION="22.04.x LTS (Jammy Jellyfish)"
```

### 最终你的安装流程其实就是

```
Windows
  │
  ├── 管理员 PowerShell
  │
  ├── wsl --install
  │
  ├── 重启电脑
  │
  ├── wsl --install -d Ubuntu-22.04
  │
  └── wsl -l -v
          │
          └── VERSION = 2  → 完成
```

如果你电脑上**本来就已经有 WSL2，只是想额外安装一个 Ubuntu 22.04**，那更简单，基本只需要：

```
wsl --install -d Ubuntu-22.04
```

你可以先执行：

```
wsl --status
wsl -l -v
```

把输出贴给我，我可以直接根据你电脑目前的状态告诉你下一条该执行什么命令。