---
title: 自定义cmp函数
author: claudecode(deepseekV4flash)
date: 2026-07-20 21:39:51
description: 自定义cmp函数
tags:
  - Cpp算法
categories:
  - guide
  - C++算法入门
---

# 自定义 cmp 函数：掌控排序规则

## 1. 为什么需要自定义比较函数

`sort` 默认使用 `operator<` 进行升序排序。但在实际开发中，我们往往需要：

- **降序排序**：从大到小排列
- **结构体排序**：按照对象的某个（或多个）字段排序
- **特殊规则排序**：按绝对值、按字符串长度、按某种业务逻辑排序

这些场景都需要通过自定义比较函数（comparator，简称 cmp）来实现。

---

## 2. cmp 函数的基本概念

### 2.1 函数签名

```cpp
bool cmp(const T& a, const T& b);
```

- 返回 `true`：表示 `a` 应该排在 `b` **前面**
- 返回 `false`：表示 `a` 应该排在 `b` **后面**（即需要交换位置）

### 2.2 核心逻辑解读

```cpp
#include <algorithm>
#include <iostream>
using namespace std;

// 降序比较：如果 a > b，a 排在 b 前面
bool cmp(int x, int y) {
    return x > y;  // x 大于 y 时，x 在前 → 降序
}

int main() {
    int arr[] = {3, 1, 4, 1, 5, 9};
    sort(arr, arr + 6, cmp);

    cout << "降序排序：";
    for (int i = 0; i < 6; i++) cout << arr[i] << " ";
    cout << endl;

    return 0;
}
```

**预期输出**：

```
降序排序：9 5 4 3 1 1
```

---

## 3. 关键概念：严格弱排序（Strict Weak Ordering）

### 3.1 什么是严格弱排序

C++ 标准要求所有比较函数必须满足**严格弱排序（Strict Weak Ordering）**的数学性质。一个合格的比较函数必须满足以下条件：

1. **非自反性（Irreflexivity）**：`cmp(x, x)` 必须返回 `false`
2. **反对称性（Antisymmetry）**：如果 `cmp(x, y)` 为 `true`，则 `cmp(y, x)` 必须为 `false`
3. **传递性（Transitivity）**：如果 `cmp(x, y)` 为 `true` 且 `cmp(y, z)` 为 `true`，则 `cmp(x, z)` 必须为 `true`
4. **等价的传递性**：如果 `cmp(x, y)` 为 `false` 且 `cmp(y, x)` 为 `false`（即 x 和 y 等价），且 `cmp(y, z)` 为 `false` 且 `cmp(z, y)` 为 `false`（即 y 和 z 等价），则 `cmp(x, z)` 必须为 `false` 且 `cmp(z, x)` 为 `false`（即 x 和 z 等价）

### 3.2 为什么不能用 <= 或 >=

```cpp
// 错误的写法！
bool cmp(int x, int y) {
    return x <= y;  // 不满足严格弱排序！
}
```

为什么是错误的？

当 `x == y` 时，`cmp(x, y)` 返回 `true`（因为 `x <= y` 成立），但同时 `cmp(y, x)` 也为 `true`（因为 `y <= x` 也成立）。这违反了**非自反性**（两个相等的元素互相认为对方应该在自己前面），导致排序行为未定义，可能造成崩溃或错误结果。

**正确的写法**：

```cpp
// 降序：正确，使用 < 或 >
bool cmp_desc(int x, int y) {
    return x > y;
}

// 升序：正确
bool cmp_asc(int x, int y) {
    return x < y;
}
```

**黄金法则**：比较函数中永远只使用 `<` 或 `>`，**不要**使用 `<=` 或 `>=`。

---

## 4. 多种 cmp 写法

### 4.1 普通函数

最传统的写法，在 C++98 时代就已支持。

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

bool cmp(int x, int y) {
    return x > y;  // 降序
}

