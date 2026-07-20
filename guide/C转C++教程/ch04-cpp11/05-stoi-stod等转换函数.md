---
title: stoi-stod等转换函数
author: claudecode(deepseekV4flash)
date: 2026-07-20 21:40:47
description: stoi-stod等转换函数
tags:
  - Cpp算法
categories:
  - guide
  - C++算法入门
---

# stoi、stod 等字符串转换函数

## 1. 为什么需要 stoi / stod？

在 C++11 之前，将字符串转换为数值通常使用以下方式：

**C 风格：`atoi`、`atol`、`strtol`、`atof`、`strtod`**

```cpp
int a = atoi("123");         // 简单，但没有错误处理
long b = strtol("123", NULL, 10);  // 有错误处理，但接口较复杂
```

**C++ 风格：`stringstream`**

```cpp
istringstream iss("123");
int a;
iss >> a;                    // 可以处理，但代码冗长
```

**C 风格的问题：**
- `atoi`/`atof`：转换失败时**返回 0**，无法区分"转换失败"和"字符串就是 0"
- `strtol`/`strtod`：接口是从 C 继承的，不够直观

C++11 提供了一组**类型安全**的字符串转数值函数，具有完善的错误处理机制。

## 2. 函数系列完整列表

这些函数都定义在 `<string>` 头文件中，并位于 `std` 命名空间：

| 函数 | 转换目标类型 | 输入字符串示例 |
|------|:----------:|:-------------:|
| `stoi` | `int` | `"123"` → `123` |
| `stol` | `long` | `"123456789"` → `123456789L` |
| `stoll` | `long long` | `"9876543210"` → `9876543210LL` |
| `stoul` | `unsigned long` | `"123"` → `123UL` |
| `stoull` | `unsigned long long` | `"123"` → `123ULL` |
| `stof` | `float` | `"3.14"` → `3.14f` |
| `stod` | `double` | `"3.14159"` → `3.14159` |
| `stold` | `long double` | `"3.1415926535"` → `3.1415926535L` |

### 2.1 基本用法示例

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    cout << "=== 基本用法 ===" << endl;

    int a = stoi("123");
    long b = stol("123456789");
    long long c = stoll("9876543210");
    float d = stof("3.14");
    double e = stod("3.1415926535");
    long double f = stold("2.718281828459045");

    cout << "stoi(\"123\")              = " << a << endl;
    cout << "stol(\"123456789\")        = " << b << endl;
    cout << "stoll(\"9876543210\")      = " << c << endl;
    cout << "stof(\"3.14\")             = " << d << endl;
    cout << "stod(\"3.1415926535\")     = " << e << endl;
    cout << "stold(\"2.71828...\")      = " << f << endl;

    return 0;
}
```

**预期输出：**

```
=== 基本用法 ===
stoi("123")              = 123
stol("123456789")        = 123456789
stoll("9876543210")      = 9876543210
stof("3.14")             = 3.14
stod("3.1415926535")     = 3.1415926535
stold("2.71828...")      = 2.71828
```

## 3. 函数原型详解

所有函数都遵循类似的原型：

```cpp
int       stoi(const string& str, size_t* idx = 0, int base = 10);
long      stol(const string& str, size_t* idx = 0, int base = 10);
long long stoll(const string& str, size_t* idx = 0, int base = 10);
// ... 以此类推
```

三个参数的作用：

| 参数 | 类型 | 含义 | 是否可选 |
|:----:|:----:|------|:-------:|
| `str` | `const string&` | 要转换的字符串 | 必选 |
| `idx` | `size_t*` | 指向存储**第一个未转换字符位置**的指针 | 可选（默认 `nullptr`） |
| `base` | `int` | 进制（2~36，或 0 表示自动检测） | 可选（默认 10） |

## 4. 第二个参数 idx：获取转换停止位置

`idx` 指针用于获取转换停止的位置（即第一个不能转换的字符的索引）。这在解析混合字符串时非常有用。

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string mixed = "123abc456";

    // 获取 idx，即第一个无法转换的字符位置
    size_t idx = 0;
    int val = stoi(mixed, &idx);

    cout << "字符串: \"" << mixed << "\"" << endl;
    cout << "转换结果: " << val << endl;       // 123
    cout << "停止位置索引: " << idx << endl;    // 3（第 3 个字符是 'a'，无法转换）
    cout << "剩余部分: \"" << mixed.substr(idx) << "\"" << endl;  // "abc456"

    // 更实际的例子：解析 "年龄:25"
    string info = "年龄:25";
    size_t pos = 0;
    // 找到冒号后的数字
    size_t colon_pos = info.find(':');
    if (colon_pos != string::npos) {
        string num_part = info.substr(colon_pos + 1);
        int age = stoi(num_part, &pos);
        cout << "\n解析 \"" << info << "\":" << endl;
        cout << "年龄 = " << age << endl;   // 25
    }

    return 0;
}
```

