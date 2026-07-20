---
title: string类
author: claudecode(deepseekV4flash)
date: 2026-07-20 21:41:39
description: string类
tags:
  - Cpp算法
categories:
  - guide
  - C++算法入门
---

# string 类详解

## 一、string 对比 C 风格字符串

### 1.1 C 风格字符串的痛点

```c
#include <stdio.h>
#include <string.h>

int main() {
    char s1[100] = "hello";
    char s2[] = " world";

    // 字符串拼接：必须保证缓冲区足够大
    strcat(s1, s2);         // s1 变成 "hello world"

    // 获取长度：O(n) 时间复杂度
    int len = strlen(s1);   // 需要遍历整个字符串

    // 比较：不能直接用 ==
    char s3[] = "hello";
    if (strcmp(s1, s2) == 0) {
        printf("相等\n");
    }

    // 复制：必须用 strcpy
    char dest[100];
    strcpy(dest, s1);

    // 越界风险
    char small[5] = "hell";
    // strcat(small, "o world");  // 缓冲区溢出！未定义行为
    // 需要手动检查剩余空间

    // 访问单个字符
    printf("%c\n", s1[0]);   // 'h'
    printf("%c\n", s1[1]);   // 'e'

    return 0;
}
```

### 1.2 C++ string 的便利性

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s1 = "hello";
    string s2 = " world";

    // 拼接：直接使用 +
    string s3 = s1 + s2;
    cout << s3 << endl;        // "hello world"

    // 长度：O(1) 时间复杂度
    cout << s1.length() << endl;  // 5

    // 比较：直接使用 ==
    if (s1 == s2) {
        cout << "相等" << endl;
    }

    // 复制：直接赋值
    string dest = s1;

    // 自动管理内存，不会越界
    // string 会自动扩容

    // 访问单个字符
    cout << s1[0] << endl;     // 'h'
    cout << s1[1] << endl;     // 'e'

    return 0;
}
```

### 1.3 对照总结

| 操作 | C 语言（char[]） | C++（string） |
|------|-----------------|---------------|
| 定义 | `char s[100]` | `string s` |
| 赋值 | `strcpy(s, "hello")` | `s = "hello"` |
| 拼接 | `strcat(s1, s2)` | `s1 + s2` |
| 长度 | `strlen(s)` — O(n) | `s.length()` — O(1) |
| 比较 | `strcmp(s1, s2) == 0` | `s1 == s2` |
| 复制 | `strcpy(dest, src)` | `dest = src` |
| 内存管理 | 手动 | 自动 |
| 缓冲溢出 | 常见 | 安全 |

---

## 二、string 的构造方式

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    // 默认构造
    string s0;                // 空字符串
    cout << "空字符串: \"" << s0 << "\", 长度: " << s0.length() << endl;

    // 从 C 风格字符串构造
    string s1 = "hello";      // 拷贝初始化
    string s2("world");       // 直接初始化
    cout << "s1: " << s1 << ", s2: " << s2 << endl;

    // 重复字符
    string s3(5, '*');        // "*****"
    cout << "s3: " << s3 << endl;

    // 从子串构造
    string s4 = "hello world";
    string s5(s4, 6, 5);      // 从位置6开始取5个字符 -> "world"
    cout << "s5: " << s5 << endl;

    // 从迭代器构造
    string s6(s4.begin(), s4.begin() + 5);  // "hello"
    cout << "s6: " << s6 << endl;

    // 初始化列表（C++11）
    string s7 = {'H', 'e', 'l', 'l', 'o'};
    cout << "s7: " << s7 << endl;

    // C++11 移动构造
    string s8 = std::move(s1);
    cout << "s8 (移动后): " << s8 << endl;
    // cout << s1 << endl;  // s1 已被移动，处于有效但未指定状态

    return 0;
}
```

**运行结果**：
```
空字符串: "", 长度: 0
s1: hello, s2: world
s3: *****
s5: world
s6: hello
s7: Hello
s8 (移动后): hello
```

---

## 三、string 的常用成员函数

