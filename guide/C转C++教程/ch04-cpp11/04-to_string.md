---
title: to_string
author: claudecode(deepseekV4flash)
date: 2026-07-20 21:40:47
description: to_string
tags:
  - Cpp算法
categories:
  - guide
  - C++算法入门
---

# to_string 函数

## 1. 为什么需要 to_string？

在 C++11 之前，将数值转换为字符串是一件比较麻烦的事。常用的方法有：

**方法一：sprintf（C 风格）**

```cpp
char buf[100];
sprintf(buf, "%d", 42);      // 整数转字符串
sprintf(buf, "%.2f", 3.14);  // 浮点数转字符串
```

**问题**：需要手动管理缓冲区、容易缓冲区溢出、类型不安全。

**方法二：stringstream（C++ 风格）**

```cpp
ostringstream oss;
oss << 42;
string s = oss.str();
```

**问题**：代码冗长、性能不如 sprintf。

C++11 引入了 `to_string` 函数，一行代码即可完成转换：

```cpp
string s = to_string(42);     // 简洁、安全、直观
```

## 2. 头文件

```cpp
#include <string>
```

`to_string` 是 `std` 命名空间中的一组重载函数。

## 3. 支持的类型

`to_string` 为以下数值类型提供了重载：

| 函数签名 | 对应的类型 |
|---------|-----------|
| `string to_string(int val)` | `int` |
| `string to_string(long val)` | `long` |
| `string to_string(long long val)` | `long long` |
| `string to_string(unsigned val)` | `unsigned int` |
| `string to_string(unsigned long val)` | `unsigned long` |
| `string to_string(unsigned long long val)` | `unsigned long long` |
| `string to_string(float val)` | `float` |
| `string to_string(double val)` | `double` |
| `string to_string(long double val)` | `long double` |

所有版本都返回 `std::string` 类型。

## 4. 完整示例：不同类型的结果

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    // 整数类型
    int a = 42;
    long b = 123456789L;
    long long c = 9876543210LL;

    // 无符号类型
    unsigned int d = 100U;
    unsigned long long e = 500ULL;

    // 浮点类型
    float f = 3.14f;
    double g = 3.1415926535;
    long double h = 3.141592653589793L;

    cout << "=== 整数类型 ===" << endl;
    cout << "to_string(int):           " << to_string(a) << endl;
    cout << "to_string(long):          " << to_string(b) << endl;
    cout << "to_string(long long):     " << to_string(c) << endl;

    cout << "\n=== 无符号类型 ===" << endl;
    cout << "to_string(unsigned):      " << to_string(d) << endl;
    cout << "to_string(unsigned LL):   " << to_string(e) << endl;

    cout << "\n=== 浮点类型 ===" << endl;
    cout << "to_string(float):         " << to_string(f) << endl;
    cout << "to_string(double):        " << to_string(g) << endl;
    cout << "to_string(long double):   " << to_string(h) << endl;

    return 0;
}
```

**预期输出：**

```
=== 整数类型 ===
to_string(int):           42
to_string(long):          123456789
to_string(long long):     9876543210

=== 无符号类型 ===
to_string(unsigned):      100
to_string(unsigned LL):   500

=== 浮点类型 ===
to_string(float):         3.140000
to_string(double):        3.141593
to_string(long double):   3.141593
```

## 5. 浮点数格式化说明

注意上面浮点数的输出结果：`to_string` 对浮点数**固定保留 6 位小数**（不包括尾随零）。

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    double d1 = 3.14;
    double d2 = 3.0;
    double d3 = 123.456789;
    double d4 = 0.0001;

    cout << "to_string(3.14)       = " << to_string(d1) << endl;
    cout << "to_string(3.0)        = " << to_string(d2) << endl;
    cout << "to_string(123.456789) = " << to_string(d3) << endl;
    cout << "to_string(0.0001)     = " << to_string(d4) << endl;

    return 0;
}
```

**预期输出：**

```
to_string(3.14)       = 3.140000
to_string(3.0)        = 3.000000
to_string(123.456789) = 123.456789
to_string(0.0001)     = 0.000100
```

**重要**：`to_string` 对浮点数总是输出 6 位小数。如果你需要自定义格式（如控制小数位数、使用科学计数法等），仍然需要使用：

- `sprintf` / `snprintf`（C 风格）
- `ostringstream` + `setprecision` / `fixed`（C++ 风格）
- `to_chars`（C++17）

