---
title: 基于范围的for循环
author: claudecode(deepseekV4flash)
date: 2026-07-20 21:40:47
description: 基于范围的for循环
tags:
  - Cpp算法
categories:
  - guide
  - C++算法入门
---

# 基于范围的 for 循环

## 1. 为什么需要范围 for 循环？

在 C++11 之前，遍历一个容器（如 `vector`、`set`、`map`）通常需要这样写：

```cpp
// 传统 for 循环遍历 vector
vector<int> v = {1, 2, 3, 4, 5};
for (vector<int>::iterator it = v.begin(); it != v.end(); ++it) {
    cout << *it << " ";
}

// 传统 for 循环遍历数组
int arr[] = {1, 2, 3, 4, 5};
for (int i = 0; i < 5; i++) {
    cout << arr[i] << " ";
}
```

这种写法不仅冗长，而且容易出错（比如下标越界、迭代器写错类型等）。

C++11 引入了**基于范围的 for 循环（range-based for loop）**，让遍历操作变得极其简洁：

```cpp
vector<int> v = {1, 2, 3, 4, 5};
for (int i : v) {
    cout << i << " ";  // 简洁、安全、直观
}
```

## 2. 原理简述

基于范围的 for 循环是**语法糖**，编译器会将它展开为传统的迭代器循环。例如：

```cpp
for (int i : v) {
    cout << i;
}
```

编译器会将其展开为类似这样的代码（伪代码）：

```cpp
auto __begin = begin(v);   // v.begin() 或 std::begin(v)
auto __end = end(v);       // v.end() 或 std::end(v)
for (; __begin != __end; ++__begin) {
    int i = *__begin;
    cout << i;
}
```

这意味着：
- 任何支持 `begin()` 和 `end()` 的容器都可以使用范围 for
- 原生数组也可以（编译器使用 `std::begin` 和 `std::end` 重载）
- 运行时性能和手写迭代器循环完全一样，没有额外开销

## 3. 三种基本遍历方式

### 3.1 传值方式（遍历副本）

```cpp
for (int i : arr) {
    // i 是每个元素的副本
    // 修改 i 不会影响原数组/容器中的元素
}
```

**特点：**
- 遍历的是元素的**拷贝**
- 修改 `i` **不会**影响原始数据
- 如果元素类型较大（如 `string`），会有复制开销

### 3.2 引用方式（可修改原值）

```cpp
for (int &i : arr) {
    // i 是每个元素的引用（别名）
    // 修改 i 会直接修改原数组/容器中的元素
}
```

**特点：**
- 遍历的是元素的引用
- 修改 `i` **会**影响原始数据
- **没有**复制开销
- 可以用于修改容器的元素

### 3.3 const 引用方式（只读且高效）

```cpp
for (const int &i : arr) {
    // i 是每个元素的只读引用
    // 不能通过 i 修改元素
    // 没有复制开销
}
```

**特点：**
- 只读访问，不能修改元素
- 没有复制开销
- 适合遍历大型对象

## 4. 完整对比示例

```cpp
#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    vector<int> v = {1, 2, 3, 4, 5};

    // ========== 方式 1：传值（副本） ==========
    cout << "方式 1——传值（修改副本）：" << endl;
    for (int i : v) {
        i *= 10;  // 只修改了副本
    }
    cout << "原始 vector：";
    for (int i : v) {
        cout << i << " ";
    }
    cout << "（未受影响）" << endl;

    // ========== 方式 2：引用（可修改原值） ==========
    cout << "\n方式 2——引用（修改原值）：" << endl;
    for (int &i : v) {
        i *= 10;  // 直接修改了原始元素
    }
    cout << "原始 vector：";
    for (int i : v) {
        cout << i << " ";
    }
    cout << "（已翻 10 倍）" << endl;

    // ========== 方式 3：const 引用（只读） ==========
    cout << "\n方式 3——const 引用（只读）：" << endl;
    const vector<string> words = {"Hello", "C++11", "World"};
    for (const string &w : words) {
        cout << w << " ";
        // w = "xxx";  // 编译错误！const 引用不能赋值
    }
    cout << "（const 引用，不会复制字符串）" << endl;

    // ========== 展示复制开销的差异 ==========
    cout << "\n方式对比总结（针对 vector<int>）：" << endl;
    cout << "传值:      复制 int（小开销，但无法修改原值）" << endl;
    cout << "引用:      不复制，可修改原值" << endl;
    cout << "const 引用: 不复制，只读" << endl;

    return 0;
}
```

**预期输出：**

```
方式 1——传值（修改副本）：
原始 vector：1 2 3 4 5 （未受影响）

方式 2——引用（修改原值）：
原始 vector：10 20 30 40 50 （已翻 10 倍）

方式 3——const 引用（只读）：
Hello C++11 World （const 引用，不会复制字符串）

方式对比总结（针对 vector<int>）：
传值:      复制 int（小开销，但无法修改原值）
引用:      不复制，可修改原值
const 引用: 不复制，只读
```

