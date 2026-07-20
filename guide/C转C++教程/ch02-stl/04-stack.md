---
title: stack
author: claudecode(deepseekV4flash)
date: 2026-07-20 21:40:45
description: stack
tags:
  - Cpp算法
categories:
  - guide
  - C++算法入门
---

## stack（栈）

### 一、概念与原理

`stack` 是 C++ STL 中的一种**容器适配器**（Container Adapter），它实现了**先进后出（FILO, First In Last Out）**的数据结构。

**生活类比：一摞盘子**

- 当你往一摞盘子上放一个新盘子时（push），它总是放在最上面
- 当你需要拿一个盘子时（pop），也是从最上面拿
- 最后放上去的盘子，总是最先被拿走
- 最早放上去的盘子，总是在最底部，最后才能被拿到

**核心特性：**
- **先进后出**：元素的插入和删除只能在**栈顶**（top）进行
- **容器适配器**：stack 本身不是独立的容器，而是基于其他容器（默认是 `deque`）封装的接口
- **不提供迭代器**：stack 不支持遍历

**典型应用场景：**
- 括号匹配检测（最经典）
- 函数调用栈（程序运行时）
- 表达式求值（中缀转后缀）
- 深度优先搜索（DFS）
- 撤销操作（Undo）

**栈的示意图：**
```
    push(3) →     push(5) →     push(7) →     pop() →
                  ┌─────┐       ┌─────┐       ┌─────┐
                  │     │       │  7  │       │     │
    ┌─────┐       ┌─────┐       ┌─────┐       ┌─────┐
    │     │       │  5  │       │  5  │       │  5  │
    ┌─────┐       ┌─────┐       ┌─────┐       ┌─────┐
    │  3  │       │  3  │       │  3  │       │  3  │
    └─────┘       └─────┘       └─────┘       └─────┘
```

### 二、头文件

```cpp
#include <stack>
```

### 三、创建方式

```cpp
#include <iostream>
#include <stack>
#include <vector>
#include <deque>
#include <list>
using namespace std;

int main() {
    // 1. 默认构造：基于 deque（双端队列）
    stack<int> s1;

    // 2. 基于其他容器的 stack（指定底层容器）
    stack<int, vector<int>> s2;     // 基于 vector
    stack<int, deque<int>> s3;      // 基于 deque（默认）
    stack<int, list<int>> s4;       // 基于 list

    // 3. 从已有容器构造
    deque<int> d = {1, 2, 3};
    stack<int> s5(d);               // 用 deque 初始化 stack

    cout << "s5 top = " << s5.top() << endl;              // 输出: 3（注意：deque 的尾部是栈顶）
    cout << "s5 size = " << s5.size() << endl;            // 输出: 3

    return 0;
}
```

**预期运行结果：**
```
s5 top = 3
s5 size = 3
```

### 四、常用操作详解

```cpp
#include <iostream>
#include <stack>
using namespace std;

int main() {
    stack<int> s;

    cout << "初始状态: empty = " << (s.empty() ? "yes" : "no") << ", size = " << s.size() << endl;

    // push()：压栈，将元素放入栈顶
    s.push(10);
    cout << "push(10): top = " << s.top() << ", size = " << s.size() << endl;

    s.push(20);
    cout << "push(20): top = " << s.top() << ", size = " << s.size() << endl;

    s.push(30);
    cout << "push(30): top = " << s.top() << ", size = " << s.size() << endl;

    // top()：访问栈顶元素（不移除）
    cout << "\n当前栈顶元素: " << s.top() << endl;        // 输出: 30

    // pop()：出栈，移除栈顶元素（不返回值）
    s.pop();
    cout << "pop 后: top = " << s.top() << ", size = " << s.size() << endl;

    s.pop();
    cout << "再次 pop 后: top = " << s.top() << ", size = " << s.size() << endl;

    // 遍历 stack（通过不断 pop——但会清空栈！）
    cout << "\n=== 通过 pop 遍历 stack ===" << endl;
    stack<int> temp = s;             // 拷贝一份
    while (!temp.empty()) {
        cout << temp.top() << " ";   // 访问栈顶
        temp.pop();                  // 移除栈顶
    }
    cout << endl;

    return 0;
}
```

**预期运行结果：**
```
初始状态: empty = yes, size = 0
push(10): top = 10, size = 1
push(20): top = 20, size = 2
push(30): top = 30, size = 3

当前栈顶元素: 30
pop 后: top = 20, size = 2
再次 pop 后: top = 10, size = 1

=== 通过 pop 遍历 stack ===
10
```

