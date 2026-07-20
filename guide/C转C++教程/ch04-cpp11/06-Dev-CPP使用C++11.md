---
title: Dev-CPP使用C++11
author: claudecode(deepseekV4flash)
date: 2026-07-20 21:40:47
description: Dev-CPP使用C++11
tags:
  - Cpp算法
categories:
  - guide
  - C++算法入门
---

# Dev C++ 使用 C++11

## 1. 为什么需要手动启用 C++11？

Dev C++ 是一款轻量级的 C/C++ 集成开发环境，它底层使用的是 **MinGW-GCC** 编译器。较老版本的 Dev C++（如 5.11 及更早）自带的 GCC 版本较低（通常是 GCC 4.x 系列），默认使用的是 **C++98** 标准。

这意味着：
- 如果你不进行任何设置，直接写 C++11 代码（如 `auto`、范围 for、`to_string` 等），编译器会报错
- 需要手动告诉编译器：**请使用 C++11 标准来编译我的代码**

## 2. Dev C++ 中启用 C++11 的详细步骤

以下步骤适用于 **Dev C++ 5.11** 及类似版本。

### 步骤 1：打开 Dev C++

启动 Dev C++ 并打开你的项目或源代码文件。

### 步骤 2：打开编译器选项

点击菜单栏的 `Tools`（工具）→ `Compiler Options`（编译器选项）。

> 文字替代图：[Tools 菜单 → 下拉 → Compiler Options]

### 步骤 3：进入 Settings 选项卡

在弹出的对话框中，点击顶部的 `Settings`（设置）选项卡。

### 步骤 4：选择 Code Generation

在 Settings 选项卡左侧的树形列表中：
- 展开 `Code Generation`（代码生成）

### 步骤 5：设置 Language standard

在右侧的设置项中找到：
- `Language standard (-std)`（语言标准）
- 点击下拉框，选择 **`ISO C++11`**

> 文字替代图：[Settings → Code Generation → Language standard (-std) → 下拉选择 ISO C++11]

### 步骤 6：保存设置

点击 `OK` 按钮保存设置并关闭对话框。

---

**如果上述路径找不到 Language standard，可以尝试另一种方法：**

**方法 B——通过 Compiler flags 直接添加编译参数：**

1. `Tools` → `Compiler Options`
2. 点击 `Compiler` 选项卡（或 `Programs` 旁边的 `Compiler`）
3. 在 `Add the following commands when calling compiler`（编译时追加以下命令）框中输入：
   ```
   -std=c++11
   ```
4. 勾选该行前面的复选框
5. 点击 `OK` 保存

> 文字替代图：[Compiler Options → Compiler 选项卡 → "Add the following commands..." 输入框 → 输入 -std=c++11]

---

**如果你的 Dev C++ 找不到这些选项（或选项不可用），可能是因为版本过老，建议升级：**

- 下载 **Dev C++ 的最新分支版本**（如 Orwell Dev C++ 或 Embarcadero Dev C++）
- 或切换到其他 IDE（如 VS Code、Code::Blocks）

## 3. 如何验证 C++11 已生效

设置完成后，编写以下检测程序，编译运行：

```cpp
#include <iostream>
using namespace std;

int main() {
    // 方法 1：检查 __cplusplus 宏
    cout << "__cplusplus = " << __cplusplus << endl;

    if (__cplusplus >= 201103L) {
        cout << "C++11 已启用!" << endl;
    } else {
        cout << "C++11 未启用，当前标准为 C++98/03" << endl;
    }

    // 方法 2：尝试编译 C++11 特性
    // auto 是 C++11 特性，如果 C++11 未启用，这行会报错
    auto x = 42;
    cout << "auto 推导: x = " << x << endl;

    // 初始化列表是 C++11 特性
    int arr[] = {1, 2, 3, 4, 5};
    // 范围 for 是 C++11 特性
    for (auto i : arr) {
        cout << i << " ";
    }
    cout << endl;

    // to_string 是 C++11 特性
    string s = to_string(3.14);
    cout << "to_string: " << s << endl;

    return 0;
}
```

**编译成功时的预期输出：**

```
__cplusplus = 201103
C++11 已启用!
auto 推导: x = 42
1 2 3 4 5
to_string: 3.140000
```

**如果 C++11 未启用**，编译时会报类似以下错误：

```
[Error] 'auto' does not name a type
[Error] range-based 'for' loops are not allowed in C++98 mode
[Error] 'to_string' was not declared in this scope
```

## 4. 常见编译错误的排查

### 问题 1：auto 报错

```
错误信息：[Error] 'auto' does not name a type
```

**原因**：编译器认为 `auto` 是一个普通标识符而非关键字 → C++11 未开启。

**解决**：按上述步骤启用 C++11，或者如果你的编译器太旧不支持 C++11，请升级。

### 问题 2：范围 for 报错

```
错误信息：[Error] range-based 'for' loops are not allowed in C++98 mode
```

**原因**：编译器用 C++98 标准编译，不支持范围 for。