int main() {
    vector<int> v = {5, 2, 8, 1, 9, 3};
    sort(v.begin(), v.end(), cmp);
    // 输出：9 8 5 3 2 1
    for (int x : v) cout << x << " ";
    return 0;
}
```

**优点**：逻辑清晰，可复用
**缺点**：函数定义和调用可能分处不同的文件，不便于阅读

### 4.2 函数对象（仿函数）

函数对象（Functor）是重载了 `operator()` 的类（或结构体）的实例。

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

struct CmpDesc {
    bool operator()(int x, int y) const {
        return x > y;  // 降序
    }
};

int main() {
    vector<int> v = {5, 2, 8, 1, 9, 3};
    sort(v.begin(), v.end(), CmpDesc());
    // 输出：9 8 5 3 2 1
    for (int x : v) cout << x << " ";
    return 0;
}
```

**优点**：
- 可以保存状态（成员变量）
- 可以内联，性能与函数指针相同或更优
- 标准库中已提供常用的仿函数，如 `std::greater<T>`、`std::less<T>`

**标准库提供的仿函数**：

```cpp
#include <functional>  // std::greater, std::less 等

sort(v.begin(), v.end(), greater<int>());   // 降序
sort(v.begin(), v.end(), less<int>());      // 升序（等价于默认）
```

### 4.3 Lambda 表达式（C++11）

Lambda 表达式是 C++11 引入的匿名函数，是编写 cmp 最现代、最简洁的方式。

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {5, 2, 8, 1, 9, 3};

    // Lambda 表达式作为 cmp
    sort(v.begin(), v.end(), [](int x, int y) {
        return x > y;  // 降序
    });

    for (int x : v) cout << x << " ";
    // 输出：9 8 5 3 2 1
    return 0;
}
```

**Lambda 语法**：

```cpp
[capture](parameters) -> return_type { body }
```

- `capture`：捕获列表，用于在 lambda 中使用外部变量（cmp 中通常为空 `[]`）
- `parameters`：参数列表，与函数签名一致
- `return_type`：返回类型（可省略，编译器自动推导）
- `body`：函数体

**优点**：
- 定义在使用处，代码紧凑，可读性强
- 可以捕获外部变量（如根据用户输入决定排序规则）
- 现代 C++ 推荐写法

### 4.4 三种写法的对比示例

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

// 1. 普通函数
bool cmp_func(int x, int y) {
    return x > y;
}

// 2. 函数对象
struct CmpFunctor {
    bool operator()(int x, int y) const {
        return x > y;
    }
};

int main() {
    vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};

    // 普通函数
    vector<int> v1 = v;
    sort(v1.begin(), v1.end(), cmp_func);
    cout << "普通函数：";
    for (int x : v1) cout << x << " ";
    cout << endl;

    // 函数对象
    vector<int> v2 = v;
    sort(v2.begin(), v2.end(), CmpFunctor());
    cout << "函数对象：";
    for (int x : v2) cout << x << " ";
    cout << endl;

    // Lambda 表达式
    vector<int> v3 = v;
    sort(v3.begin(), v3.end(), [](int x, int y) { return x > y; });
    cout << "Lambda：  ";
    for (int x : v3) cout << x << " ";
    cout << endl;

    return 0;
}
```

**预期输出**：

```
普通函数：9 6 5 4 3 2 1 1
函数对象：9 6 5 4 3 2 1 1
Lambda：  9 6 5 4 3 2 1 1
```

---

## 5. 对结构体自定义排序

### 5.1 按单个字段排序

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
#include <string>
using namespace std;

struct Student {
    string name;
    int score;
};

int main() {
    vector<Student> students = {
        {"Alice", 85},
        {"Bob",   92},
        {"Charlie", 78},
        {"David",  92},
        {"Eve",    85}
    };

    // 按成绩降序（从高到低）
    sort(students.begin(), students.end(),
         [](const Student& a, const Student& b) {
             return a.score > b.score;
         });

    cout << "按成绩降序：\n";
    for (const auto& s : students) {
        cout << s.name << " : " << s.score << endl;
    }

    return 0;
}
```

**预期输出**：

```
按成绩降序：
Bob : 92
David : 92
Alice : 85
Eve : 85
Charlie : 78
```

### 5.2 多字段排序

实际开发中常常需要按多个字段排序，例如"先按成绩降序，成绩相同的按姓名升序"。

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
#include <string>
using namespace std;

struct Student {
    string name;
    int score;
    int id;
};

int main() {
    vector<Student> students = {
        {"Alice",   85, 101},
        {"Bob",     92, 102},
        {"Charlie", 78, 103},
        {"David",   92, 104},
        {"Eve",     85, 105},
        {"Frank",   92, 106}
    };

    // 多字段排序：先按成绩降序，成绩相同按姓名升序
    sort(students.begin(), students.end(),
         [](const Student& a, const Student& b) {
             if (a.score != b.score) {
                 return a.score > b.score;  // 主排序：成绩降序
             }
             return a.name < b.name;  // 次排序：姓名升序
         });

    cout << "多字段排序（成绩降序 + 姓名升序）：\n";
    for (const auto& s : students) {
        cout << s.name << " : " << s.score << " (id=" << s.id << ")\n";
    }

    return 0;
}
```