### 五、典型应用：括号匹配检测

这是栈最经典的应用之一。算法的核心思想：
- 遇到左括号 `(` `[` `{` 时，将其压入栈
- 遇到右括号 `)` `]` `}` 时，检查栈顶是否是对应的左括号
  - 如果匹配：栈顶出栈
  - 如果不匹配或栈为空：括号不匹配
- 遍历结束后，如果栈为空则所有括号匹配，否则不匹配

```cpp
#include <iostream>
#include <stack>
#include <string>
using namespace std;

// 判断括号是否匹配
bool isMatching(char open, char close) {
    return (open == '(' && close == ')') ||
           (open == '[' && close == ']') ||
           (open == '{' && close == '}');
}

// 检测括号匹配
bool isBalanced(const string& expr) {
    stack<char> s;

    for (char ch : expr) {
        if (ch == '(' || ch == '[' || ch == '{') {
            // 左括号：压栈
            s.push(ch);
        } else if (ch == ')' || ch == ']' || ch == '}') {
            // 右括号：检查栈顶是否匹配
            if (s.empty()) {
                cout << "  多余右括号: " << ch << endl;
                return false;
            }

            char top = s.top();
            if (isMatching(top, ch)) {
                s.pop();        // 匹配，出栈
            } else {
                cout << "  括号不匹配: " << top << " vs " << ch << endl;
                return false;
            }
        }
        // 其他字符忽略
    }

    // 遍历结束后栈应为空
    if (!s.empty()) {
        cout << "  还有未匹配的左括号: " << s.top() << endl;
        return false;
    }

    return true;
}

int main() {
    cout << "========== 括号匹配检测 ==========" << endl;

    // 测试用例
    string tests[] = {
        "()",
        "()[]{}",
        "({[]})",
        "(]",
        "([)]",
        "((())",
        "())(",
        "int main() { if (x > 0) { return 1; } }"
    };

    for (const string& expr : tests) {
        cout << "表达式: \"" << expr << "\"";
        if (isBalanced(expr)) {
            cout << "  => 匹配 ✓" << endl;
        } else {
            cout << "  => 不匹配 ✗" << endl;
        }
        cout << endl;
    }

    return 0;
}
```

**预期运行结果：**
```
========== 括号匹配检测 ==========
表达式: "()"  => 匹配 ✓

表达式: "()[]{}"  => 匹配 ✓

表达式: "({[]})"  => 匹配 ✓

表达式: "(]"  => 不匹配 ✗
  括号不匹配: ( vs ]

表达式: "([)]"  => 不匹配 ✗
  括号不匹配: [ vs )

表达式: "((())"  => 不匹配 ✗
  还有未匹配的左括号: (

表达式: "())("  => 不匹配 ✗
  多余右括号: )

表达式: "int main() { if (x > 0) { return 1; } }"  => 匹配 ✓
```

### 六、性能说明

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| `push()` | O(1) | 在栈顶插入元素 |
| `pop()` | O(1) | 移除栈顶元素 |
| `top()` | O(1) | 访问栈顶元素 |
| `size()` | O(1) | 返回元素个数 |
| `empty()` | O(1) | 判断是否为空 |

所有操作都是 O(1)，效率极高。这也是栈在很多算法中如此受欢迎的原因。

### 七、注意事项与常见坑

#### 1. 对空栈进行 top() 或 pop() 是未定义行为

```cpp
stack<int> s;
// cout << s.top() << endl;     // 崩溃！空栈没有 top
// s.pop();                     // 崩溃！空栈不能 pop

// 安全做法：先检查
if (!s.empty()) {
    cout << s.top() << endl;
    s.pop();
}
```

#### 2. pop() 不返回值

很多初学者会以为 pop 像函数调用那样返回值：

```cpp
stack<int> s;
s.push(10);
// int x = s.pop();        // 编译错误！pop 返回 void

// 正确做法
int x = s.top();           // 先获取值
s.pop();                   // 再移除
```

> 这是 C++ 设计上的考虑——如果 pop 返回值，就会涉及拷贝构造，在异常安全方面有问题。

#### 3. stack 不支持遍历

与 vector、set、map 不同，stack **没有迭代器**，不能使用范围 for 或迭代器遍历。如果要遍历栈的所有元素，必须通过不断 pop 来访问（但会清空栈），或者拷贝一份再遍历。

#### 4. stack 的内存行为

默认情况下 stack 基于 deque，不会像 vector 那样频繁扩容。但如果使用 `stack<int, vector<int>>`，则在大量 push 时会有和 vector 一样的扩容代价。