**预期输出：**

```
字符串: "123abc456"
转换结果: 123
停止位置索引: 3
剩余部分: "abc456"

解析 "年龄:25":
年龄 = 25
```

### 4.1 实战：解析配置文件或混合文本

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    // 模拟解析 "CPU:3.5GHz,RAM:16GB,DISK:512GB"
    string specs = "CPU:3.5GHz,RAM:16GB,DISK:512GB";
    string current = specs;
    size_t idx = 0;

    cout << "解析配置字符串: " << specs << endl;

    // 提取 CPU 频率
    size_t colon1 = current.find(':');
    size_t comma1 = current.find(',');
    string cpu_str = current.substr(colon1 + 1, comma1 - colon1 - 1);
    double cpu = stod(cpu_str, &idx);
    cout << "CPU: " << cpu << " GHz (停止于: \"" << cpu_str.substr(idx) << "\")" << endl;

    // 提取 RAM 大小
    size_t colon2 = current.find(':', comma1);
    size_t comma2 = current.find(',', colon2);
    string ram_str = current.substr(colon2 + 1, comma2 - colon2 - 1);
    // 注意 ram_str 是 "16GB"，数字部分到 "GB" 前停止
    int ram = stoi(ram_str, &idx);
    cout << "RAM: " << ram << " GB (停止于: \"" << ram_str.substr(idx) << "\")" << endl;

    // 提取 DISK 大小
    size_t colon3 = current.find(':', comma2);
    string disk_str = current.substr(colon3 + 1);
    int disk = stoi(disk_str, &idx);
    cout << "DISK: " << disk << " GB (停止于: \"" << disk_str.substr(idx) << "\")" << endl;

    return 0;
}
```

**预期输出：**

```
解析配置字符串: CPU:3.5GHz,RAM:16GB,DISK:512GB
CPU: 3.5 GHz (停止于: "GHz")
RAM: 16 GB (停止于: "GB")
DISK: 512 GB (停止于: "GB")
```

## 5. 第三个参数 base：指定进制

`base` 参数可以指定转换的进制（2~36），或使用 `0` 让编译器自动检测（通过前缀判断）。

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    cout << "=== 进制转换演示 ===" << endl;

    // 指定进制
    cout << "二进制 \"1010\" 转十进制: " << stoi("1010", nullptr, 2) << endl;   // 10
    cout << "八进制 \"17\" 转十进制:   " << stoi("17", nullptr, 8) << endl;     // 15
    cout << "十进制 \"255\" 转十进制:  " << stoi("255", nullptr, 10) << endl;   // 255
    cout << "十六进制 \"FF\" 转十进制: " << stoi("FF", nullptr, 16) << endl;    // 255
    cout << "三十六进制 \"ZZ\" 转十进制: " << stoi("ZZ", nullptr, 36) << endl;  // 35*36 + 35 = 1295

    cout << "\n=== 自动检测进制（base = 0）===" << endl;
    cout << "\"0x1A\" 自动解析为: " << stoi("0x1A", nullptr, 0) << endl;  // 26（十六进制）
    cout << "\"0o17\" 自动解析为: " << stoi("0o17", nullptr, 0) << endl;  // 15（八进制？不，0o 不是标准前缀）
    cout << "\"0755\" 自动解析为:  " << stoi("0755", nullptr, 0) << endl; // 493（八进制，前导 0）
    cout << "\"123\" 自动解析为:   " << stoi("123", nullptr, 0) << endl;  // 123（十进制）

    return 0;
}
```

**预期输出：**

