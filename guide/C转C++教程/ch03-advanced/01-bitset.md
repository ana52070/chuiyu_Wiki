---
title: bitset
author: claudecode(deepseekV4flash)
date: 2026-07-20 21:39:51
description: bitset
tags:
  - Cpp算法
categories:
  - guide
  - C++算法入门
---

# bitset：固定大小的二进制位容器

## 1. bitset 概述

`bitset` 是 C++ 标准库中一个非常实用的模板类，它提供了一种**固定大小**的二进制位容器，可以对二进制位进行高效的操作和运算。与 `vector<bool>` 或 `std::bitset` 的 Boost 版本不同，`std::bitset` 的大小在**编译期确定**（通过模板参数指定），因此具有极高的运行效率。

### 头文件

```cpp
#include <bitset>
```

### 模板声明

```cpp
template<size_t N>
class bitset;
```

其中 `N` 是一个非类型模板参数，表示 bitset 中包含的二进制位的个数。`N` 必须是编译期常量。

### 基本原理

`bitset` 内部通常使用 `unsigned long` 或 `unsigned long long` 数组来存储位数据，每个位只占用 1 bit 的内存空间，因此存储密度极高。例如 `bitset<64>` 只需要 8 字节（一个 64 位整数）即可存储。

---

## 2. 核心概念：索引方向

这是初学者最容易搞混的地方，务必仔细阅读。

**`b[0]` 表示最低位（LSB，Least Significant Bit）**，即二进制数的最右边一位。而直接输出 bitset 对象时，显示的是从最高位（MSB，Most Significant Bit）到最低位（LSB）的顺序。

```cpp
#include <bitset>
#include <iostream>
using namespace std;

int main() {
    bitset<8> b(0b00001101);  // 二进制字面量，十进制 13

    cout << "bitset 内容 : " << b << endl;   // 输出：00001101
    cout << "b[0]       : " << b[0] << endl;  // 输出：1  （最低位）
    cout << "b[1]       : " << b[1] << endl;  // 输出：0
    cout << "b[2]       : " << b[2] << endl;  // 输出：1
    cout << "b[3]       : " << b[3] << endl;  // 输出：1
    cout << "b[7]       : " << b[7] << endl;  // 输出：0  （最高位）
    return 0;
}
```

**预期输出：**

```
bitset 内容 : 00001101
b[0]       : 1
b[1]       : 0
b[2]       : 1
b[3]       : 1
b[7]       : 0
```

**重要结论**：
- 直接输出的二进制字符串 `00001101`，最左边是第 7 位（MSB），最右边是第 0 位（LSB）
- `b[0]` 访问的是字符串的最后一个字符（最右边的那一位）
- 在使用位索引进行操作时，始终记住：**索引 0 对应 2^0（值为 1），索引 n 对应 2^n**

---

## 3. 构造函数（构造方式）

`bitset` 提供多种构造方式，其中字符串构造最为灵活。

### 3.1 默认构造

```cpp
bitset<8> b;  // 所有位初始化为 0
// 输出：00000000
```

### 3.2 从 unsigned long 构造

```cpp
bitset<8> b(13);   // 十进制 13 = 二进制 00001101
cout << b;         // 输出：00001101

bitset<8> b2(255); // 十进制 255 = 二进制 11111111
cout << b2;        // 输出：11111111
```

如果数值的二进制位数超过 bitset 大小，高位被截断：

```cpp
bitset<4> b(255);  // 255 = 11111111（8 位），截断后保留低 4 位
cout << b;         // 输出：1111
```

### 3.3 从字符串构造

```cpp
// 完整字符串构造
bitset<8> b1(string("1101"));
cout << b1;        // 输出：00001101（高位补 0）

// 也可以直接传 C 风格字符串
bitset<8> b2("1101");
```

**重要细节**：字符串的第一个字符对应最高位（MSB），最后一个字符对应最低位（LSB）。因此 `string("1101")` 中，'1' 是第 7 位（最高位），'0' 是第 6 位，'1' 是第 5 位，'1' 是第 4 位，其余高 4 位（第 3~0 位）补 0。