```cpp
#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
using namespace std;

int main() {
    double pi = 3.1415926535;

    // to_string：固定 6 位小数
    cout << "to_string:   " << to_string(pi) << endl;

    // stringstream + 控制格式
    ostringstream oss;
    oss << fixed << setprecision(2) << pi;
    cout << "保留 2 位:   " << oss.str() << endl;

    // stringstream + 科学计数法
    ostringstream oss2;
    oss2 << scientific << setprecision(4) << pi;
    cout << "科学计数法:  " << oss2.str() << endl;

    return 0;
}
```

**预期输出：**

```
to_string:   3.141593
保留 2 位:   3.14
科学计数法:  1.5916e+00
```

## 6. 输出 string 的两种方式

### 6.1 使用 cout（推荐）

`cout` 可以直接输出 `std::string` 类型：

```cpp
string s = to_string(42);
cout << s << endl;   // 直接输出，不需要特殊处理
```

### 6.2 使用 printf

`printf` 是 C 风格的输出函数，**不支持**直接输出 `std::string`。如果你一定要用 `printf`，需要调用 `.c_str()` 方法将 `string` 转换为 C 风格字符串（`const char*`）：

```cpp
string s = to_string(42);
printf("%s\n", s.c_str());   // 必须加 .c_str()
// printf("%s\n", s);        // 错误！printf 不能直接输出 string
```

```cpp
#include <iostream>
#include <cstdio>   // printf
#include <string>
using namespace std;

int main() {
    string s1 = to_string(100);
    string s2 = to_string(3.14159);
    string s3 = to_string(42) + " apples";
    string s4 = "value = " + to_string(3.14) + " end";

    // cout 输出（推荐）
    cout << "=== cout 输出 ===" << endl;
    cout << "s1 = " << s1 << endl;
    cout << "s2 = " << s2 << endl;
    cout << "s3 = " << s3 << endl;
    cout << "s4 = " << s4 << endl;

    // printf 输出（需要 .c_str()）
    cout << "\n=== printf 输出 ===" << endl;
    printf("s1 = %s\n", s1.c_str());
    printf("s2 = %s\n", s2.c_str());
    printf("s3 = %s\n", s3.c_str());
    printf("s4 = %s\n", s4.c_str());

    return 0;
}
```

**预期输出：**

```
=== cout 输出 ===
s1 = 100
s2 = 3.141590
s3 = 42 apples
s4 = value = 3.140000 end

=== printf 输出 ===
s1 = 100
s2 = 3.141590
s3 = 42 apples
s4 = value = 3.140000 end
```

## 7. to_string 与 sprintf 的对比

```cpp
#include <iostream>
#include <cstdio>
#include <string>
#include <cstring>  // strcmp
using namespace std;

int main() {
    int num = 42;
    double pi = 3.14159;

    // ---- to_string ----
    string s1 = to_string(num);
    string s2 = to_string(pi);

    // ---- sprintf ----
    char buf1[100], buf2[100];
    sprintf(buf1, "%d", num);
    sprintf(buf2, "%.6f", pi);  // to_string 风格

    cout << "=== to_string vs sprintf ===" << endl;
    cout << "to_string(int):    " << s1 << endl;
    cout << "sprintf(int):      " << buf1 << endl;
    cout << "to_string(double): " << s2 << endl;
    cout << "sprintf(double):   " << buf2 << endl;

    // 检查结果是否一致
    cout << "\n整数结果一致: " << (s1 == buf1 ? "是" : "否") << endl;
    cout << "浮点数结果一致: " << (s2 == buf2 ? "是" : "否") << endl;

    return 0;
}
```

**预期输出：**

```
=== to_string vs sprintf ===
to_string(int):    42
sprintf(int):      42
to_string(double): 3.141590
sprintf(double):   3.141590

整数结果一致: 是
浮点数结果一致: 是
```

| 对比项 | `to_string` | `sprintf` |
|-------|:-----------:|:---------:|
| 类型安全 | 是（编译期重载） | 否（靠格式字符串） |
| 缓冲区管理 | 自动 | 手动（可能溢出） |
| 格式化灵活性 | 固定 6 位小数 | 极高（完整 printf 格式） |
| 返回类型 | `std::string` | `char*`（需手动转换） |
| 易用性 | 非常高 | 较低 |