```
=== 进制转换演示 ===
二进制 "1010" 转十进制: 10
八进制 "17" 转十进制:   15
十进制 "255" 转十进制:  255
十六进制 "FF" 转十进制: 255
三十六进制 "ZZ" 转十进制: 1295

=== 自动检测进制（base = 0）===
"0x1A" 自动解析为: 26
"0o17" 自动解析为: 0
"0755" 自动解析为:  493
"123" 自动解析为:   123
```

> **注意**：`base = 0` 时，编译器根据前缀判断：`0x`/`0X` 开头是十六进制，`0` 开头是八进制，否则是十进制。现代 C++ 不支持 `0o` 前缀（这是 Python 的写法），所以 `"0o17"` 会被当作 0（因为 `o` 不是数字）。

## 6. 异常处理

这是 `stoi` 系列函数相比 C 的 `atoi` 最重要的优势：**完善的异常处理机制**。

### 6.1 可能抛出的异常

| 异常类型 | 抛出条件 |
|---------|---------|
| `std::invalid_argument` | 没有进行任何有效的数字转换（如字符串为空、全是空格、首字符不是数字/符号） |
| `std::out_of_range` | 转换后的数值超出了目标类型的范围 |

```cpp
#include <iostream>
#include <string>
#include <stdexcept>   // 异常类
using namespace std;

int main() {
    cout << "=== 异常处理演示 ===" << endl;

    // 情况 1：正常转换
    try {
        int val = stoi("123");
        cout << "正常转换: " << val << endl;
    } catch (const exception &e) {
        cout << "不应该执行到这里" << endl;
    }

    // 情况 2：无效参数（空字符串）
    cout << "\n1. 无效参数（空字符串）:" << endl;
    try {
        int val = stoi("");
        cout << "结果: " << val << endl;
    } catch (const invalid_argument &e) {
        cout << "捕获 invalid_argument: " << e.what() << endl;
    }

    // 情况 3：无效参数（全是非数字字符）
    cout << "\n2. 无效参数（非数字字符）:" << endl;
    try {
        int val = stoi("abc");
        cout << "结果: " << val << endl;
    } catch (const invalid_argument &e) {
        cout << "捕获 invalid_argument: " << e.what() << endl;
    }

    // 情况 4：超出范围
    cout << "\n3. 超出 int 范围:" << endl;
    try {
        // 2147483647 是 INT_MAX，加 1 就超出了 int 范围
        int val = stoi("2147483648");
        cout << "结果: " << val << endl;
    } catch (const out_of_range &e) {
        cout << "捕获 out_of_range: " << e.what() << endl;
    }

    // 情况 5：前导空格和尾随字符
    cout << "\n4. 前导空格和尾随字符:" << endl;
    try {
        // 前导空格会被跳过！尾随字符通过 idx 参数获取位置
        size_t idx;
        int val = stoi("   123abc", &idx);
        cout << "结果: " << val << ", 停止位置: " << idx << endl;
    } catch (const exception &e) {
        cout << "不应抛出异常" << endl;
    }

    return 0;
}
```

**预期输出：**

```
=== 异常处理演示 ===
正常转换: 123

1. 无效参数（空字符串）:
捕获 invalid_argument: stoi

2. 无效参数（非数字字符）:
捕获 invalid_argument: stoi

3. 超出 int 范围:
捕获 out_of_range: stoi

4. 前导空格和尾随字符:
结果: 123, 停止位置: 6
```

### 6.2 实用建议：安全的包装函数

在实际项目中，建议编写一个安全包装函数来处理可能的异常：

```cpp
#include <iostream>
#include <string>
#include <optional>    // C++17，如果不支持可以用 bool 返回值代替
using namespace std;

// 安全的字符串转 int 函数
bool safe_stoi(const string &str, int &result, int base = 10) {
    try {
        size_t idx;
        result = stoi(str, &idx, base);
        // 检查是否整个字符串都被转换了（可选）
        // if (idx != str.length()) return false;
        return true;
    } catch (const invalid_argument &) {
        return false;
    } catch (const out_of_range &) {
        return false;
    }
}

int main() {
    string tests[] = {"123", "abc", "9999999999", "  -42", "3.14"};

    for (const string &s : tests) {
        int val;
        if (safe_stoi(s, val)) {
            cout << "成功转换 \"" << s << "\" -> " << val << endl;
        } else {
            cout << "转换失败: \"" << s << "\"" << endl;
        }
    }

    return 0;
}
```

