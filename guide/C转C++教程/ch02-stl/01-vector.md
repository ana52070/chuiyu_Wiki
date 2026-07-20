---
title: vector
author: claudecode(deepseekV4flash)
date: 2026-07-20 21:40:45
description: vector
tags:
  - Cpp算法
categories:
  - guide
  - C++算法入门
---

## vector（动态数组）

### 一、概念与原理

`vector` 是 C++ STL（标准模板库）中最常用的容器之一。它的本质是**动态数组**——即可以自动扩容的连续内存数组。

**核心原理：**
- vector 内部维护一块连续的动态内存，元素在内存中紧密排列
- 当当前容量（capacity）不足以容纳新元素时，vector 会自动申请一块更大的内存（通常为原容量的 1.5~2 倍），将现有元素全部拷贝/移动到新内存，然后释放旧内存
- 这种"自动扩容"的机制使得用户可以像使用普通数组一样使用 vector，但无需关心手动管理内存

**与普通数组的关键区别：**

| 特性 | 普通数组 `int a[10]` | `vector<int>` |
|------|---------------------|---------------|
| 大小 | 编译时固定，不可改变 | 运行时动态增长 |
| 内存管理 | 自动（栈上或全局） | 自动（堆上） |
| 边界检查 | 不检查 | `at()` 方法会检查 |
| 功能方法 | 无 | 丰富（size, push_back 等） |

### 二、头文件

使用 vector 需要包含头文件：

```cpp
#include <vector>
```

### 三、创建方式

vector 提供了多种不同的构造方式，以适应不同的场景：

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    // 1. 空构造：创建一个空的 vector，不含任何元素
    vector<int> v1;
    cout << "v1 size = " << v1.size() << endl;          // 输出: 0

    // 2. 指定大小：创建包含 10 个元素的 vector，每个元素默认初始化为 0
    vector<int> v2(10);
    cout << "v2 size = " << v2.size() << ", v2[3] = " << v2[3] << endl;   // 输出: 10, 0

    // 3. 指定大小和初值：创建包含 10 个元素的 vector，每个元素值为 2
    vector<int> v3(10, 2);
    cout << "v3 size = " << v3.size() << ", v3[3] = " << v3[3] << endl;   // 输出: 10, 2

    // 4. 初始化列表（C++11 起）：直接用花括号指定所有元素
    vector<int> v4 = {1, 2, 3, 4, 5};
    // 或者：
    // vector<int> v4{1, 2, 3, 4, 5};
    cout << "v4 size = " << v4.size() << ", v4[0] = " << v4[0] << endl;   // 输出: 5, 1

    // 5. 拷贝构造：用一个 vector 创建另一个 vector
    vector<int> v5(v4);
    cout << "v5 size = " << v5.size() << ", v5[4] = " << v5[4] << endl;   // 输出: 5, 5

    // 6. 从数组构造（通过迭代器）
    int arr[] = {10, 20, 30, 40};
    vector<int> v6(arr, arr + 4);
    cout << "v6 size = " << v6.size() << ", v6[2] = " << v6[2] << endl;   // 输出: 4, 30

    return 0;
}
```

**预期运行结果：**
```
v1 size = 0
v2 size = 10, v2[3] = 0
v3 size = 10, v3[3] = 2
v4 size = 5, v4[0] = 1
v5 size = 5, v5[4] = 5
v6 size = 4, v6[2] = 30
```

### 四、常用成员函数详解

#### 1. 添加元素

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v;

    // push_back()：在尾部追加一个元素（最常用的添加方式）
    v.push_back(10);
    v.push_back(20);
    v.push_back(30);

    // 输出: 10 20 30
    for (int x : v) cout << x << " ";
    cout << endl;

    return 0;
}
```

> **注意：** C++11 之后 vector 也提供了 `emplace_back()`，它直接在容器尾部构造元素，避免了拷贝/移动操作，性能优于 `push_back()`。详见本节末尾的进阶讨论。

#### 2. 删除元素

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {1, 2, 3, 4, 5};

    // pop_back()：移除尾部元素（不返回值）
    v.pop_back();                     // 移除 5
    // 现在 v = {1, 2, 3, 4}

    cout << "After pop_back: ";
    for (int x : v) cout << x << " ";
    cout << endl;

    return 0;
}
```

**预期运行结果：**
```
After pop_back: 1 2 3 4
```

> **注意：** `pop_back()` 不会返回被删除的元素，要获取尾部元素可以先使用 `back()`。对空 vector 调用 `pop_back()` 是**未定义行为**（程序可能崩溃）！

#### 3. 查询大小与容量

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v;
    cout << "Initial: size = " << v.size() << ", capacity = " << v.capacity() << endl;

    v.push_back(1);
    cout << "After 1 push: size = " << v.size() << ", capacity = " << v.capacity() << endl;

    v.push_back(2);
    cout << "After 2 push: size = " << v.size() << ", capacity = " << v.capacity() << endl;

    v.push_back(3);
    cout << "After 3 push: size = " << v.size() << ", capacity = " << v.capacity() << endl;

    // resize()：重新调整大小
    v.resize(5);    // 扩展为 5 个元素，新增元素默认初始化为 0
    cout << "After resize(5): size = " << v.size() << ", capacity = " << v.capacity() << endl;
    for (int x : v) cout << x << " ";
    cout << endl;

    v.resize(2);    // 缩小为 2 个元素，多余元素被丢弃
    cout << "After resize(2): size = " << v.size() << ", capacity = " << v.capacity() << endl;
    for (int x : v) cout << x << " ";
    cout << endl;

    // empty()：判断是否为空
    cout << "Is empty? " << (v.empty() ? "Yes" : "No") << endl;

    return 0;
}
```

