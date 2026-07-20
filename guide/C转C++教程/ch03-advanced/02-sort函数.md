---
title: sort函数
author: claudecode(deepseekV4flash)
date: 2026-07-20 21:39:51
description: sort函数
tags:
  - Cpp算法
categories:
  - guide
  - C++算法入门
---

# sort 函数：高效排序

## 1. sort 概述

`sort` 是 C++ 标准库 `<algorithm>` 头文件中提供的排序函数，它是 C++ 中最常用的排序工具。与 C 语言的 `qsort` 相比，`sort` 具有类型安全、使用简便、性能优异的优点。

### 头文件

```cpp
#include <algorithm>
```

### 函数原型

```cpp
template<class RandomIt>
void sort(RandomIt first, RandomIt last);

template<class RandomIt, class Compare>
void sort(RandomIt first, RandomIt last, Compare comp);
```

- `first`：指向待排序范围起始的迭代器
- `last`：指向待排序范围末尾的迭代器（**开区间**，即 last 指向的元素不参与排序）
- `comp`：可选的比较函数/函数对象（见下一节）

---

## 2. 算法原理：内省排序（IntroSort）

`std::sort` 通常实现为**内省排序（IntroSort）**，它是一种混合排序算法：

1. **快速排序（QuickSort）**：作为主要排序算法，平均时间复杂度 O(n log n)
2. **堆排序（HeapSort）**：当快速排序的递归深度超过一定限度时切换，避免最坏情况 O(n^2)
3. **插入排序（InsertionSort）**：当子数组规模较小时（通常小于 16 个元素），在小数据集上插入排序效率更高

这种混合策略保证了：
- 最坏情况时间复杂度为 O(n log n)
- 平均性能极佳
- 不需要额外的辅助空间（原地排序）

---

## 3. 适用范围

`sort` 要求传入**随机访问迭代器（Random Access Iterator）**，因此适用于：

| 容器 | 是否支持 sort | 说明 |
|------|:-------------:|------|
| 原生数组 | 是 | `sort(arr, arr + n)` |
| `vector` | 是 | `sort(v.begin(), v.end())` |
| `deque` | 是 | `sort(d.begin(), d.end())` |
| `array` (C++11) | 是 | `sort(a.begin(), a.end())` |
| `string` | 是 | `sort(s.begin(), s.end())` |
| `list` | **否** | 必须使用 `list::sort()` 成员函数 |
| `forward_list` | **否** | 必须使用 `forward_list::sort()` 成员函数 |

**为什么 list 不能使用 std::sort？**

`list` 是双向链表，只提供**双向迭代器（Bidirectional Iterator）**，不支持随机访问（不能进行 `it + n` 这样的操作）。而 `sort` 需要随机访问迭代器才能高效工作。链表排序应使用其成员函数 `list::sort()`。

---

## 4. 基本用法

### 4.1 对数组排序

```cpp
#include <algorithm>
#include <iostream>
using namespace std;

int main() {
    int arr[] = {5, 2, 8, 1, 9, 3};

    // 对数组排序：arr 是首地址，arr + 6 是尾后地址
    sort(arr, arr + 6);

    cout << "排序结果：";
    for (int i = 0; i < 6; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;

    return 0;
}
```

**预期输出**：

```
排序结果：1 2 3 5 8 9
```

`sort(arr, arr + n)` 中：
- `arr` 是数组首元素的地址，等价于 `&arr[0]`
- `arr + n` 是尾后地址，等价于 `&arr[n]`，该元素不参与排序
- 排序范围是 **[arr, arr + n)**，即左闭右开区间

### 4.2 对 vector 排序

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {5, 2, 8, 1, 9, 3};

    // 对 vector 排序：传入 begin() 和 end() 迭代器
    sort(v.begin(), v.end());

    cout << "排序结果：";
    for (int x : v) {
        cout << x << " ";
    }
    cout << endl;

    return 0;
}
```

**预期输出**：

```
排序结果：1 2 3 5 8 9
```

### 4.3 对 string 排序

```cpp
#include <algorithm>
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "hello";

    sort(s.begin(), s.end());

    cout << "排序结果：" << s << endl;

    return 0;
}
```

**预期输出**：

```
排序结果：ehllo
```

### 4.4 部分排序

```cpp
#include <algorithm>
#include <iostream>
using namespace std;

