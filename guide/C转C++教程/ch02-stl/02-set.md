---
title: set
author: claudecode(deepseekV4flash)
date: 2026-07-20 21:40:45
description: set
tags:
  - Cpp算法
categories:
  - guide
  - C++算法入门
---

## set（集合）

### 一、概念与原理

`set` 是 C++ STL 中一种**有序且元素唯一**的容器。它的内部实现是**红黑树**（Red-Black Tree），一种自平衡的二叉搜索树。

**核心特性：**
- **有序**：元素按照键值自动升序排列（默认使用 `operator<` 比较）
- **唯一**：不允许重复元素，每个元素最多出现一次（如果尝试插入已存在的元素，插入操作会被忽略）
- **自平衡**：红黑树保证了插入、删除、查找的时间复杂度都是 O(log n）

**与 `unordered_set` 的简单对比：**

| 特性 | `set` | `unordered_set` |
|------|-------|-----------------|
| 底层结构 | 红黑树（平衡二叉搜索树） | 哈希表 |
| 元素顺序 | 升序 | 无序 |
| 时间复杂度 | O(log n) | 均摊 O(1) |
| 内存占用 | 较小（只需要树节点） | 较大（需要额外维护哈希表） |
| 需要头文件 | `<set>` | `<unordered_set>` |

> **适用场景：** 当需要元素自动排序、或者需要范围查询（如查找一定范围内的元素）时使用 `set`；当只关心快速插入/查找，不关心顺序时使用 `unordered_set`。

### 二、头文件

```cpp
#include <set>
```

### 三、创建方式

```cpp
#include <iostream>
#include <set>
using namespace std;

int main() {
    // 1. 空构造：创建一个空 set
    set<int> s1;
    cout << "s1 size = " << s1.size() << endl;          // 输出: 0

    // 2. 从初始化列表构造（C++11）
    set<int> s2 = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3};
    cout << "s2 size = " << s2.size() << " (应为 7，因为重复的被去重)" << endl;
    for (int x : s2) cout << x << " ";                   // 输出: 1 2 3 4 5 6 9
    cout << endl;

    // 3. 拷贝构造
    set<int> s3(s2);

    // 4. 指定比较方式的 set（降序）
    set<int, greater<int>> s4 = {3, 1, 4, 1, 5};
    cout << "s4 (降序): ";
    for (int x : s4) cout << x << " ";                   // 输出: 5 4 3 1
    cout << endl;

    // 5. 自定义类型的 set（需要提供比较函数）
    // 见后文"注意事项"部分

    return 0;
}
```

**预期运行结果：**
```
s1 size = 0
s2 size = 7 (应为 7，因为重复的被去重)
1 2 3 4 5 6 9
s4 (降序): 5 4 3 1
```

> **⚠ 关键点：** `set` 不支持通过下标添加内容。必须使用 `insert()` 方法。

### 四、常用操作详解

#### 1. 插入元素 insert()

```cpp
#include <iostream>
#include <set>
using namespace std;

int main() {
    set<int> s;

    // 插入单个元素
    s.insert(3);
    s.insert(1);
    s.insert(4);
    s.insert(1);              // 重复元素，插入被忽略

    cout << "size = " << s.size() << endl;               // 输出: 3
    for (int x : s) cout << x << " ";
    cout << endl;

    // insert 返回一个 pair<iterator, bool>
    // second 为 true 表示插入成功，false 表示元素已存在
    auto [it, inserted] = s.insert(5);
    cout << "插入 5: " << (inserted ? "成功" : "失败") << endl;

    auto [it2, inserted2] = s.insert(1);
    cout << "插入 1: " << (inserted2 ? "成功" : "失败") << endl;

    return 0;
}
```

**预期运行结果：**
```
size = 3
1 3 4
插入 5: 成功
插入 1: 失败
```

#### 2. 删除元素 erase()

```cpp
#include <iostream>
#include <set>
using namespace std;

int main() {
    set<int> s = {1, 2, 3, 4, 5, 6, 7};

    // 方式一：按值删除
    s.erase(3);                // 删除值为 3 的元素
    cout << "erase(3) 后: ";
    for (int x : s) cout << x << " ";
    cout << endl;              // 输出: 1 2 4 5 6 7

    // 方式二：按迭代器删除
    auto it = s.find(5);
    if (it != s.end()) {
        s.erase(it);           // 删除迭代器指向的元素
        cout << "erase(5) 后: ";
        for (int x : s) cout << x << " ";
        cout << endl;          // 输出: 1 2 4 6 7
    }

    // 方式三：删除一个范围
    auto first = s.find(2);
    auto last = s.find(6);
    if (first != s.end() && last != s.end()) {
        s.erase(first, last);  // 删除 [2, 6) 范围，即删除 2, 4
        cout << "erase [2,6) 后: ";
        for (int x : s) cout << x << " ";
        cout << endl;          // 输出: 1 6 7
    }

    return 0;
}
```

**预期运行结果：**
```
erase(3) 后: 1 2 4 5 6 7
erase(5) 后: 1 2 4 6 7
erase [2,6) 后: 1 6 7
```

#### 3. 查找元素 find() 和 count()

```cpp
#include <iostream>
#include <set>
using namespace std;

int main() {
    set<int> s = {10, 20, 30, 40, 50};

    // find()：返回迭代器，找不到返回 end()
    auto it = s.find(30);
    if (it != s.end()) {
        cout << "找到了: " << *it << endl;           // 输出: 找到了: 30
    } else {
        cout << "未找到" << endl;
    }

    it = s.find(35);
    if (it == s.end()) {
        cout << "35 不存在于集合中" << endl;         // 输出: 35 不存在于集合中
    }

    // count()：返回元素个数（对于 set 只能是 0 或 1）
    cout << "30 的个数: " << s.count(30) << endl;    // 输出: 1
    cout << "35 的个数: " << s.count(35) << endl;    // 输出: 0

    return 0;
}
```

**预期运行结果：**
```
找到了: 30
35 不存在于集合中
30 的个数: 1
35 的个数: 0
```

#### 4. lower_bound() 和 upper_bound()

这两个函数是 set 的**重要优势**，特别是在需要范围查询时：

```cpp
#include <iostream>
#include <set>
using namespace std;

int main() {
    set<int> s = {1, 3, 5, 7, 9, 11, 13};

    // lower_bound(x)：返回第一个 >= x 的元素的迭代器
    auto it1 = s.lower_bound(6);
    cout << "lower_bound(6) = " << *it1 << endl;      // 输出: 7（第一个 >=6 的元素）

    auto it2 = s.lower_bound(5);
    cout << "lower_bound(5) = " << *it2 << endl;      // 输出: 5（>=5 的第一个元素就是 5 本身）

    // upper_bound(x)：返回第一个 > x 的元素的迭代器
    auto it3 = s.upper_bound(6);
    cout << "upper_bound(6) = " << *it3 << endl;      // 输出: 7（第一个 >6 的元素）

    auto it4 = s.upper_bound(5);
    cout << "upper_bound(5) = " << *it4 << endl;      // 输出: 7（第一个 >5 的是 7，不是 5）

    // 实用技巧：用 lower_bound 和 upper_bound 配合打印区间
    cout << "\n区间 [3, 9] 内的元素: ";
    auto low = s.lower_bound(3);
    auto high = s.upper_bound(9);
    for (auto it = low; it != high; ++it) {
        cout << *it << " ";                            // 输出: 3 5 7 9
    }
    cout << endl;

    return 0;
}
```

**预期运行结果：**
```
lower_bound(6) = 7
lower_bound(5) = 5
upper_bound(6) = 7
upper_bound(5) = 7

区间 [3, 9] 内的元素: 3 5 7 9
```

> **lower_bound vs upper_bound 总结：**
> - `lower_bound(x)`：第一个 `>= x` 的元素
> - `upper_bound(x)`：第一个 `> x` 的元素
> - 所以在 set 中，对于不存在的元素，两者返回相同；对于存在的元素，`upper_bound` 会返回下一个元素

#### 5. 其他常用操作

```cpp
#include <iostream>
#include <set>
using namespace std;

int main() {
    set<int> s = {2, 4, 6, 8, 10};

    // size()：元素个数
    cout << "size = " << s.size() << endl;              // 输出: 5

    // empty()：是否为空
    cout << "empty = " << (s.empty() ? "yes" : "no") << endl;  // 输出: no

    // clear()：清空所有元素
    s.clear();
    cout << "after clear, size = " << s.size() << endl; // 输出: 0
    cout << "empty = " << (s.empty() ? "yes" : "no") << endl;  // 输出: yes

    // max_size()：最多能容纳的元素个数（取决于系统/内存）
    cout << "max_size = " << s.max_size() << endl;
    // 通常是一个很大的数，如 461168601842738790

    return 0;
}
```

### 五、遍历方式

```cpp
#include <iostream>
#include <set>
using namespace std;

int main() {
    set<int> s = {5, 2, 8, 1, 9, 3};

    cout << "=== 方式一：迭代器遍历 ===" << endl;
    for (auto it = s.begin(); it != s.end(); ++it) {
        cout << *it << " ";
    }
    cout << endl;

    cout << "=== 方式二：范围 for（推荐） ===" << endl;
    for (int x : s) {
        cout << x << " ";
    }
    cout << endl;

    // 反向遍历
    cout << "=== 方式三：反向迭代器 ===" << endl;
    for (auto it = s.rbegin(); it != s.rend(); ++it) {
        cout << *it << " ";
    }
    cout << endl;

    return 0;
}
```

**预期运行结果：**
```
=== 方式一：迭代器遍历 ===
1 2 3 5 8 9
=== 方式二：范围 for（推荐） ===
1 2 3 5 8 9
=== 方式三：反向迭代器 ===
9 8 5 3 2 1
```

### 六、性能说明

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| 插入 `insert()` | O(log n) | 红黑树的自平衡插入 |
| 删除 `erase()` | O(log n) | 红黑树的自平衡删除 |
| 查找 `find()` | O(log n) | 树的高度为 log n |
| 判断存在 `count()` | O(log n) | 实际上就是 find 的封装 |
| `lower_bound()` | O(log n) | 二分查找 |
| `upper_bound()` | O(log n) | 二分查找 |
| 遍历 | O(n) | 中序遍历 |
| 清空 `clear()` | O(n) | 需要释放所有节点 |

### 七、注意事项与常见坑

#### 1. set 插入重复元素不会报错，但插入会被忽略

```cpp
set<int> s;
s.insert(1);
s.insert(1);     // 什么都不会发生，set 仍然只有一个元素
// 可以通过 insert 的返回值判断是否插入成功
auto [it, ok] = s.insert(1);
cout << boolalpha << ok << endl;   // 输出: false
```

#### 2. set 的元素本身不能修改

set 中的元素是 `const` 的，不能通过迭代器修改元素值：

```cpp
set<int> s = {1, 2, 3};
auto it = s.begin();
// *it = 10;     // 编译错误！不能通过迭代器修改 set 中的元素
```

如果需要修改，必须先删除再插入。

#### 3. 自定义类型的存储

如果需要将自定义类型存入 set，必须提供比较运算符或自定义比较函数：

```cpp
#include <iostream>
#include <set>
#include <string>
using namespace std;

struct Person {
    string name;
    int age;
};

// 方式一：定义 operator<
bool operator<(const Person& a, const Person& b) {
    return a.age < b.age;        // 按年龄排序
}

int main() {
    set<Person> people;
    people.insert({"Alice", 25});
    people.insert({"Bob", 20});
    people.insert({"Charlie", 30});

    for (const auto& p : people) {
        cout << p.name << " (" << p.age << ")" << endl;
    }

    return 0;
}
```

**预期运行结果：**
```
Bob (20)
Alice (25)
Charlie (30)
```

#### 4. erase 迭代器时的注意事项

在使用迭代器删除元素时，旧迭代器会失效：

```cpp
set<int> s = {1, 2, 3, 4, 5};

// 正确用法：erase 返回下一个有效的迭代器（C++11）
for (auto it = s.begin(); it != s.end(); ) {
    if (*it % 2 == 0) {
        it = s.erase(it);      // erase 返回下一个迭代器
    } else {
        ++it;
    }
}
// s = {1, 3, 5}
```

#### 5. `std::multiset` 简介

如果需要一个**有序但允许重复元素**的容器，可以使用 `multiset`：

```cpp
#include <iostream>
#include <set>
using namespace std;

int main() {
    multiset<int> ms = {1, 1, 2, 2, 2, 3};
    cout << "multiset: ";
    for (int x : ms) cout << x << " ";
    cout << endl;

    cout << "1 的个数: " << ms.count(1) << endl;        // 输出: 2
    cout << "2 的个数: " << ms.count(2) << endl;        // 输出: 3

    return 0;
}
```

**预期运行结果：**
```
multiset: 1 1 2 2 2 3
1 的个数: 2
2 的个数: 3
```

### 八、完整可运行示例

```cpp
#include <iostream>
#include <set>
#include <string>
using namespace std;

int main() {
    cout << "========== set 综合示例 ==========" << endl;

    // 1. 创建并插入 —— 展示 set 的去重和排序特性
    set<int> scores;

    // 模拟输入一批分数
    int input[] = {85, 92, 78, 85, 90, 92, 60, 70, 88, 78};
    for (int s : input) {
        scores.insert(s);
    }

    cout << "输入了 " << sizeof(input)/sizeof(input[0]) << " 个分数，去重后剩余 ";
    cout << scores.size() << " 个" << endl;
    cout << "排序后的分数: ";
    for (int s : scores) cout << s << " ";
    cout << endl;

    // 2. 查找操作
    int query = 85;
    if (scores.find(query) != scores.end()) {
        cout << "分数 " << query << " 存在" << endl;
    } else {
        cout << "分数 " << query << " 不存在" << endl;
    }

    // 3. 范围查询
    cout << "\n--- 范围查询示例 ---" << endl;
    set<int> numbers = {1, 4, 7, 10, 13, 16, 19, 22};

    int left = 5, right = 15;
    auto low = numbers.lower_bound(left);
    auto high = numbers.upper_bound(right);

    cout << "区间 [" << left << ", " << right << "] 内的元素: ";
    for (auto it = low; it != high; ++it) {
        cout << *it << " ";
    }
    cout << endl;

    // 4. 删除操作
    cout << "\n--- 删除操作 ---" << endl;
    set<string> names = {"Charlie", "Alice", "Bob", "David", "Eve"};
    cout << "原始: ";
    for (const auto& name : names) cout << name << " ";
    cout << endl;

    // 按值删除
    names.erase("Bob");
    cout << "删除 Bob 后: ";
    for (const auto& name : names) cout << name << " ";
    cout << endl;

    return 0;
}
```

**预期运行结果：**
```
========== set 综合示例 ==========
输入了 10 个分数，去重后剩余 7 个
排序后的分数: 60 70 78 85 88 90 92
分数 85 存在

--- 范围查询示例 ---
区间 [5, 15] 内的元素: 7 10 13

--- 删除操作 ---
原始: Alice Bob Charlie David Eve
删除 Bob 后: Alice Charlie David Eve
```

### 九、总结

- `set` 是基于红黑树的有序容器，元素自动升序且唯一
- 插入、删除、查找均为 O(log n)，性能稳定
- 不支持通过下标或迭代器修改元素，需要修改时必须先删除再插入
- `lower_bound()` 和 `upper_bound()` 是 set 特有的优势功能，适合范围查询
- 需要有序且唯一时用 `set`；需要有序但可重复时用 `multiset`；只需快速存取时用 `unordered_set`