**预期运行结果：**
```
Initial: size = 0, capacity = 0
After 1 push: size = 1, capacity = 1
After 2 push: size = 2, capacity = 2
After 3 push: size = 3, capacity = 4
After resize(5): size = 5, capacity = 6
1 2 3 0 0
After resize(2): size = 2, capacity = 6
1 2
Is empty? No
```

> **`size()` vs `capacity()` 的关键区别：**
> - `size()`：当前实际有多少个元素
> - `capacity()`：当前分配的内存能容纳多少个元素（不需要重新申请内存）
> - 当 `size() > capacity()` 时，vector 会自动扩容

#### 4. 首尾元素访问

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {10, 20, 30, 40, 50};

    // front()：返回第一个元素的引用
    cout << "front() = " << v.front() << endl;    // 输出: 10

    // back()：返回最后一个元素的引用
    cout << "back() = " << v.back() << endl;      // 输出: 50

    // 可以通过 front/back 修改元素
    v.front() = 100;
    v.back() = 500;
    cout << "After modify: front = " << v.front() << ", back = " << v.back() << endl;

    return 0;
}
```

**预期运行结果：**
```
front() = 10
back() = 50
After modify: front = 100, back = 500
```

> **注意：** 对空 vector 调用 `front()` 或 `back()` 是未定义行为。务必先检查 `!v.empty()`。

#### 5. 下标访问：`[]` 运算符 vs `at()` 方法

```cpp
#include <iostream>
#include <vector>
#include <stdexcept>   // for out_of_range
using namespace std;

int main() {
    vector<int> v = {1, 2, 3, 4, 5};

    // 方式一：[] 运算符（不检查越界）
    cout << "v[2] = " << v[2] << endl;             // 正常: 3
    // cout << v[100] << endl;                      // 危险！越界但不报错，结果是未定义行为

    // 方式二：at() 方法（检查越界）
    cout << "v.at(2) = " << v.at(2) << endl;       // 正常: 3

    // at() 越界时会抛出 out_of_range 异常
    try {
        cout << v.at(100) << endl;                  // 越界，抛出异常
    } catch (const out_of_range& e) {
        cout << "Caught exception: " << e.what() << endl;
    }

    return 0;
}
```

**预期运行结果：**
```
v[2] = 3
v.at(2) = 3
Caught exception: vector::_M_range_check: __n (which is 100) >= this->size() (which is 5)
```

> **`[]` 与 `at()` 的选择：**
> - 如果确定索引不会越界，用 `[]`（性能好，无额外开销）
> - 如果不确定索引是否越界，用 `at()`（安全，抛出异常）
> - 算法竞赛/刷题中通常用 `[]`，因为追求速度且通常不会越界

### 五、三种遍历方式

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {10, 20, 30, 40, 50};

    cout << "=== 方式一：下标遍历 ===" << endl;
    for (size_t i = 0; i < v.size(); i++) {
        cout << "v[" << i << "] = " << v[i] << endl;
    }

    cout << "=== 方式二：迭代器遍历 ===" << endl;
    for (auto it = v.begin(); it != v.end(); ++it) {
        cout << *it << " ";
    }
    cout << endl;

    cout << "=== 方式三：范围 for（C++11） ===" << endl;
    for (int x : v) {
        cout << x << " ";
    }
    cout << endl;

    // 使用引用修改元素
    cout << "=== 通过引用修改元素 ===" << endl;
    for (int& x : v) {
        x *= 2;
    }
    for (int x : v) cout << x << " ";
    cout << endl;

    return 0;
}
```

**预期运行结果：**
```
=== 方式一：下标遍历 ===
v[0] = 10
v[1] = 20
v[2] = 30
v[3] = 40
v[4] = 50
=== 方式二：迭代器遍历 ===
10 20 30 40 50
=== 方式三：范围 for（C++11） ===
10 20 30 40 50
=== 通过引用修改元素 ===
20 40 60 80 100
```

> **三种方式的选择建议：**
> - **下标遍历**：最直观，需要索引时用
> - **迭代器遍历**：C++ 标准风格，通用性最强（对其他容器也适用），但语法相对繁琐
> - **范围 for**：C++11 起推荐，简洁优雅，无需关心索引或迭代器