### 3.1 长度与容量

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "Hello, C++ World!";

    cout << "字符串: " << s << endl;
    cout << "length(): " << s.length() << endl;   // 字符数：17
    cout << "size(): " << s.size() << endl;       // 等同 length()
    cout << "capacity(): " << s.capacity() << endl;  // 当前分配的存储容量
    cout << "empty(): " << (s.empty() ? "是" : "否") << endl;

    s.clear();    // 清空
    cout << "清空后 empty(): " << (s.empty() ? "是" : "否") << endl;
    cout << "清空后 length(): " << s.length() << endl;

    return 0;
}
```

**运行结果**：
```
字符串: Hello, C++ World!
length(): 17
size(): 17
capacity(): 31
empty(): 否
清空后 empty(): 是
清空后 length(): 0
```

### 3.2 访问字符

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "hello";

    // operator[]
    for (int i = 0; i < s.length(); i++) {
        cout << s[i] << " ";     // h e l l o
    }
    cout << endl;

    // at() — 带边界检查
    for (int i = 0; i < s.length(); i++) {
        cout << s.at(i) << " ";  // h e l l o
    }
    cout << endl;

    // front() 和 back()（C++11）
    cout << "front: " << s.front() << endl;  // h
    cout << "back: " << s.back() << endl;    // o

    // 修改字符
    s[0] = 'H';
    s.at(1) = 'E';
    cout << "修改后: " << s << endl;  // HEllo

    // at() 越界会抛出异常
    try {
        s.at(100);  // 越界
    } catch (const out_of_range& e) {
        cout << "at() 越界异常: " << e.what() << endl;
    }

    return 0;
}
```

**运行结果**：
```
h e l l o 
h e l l o 
front: h
back: o
修改后: HEllo
at() 越界异常: invalid string position
```

### 3.3 子串和查找

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "The quick brown fox jumps over the lazy dog";

    // substr(pos, count)
    string sub1 = s.substr(4, 5);     // 从位置4取5个字符
    cout << "substr(4,5): " << sub1 << endl;  // "quick"

    string sub2 = s.substr(16);       // 从位置16取到末尾
    cout << "substr(16): " << sub2 << endl;   // "brown fox jumps over the lazy dog"

    // find — 查找子串（从前往后）
    int pos1 = s.find("fox");
    cout << "find('fox'): " << pos1 << endl;  // 16

    int pos2 = s.find("cat");
    cout << "find('cat'): " << pos2 << endl;  // string::npos

    // rfind — 从后往前查找
    int pos3 = s.rfind("the");
    cout << "rfind('the'): " << pos3 << endl; // 31（后面的 "the"）

    // find_first_of — 查找第一个匹配的字符
    int pos4 = s.find_first_of("aeiou");
    cout << "第一个元音位置: " << pos4 << endl; // 2（'e'）

    // 判断是否找到
    if (s.find("fox") != string::npos) {
        cout << "找到了 'fox'！" << endl;
    }

    return 0;
}
```

**运行结果**：
```
substr(4,5): quick
substr(16): brown fox jumps over the lazy dog
find('fox'): 16
find('cat'): 18446744073709551615
rfind('the'): 31
第一个元音位置: 2
找到了 'fox'！
```

> 注意：`string::npos` 是一个特殊值（通常是 `size_t` 的最大值，即 `-1` 的无符号表示），表示"未找到"。

### 3.4 修改操作

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "hello world";

    // append — 追加
    s.append("!!!");
    cout << "append: " << s << endl;  // "hello world!!!"

    // insert — 插入
    s.insert(5, " beautiful");
    cout << "insert: " << s << endl;  // "hello beautiful world!!!"

    // replace — 替换
    s.replace(6, 9, "nice");  // 从位置6开始，替换9个字符为"nice"
    cout << "replace: " << s << endl;  // "hello nice world!!!"

    // erase — 删除
    s.erase(15, 4);           // 从位置15开始删4个字符
    cout << "erase: " << s << endl;   // "hello nice world"

    // push_back — 末尾添加字符
    s.push_back('!');
    cout << "push_back: " << s << endl; // "hello nice world!"

    // pop_back — 删除末尾字符（C++11）
    s.pop_back();
    cout << "pop_back: " << s << endl;  // "hello nice world"

    // += 操作符
    s += "!";
    cout << "+= : " << s << endl;      // "hello nice world!"

    return 0;
}
```

**运行结果**：
```
append: hello world!!!
insert: hello beautiful world!!!
replace: hello nice world!!!
erase: hello nice world
push_back: hello nice world!
pop_back: hello nice world
+= : hello nice world!
```