## 5. 配合 auto 使用

在实际开发中，`auto` 和范围 for 几乎总是搭配使用，编译器会根据容器元素类型自动推导：

```cpp
#include <iostream>
#include <vector>
#include <map>
#include <string>
using namespace std;

int main() {
    vector<int> v = {1, 2, 3, 4, 5};

    // auto 传值，自动推导元素类型为 int
    cout << "auto 传值: ";
    for (auto i : v) {
        cout << i << " ";
    }
    cout << endl;

    // auto& 引用，可以修改原值
    cout << "auto& 引用翻倍: ";
    for (auto &i : v) {
        i *= 2;
    }
    for (auto i : v) {
        cout << i << " ";
    }
    cout << endl;

    // const auto& 只读引用，高效且安全
    const vector<string> words = {"apple", "banana", "cherry"};
    cout << "const auto& 遍历 string: ";
    for (const auto &w : words) {
        cout << w << " ";
        // w = "xxx";  // 编译错误
    }
    cout << endl;

    // 遍历 map（元素是 pair）
    map<string, int> scores = {{"Alice", 95}, {"Bob", 87}};
    cout << "const auto& 遍历 map: ";
    for (const auto &p : scores) {
        cout << p.first << ":" << p.second << " ";
    }
    cout << endl;

    return 0;
}
```

**预期输出：**

```
auto 传值: 1 2 3 4 5
auto& 引用翻倍: 2 4 6 8 10
const auto& 遍历 string: apple banana cherry
const auto& 遍历 map: Alice:95 Bob:87
```

> **建议**：在范围 for 中，对于基本类型（int、char 等），用 `auto` 传值即可；对于复杂类型（string、自定义类等），优先使用 `const auto &`（只读）或 `auto &`（需修改）。

## 6. 适用范围

基于范围的 for 循环适用于所有**支持 begin()/end() 的容器**：

| 容器类型 | 是否支持 | 说明 |
|---------|:-------:|------|
| 原生数组 `T arr[N]` | 支持 | 编译器推导长度 |
| `vector<T>` | 支持 | |
| `list<T>` | 支持 | |
| `deque<T>` | 支持 | |
| `set<T>` / `multiset<T>` | 支持 | |
| `map<K,V>` / `multimap<K,V>` | 支持 | 元素类型是 `pair<const K, V>` |
| `unordered_set<T>` | 支持 | |
| `unordered_map<K,V>` | 支持 | |
| `string` | 支持 | 元素类型是 `char` |
| 动态分配的数组 `new T[n]` | **不支持** | 只有引用和数组名才有范围语义 |
| 链表节点等无 begin/end 的自定义类型 | **不支持** | 需要自己实现迭代器 |

```cpp
#include <iostream>
#include <vector>
#include <list>
#include <set>
#include <map>
#include <string>
#include <unordered_set>
#include <unordered_map>
using namespace std;

int main() {
    // 原生数组
    cout << "=== 原生数组 ===" << endl;
    int arr[] = {1, 2, 3, 4, 5};
    for (int x : arr) cout << x << " ";
    cout << endl;

    // vector
    cout << "=== vector ===" << endl;
    vector<string> v = {"a", "b", "c"};
    for (const auto &s : v) cout << s << " ";
    cout << endl;

    // set
    cout << "=== set ===" << endl;
    set<int> s = {5, 1, 3, 2, 4};
    for (int x : s) cout << x << " ";  // 自动排序
    cout << endl;

    // map
    cout << "=== map ===" << endl;
    map<int, string> m = {{1, "one"}, {2, "two"}, {3, "three"}};
    for (const auto &p : m) {
        cout << p.first << "->" << p.second << " ";
    }
    cout << endl;

    // string（按字符遍历）
    cout << "=== string ===" << endl;
    string text = "hello";
    for (char c : text) cout << "[" << c << "]";
    cout << endl;

    // unordered_set
    cout << "=== unordered_set ===" << endl;
    unordered_set<int> us = {10, 20, 30, 40, 50};
    for (int x : us) cout << x << " ";  // 无序输出
    cout << endl;

    return 0;
}
```

**预期输出**（顺序因 unordered_set 的实现可能不同）：

```
=== 原生数组 ===
1 2 3 4 5
=== vector ===
a b c
=== set ===
1 2 3 4 5
=== map ===
1->one 2->two 3->three
=== string ===
[h][e][l][l][o]
=== unordered_set ===
50 40 30 20 10
```

## 7. 注意事项和常见坑

### 7.1 遍历过程中不能修改容器大小