### 六、性能说明

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| 随机访问（`[]` / `at()`） | O(1) | 连续内存，直接计算偏移 |
| 尾部插入 `push_back()` | **均摊** O(1) | 扩容时需拷贝所有元素，但扩容不频繁 |
| 尾部删除 `pop_back()` | O(1) | 直接减小 size，不释放内存 |
| 中间/头部插入 `insert()` | O(n) | 需要移动后续所有元素 |
| 中间/头部删除 `erase()` | O(n) | 需要移动后续所有元素 |
| 查找（未排序） | O(n) | 线性搜索 |
| 排序后二分查找 | O(log n) | 需先调用 `std::sort()` |

### 七、注意事项与常见坑

#### 1. 迭代器失效

对 vector 进行插入或删除操作后，之前获取的迭代器、指针、引用**可能失效**：

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {1, 2, 3, 4, 5};

    auto it = v.begin();          // 指向 v[0]
    v.push_back(6);               // 可能触发扩容，it 可能失效！
    // cout << *it;               // 危险！未定义行为

    // 正确做法：重新获取迭代器
    it = v.begin();
    cout << *it << endl;           // 安全

    return 0;
}
```

#### 2. 扩容的代价

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    // 如果预先知道需要存储大量元素，使用 reserve 可以避免多次扩容
    vector<int> v;
    v.reserve(1000);               // 预先分配 1000 个元素的空间

    for (int i = 0; i < 1000; i++) {
        v.push_back(i);            // 不会触发扩容，性能更好
    }

    cout << "size = " << v.size() << ", capacity = " << v.capacity() << endl;

    return 0;
}
```

#### 3. 二维 vector

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    // 创建 3 行 4 列的二维 vector
    vector<vector<int>> matrix(3, vector<int>(4, 0));

    // 赋值和访问
    matrix[1][2] = 5;

    // 遍历二维 vector
    for (const auto& row : matrix) {
        for (int x : row) {
            cout << x << " ";
        }
        cout << endl;
    }

    return 0;
}
```

**预期运行结果：**
```
0 0 0 0
0 0 5 0
0 0 0 0
```

#### 4. `push_back` vs `emplace_back`

`emplace_back` 在 C++11 中引入，它在容器尾部**直接构造**元素，而 `push_back` 先构造再拷贝/移动。对于自定义类型，`emplace_back` 通常更高效：

```cpp
#include <iostream>
#include <vector>
using namespace std;

struct Point {
    int x, y;
    Point(int a, int b) : x(a), y(b) {
        cout << "Point(" << x << "," << y << ") constructed" << endl;
    }
};

int main() {
    vector<Point> v;
    v.reserve(10);

    cout << "Using emplace_back:" << endl;
    v.emplace_back(1, 2);     // 直接构造，只有 1 次构造

    cout << "Using push_back:" << endl;
    v.push_back(Point(3, 4)); // 构造 + 拷贝（或移动），至少 2 次构造

    return 0;
}
```

### 八、完整可运行示例

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    cout << "========== vector 综合示例 ==========" << endl;

    // 1. 创建 vector
    vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};

    cout << "初始元素: ";
    for (int x : v) cout << x << " ";
    cout << endl;
    cout << "size = " << v.size() << ", capacity = " << v.capacity() << endl;

    // 2. 添加元素
    v.push_back(5);
    v.push_back(3);
    cout << "push_back 5, 3 后: ";
    for (int x : v) cout << x << " ";
    cout << endl;

    // 3. 访问元素
    cout << "首元素: " << v.front() << endl;
    cout << "尾元素: " << v.back() << endl;
    cout << "v[3] = " << v[3] << ", v.at(3) = " << v.at(3) << endl;

    // 4. 删除元素
    v.pop_back();
    cout << "pop_back 后: ";
    for (int x : v) cout << x << " ";
    cout << endl;

    // 5. 重新调整大小
    v.resize(5);
    cout << "resize(5) 后: ";
    for (int x : v) cout << x << " ";
    cout << endl;

    // 6. 多维 vector
    cout << "\n--- 二维 vector ---" << endl;
    vector<vector<int>> matrix(3, vector<int>(4));

    // 填充
    int val = 1;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 4; j++) {
            matrix[i][j] = val++;
        }
    }

    // 打印
    for (const auto& row : matrix) {
        for (int x : row) {
            cout << x << "\t";
        }
        cout << endl;
    }

    return 0;
}
```

**预期运行结果：**
```
========== vector 综合示例 ==========
初始元素: 3 1 4 1 5 9 2 6
size = 8, capacity = 8
push_back 5, 3 后: 3 1 4 1 5 9 2 6 5 3
首元素: 3
尾元素: 3
v[3] = 1, v.at(3) = 1
pop_back 后: 3 1 4 1 5 9 2 6 5
resize(5) 后: 3 1 4 1 5

--- 二维 vector ---
1	2	3	4
5	6	7	8
9	10	11	12
```

### 九、总结

- `vector` 是 C++ 中最常用的容器，适合需要**动态增长**且**随机访问**频繁的场景
- 尾部添加/删除效率高（均摊 O(1)），中间插入/删除效率低（O(n)）
- `[]` 不检查越界，`at()` 检查越界但有小性能开销
- 预先调用 `reserve()` 可以避免多次扩容，提升大量添加元素时的性能
- 遍历有下标、迭代器、范围 for 三种方式，推荐使用范围 for（C++11 起）