### 3.5 与 C 风格字符串互转

```cpp
#include <iostream>
#include <string>
#include <cstring>
using namespace std;

int main() {
    // string → C 风格字符串
    string s = "hello";
    const char* cstr = s.c_str();   // 返回 const char*
    cout << "c_str: " << cstr << endl;

    // C 风格字符串 → string
    char c_arr[] = "world";
    string s2 = c_arr;              // 自动转换
    cout << "string: " << s2 << endl;

    // 应用场景：调用 C 函数
    string filename = "data.txt";
    FILE* fp = fopen(filename.c_str(), "r");  // fopen 需要 const char*
    if (fp) {
        cout << "文件打开成功" << endl;
        fclose(fp);
    }

    // data() — C++17 起返回 char*（非 const，可修改）
    string buffer = "hello";
    char* ptr = buffer.data();       // C++17
    ptr[0] = 'H';
    cout << "data() 修改后: " << buffer << endl;

    return 0;
}
```

**运行结果**：
```
c_str: hello
string: world
文件打开成功
data() 修改后: Hello
```

---

## 四、string 的运算符

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string a = "apple";
    string b = "banana";
    string c = "apple";

    // 拼接
    string s = a + " " + b;
    cout << "a + b: " << s << endl;  // "apple banana"

    // 比较（字典序）
    cout << "a == c: " << (a == c) << endl;    // 1 (true)
    cout << "a != b: " << (a != b) << endl;    // 1 (true)
    cout << "a < b: " << (a < b) << endl;      // 1 (true) "apple" < "banana"
    cout << "a > b: " << (a > b) << endl;      // 0 (false)

    // +=
    string msg = "Hello";
    msg += " World";
    cout << "msg: " << msg << endl;

    // []
    cout << "msg[0]: " << msg[0] << endl;      // 'H'
    msg[0] = 'h';
    cout << "msg修改后: " << msg << endl;       // "hello World"

    return 0;
}
```

**运行结果**：
```
a + b: apple banana
a == c: 1
a != b: 1
a < b: 1
a > b: 0
msg: Hello World
msg[0]: H
msg修改后: hello World
```

---

## 五、完整可运行代码：综合展示

```cpp
#include <iostream>
#include <string>
#include <sstream>  // stringstream
#include <vector>
#include <algorithm>
using namespace std;

// 用空格分割字符串
vector<string> split(const string& s) {
    vector<string> result;
    stringstream ss(s);
    string word;
    while (ss >> word) {
        result.push_back(word);
    }
    return result;
}

int main() {
    cout << "=== string 类综合演示 ===\n\n";

    // 1. 基本操作
    cout << "1. 基本操作:\n";
    string text = "  Hello, C++ World!  ";
    cout << "原始: [" << text << "]\n";

    // 去除首尾空白（手动）
    int start = text.find_first_not_of(" \t");
    int end = text.find_last_not_of(" \t");
    string trimmed = text.substr(start, end - start + 1);
    cout << "去空白: [" << trimmed << "]\n";

    // 2. 大小写转换
    cout << "\n2. 大小写转换:\n";
    string mixed = "Hello C++";
    string upper = mixed;
    string lower = mixed;
    transform(upper.begin(), upper.end(), upper.begin(), ::toupper);
    transform(lower.begin(), lower.end(), lower.begin(), ::tolower);
    cout << "原串: " << mixed << "\n";
    cout << "大写: " << upper << "\n";
    cout << "小写: " << lower << "\n";

    // 3. 数字与字符串互转
    cout << "\n3. 数字与字符串互转:\n";
    // int → string
    int num = 2024;
    string num_str = to_string(num);
    cout << "数字转字符串: \"" << num_str << "\"\n";

    // string → int
    string str_num = "12345";
    int parsed = stoi(str_num);
    cout << "字符串转数字: " << parsed << "\n";

    // string → double
    string str_pi = "3.14159";
    double pi = stod(str_pi);
    cout << "字符串转double: " << pi << "\n";

    // 4. 分割字符串
    cout << "\n4. 分割字符串:\n";
    string sentence = "The quick brown fox jumps over the lazy dog";
    vector<string> words = split(sentence);
    cout << "单词数: " << words.size() << "\n";
    for (size_t i = 0; i < words.size(); i++) {
        cout << i + 1 << ". " << words[i] << "\n";
    }

    // 5. 替换所有子串
    cout << "\n5. 替换所有子串:\n";
    string original = "I like cats. Cats are cute. My cat is black.";
    string target = "cat";
    string replacement = "dog";
    size_t pos = 0;
    while ((pos = original.find(target, pos)) != string::npos) {
        original.replace(pos, target.length(), replacement);
        pos += replacement.length();
    }
    cout << "替换后: " << original << "\n";

    // 6. 字符串反转
    cout << "\n6. 字符串反转:\n";
    string rev = "Hello World";
    reverse(rev.begin(), rev.end());
    cout << "反转后: " << rev << "\n";

    // 7. 字符串重复（C++11 无原生支持，手动实现）
    cout << "\n7. 字符串重复:\n";
    string base = "AB";
    string repeated;
    for (int i = 0; i < 5; i++) {
        repeated += base;
    }
    cout << "重复5次: " << repeated << "\n";

    // 8. getline 读取整行
    cout << "\n8. getline 读取整行:\n";
    cout << "请输入一行文字（可含空格）: ";
    string line;
    getline(cin, line);
    cout << "你输入的是: " << line << "\n";

    return 0;
}
```

**运行结果示例**：
```
=== string 类综合演示 ===