在范围 for 循环中**添加或删除元素**会导致迭代器失效，程序可能崩溃：

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {1, 2, 3, 4, 5};

    // 错误示范：在遍历过程中删除元素
    // for (auto it = v.begin(); it != v.end(); ++it) { // 等价展开
    for (int x : v) {
        if (x % 2 == 0) {
            // 删除偶数——危险！
            // v.erase(...);  // 迭代器可能失效！
        }
    }

    // 正确做法：使用传统迭代器循环并处理返回值
    for (auto it = v.begin(); it != v.end(); ) {
        if (*it % 2 == 0) {
            it = v.erase(it);  // erase 返回下一个有效迭代器
        } else {
            ++it;
        }
    }

    cout << "删除偶数后: ";
    for (int x : v) cout << x << " ";
    cout << endl;

    return 0;
}
```

**预期输出：**

```
删除偶数后: 1 3 5
```

### 7.2 传值方式修改不生效

这是最常见的新手错误——使用 `auto`（传值）遍历，发现对元素的修改没有反映到容器中：

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {1, 2, 3};

    // 错误：auto 传值，修改的是副本
    for (auto i : v) {
        i *= 10;
    }
    cout << "用 auto 传值修改后: ";
    for (auto i : v) cout << i << " ";  // 仍然是 1 2 3
    cout << endl;

    // 正确：auto& 引用，修改原值
    for (auto &i : v) {
        i *= 10;
    }
    cout << "用 auto& 引用修改后: ";
    for (auto i : v) cout << i << " ";  // 变为 10 20 30
    cout << endl;

    return 0;
}
```

**预期输出：**

```
用 auto 传值修改后: 1 2 3
用 auto& 引用修改后: 10 20 30
```

### 7.3 数组退化为指针（size 信息丢失）

当数组作为函数参数传递时，会退化为指针，此时范围 for 会失效，因为编译器不知道数组的大小：

```cpp
#include <iostream>
using namespace std;

// 错误：arr 已经退化为指针，不是数组
void printArray_bad(int arr[]) {
    // 编译错误！arr 是指针，没有 begin/end
    // for (int x : arr) {  // 不编译！
    //     cout << x << " ";
    // }
}

// 正确方式：传递引用以保留数组大小信息
void printArray_good(const int (&arr)[5]) {
    for (int x : arr) {
        cout << x << " ";
    }
    cout << endl;
}

int main() {
    int arr[] = {10, 20, 30, 40, 50};
    printArray_good(arr);
    return 0;
}
```

但是更好的做法是直接使用 `vector`。

### 7.4 不要在范围 for 中修改 map 的 key

遍历 `map` 时，key 是 `const` 的（`pair<const K, V>`），尝试修改 key 会导致编译错误：

```cpp
map<string, int> m = {{"a", 1}, {"b", 2}};
for (auto &p : m) {
    // p.first = "c";   // 编译错误！key 是 const
    p.second = 999;      // 正确，可以修改 value
}
```

## 8. 综合练习

```cpp
#include <iostream>
#include <vector>
#include <map>
#include <string>
using namespace std;

int main() {
    // 练习 1：遍历并修改 vector
    vector<double> prices = {9.99, 19.99, 29.99, 39.99};
    cout << "原价: ";
    for (auto p : prices) cout << p << " ";
    cout << endl;

    // 打 8 折
    for (auto &p : prices) {
        p *= 0.8;
    }
    cout << "8 折后: ";
    for (auto p : prices) cout << p << " ";
    cout << endl;

    // 练习 2：统计 map 中 value 的总和
    map<string, int> inventory = {{"apple", 10}, {"banana", 5}, {"orange", 8}};
    int total = 0;
    for (const auto &item : inventory) {
        total += item.second;
    }
    cout << "库存总数: " << total << endl;

    // 练习 3：找出 vector 中的最大值
    vector<int> scores = {78, 92, 85, 96, 88, 73};
    int max_score = scores[0];
    for (int s : scores) {
        if (s > max_score) max_score = s;
    }
    cout << "最高分: " << max_score << endl;

    return 0;
}
```

**预期输出：**

```
原价: 9.99 19.99 29.99 39.99
8 折后: 7.992 15.992 23.992 31.992
库存总数: 23
最高分: 96
```

## 9. 小结

- 基于范围的 for 循环是 C++11 提供的**语法糖**，编译期展开为迭代器循环，**无运行时开销**
- 三种方式：`auto`（传值）、`auto &`（引用）、`const auto &`（const 引用）
- **传值**修改不影响原容器；**引用**修改反映到原容器
- 适用于所有有 `begin()/end()` 的容器，包括原生数组
- **禁止**在遍历过程中增删容器元素
- 建议：基本类型用 `auto`，复杂类型或需要修改用 `auto &`，只读用 `const auto &`