### 3.4 子串构造

```cpp
string s = "11001100";
bitset<8> b(s, 2, 4);  // 从 s 的索引 2 开始，取 4 个字符："0011"
cout << b;             // 输出：00000011（高位补 0）
```

**完整示例**：

```cpp
#include <bitset>
#include <iostream>
#include <string>
using namespace std;

int main() {
    // 1. 默认构造
    bitset<8> b1;
    cout << "b1 (默认)          : " << b1 << endl;

    // 2. unsigned long 构造
    bitset<8> b2(13);
    cout << "b2 (13)            : " << b2 << endl;

    // 3. 字符串构造
    bitset<8> b3(string("1101"));
    cout << "b3 (\"1101\")        : " << b3 << endl;

    // 4. 子串构造
    string s = "10101111";
    bitset<4> b4(s, 2, 2);
    cout << "b4 (s[2..3])       : " << b4 << endl;

    // 5. 截断情况
    bitset<4> b5(255);
    cout << "b5 (255 截断 4 位) : " << b5 << endl;

    return 0;
}
```

**预期输出**：

```
b1 (默认)          : 00000000
b2 (13)            : 00001101
b3 ("1101")        : 00001101
b4 (s[2..3])       : 1010
b5 (255 截断 4 位) : 1111
```

---

## 4. 常用成员函数

### 4.1 状态查询函数

| 函数 | 原型 | 说明 |
|------|------|------|
| `any()` | `bool any() const` | 是否存在至少一个 1 |
| `none()` | `bool none() const` | 是否全为 0（没有 1） |
| `all()` | `bool all() const` | 是否全为 1（C++11 起） |
| `count()` | `size_t count() const` | 返回 1 的个数 |
| `size()` | `size_t size() const` | 返回 bitset 总位数（即 N） |
| `test(i)` | `bool test(size_t i) const` | 第 i 位是否为 1（带边界检查） |

```cpp
#include <bitset>
#include <iostream>
using namespace std;

int main() {
    bitset<8> b(0b01011010);  // 二进制：01011010

    cout << boolalpha;  // 以 true/false 输出布尔值
    cout << "bitset    : " << b << endl;
    cout << "any()     : " << b.any() << endl;     // true（有 1）
    cout << "none()    : " << b.none() << endl;    // false（有 1）
    cout << "all()     : " << b.all() << endl;     // false（不全为 1）
    cout << "count()   : " << b.count() << endl;    // 4
    cout << "size()    : " << b.size() << endl;     // 8
    cout << "test(0)   : " << b.test(0) << endl;   // false（b[0]=0）
    cout << "test(1)   : " << b.test(1) << endl;   // true（b[1]=1）

    // test() 与 operator[] 的区别：test() 会做边界检查，越界抛出异常
    // cout << b.test(100);  // 抛出 std::out_of_range 异常

    return 0;
}
```

**预期输出**：

```
bitset    : 01011010
any()     : true
none()    : false
all()     : false
count()   : 4
size()    : 8
test(0)   : false
test(1)   : true
```

**注意事项**：
- `all()` 是 C++11 新增的，早期编译器可能不支持
- `test(i)` 会检查 `i < N`，如果越界抛出 `std::out_of_range` 异常
- `operator[]` **不做**边界检查，越界访问导致未定义行为
- `count()` 的时间复杂度在不同的实现中可能不同，但通常经过精心优化

### 4.2 位操作函数

| 函数 | 说明 |
|------|------|
| `set()` | 将所有位设为 1 |
| `set(i, val)` | 将第 i 位设为 val（val 默认为 true） |
| `reset()` | 将所有位设为 0 |
| `reset(i)` | 将第 i 位设为 0 |
| `flip()` | 将所有位取反（0 变 1，1 变 0） |
| `flip(i)` | 将第 i 位取反 |