**预期输出**：

```
多字段排序（成绩降序 + 姓名升序）：
Bob : 92 (id=102)
David : 92 (id=104)
Frank : 92 (id=106)
Alice : 85 (id=101)
Eve : 85 (id=105)
Charlie : 78 (id=103)
```

**多字段排序的通用模式**：

```cpp
// 通用模式
sort(v.begin(), v.end(), [](const T& a, const T& b) {
    if (a.field1 != b.field1) {
        return a.field1 < b.field1;   // 按 field1 升序
    }
    if (a.field2 != b.field2) {
        return a.field2 > b.field2;   // 按 field2 降序
    }
    return a.field3 < b.field3;       // 按 field3 升序
});
```

**注意事项**：
- 每个字段的比较必须使用 `<` 或 `>`，不能使用 `<=` 或 `>=`
- 多字段排序时，先比较主要字段，如果不同则直接返回结果；如果相同，再比较次要字段
- 这种方法可以扩展到任意多个字段，且每个字段可以独立控制升降序

### 5.3 使用 tuple 简化多字段排序

对于 C++11 及以后版本，可以使用 `std::tuple` 或 `std::tie` 来简化多字段比较：

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
#include <string>
#include <tuple>
using namespace std;

struct Student {
    string name;
    int score;
    int id;
};

int main() {
    vector<Student> students = {
        {"Alice",   85, 101},
        {"Bob",     92, 102},
        {"Charlie", 78, 103},
        {"David",   92, 104},
        {"Eve",     85, 105}
    };

    // 使用 tuple 简化多字段排序
    // 先按成绩降序，再按姓名升序
    sort(students.begin(), students.end(),
         [](const Student& a, const Student& b) {
             // 使用 tie 将多个字段打包比较
             // 注意：score 要降序，所以用 -a.score 与 -b.score
             return tie(b.score, a.name) < tie(a.score, b.name);
         });

    cout << "使用 tie 排序：\n";
    for (const auto& s : students) {
        cout << s.name << " : " << s.score << "\n";
    }

    return 0;
}
```

**原理**：`std::tie` 创建引用元组，`tuple` 的 `operator<` 按字典序进行比较：先比较第一个元素，若相等再比较第二个，以此类推。

对于降序的情况，可以利用交换位置来实现：`tie(b.score, a.name) < tie(a.score, b.name)` 等价于按 score 降序、按 name 升序。

---

## 6. 综合示例

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
#include <string>
#include <functional>
using namespace std;

// 结构体定义
struct Product {
    string name;
    double price;
    int sales;  // 销量

    void print() const {
        cout << name << " | ￥" << price << " | 销量 " << sales << "\n";
    }
};

// 普通函数：按价格降序
bool cmp_by_price_desc(const Product& a, const Product& b) {
    return a.price > b.price;
}

// 函数对象：按销量升序
struct CmpBySalesAsc {
    bool operator()(const Product& a, const Product& b) const {
        return a.sales < b.sales;
    }
};

int main() {
    vector<Product> products = {
        {"鼠标",  29.9,  500},
        {"键盘",  199.0, 300},
        {"显示器", 1299.0, 150},
        {"耳机",  99.0,  800},
        {"音箱",  299.0, 200}
    };

    // 1. 普通函数 - 价格降序
    cout << "===== 价格降序（普通函数）=====\n";
    sort(products.begin(), products.end(), cmp_by_price_desc);
    for (const auto& p : products) p.print();
    cout << endl;

    // 2. 函数对象 - 销量升序
    cout << "===== 销量升序（函数对象）=====\n";
    sort(products.begin(), products.end(), CmpBySalesAsc());
    for (const auto& p : products) p.print();
    cout << endl;

    // 3. Lambda - 价格升序
    cout << "===== 价格升序（Lambda）=====\n";
    sort(products.begin(), products.end(),
         [](const Product& a, const Product& b) {
             return a.price < b.price;
         });
    for (const auto& p : products) p.print();
    cout << endl;

    // 4. Lambda - 多字段排序：先按销量降序，销量相同按价格升序
    cout << "===== 多字段排序（Lambda）=====\n";
    sort(products.begin(), products.end(),
         [](const Product& a, const Product& b) {
             if (a.sales != b.sales) {
                 return a.sales > b.sales;  // 主：销量降序
             }
             return a.price < b.price;     // 次：价格升序
         });
    for (const auto& p : products) p.print();
    cout << endl;

    // 5. 使用标准库 greater<>
    cout << "===== 使用标准库 greater<int>（对 int 数组降序）=====\n";
    int arr[] = {3, 1, 4, 1, 5, 9};
    sort(arr, arr + 6, greater<int>());
    for (int x : arr) cout << x << " ";
    cout << endl;

    return 0;
}
```

