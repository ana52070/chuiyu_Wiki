---
title: const定义常量
author: claudecode(deepseekV4flash)
date: 2026-07-20 21:41:39
description: const定义常量
tags:
  - Cpp算法
categories:
  - guide
  - C++算法入门
---

# const 定义常量

## 一、const 的基本用法

`const` 是 C++ 的关键字，用于定义**常量**——初始化后不可修改的变量。

```cpp
#include <iostream>
using namespace std;

int main() {
    const int MAX_N = 100000;       // 整型常量
    const double PI = 3.1415926535; // 双精度常量
    const string GREETING = "Hello"; // 字符串常量

    cout << "MAX_N = " << MAX_N << endl;
    cout << "PI = " << PI << endl;
    cout << "GREETING = " << GREETING << endl;

    // MAX_N = 200;  // 编译错误！不能修改 const 变量

    return 0;
}
```

**运行结果**：
```
MAX_N = 100000
PI = 3.14159265
GREETING = Hello
```

---

## 二、const 的原理

### 2.1 编译时常量（Compile-time Constant）

值在编译时就能确定，编译器可以用它来替代字面量：

```cpp
const int SIZE = 100;
int arr[SIZE];  // 编译时已知 SIZE = 100，可以定义数组
```

### 2.2 运行时常量（Run-time Constant）

值在运行时才能确定，但一旦确定就不能修改：

```cpp
#include <iostream>
using namespace std;

int main() {
    int x;
    cout << "请输入一个数字: ";
    cin >> x;
    const int VALUE = x * 2;   // 运行时确定，但之后不能修改
    cout << "VALUE = " << VALUE << endl;

    // VALUE = 10;  // 编译错误！
    return 0;
}
```

### 2.3 const 的编译期优化

```cpp
const int N = 100;
// 编译器会在编译时直接用 100 替换 N，不会产生运行时开销
int sum = N * (N + 1) / 2;   // 编译时计算为 5050
```

---

## 三、const 与 #define 的详细对比

`#define` 是 C 预处理器指令，在**预处理阶段**进行文本替换。`const` 是 C++ 关键字，由**编译器**处理。

### 对比表

| 特性 | `const` | `#define` |
|------|---------|-----------|
| 处理阶段 | 编译期 | 预处理（编译前） |
| 类型检查 | 有 | 无（纯文本替换） |
| 作用域 | 遵循 C++ 作用域规则 | 从定义处到文件结束（除非取消定义） |
| 调试友好 | 是（符号表可见） | 否（预处理阶段已替换，符号表不可见） |
| 是否占用内存 | 是（可能分配存储空间） | 否（直接替换为字面量） |
| 可否定义复杂类型 | 可以（string、vector 等） | 不可以（只能做简单文本替换） |
| 可否用于类成员 | 可以 | 不可以 |
| 可否用于指针/引用 | 可以 | 不可以 |
| 是否有作用域 | 是（块作用域、函数作用域） | 否（全局替换） |

### 3.1 #define 的典型问题

```cpp
#include <iostream>
using namespace std;

#define MAX 100
#define MIN 50
#define AREA(x) x * x  // 宏函数

int main() {
    cout << MAX << endl;  // 输出 100

    // 问题 1：没有类型检查
    #define PI 3.14
    // PI 只是文本替换，没有类型信息

    // 问题 2：宏函数容易出错
    cout << AREA(5) << endl;      // 25
    cout << AREA(1 + 2) << endl;  // 1 + 2 * 1 + 2 = 5，不是 9！

    // 问题 3：宏没有作用域
    #define TEMP 42
    // TEMP 从定义到文件结束都有效，无法限定在某个局部

    return 0;
}
```

**运行结果**：
```
100
25
5
```

### 3.2 使用 const 解决这些问题