```cpp
#include <bitset>
#include <iostream>
using namespace std;

int main() {
    bitset<8> b;

    cout << "初始值      : " << b << endl;   // 00000000

    // set() — 全部置 1
    b.set();
    cout << "set()       : " << b << endl;   // 11111111

    // reset() — 全部置 0
    b.reset();
    cout << "reset()     : " << b << endl;   // 00000000

    // set(i) — 将第 i 位置 1
    b.set(0);   // LSB 置 1
    b.set(3);
    b.set(7);   // MSB 置 1
    cout << "set(0/3/7)  : " << b << endl;   // 10001001

    // reset(i) — 将第 i 位置 0
    b.reset(3);
    cout << "reset(3)    : " << b << endl;   // 10000001

    // flip() — 全部取反
    b.flip();
    cout << "flip()      : " << b << endl;   // 01111110

    // flip(i) — 第 i 位取反
    b.flip(0);
    cout << "flip(0)     : " << b << endl;   // 01111111

    // set(i, val) — 指定值
    b.set(7, false);
    cout << "set(7, 0)   : " << b << endl;   // 01111111

    return 0;
}
```

**预期输出**：

```
初始值      : 00000000
set()       : 11111111
reset()     : 00000000
set(0/3/7)  : 10001001
reset(3)    : 10000001
flip()      : 01111110
flip(0)     : 01111111
set(7, 0)   : 01111111
```

**注意事项**：
- `set()`（无参数）和 `set(i)` 是不同的重载，前者操作所有位，后者操作指定位
- `set(i)` 的第二个参数 `val` 默认为 `true`（即 1），可以显式传入 `false`（即 0），效果等价于 `reset(i)`

### 4.3 类型转换函数

| 函数 | 说明 |
|------|------|
| `to_ulong()` | 转换为 `unsigned long`，如果超出范围抛出 `overflow_error` |
| `to_ullong()` | 转换为 `unsigned long long`（C++11 起） |
| `to_string()` | 转换为 `string`，'0'/'1' 组成的字符串 |

```cpp
#include <bitset>
#include <iostream>
#include <string>
using namespace std;

int main() {
    bitset<8> b(0b01001101);

    // to_string() — 转换为字符串
    string s = b.to_string();
    cout << "to_string() : " << s << endl;       // "01001101"

    // to_ulong() — 转换为 unsigned long
    unsigned long ul = b.to_ulong();
    cout << "to_ulong()  : " << ul << endl;       // 77

    // to_ullong() — 转换为 unsigned long long
    unsigned long long ull = b.to_ullong();
    cout << "to_ullong() : " << ull << endl;      // 77

    // 超出范围的情况
    bitset<100> big;
    big.set();
    // unsigned long val = big.to_ulong();  // 抛出 std::overflow_error

    return 0;
}
```

**预期输出**：

```
to_string() : 01001101
to_ulong()  : 77
to_ullong() : 77
```

**注意事项**：
- `to_string()` 可以不指定模板参数，默认使用 `char`、`char_traits<char>`、`allocator<char>`
- 可以自定义字符类型：`b.to_string<'X', '_'>()` 用 'X' 表示 1，'_' 表示 0
- 如果 bitset 的值超过了 `unsigned long` 或 `unsigned long long` 的表示范围，`to_ulong()` 和 `to_ullong()` 会抛出 `std::overflow_error` 异常

---

## 5. 运算符支持

`bitset` 支持丰富的位运算符，让位操作更加直观。

### 5.1 位运算符