**预期输出**：

```
===== 价格降序（普通函数）=====
显示器 | ￥1299 | 销量 150
音箱 | ￥299 | 销量 200
键盘 | ￥199 | 销量 300
耳机 | ￥99 | 销量 800
鼠标 | ￥29.9 | 销量 500

===== 销量升序（函数对象）=====
显示器 | ￥1299 | 销量 150
音箱 | ￥299 | 销量 200
键盘 | ￥199 | 销量 300
鼠标 | ￥29.9 | 销量 500
耳机 | ￥99 | 销量 800

===== 价格升序（Lambda）=====
鼠标 | ￥29.9 | 销量 500
耳机 | ￥99 | 销量 800
键盘 | ￥199 | 销量 300
音箱 | ￥299 | 销量 200
显示器 | ￥1299 | 销量 150

===== 多字段排序（Lambda）=====
耳机 | ￥99 | 销量 800
鼠标 | ￥29.9 | 销量 500
键盘 | ￥199 | 销量 300
音箱 | ￥299 | 销量 200
显示器 | ￥1299 | 销量 150

===== 使用标准库 greater<int>（对 int 数组降序）=====
9 5 4 3 1 1
```

---

## 7. 常见坑与注意事项

1. **严格弱排序违规是未定义行为**：使用 `<=` 或 `>=` 会破坏严格弱排序，编译器不会给出警告，但程序可能崩溃或产生错误的排序结果。

2. **cmp 函数不能修改传入的参数**：比较函数应该只读地访问参数，不要修改它们。

3. **cmp 函数必须保持一致**：同一个排序过程中，对相同的两个元素，比较结果必须始终一致。不要在 cmp 中使用随机数或依赖于可变的外部状态。

4. **Lambda 的捕获列表**：如果 cmp 需要用到外部变量，确保正确捕获（按值 `[=]` 或按引用 `[&]`）。注意按引用捕获时，lambda 的生命周期不应超过所捕获变量的生命周期。

5. **性能考虑**：对于大规模数据排序，普通函数和函数对象的性能通常优于 lambda（虽然编译器通常能优化）。但在绝大多数情况下，差异可以忽略不计，优先选择可读性最好的方式。

6. **`std::sort` 不保证稳定**：如果有多个元素比较结果相同，`std::sort` 不保证它们的相对顺序。如果需要稳定排序，使用 `std::stable_sort`。

7. **浮点数比较**：对浮点数排序通常没有问题，但如果涉及 NaN（Not a Number），比较结果会违反严格弱排序（NaN 与任何值比较都返回 false），导致未定义行为。

8. **间接排序**：如果排序的代价很高（如排序对象很大），可以考虑对索引或指针进行排序（即 Schwartzian transform 或装饰-排序-去装饰模式）。