int main() {
    int arr[] = {5, 2, 8, 1, 9, 3, 7, 4, 6};

    // 只对前 5 个元素排序，后面 4 个保持原顺序
    sort(arr, arr + 5);

    cout << "部分排序结果：";
    for (int i = 0; i < 9; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;

    return 0;
}
```

**预期输出**：

```
部分排序结果：1 2 5 8 9 3 7 4 6
```

---

## 5. 默认排序规则

默认情况下，`sort` 使用 `operator<` 进行比较，结果按**升序（从小到大）**排列。

```cpp
#include <algorithm>
#include <iostream>
using namespace std;

int main() {
    int arr[] = {3, 1, 4, 1, 5, 9, 2, 6};

    // 升序排序
    sort(arr, arr + 8);

    cout << "升序排序：";
    for (int x : arr) cout << x << " ";
    cout << endl;

    return 0;
}
```

**预期输出**：

```
升序排序：1 1 2 3 4 5 6 9
```

如果需要降序或自定义排序规则，需要提供自定义比较函数（见下一节）。

---

## 6. 时间复杂度

- **平均情况**：O(n log n)
- **最坏情况**：O(n log n)（归功于内省排序，避免了快速排序的最坏情况 O(n^2)）
- **最佳情况**：O(n log n)（有些实现会对近乎有序的序列进行优化，但标准未做此保证）

空间复杂度：O(log n)（递归调用栈的深度）

---

## 7. 综合示例

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    cout << "========== sort 综合示例 ==========\n\n";

    // 1. 数组排序
    cout << "--- 1. 数组排序 ---\n";
    int arr[] = {42, 7, 15, 3, 8, 22, 31, 10};
    int n = sizeof(arr) / sizeof(arr[0]);

    sort(arr, arr + n);
    cout << "数组升序：";
    for (int i = 0; i < n; i++) cout << arr[i] << " ";
    cout << "\n\n";

    // 2. vector 排序
    cout << "--- 2. vector 排序 ---\n";
    vector<double> v = {3.14, 2.71, 1.41, 1.73, 2.23};
    sort(v.begin(), v.end());
    cout << "vector 升序：";
    for (double x : v) cout << x << " ";
    cout << "\n\n";

    // 3. string 排序
    cout << "--- 3. string 排序 ---\n";
    string s = "algorithm";
    sort(s.begin(), s.end());
    cout << "字符串排序后：" << s << "\n\n";

    // 4. 部分排序
    cout << "--- 4. 部分排序 ---\n";
    int arr2[] = {9, 8, 7, 6, 5, 4, 3, 2, 1};
    sort(arr2, arr2 + 4);  // 只排前 4 个
    cout << "前 4 个元素排序：";
    for (int x : arr2) cout << x << " ";
    cout << "\n\n";

    // 5. 降序（使用 greater<T>）
    cout << "--- 5. 降序排序（利用 greater<T>）---\n";
    vector<int> v2 = {5, 2, 8, 1, 9, 3};
    sort(v2.begin(), v2.end(), greater<int>());
    cout << "降序：";
    for (int x : v2) cout << x << " ";
    cout << "\n\n";

    // 6. 验证 list 不能使用 std::sort（编译错误）
    cout << "--- 6. 说明 ---\n";
    cout << "std::sort 不支持 list，必须用 list::sort()\n";

    return 0;
}
```

**预期输出**：

```
========== sort 综合示例 ==========

--- 1. 数组排序 ---
数组升序：3 7 8 10 15 22 31 42

--- 2. vector 排序 ---
vector 升序：1.41 1.73 2.23 2.71 3.14

--- 3. string 排序 ---
字符串排序后：aghilmort

--- 4. 部分排序 ---
前 4 个元素排序：6 7 8 9 5 4 3 2 1

--- 5. 降序排序（利用 greater<T>）---
降序：9 8 5 3 2 1

--- 6. 说明 ---
std::sort 不支持 list，必须用 list::sort()
```

---

## 8. 常见坑与注意事项

1. **迭代器范围是左闭右开**：`sort(first, last)` 排序的范围是 `[first, last)`，即 last 指向的元素**不参与排序**。常见的错误是对数组使用 `sort(arr, arr + n - 1)`，这会导致最后一个元素未被排序。

2. **不能对 list 使用 std::sort**：`std::list` 只提供双向迭代器，不满足随机访问迭代器的要求。编译时会出现大量模板错误信息。

3. **sort 是不稳定排序**：`std::sort` 不保证相等元素的相对顺序。如果需要稳定排序，使用 `std::stable_sort`，它的时间复杂度为 O(n log^2 n)，在内存充足时退化为 O(n log n)。

4. **不要对已排序的迭代器范围重复排序**：虽然不会出错，但浪费性能。如果需要在有序序列中插入新元素，使用 `lower_bound` / `upper_bound` 找到插入位置，然后用 `vector::insert`。

5. **默认行为是升序**：`sort(v.begin(), v.end())` 默认按升序（从小到大）排序。如果需要降序，使用 `greater<T>()` 或自定义比较函数。

6. **`greater<T>()` 需要头文件 `<functional>`**：实际上 `<algorithm>` 通常会间接包含它，但明确包含 `<functional>` 是好的编程习惯。

7. **对 const 容器无法排序**：`sort` 会修改容器中的元素，因此不能对 const 容器或通过 const 引用传入的容器排序。

8. **自定义比较函数必须满足严格弱排序**（见下一节）。