**预期输出：**

```
成功转换 "123" -> 123
转换失败: "abc"
转换失败: "9999999999"
成功转换 "  -42" -> -42
转换失败: "3.14"
```

## 7. 与 C 的 atoi / atol / strtol 对比

```cpp
#include <iostream>
#include <string>
#include <cstdlib>   // atoi, atol, strtol
#include <cerrno>    // errno
using namespace std;

int main() {
    cout << "=== stoi vs atoi vs strtol 对比 ===" << endl;

    string inputs[] = {"123", "abc", "  456xyz", "2147483648", "-42"};

    for (const string &s : inputs) {
        cout << "\n输入: \"" << s << "\"" << endl;

        // ---- stoi（C++11）----
        try {
            size_t idx;
            int val = stoi(s, &idx);
            cout << "  stoi:  成功, 结果 = " << val
                 << ", 停止位置 = " << idx << endl;
        } catch (const exception &e) {
            cout << "  stoi:  失败 (" << e.what() << ")" << endl;
        }

        // ---- atoi（C 风格）----
        int a_val = atoi(s.c_str());
        cout << "  atoi:  结果 = " << a_val
             << "（无法区分 0 是值还是错误）" << endl;

        // ---- strtol（C 风格，有错误检测）----
        errno = 0;
        char *end;
        long str_val = strtol(s.c_str(), &end, 10);
        if (errno == ERANGE) {
            cout << "  strtol: 溢出" << endl;
        } else if (end == s.c_str()) {
            cout << "  strtol: 未进行任何转换" << endl;
        } else {
            cout << "  strtol: 成功, 结果 = " << str_val
                 << ", 剩余 = \"" << end << "\"" << endl;
        }
    }

    return 0;
}
```

**预期输出：**

```
=== stoi vs atoi vs strtol 对比 ===

输入: "123"
  stoi:  成功, 结果 = 123, 停止位置 = 3
  atoi:  结果 = 123（无法区分 0 是值还是错误）
  strtol: 成功, 结果 = 123, 剩余 = ""

输入: "abc"
  stoi:  失败 (stoi)
  atoi:  结果 = 0（无法区分 0 是值还是错误）
  strtol: 未进行任何转换

输入: "  456xyz"
  stoi:  成功, 结果 = 456, 停止位置 = 6
  atoi:  结果 = 456（无法区分 0 是值还是错误）
  strtol: 成功, 结果 = 456, 剩余 = "xyz"

输入: "2147483648"
  stoi:  失败 (stoi)
  atoi:  结果 = 2147483647（截断，无提示！）
  strtol: 溢出

输入: "-42"
  stoi:  成功, 结果 = -42, 停止位置 = 3
  atoi:  结果 = -42（无法区分 0 是值还是错误）
  strtol: 成功, 结果 = -42, 剩余 = ""
```

| 对比项 | `stoi` (C++11) | `atoi` (C) | `strtol` (C) |
|-------|:-------------:|:----------:|:------------:|
| 类型安全 | 是（重载） | 不（只能转 int） | 不 |
| 异常处理 | `invalid_argument` / `out_of_range` | 无 | `errno` 错误码 |
| 停止位置检测 | 第二个参数 `idx` | 无 | `endptr` |
| 进制控制 | 第三个参数 `base` | 不支持 | 第三个参数 `base` |
| 错误 vs 0 的区别 | 能区分 | **不能区分** | 能区分 |
| 接口风格 | C++ string | C 字符串 | C 字符串 |

**结论**：在 C++ 项目中，**优先使用 `stoi` 系列函数**，它们更安全、更易用。