**解决**：启用 C++11。

### 问题 3：to_string 报错

```
错误信息：[Error] 'to_string' was not declared in this scope
```

**原因**：
1. 未包含 `<string>` 头文件
2. 编译器不支持 C++11（或 C++11 未开启）

**解决**：检查头文件是否包含，检查编译标准。

### 问题 4：初始化列表报错

```
错误信息：[Error] in C++98 'v' must be initialized by constructor, not by '{...}'
```

**原因**：C++11 的初始化列表不支持 C++98 模式。

**解决**：启用 C++11。

### 整套检查流程

```
遇到 C++11 代码编译错误
         │
         ▼
头文件都包含了吗？ ──否──→ 添加正确的 #include
         │
        是
         ▼
检查 Dev C++ 的编译器选项 ──未设置──→ 启用 C++11
         │
        已设置
         ▼
检查 Dev C++ 自带的 GCC 版本
gcc --version
         │
        旧（< 4.8）────→ 升级 Dev C++ 或更换 IDE
         │
        新（>= 4.8）
         │
         ▼
检查编译命令行是否被项目设置覆盖
```

### 查看 Dev C++ 使用的 GCC 版本

打开 Dev C++，点击 `Tools` → `Compiler Options` → `Compiler` 选项卡（或 `Programs`），可以看到 GCC 的路径。或者打开命令行：

```bash
# 在 Dev C++ 的安装目录下的 bin 文件夹中执行
g++ --version
```

一般输出类似：
```
g++ (MinGW.org GCC Build-2) 4.9.2
```

**C++11 支持程度与 GCC 版本对照：**

| GCC 版本 | C++11 支持状态 |
|:--------:|:-------------:|
| < 4.3 | 基本不支持 |
| 4.3~4.6 | 部分支持 |
| 4.7~4.8 | 基本完整支持 |
| 4.9+ | 完整支持 C++11 |
| 5.x+ | 默认不再使用 C++98，但需要 `-std=c++11` 或 `-std=c++14` |
| 6.1+ | **默认启用 C++14**（向后兼容 C++11） |

## 5. 其他常见 IDE 中开启 C++11

### 5.1 Code::Blocks

1. 打开 Code::Blocks
2. 点击菜单栏 `Settings` → `Compiler`
3. 在 `Selected compiler` 中确保选中 `GNU GCC Compiler`
4. 点击 `Compiler settings` 选项卡
5. 勾选 `Compiler flags` 列表中的：
   - `Have g++ follow the C++11 ISO standard [-std=c++11]`
6. 点击 `OK` 保存

![文字替代示意图]

或者使用命令行参数方式：
1. 在 `Other compiler options` 文本框中手动输入：
   ```
   -std=c++11
   ```

### 5.2 Visual Studio Code（VS Code）

VS Code 本身是一个编辑器，C++ 编译依赖于配置的编译器。常配合 MinGW-GCC 使用。

**如果使用 GCC 编译器（通过 tasks.json）：**

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "build",
            "type": "shell",
            "command": "g++",
            "args": [
                "-std=c++11",         // 关键：添加这一行
                "-o", "${fileDirname}/${fileBasenameNoExtension}.exe",
                "${file}"
            ],
            "group": "build"
        }
    ]
}
```

**如果使用 CMake：**

```cmake
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
```

### 5.3 Visual Studio（MSVC）

Visual Studio 2013 及以上版本默认就支持 C++11。如需手动确认：

1. 右键项目 → `Properties`
2. `Configuration Properties` → `C/C++` → `Language`
3. `C++ Language Standard` → 选择 `ISO C++11 Standard (/std:c++11)` 或直接使用默认值

注意：VS 2012 及以前版本对 C++11 支持有限，建议升级。

### 5.4 CLion（JetBrains）

1. `File` → `Settings` → `Build, Execution, Deployment` → `CMake`
2. 在 `CMake options` 中添加：
   ```
   -DCMAKE_CXX_STANDARD=11
   ```
3. 或者在 `CMakeLists.txt` 中添加：
   ```cmake
   set(CMAKE_CXX_STANDARD 11)
   set(CMAKE_CXX_STANDARD_REQUIRED ON)
   ```

## 6. 完整可运行检测程序

将以下代码保存为一个 `.cpp` 文件，用于检测你的开发环境是否已正确配置 C++11 支持。

```cpp
/*
 * C++11 检测程序
 * 编译并运行此程序，验证你的开发环境是否支持 C++11
 */

#include <iostream>
#include <vector>
#include <set>
#include <map>
#include <string>
#include <unordered_map>
#include <unordered_set>
using namespace std;