## 8. 注意事项和常见坑

### 8.1 浮点数精度问题

`to_string` 对浮点数保留 6 位有效小数（rounds to 6 decimal places），这**不是**精确表示，可能和预期不同：

```cpp
double x = 0.1 + 0.2;       // 实际是 0.30000000000000004
cout << to_string(x);        // 输出 "0.300000"（截断到了 6 位）
```

### 8.2 负数的处理

`to_string` 对负数正常工作：

```cpp
string s1 = to_string(-42);     // "-42"
string s2 = to_string(-3.14);   // "-3.140000"
```

### 8.3 大整数的转换

`long long` 最大可表示约 922 京（9.22e18），`to_string` 可以正确处理：

```cpp
string s = to_string(9223372036854775807LL);  // LLONG_MAX
cout << s;  // "9223372036854775807"
```

### 8.4 拼接字符串时的陷阱

`to_string` 返回的是 `string`，你可以直接用 `+` 拼接：

```cpp
// 正确：string + string
string msg = "The answer is " + to_string(42);

// 正确：也可以分开写
string msg2 = "Value: " + to_string(3.14) + ", Code: " + to_string(100);
```

## 9. 完整综合示例

```cpp
#include <iostream>
#include <string>
#include <cstdio>
using namespace std;

int main() {
    cout << "=== to_string 综合演示 ===" << endl;

    // 1. 基本类型转换
    int age = 25;
    double price = 19.99;
    long long population = 7800000000LL;
    float score = 92.5f;

    cout << "\n1. 基本类型转换：" << endl;
    cout << "年龄: " + to_string(age) << endl;
    cout << "价格: " + to_string(price) << endl;
    cout << "人口: " + to_string(population) << endl;
    cout << "分数: " + to_string(score) << endl;

    // 2. 拼接输出
    cout << "\n2. 拼接输出：" << endl;
    string report = "===== 报告 =====\n"
                    "年龄: " + to_string(age) + "\n"
                    "价格: $" + to_string(price) + "\n"
                    "人口: " + to_string(population) + "\n";
    cout << report;

    // 3. 与 printf 混合使用
    cout << "\n3. printf 输出（需要 .c_str()）：" << endl;
    string s = to_string(3.14159);
    printf("Pi 的值为: %s\n", s.c_str());

    // 4. 浮点数格式对比
    cout << "\n4. 浮点数格式对比：" << endl;
    double values[] = {0.5, 1.0 / 3.0, 123.456789, 1e-10, -2.71828};
    for (double v : values) {
        cout << "原始值: " << v << " -> to_string: " << to_string(v) << endl;
    }

    // 5. 复杂的字符串拼接（包含数字和文字）
    cout << "\n5. 复杂字符串拼接：" << endl;
    string item = "book";
    int qty = 3;
    double unit_price = 12.50;
    string receipt = item + " x " + to_string(qty) +
                     " = $" + to_string(qty * unit_price);
    cout << receipt << endl;

    return 0;
}
```

**预期输出（浮点数可能有微小差异）：**

```
=== to_string 综合演示 ===

1. 基本类型转换：
年龄: 25
价格: 19.990000
人口: 7800000000
分数: 92.500000

2. 拼接输出：
===== 报告 =====
年龄: 25
价格: $19.990000
人口: 7800000000

3. printf 输出（需要 .c_str()）：
Pi 的值为: 3.141590

4. 浮点数格式对比：
原始值: 0.5 -> to_string: 0.500000
原始值: 0.333333 -> to_string: 0.333333
原始值: 123.456789 -> to_string: 123.456789
原始值: 1e-10 -> to_string: 0.000000
原始值: -2.71828 -> to_string: -2.718280

5. 复杂字符串拼接：
book x 3 = $37.500000
```

## 10. 小结

- `to_string` 是 C++11 引入的便捷函数，可将数值**安全、简洁**地转换为 `std::string`
- 支持 `int`、`long`、`long long`、`unsigned` 系列、`float`、`double`、`long double`
- 对浮点数**固定保留 6 位小数**，需要自定义格式时应使用 `ostringstream` 或 `sprintf`
- `printf` 输出 `string` 时必须使用 `.c_str()`，推荐直接用 `cout`
- 相比 C 的 `sprintf`，`to_string` 更安全（无缓冲区溢出）、更易用（自动管理内存）