```cpp
#include <iostream>
using namespace std;

const int MAX = 100;
const int MIN = 50;

inline int area(int x) { return x * x; }  // 内联函数

int main() {
    cout << MAX << endl;      // 100
    cout << area(5) << endl;       // 25
    cout << area(1 + 2) << endl;   // 9，正确的计算

    // const 有作用域
    {
        const int LOCAL = 10;
        cout << LOCAL << endl;  // 10
    }
    // cout << LOCAL << endl;  // 编译错误：LOCAL 已超出作用域

    return 0;
}
```

**运行结果**：
```
100
25
9
10
```

---

## 四、const 的多种使用场景

### 4.1 修饰变量

```cpp
const double PI = 3.14159;
const int MONTHS = 12;
```

### 4.2 修饰指针

```cpp
#include <iostream>
using namespace std;

int main() {
    int a = 10, b = 20;

    // 指向常量的指针：不能通过指针修改所指对象的值
    const int* p1 = &a;
    // *p1 = 100;  // 编译错误
    p1 = &b;        // 可以改变指针指向

    // 指针常量：指针本身不能改变
    int* const p2 = &a;
    *p2 = 100;      // 可以修改所指对象
    // p2 = &b;     // 编译错误

    // 指向常量的指针常量：都不能改
    const int* const p3 = &a;
    // *p3 = 100;   // 编译错误
    // p3 = &b;     // 编译错误

    cout << "a = " << a << endl;    // 100
    cout << "*p1 = " << *p1 << endl; // 100

    return 0;
}
```

### 4.3 修饰函数参数

```cpp
#include <iostream>
#include <string>
using namespace std;

// const 引用参数：不复制，同时保证不修改原对象
void printMessage(const string& msg) {
    // msg += "!";  // 编译错误：不能修改 const 引用
    cout << msg << endl;
}

// const 指针参数
void printArray(const int* arr, int size) {
    for (int i = 0; i < size; i++) {
        cout << arr[i] << " ";
        // arr[i] = 0;   // 编译错误
    }
    cout << endl;
}

int main() {
    string s = "Hello, World!";
    printMessage(s);

    int nums[] = {1, 2, 3, 4, 5};
    printArray(nums, 5);

    return 0;
}
```

**运行结果**：
```
Hello, World!
1 2 3 4 5 
```

### 4.4 修饰函数返回值

```cpp
#include <iostream>
using namespace std;

const int getValue() {
    return 42;
}

// 返回 const 引用（避免复制）
const string& getGreeting() {
    static const string msg = "Hello";
    return msg;
}

int main() {
    int x = getValue();      // 可以赋值给非 const 变量
    // getValue() = 100;     // 编译错误：不能修改 const 返回值

    cout << getGreeting() << endl;
    return 0;
}
```

### 4.5 const 成员函数

```cpp
#include <iostream>
#include <string>
using namespace std;

class Student {
private:
    string name;
    int score;
public:
    Student(const string& n, int s) : name(n), score(s) {}

    // const 成员函数：承诺不修改对象状态
    string getName() const {
        return name;
    }

    int getScore() const {
        return score;
    }

    // 非 const 成员函数
    void setScore(int s) {
        score = s;
    }
};

int main() {
    const Student s("Alice", 95);
    cout << s.getName() << ": " << s.getScore() << endl;
    // s.setScore(100);  // 编译错误：const 对象只能调用 const 成员函数

    Student s2("Bob", 87);
    s2.setScore(90);       // 非 const 对象可以调用任何函数
    cout << s2.getName() << ": " << s2.getScore() << endl;

    return 0;
}
```

**运行结果**：
```
Alice: 95
Bob: 90
```

---

## 五、完整可运行代码：综合展示 const 的多种场景