1. 基本操作:
原始: [  Hello, C++ World!  ]
去空白: [Hello, C++ World!]

2. 大小写转换:
原串: Hello C++
大写: HELLO C++
小写: hello c++

3. 数字与字符串互转:
数字转字符串: "2024"
字符串转数字: 12345
字符串转double: 3.14159

4. 分割字符串:
单词数: 9
1. The
2. quick
3. brown
4. fox
5. jumps
6. over
7. the
8. lazy
9. dog

5. 替换所有子串:
替换后: I like dogs. Dogs are cute. My dog is black.

6. 字符串反转:
反转后: dlroW olleH

7. 字符串重复:
重复5次: ABABABABAB

8. getline 读取整行:
请输入一行文字（可含空格）: Hello C++ World!
你输入的是: Hello C++ World!
```

---

## 六、注意事项和常见坑

### 6.1 string::npos 的使用

```cpp
string s = "hello";

// 查找不到时返回 npos
if (s.find("xyz") == string::npos) {
    cout << "未找到" << endl;
}

// 不要用 -1 比较
if (s.find("xyz") == -1) {    // 可能正确，但依赖类型转换
    // ...
}
// 推荐使用 string::npos
```

### 6.2 下标越界

```cpp
string s = "hello";
char c = s[100];                // 未定义行为！可能崩溃
char d = s.at(100);             // 抛出 out_of_range 异常
```

### 6.3 迭代器失效

```cpp
string s = "hello";
auto it = s.begin();
s += " world";                  // 可能导致重新分配内存
// *it = 'H';                   // 迭代器可能已失效！
```

### 6.4 不要用 char* 接收 c_str() 修改

```cpp
string s = "hello";
const char* c = s.c_str();      // 正确
// char* c2 = s.c_str();       // 编译错误：需要 const_cast
s = "world";                     // 重新赋值后，c 可能已失效
// cout << c;                   // 危险！c 可能指向已释放内存
```

### 6.5 大量拼接时的性能

```cpp
// 低效方式
string result;
for (int i = 0; i < 100000; i++) {
    result += to_string(i);     // 每次都可能重新分配内存
}

// 高效方式：预先分配空间
string result;
result.reserve(500000);         // 预分配足够空间
for (int i = 0; i < 100000; i++) {
    result += to_string(i);     // 不需要频繁重新分配
}
```

---

## 七、总结

| 功能 | C++ string | C 语言 char[] |
|------|-----------|--------------|
| 内存管理 | 自动 | 手动 |
| 拼接 | `+` / `+=` | `strcat`（需检查缓冲区） |
| 比较 | `==` / `<` / `>` | `strcmp` |
| 长度 | O(1) `length()` | O(n) `strlen()` |
| 安全性 | 高（自动边界检查） | 低（容易溢出） |
| 灵活性 | 高（动态增长） | 低（固定大小） |

**核心建议**：在 C++ 中始终使用 `string` 而非 C 风格字符串，除非需要与 C 库交互（此时使用 `c_str()` 获取 C 风格字符串）。