#### 5. 底层容器的选择

```cpp
#include <iostream>
#include <stack>
#include <vector>
#include <list>
#include <deque>
using namespace std;

int main() {
    // 基于 vector 的 stack（内存连续，访问快）
    stack<int, vector<int>> sv;
    sv.push(1);
    sv.push(2);
    cout << "vector-based stack top: " << sv.top() << endl;

    // 基于 list 的 stack（无重新分配开销）
    stack<int, list<int>> sl;
    sl.push(1);
    sl.push(2);
    cout << "list-based stack top: " << sl.top() << endl;

    // 默认基于 deque（折中方案）
    stack<int> sd;
    sd.push(1);
    sd.push(2);
    cout << "deque-based stack top: " << sd.top() << endl;

    return 0;
}
```

**预期运行结果：**
```
vector-based stack top: 2
list-based stack top: 2
deque-based stack top: 2
```

### 八、其他应用示例

#### 示例1：十进制转二进制

```cpp
#include <iostream>
#include <stack>
using namespace std;

int main() {
    int n = 42;
    stack<int> s;

    cout << n << " 的二进制: ";

    while (n > 0) {
        s.push(n % 2);
        n /= 2;
    }

    while (!s.empty()) {
        cout << s.top();
        s.pop();
    }
    cout << endl;   // 输出: 101010

    return 0;
}
```

**预期运行结果：**
```
42 的二进制: 101010
```

#### 示例2：简单计算器（逆波兰表达式求值）

```cpp
#include <iostream>
#include <stack>
#include <string>
#include <sstream>
using namespace std;

int main() {
    // 逆波兰表达式（后缀表达式）求值
    // 例如: "3 4 + 5 *" 等价于 (3 + 4) * 5 = 35
    string expr = "3 4 + 5 *";
    stringstream ss(expr);
    stack<int> s;
    string token;

    while (ss >> token) {
        if (token == "+" || token == "-" || token == "*" || token == "/") {
            // 运算符：弹出两个操作数，计算结果后入栈
            int b = s.top(); s.pop();   // 注意：先弹出的是右操作数
            int a = s.top(); s.pop();   // 后弹出的是左操作数

            if (token == "+") s.push(a + b);
            else if (token == "-") s.push(a - b);
            else if (token == "*") s.push(a * b);
            else if (token == "/") s.push(a / b);
        } else {
            // 数字：直接入栈
            s.push(stoi(token));
        }
    }

    cout << "\"" << expr << "\" = " << s.top() << endl;  // 输出: 35

    return 0;
}
```

**预期运行结果：**
```
"3 4 + 5 *" = 35
```

### 九、完整可运行示例

```cpp
#include <iostream>
#include <stack>
#include <string>
using namespace std;

int main() {
    cout << "========== stack 综合示例 ==========" << endl;

    // 示例：浏览器后退功能模拟
    stack<string> history;
    string currentPage = "首页";

    cout << "当前页面: " << currentPage << endl;

    // 浏览新页面
    auto visit = [&](const string& page) {
        history.push(currentPage);           // 当前页面入栈
        currentPage = page;                  // 切换到新页面
        cout << "访问: " << currentPage << endl;
    };

    // 后退
    auto back = [&]() {
        if (history.empty()) {
            cout << "无法后退：没有历史记录" << endl;
            return;
        }
        currentPage = history.top();         // 取回上一页
        history.pop();                       // 从栈中移除
        cout << "后退到: " << currentPage << endl;
    };

    visit("新闻");
    visit("体育");
    visit("科技");

    back();        // 科技 -> 体育
    back();        // 体育 -> 新闻
    back();        // 新闻 -> 首页
    back();        // 无法后退

    cout << "\n最终页面: " << currentPage << endl;

    return 0;
}
```

**预期运行结果：**
```
========== stack 综合示例 ==========
当前页面: 首页
访问: 新闻
访问: 体育
访问: 科技
后退到: 体育
后退到: 新闻
后退到: 首页
无法后退：没有历史记录

最终页面: 首页
```

### 十、总结

- `stack` 是基于容器适配器实现的 FILO（先进后出）数据结构
- 核心操作：`push()`、`pop()`、`top()`，所有操作均为 O(1)
- `pop()` 不返回值，`top()` 不移除元素——需要先 `top()` 后 `pop()`
- 对空栈调用 `top()` 或 `pop()` 是**未定义行为**（可能崩溃）
- stack 没有迭代器，不支持遍历
- 典型应用：括号匹配、表达式求值、DFS、浏览器历史记录