```cpp
#include <iostream>
#include <vector>
using namespace std;

// 比较两个 const 数组
const int DAYS_IN_WEEK = 7;
const double TAX_RATE = 0.08;

// const 指针参数实例
int findMax(const vector<int>& arr) {
    int max_val = arr[0];
    for (size_t i = 1; i < arr.size(); i++) {
        if (arr[i] > max_val) max_val = arr[i];
    }
    return max_val;
}

inline int square(int x) {
    return x * x;
}

int main() {
    cout << "=== const 详解 ===\n\n";

    // 1. 基本常量
    cout << "1. 基本常量:\n";
    const int MAX_USERS = 1000;
    const string APP_NAME = "MyApp";
    cout << "MAX_USERS = " << MAX_USERS << "\n";
    cout << "APP_NAME = " << APP_NAME << "\n\n";

    // 2. 指针与 const
    cout << "2. 指针与 const:\n";
    int value = 42;
    const int* p_readonly = &value;   // 指向常量的指针
    // *p_readonly = 100;             // 编译错误
    cout << "*p_readonly = " << *p_readonly << "\n\n";

    // 3. const 参数的好处
    cout << "3. const vector 参数:\n";
    vector<int> data = {3, 1, 4, 1, 5, 9, 2, 6};
    cout << "最大值: " << findMax(data) << "\n\n";

    // 4. 使用 const 替代 #define 的宏
    cout << "4. 内联函数替代宏:\n";
    cout << "square(5) = " << square(5) << "\n";
    cout << "square(1+2) = " << square(1 + 2) << "\n\n";

    // 5. 常量表达式（constexpr，C++11）
    cout << "5. constexpr 编译期常量:\n";
    constexpr int FACTORIAL_5 = 5 * 4 * 3 * 2 * 1;
    cout << "5! = " << FACTORIAL_5 << "\n";
    constexpr int ARRAY_SIZE = 100;
    int fixed_arr[ARRAY_SIZE];  // 编译期确定大小
    cout << "数组大小: " << sizeof(fixed_arr) / sizeof(fixed_arr[0]) << "\n";

    return 0;
}
```

**运行结果**：
```
=== const 详解 ===

1. 基本常量:
MAX_USERS = 1000
APP_NAME = MyApp

2. 指针与 const:
*p_readonly = 42

3. const vector 参数:
最大值: 9

4. 内联函数替代宏:
square(5) = 25
square(1+2) = 9

5. constexpr 编译期常量:
5! = 120
数组大小: 100
```

---

## 六、注意事项和常见坑

### 6.1 const 变量必须初始化

```cpp
const int X;      // 编译错误：const 变量必须初始化
const int Y = 10; // 正确
```

### 6.2 顶层 const 和底层 const

```cpp
const int a = 10;          // 顶层 const（对象本身是常量）
int* const p = &a;         // 顶层 const（指针本身是常量）
const int* q = &a;         // 底层 const（所指物是常量）
const int* const r = &a;   // 顶层 + 底层 const
```

### 6.3 const_cast 的使用

`const_cast` 可以移除变量的 const 属性，但**修改原本就是 const 的变量是未定义行为**：

```cpp
const int x = 10;
const_cast<int&>(x) = 20;  // 未定义行为！x 原本就是 const

int y = 10;
const int& ref = y;          // 通过 const 引用绑定
const_cast<int&>(ref) = 20;  // 可以，因为 y 本身不是 const
cout << y << endl;           // 20
```

### 6.4 不要滥用 const_cast

```cpp
// 不推荐这种设计
void process(const int& val) {
    int& ref = const_cast<int&>(val);
    ref = 100;  // 破坏了 const 的意义
}
```

---

## 七、总结

| 对比维度 | `const` | `#define` |
|---------|---------|-----------|
| 类型安全 | 是 | 否 |
| 作用域 | 块作用域 | 文件作用域 |
| 调试 | 符号表可见 | 符号表不可见 |
| 复杂类型 | 支持 | 不支持 |
| C++ 推荐度 | **推荐** | **不推荐**（定义常量时） |

**核心建议**：
1. 在 C++ 中始终使用 `const` 而非 `#define` 来定义常量
2. 使用 `const` 引用（`const T&`）传递大对象参数，避免复制
3. 使用 `constexpr`（C++11）定义编译期常量
4. 成员函数如果不会修改对象状态，标记为 `const`
5. 避免使用 `const_cast` 修改真正的 const 变量