```cpp
#include <bitset>
#include <iostream>
using namespace std;

int main() {
    bitset<8> a(0b10101010);  // 170
    bitset<8> b(0b11001100);  // 204

    cout << "a       : " << a << endl;   // 10101010
    cout << "b       : " << b << endl;   // 11001100

    // 按位与
    cout << "a & b   : " << (a & b) << endl;   // 10001000

    // 按位或
    cout << "a | b   : " << (a | b) << endl;   // 11101110

    // 按位异或
    cout << "a ^ b   : " << (a ^ b) << endl;   // 01100110

    // 取反
    cout << "~a      : " << (~a) << endl;       // 01010101

    // 左移
    cout << "a << 2  : " << (a << 2) << endl;   // 10101000（左移 2 位，低位补 0）

    // 右移
    cout << "a >> 2  : " << (a >> 2) << endl;   // 00101010（右移 2 位，高位补 0）

    return 0;
}
```

**预期输出**：

```
a       : 10101010
b       : 11001100
a & b   : 10001000
a | b   : 11101110
a ^ b   : 01100110
~a      : 01010101
a << 2  : 10101000
a >> 2  : 00101010
```

### 5.2 比较运算符和下标运算符

```cpp
#include <bitset>
#include <iostream>
using namespace std;

int main() {
    bitset<8> a(0b10101010);
    bitset<8> b(0b10101010);  // 与 a 相同
    bitset<8> c(0b11001100);  // 与 a 不同

    // == 和 !=
    cout << boolalpha;
    cout << "a == b : " << (a == b) << endl;   // true
    cout << "a != b : " << (a != b) << endl;   // false
    cout << "a == c : " << (a == c) << endl;   // false
    cout << "a != c : " << (a != c) << endl;   // true

    // operator[] - 读写下标
    cout << "a[0]   : " << a[0] << endl;        // 0
    cout << "a[1]   : " << a[1] << endl;        // 1

    a[0] = 1;   // 修改第 0 位
    cout << "a[0]=1 : " << a << endl;           // 10101011

    return 0;
}
```

**预期输出**：

```
a == b : true
a != b : false
a == c : false
a != c : true
a[0]   : 0
a[1]   : 1
a[0]=1 : 10101011
```

**注意事项**：
- `operator[]` 返回一个特殊的引用类型（`bitset::reference`），它可以隐式转换为 `bool`，也可以被赋值
- `operator[]` **不做**边界检查；越界访问是未定义行为
- 位运算符 `&`、`|`、`^`、`~`、`<<`、`>>` 返回一个新的 `bitset` 对象，不会修改原对象

---

## 6. 综合示例

```cpp
#include <bitset>
#include <iostream>
#include <string>
using namespace std;

int main() {
    cout << "========== bitset 综合示例 ==========\n\n";

    // 1. 构造与输出
    cout << "--- 构造与输出 ---\n";
    bitset<8> b1;                    // 默认全 0
    bitset<8> b2(42);                // 42 = 0b00101010
    bitset<8> b3(string("1010"));    // 字符串构造
    bitset<8> b4(b2);                // 拷贝构造

    cout << "b1 (默认)        : " << b1 << endl;
    cout << "b2 (42)          : " << b2 << endl;
    cout << "b3 (\"1010\")      : " << b3 << endl;
    cout << "b4 (b2 的拷贝)   : " << b4 << endl;
    cout << endl;

    // 2. 索引方向验证
    cout << "--- 索引方向验证 ---\n";
    bitset<8> b(0b00001101);  // 十进制 13
    cout << "b = " << b << endl;
    cout << "第 0 位（LSB）: " << b[0] << endl;
    cout << "第 7 位（MSB）: " << b[7] << endl;
    cout << "最低位 " << b[0]
         << " 对应十进制的 " << (b[0] ? 1 : 0) << endl;
    cout << endl;

    // 3. 状态查询
    cout << "--- 状态查询 ---\n";
    bitset<8> c(0b01101001);
    cout << "c = " << c << endl;
    cout << "any()  : " << boolalpha << c.any() << endl;
    cout << "none() : " << c.none() << endl;
    cout << "all()  : " << c.all() << endl;
    cout << "count(): " << c.count() << " 个 1\n";
    cout << "size() : " << c.size() << " 位\n";
    cout << "test(3): " << c.test(3) << endl;
    cout << endl;

    // 4. 位操作
    cout << "--- 位操作 ---\n";
    bitset<8> d;
    d.set();
    cout << "d.set()          : " << d << endl;
    d.reset(7);
    cout << "d.reset(7)       : " << d << endl;
    d.flip(0);
    cout << "d.flip(0)        : " << d << endl;
    d.set(3, false);
    cout << "d.set(3, false)  : " << d << endl;
    cout << endl;

    // 5. 类型转换
    cout << "--- 类型转换 ---\n";
    bitset<8> e(0b11111111);
    cout << "e = " << e << endl;
    cout << "to_ulong()       : " << e.to_ulong() << endl;
    cout << "to_string()      : " << e.to_string() << endl;

    // 6. 位运算
    cout << "\n--- 位运算 ---\n";
    bitset<8> x(0b10101010);
    bitset<8> y(0b11001100);
    cout << "x       : " << x << endl;
    cout << "y       : " << y << endl;
    cout << "x & y   : " << (x & y) << endl;
    cout << "x | y   : " << (x | y) << endl;
    cout << "x ^ y   : " << (x ^ y) << endl;
    cout << "~x      : " << (~x) << endl;
    cout << "x << 2  : " << (x << 2) << endl;
    cout << "x >> 2  : " << (x >> 2) << endl;

    return 0;
}
```