int main() {
    cout << "====== C++11 特性检测程序 ======" << endl;

    // ====== 1. 编译标准检测 ======
    cout << "\n--- 1. 编译标准检测 ---" << endl;
    cout << "__cplusplus = " << __cplusplus << endl;

    if (__cplusplus >= 201103L) {
        cout << "[通过] 当前使用 C++11 或更高标准" << endl;
    } else {
        cout << "[失败] 当前使用 C++98/03 标准，请启用 C++11" << endl;
        return 1;
    }

    // ====== 2. auto 类型推导 ======
    cout << "\n--- 2. auto 类型推导 ---" << endl;
    auto num = 42;
    auto pi = 3.14159;
    auto text = "hello";
    cout << "[通过] auto 推导: num=" << num
         << ", pi=" << pi
         << ", text=" << text << endl;

    // ====== 3. 初始化列表 ======
    cout << "\n--- 3. 初始化列表 ---" << endl;
    vector<int> v = {1, 2, 3, 4, 5};
    set<string> s = {"apple", "banana", "cherry"};
    map<string, int> m = {{"Alice", 95}, {"Bob", 87}};
    cout << "[通过] 初始化列表编译成功" << endl;

    // ====== 4. 范围 for 循环 ======
    cout << "\n--- 4. 范围 for 循环 ---" << endl;
    cout << "vector: ";
    for (auto i : v) cout << i << " ";
    cout << "\nset:    ";
    for (const auto &x : s) cout << x << " ";
    cout << "\nmap:    ";
    for (const auto &p : m) {
        cout << p.first << ":" << p.second << " ";
    }
    cout << endl;
    cout << "[通过] 范围 for 循环执行成功" << endl;

    // ====== 5. to_string ======
    cout << "\n--- 5. to_string ---" << endl;
    string s1 = to_string(123);
    string s2 = to_string(3.14159);
    cout << "to_string(123)     = " << s1 << endl;
    cout << "to_string(3.14159) = " << s2 << endl;
    cout << "[通过] to_string 执行成功" << endl;

    // ====== 6. stoi/stod ======
    cout << "\n--- 6. stoi/stod ---" << endl;
    int a = stoi("42");
    double b = stod("3.14");
    cout << "stoi(\"42\")  = " << a << endl;
    cout << "stod(\"3.14\") = " << b << endl;

    size_t idx;
    int c = stoi("100XYZ", &idx);
    cout << "stoi(\"100XYZ\") = " << c
         << ", 停止于 idx=" << idx << endl;
    cout << "[通过] stoi/stod 执行成功" << endl;

    // ====== 7. unordered_map / unordered_set ======
    cout << "\n--- 7. unordered_map/unordered_set ---" << endl;
    unordered_map<string, int> um = {{"one", 1}, {"two", 2}, {"three", 3}};
    unordered_set<int> us = {100, 200, 300, 400, 500};

    cout << "unordered_map: ";
    for (const auto &p : um) cout << p.first << ":" << p.second << " ";
    cout << "\nunordered_set: ";
    for (auto x : us) cout << x << " ";
    cout << endl;
    cout << "[通过] unordered_map/unordered_set 执行成功" << endl;

    // ====== 汇总 ======
    cout << "\n====== 检测完成 ======" << endl;
    cout << "所有 C++11 特性均工作正常！" << endl;

    return 0;
}
```

**编译方式：**

```bash
# 如果使用命令行
g++ -std=c++11 check_cpp11.cpp -o check_cpp11
./check_cpp11

# 或者在 Dev C++ 中直接按 F11 编译运行（前提已设置 C++11）
```

**预期输出（顺序可能因 unordered 类型有所不同）：**

```
====== C++11 特性检测程序 ======

--- 1. 编译标准检测 ---
__cplusplus = 201103
[通过] 当前使用 C++11 或更高标准

--- 2. auto 类型推导 ---
[通过] auto 推导: num=42, pi=3.14159, text=hello

--- 3. 初始化列表 ---
[通过] 初始化列表编译成功

--- 4. 范围 for 循环 ---
vector: 1 2 3 4 5
set:    apple banana cherry
map:    Alice:95 Bob:87
[通过] 范围 for 循环执行成功

--- 5. to_string ---
to_string(123)     = 123
to_string(3.14159) = 3.141590
[通过] to_string 执行成功

--- 6. stoi/stod ---
stoi("42")  = 42
stod("3.14") = 3.14
stoi("100XYZ") = 100, 停止于 idx=3
[通过] stoi/stod 执行成功

--- 7. unordered_map/unordered_set ---
unordered_map: one:1 two:2 three:3
unordered_set: 400 200 300 100 500
[通过] unordered_map/unordered_set 执行成功

====== 检测完成 ======
所有 C++11 特性均工作正常！
```

## 7. 小结

- Dev C++ 默认使用 C++98 标准，需要使用 C++11 特性时必须**手动开启**
- 开启方法：`Tools` → `Compiler Options` → `Settings` → `Code Generation` → `Language standard` → 选择 `ISO C++11`
- 备选方案：在 Compiler Options 的文本框中直接添加 `-std=c++11`
- 验证方法：检查 `__cplusplus >= 201103L` 或尝试编译使用了 C++11 特性的代码
- 如果 Dev C++ 版本太老无法支持，建议升级或换用 VS Code / Code::Blocks 等工具