## 8. 综合完整示例

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    cout << "====== stoi/stod 综合演示 ======" << endl;

    // ---- 1. 基本用法 ----
    cout << "\n--- 1. 基本用法 ---" << endl;
    cout << stoi("42") + stoi("58") << endl;         // 100，先转再相加
    cout << "PI = " << stod("3.14159") << endl;

    // ---- 2. 进制转换 ----
    cout << "\n--- 2. 进制转换 ---" << endl;
    string hex = "FF";
    string bin = "1010";
    string oct = "77";
    cout << "十六进制 FF = " << stoi(hex, nullptr, 16) << endl;
    cout << "二进制 1010 = " << stoi(bin, nullptr, 2) << endl;
    cout << "八进制 77 = " << stoi(oct, nullptr, 8) << endl;

    // ---- 3. 解析混合字符串 ----
    cout << "\n--- 3. 解析混合字符串 ---" << endl;
    vector<string> data = {
        "温度:25°C",
        "湿度:60%",
        "价格:$19.99"
    };

    for (const string &line : data) {
        size_t colon = line.find(':');
        if (colon != string::npos) {
            string label = line.substr(0, colon);
            string value_str = line.substr(colon + 1);

            size_t idx;
            // 尝试解析为 double
            try {
                double value = stod(value_str, &idx);
                string unit = value_str.substr(idx);
                cout << label << " = " << value << " " << unit << endl;
            } catch (...) {
                cout << "无法解析: " << line << endl;
            }
        }
    }

    // ---- 4. 错误处理 ----
    cout << "\n--- 4. 错误处理 ---" << endl;
    string bad_inputs[] = {"", "   ", "abc", "12.34.56", "9999999999999999999999"};

    for (const string &s : bad_inputs) {
        try {
            int val = stoi(s);
            cout << "stoi(\"" << s << "\") = " << val << endl;
        } catch (const invalid_argument &) {
            cout << "无效参数: \"" << s << "\"" << endl;
        } catch (const out_of_range &) {
            cout << "超出范围: \"" << s << "\"" << endl;
        }
    }

    return 0;
}
```

**预期输出：**

```
====== stoi/stod 综合演示 ======

--- 1. 基本用法 ---
100
PI = 3.14159

--- 2. 进制转换 ---
十六进制 FF = 255
二进制 1010 = 10
八进制 77 = 63

--- 3. 解析混合字符串 ---
温度 = 25 °C
湿度 = 60 %
价格 = 19.99 $

--- 4. 错误处理 ---
无效参数: ""
无效参数: "   "
无效参数: "abc"
无效参数: "12.34.56"
超出范围: "9999999999999999999999"
```

## 9. 注意事项和常见坑

### 9.1 前导空格被自动跳过

所有 `stoi` 系列函数都会自动跳过前导空格：

```cpp
stoi("  123");   // 成功，返回 123
stod(" 3.14");  // 成功，返回 3.14
```

### 9.2 首字符不能是有效数字则抛出异常

```cpp
stoi("abc123");       // 抛出 invalid_argument，首字符不是数字/符号
stoi("   abc123");    // 抛出 invalid_argument，跳过空格后首字符仍是字母
stoi("   +123abc");   // 成功，返回 123（前导空格跳过，+ 是合法符号）
```

### 9.3 浮点数转整数会截断

`stoi` 在遇到小数点时停止转换（不是抛出异常），并返回小数点之前的部分：

```cpp
stoi("3.14");    // 返回 3（在小数点处停止）
stod("3.14abc"); // 返回 3.14
```

### 9.4 数值超出范围的处理

`stoi` 抛 `out_of_range`，但 `atoi` 会返回未定义结果或截断：

```cpp
stoi("9999999999999");    // 抛出 out_of_range
atoi("9999999999999");   // 返回不确定的值（未定义行为）
```

### 9.5 `size_t idx` 检查转换完整性

通过检查 `idx` 是否等于字符串长度，可以判断整个字符串是否都被成功转换：

```cpp
string s = "123abc";
size_t idx;
int val = stoi(s, &idx);
if (idx == s.length()) {
    // 整个字符串都被转换了
} else {
    // 从 idx 位置开始有未转换的字符
    cout << "剩余字符: " << s.substr(idx) << endl;
}
```

## 10. 小结

- C++11 提供了 8 个字符串转数值函数：`stoi`、`stol`、`stoll`、`stoul`、`stoull`、`stof`、`stod`、`stold`
- 第二个参数 `idx`：获取转换停止位置，用于解析混合文本
- 第三个参数 `base`：指定进制（2~36），或 `0` 表示自动检测
- 异常处理：`invalid_argument`（无效输入）和 `out_of_range`（超出范围）
- 相比 C 的 `atoi`/`strtol`，`stoi` 系列函数接口更简洁、类型更安全、错误处理更完善
- 在 C++ 项目中，**优先使用 `stoi` 系列函数**而不是 C 风格的转换函数