**预期输出**：

```
========== bitset 综合示例 ==========

--- 构造与输出 ---
b1 (默认)        : 00000000
b2 (42)          : 00101010
b3 ("1010")      : 00001010
b4 (b2 的拷贝)   : 00101010

--- 索引方向验证 ---
b = 00001101
第 0 位（LSB）: 1
第 7 位（MSB）: 0
最低位 1 对应十进制的 1

--- 状态查询 ---
c = 01101001
any()  : true
none() : false
all()  : false
count(): 4 个 1
size() : 8 位
test(3): 0

--- 位操作 ---
d.set()          : 11111111
d.reset(7)       : 01111111
d.flip(0)        : 01111110
d.set(3, false)  : 01110110

--- 类型转换 ---
e = 11111111
to_ulong()       : 255
to_string()      : 11111111

--- 位运算 ---
x       : 10101010
y       : 11001100
x & y   : 10001000
x | y   : 11101110
x ^ y   : 01100110
~x      : 01010101
x << 2  : 10101000
x >> 2  : 00101010
```

---

## 7. 常见坑与注意事项总结

1. **索引方向**：`b[0]` 是最低位（LSB），输出字符串的最右边字符。这是最容易出错的地方。

2. **编译期大小**：bitset 的大小必须在编译期确定（模板参数），不能动态改变。如果需要动态大小的位集，考虑 `vector<bool>` 或 Boost 的 `dynamic_bitset`。

3. **边界检查**：`operator[]` 不做边界检查；`test(i)` 做边界检查。出于性能考虑，如果确定索引合法，使用 `operator[]`。

4. **`to_ulong()` 的溢出异常**：如果 bitset 的值无法用 `unsigned long` 表示，会抛出 `std::overflow_error`。使用时最好用 try-catch 包裹。

5. **字符串构造的顺序**：字符串的第一个字符对应最高位（MSB），最后一个字符对应最低位（LSB）。这与 `b[0]` 是最低位一致，但与直觉可能相反。

6. **空字符的处理**：字符串中的字符只能是 `'0'` 或 `'1'`，包含其他字符会抛出 `std::invalid_argument` 异常。

7. **`operator[]` 返回引用类型**：`b[i]` 返回的不是普通的 `bool&`，而是 `std::bitset::reference`，这是一个代理类，支持隐式转换为 `bool` 和赋值操作。

8. **`all()` 需要 C++11**：如果编译标准低于 C++11，`all()` 不可用，可以用 `count() == size()` 替代。

9. **位移操作不修改原对象**：`b << 2` 返回一个新的 bitset，`b` 本身不变。如果要修改 b，需要用 `b = b << 2;`。
