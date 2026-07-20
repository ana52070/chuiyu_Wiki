---
title: map
author: claudecode(deepseekV4flash)
date: 2026-07-20 21:40:45
description: map
tags:
  - Cpp算法
categories:
  - guide
  - C++算法入门
---

## map（键值对）

### 一、概念与原理

`map` 是 C++ STL 中一种**有序的键值对（key-value）容器**。它的内部实现是**红黑树**（Red-Black Tree），一种自平衡的二叉搜索树。

**核心特性：**
- **键值对存储**：每个元素是一个 `pair<const Key, T>`，包含键（key）和值（value）
- **按键排序**：所有键值对按照键的大小自动升序排列（默认使用 `operator<` 比较键）
- **键唯一**：每个键最多出现一次，如果插入已存在的键，插入被忽略（但 `[]` 会覆盖值）
- **快速查找**：基于红黑树实现，插入、删除、查找均为 O(log n）

**可以类比为"字典"：**
- 就像查字典时用拼音（键）找释义（值）
- 每个拼音对应一个释义，一个拼音不能对应多个不同释义

**与 `unordered_map` 的简单对比：**

| 特性 | `map` | `unordered_map` |
|------|-------|-----------------|
| 底层结构 | 红黑树 | 哈希表 |
| 键的顺序 | 升序 | 无序 |
| 时间复杂度 | O(log n) | 均摊 O(1) |
| 内存占用 | 较小 | 较大 |
| 需要头文件 | `<map>` | `<unordered_map>` |

### 二、头文件

```cpp
#include <map>
```

### 三、创建方式

```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    // 1. 空构造：创建一个空的 map
    map<string, int> m1;

    // 2. 从初始化列表构造（C++11）
    map<string, int> m2 = {
        {"Alice", 85},
        {"Bob", 92},
        {"Charlie", 78}
    };
    cout << "m2 size = " << m2.size() << endl;                   // 输出: 3

    // 3. 拷贝构造
    map<string, int> m3(m2);

    // 4. 指定排序方式的 map（降序）
    map<int, string, greater<int>> m4 = {
        {1, "one"}, {2, "two"}, {3, "three"}
    };
    cout << "m4 (降序): ";
    for (const auto& [k, v] : m4) {
        cout << k << ":" << v << " ";                              // 输出: 3:three 2:two 1:one
    }
    cout << endl;

    return 0;
}
```

**预期运行结果：**
```
m2 size = 3
m4 (降序): 3:three 2:two 1:one
```

### 四、常用操作详解

#### 1. 插入元素

```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    map<string, int> scores;

    // 方式一：使用 [] 运算符（最简单，但需注意默认值问题）
    scores["Alice"] = 85;
    scores["Bob"] = 92;

    // 方式二：使用 insert() 传入 pair
    scores.insert({"Charlie", 78});          // C++11 初始化列表方式
    // 等价于：
    // scores.insert(pair<string, int>("Charlie", 78));
    // scores.insert(make_pair("Charlie", 78));

    // insert 返回 pair<iterator, bool>，bool 表示是否插入成功
    auto [it, success] = scores.insert({"Bob", 100});
    cout << "插入 Bob: " << (success ? "成功" : "失败（键已存在）") << endl;
    cout << "Bob 的得分为: " << it->second << endl;   // 仍为 92，未被覆盖

    // 方式三：insert_or_assign（C++17，如果键已存在则覆盖）
    scores.insert_or_assign("Bob", 100);
    cout << "insert_or_assign 后 Bob: " << scores["Bob"] << endl;  // 输出: 100

    return 0;
}
```

**预期运行结果：**
```
插入 Bob: 失败（键已存在）
Bob 的得分为: 92
insert_or_assign 后 Bob: 100
```

#### 2. 访问元素

```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    map<string, int> scores = {
        {"Alice", 85}, {"Bob", 92}, {"Charlie", 78}
    };

    // 方式一：[] 运算符
    // ⚠ 危险！如果键不存在，[] 会默认创建一个键值对（值初始化为 0 或空）
    cout << "Alice: " << scores["Alice"] << endl;      // 输出: 85
    cout << "David: " << scores["David"] << endl;      // 输出: 0（David 被自动插入！）

    cout << "size after accessing David: " << scores.size() << endl;  // 输出: 4

    // 方式二：at() 方法（安全，键不存在时抛出异常）
    try {
        cout << scores.at("Eve") << endl;              // 抛出 out_of_range 异常
    } catch (const out_of_range& e) {
        cout << "Exception: " << e.what() << endl;
    }

    // 验证：at() 不会自动插入键
    cout << "size after at(Eve): " << scores.size() << endl;  // 仍是 4

    return 0;
}
```

**预期运行结果：**
```
Alice: 85
David: 0
size after accessing David: 4
Exception: map::at
size after at(Eve): 4
```

> **`[]` vs `at()` 的选择：**
> - 当你要**写入**值或确定键存在时，用 `[]`（简洁直观，但注意它会创建不存在的键）
> - 当你要**读取**值但不希望意外创建新键时，用 `at()`（安全，会抛异常）
> - 在不明确键是否存在时，先用 `find()` 或 `count()` 判断

#### 3. 查找元素

```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    map<string, int> scores = {
        {"Alice", 85}, {"Bob", 92}, {"Charlie", 78}
    };

    // find()：返回迭代器，找不到返回 end()
    auto it = scores.find("Bob");
    if (it != scores.end()) {
        cout << "找到 Bob: " << it->first << " -> " << it->second << endl;
    }

    it = scores.find("David");
    if (it == scores.end()) {
        cout << "David 不存在于 map 中" << endl;
    }

    // count()：返回键的个数（对于 map 只能是 0 或 1）
    if (scores.count("Charlie") > 0) {
        cout << "Charlie 存在，得分 " << scores["Charlie"] << endl;
    }

    // 安全的读取模式：先 find 再读取
    string name = "Eve";
    auto it2 = scores.find(name);
    if (it2 != scores.end()) {
        cout << name << ": " << it2->second << endl;
    } else {
        cout << name << " 不存在" << endl;
    }

    cout << "最终 size = " << scores.size() << endl;   // 输出: 3（没有被意外插入）

    return 0;
}
```

**预期运行结果：**
```
找到 Bob: Bob -> 92
David 不存在于 map 中
Charlie 存在，得分 78
Eve 不存在
最终 size = 3
```

#### 4. 删除元素

```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    map<int, string> m = {
        {1, "one"}, {2, "two"}, {3, "three"},
        {4, "four"}, {5, "five"}
    };

    // 方式一：按键删除
    m.erase(3);
    cout << "erase(3) 后: ";
    for (const auto& [k, v] : m) cout << k << ":" << v << " ";
    cout << endl;

    // 方式二：按迭代器删除
    auto it = m.find(5);
    if (it != m.end()) {
        m.erase(it);
    }
    cout << "erase(5) 后: ";
    for (const auto& [k, v] : m) cout << k << ":" << v << " ";
    cout << endl;

    // 方式三：删除一个范围
    auto first = m.lower_bound(2);
    auto last = m.upper_bound(4);
    m.erase(first, last);                // 删除 [2, 4)，即删除键 2 和 4
    cout << "erase [2,4) 后: ";
    for (const auto& [k, v] : m) cout << k << ":" << v << " ";
    cout << endl;

    // 方式四：清空
    m.clear();
    cout << "clear 后 size = " << m.size() << endl;

    return 0;
}
```

**预期运行结果：**
```
erase(3) 后: 1:one 2:two 4:four 5:five
erase(5) 后: 1:one 2:two 4:four
erase [2,4) 后: 1:one
clear 后 size = 0
```

### 五、遍历方式

```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    map<string, int> scores = {
        {"Alice", 85}, {"Bob", 92}, {"Charlie", 78},
        {"David", 90}, {"Eve", 88}
    };

    cout << "=== 方式一：迭代器（it->first / it->second） ===" << endl;
    for (auto it = scores.begin(); it != scores.end(); ++it) {
        cout << it->first << " -> " << it->second << endl;
    }

    cout << "\n=== 方式二：范围 for + pair（C++11） ===" << endl;
    for (const pair<const string, int>& p : scores) {
        cout << p.first << " -> " << p.second << endl;
    }

    cout << "\n=== 方式三：结构化绑定（C++17 推荐） ===" << endl;
    for (const auto& [name, score] : scores) {
        cout << name << " -> " << score << endl;
    }

    cout << "\n=== 方式四：反向遍历 ===" << endl;
    for (auto it = scores.rbegin(); it != scores.rend(); ++it) {
        cout << it->first << " -> " << it->second << endl;
    }

    return 0;
}
```

**预期运行结果：**
```
=== 方式一：迭代器（it->first / it->second） ===
Alice -> 85
Bob -> 92
Charlie -> 78
David -> 90
Eve -> 88

=== 方式二：范围 for + pair（C++11） ===
Alice -> 85
Bob -> 92
Charlie -> 78
David -> 90
Eve -> 88

=== 方式三：结构化绑定（C++17 推荐） ===
Alice -> 85
Bob -> 92
Charlie -> 78
David -> 90
Eve -> 88

=== 方式四：反向遍历 ===
Eve -> 88
David -> 90
Charlie -> 78
Bob -> 92
Alice -> 85
```

### 六、性能说明

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| 插入 `[]` / `insert()` | O(log n) | 红黑树自平衡插入 |
| 访问 `[]`（键存在） | O(log n) | 搜索键并返回值 |
| 访问 `[]`（键不存在） | O(log n) | 会创建新节点 |
| 访问 `at()` | O(log n) | 搜索键，不存在则抛出异常 |
| 查找 `find()` | O(log n) | 红黑树搜索 |
| 计数 `count()` | O(log n) | 实际就是 find |
| 删除 `erase()` | O(log n) | 红黑树自平衡删除 |
| 遍历 | O(n) | 中序遍历 |

### 七、注意事项与常见坑

#### 1. `[]` 的默认构造陷阱

这是 map 最经典的坑 —— 使用 `[]` 访问不存在的键会**默认创建**它：

```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    map<string, int> freq;
    
    // 下面的代码本意是检查键是否存在
    if (freq["hello"] == 0) {
        cout << "hello 不存在" << endl;
    }
    // 但实际上，"hello" 已经被创建了！
    cout << "size = " << freq.size() << endl;     // 输出: 1
    cout << "freq[\"hello\"] = " << freq["hello"] << endl;  // 输出: 0

    // 正确做法：先 find 再操作
    // if (freq.find("hello") == freq.end()) { ... }

    return 0;
}
```

**预期运行结果：**
```
hello 不存在
size = 1
freq["hello"] = 0
```

#### 2. 修改 map 中的键

map 的键是 `const` 的，不能直接修改：

```cpp
map<int, string> m = {{1, "one"}};
auto it = m.begin();
// it->first = 2;        // 编译错误！键是 const 的
it->second = "ONE";       // 值可以修改，正确
```

#### 3. 自定义类型作为键

自定义类型作为 map 的键需要提供比较函数：

```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

struct Person {
    string name;
    int age;
};

bool operator<(const Person& a, const Person& b) {
    if (a.age != b.age) return a.age < b.age;
    return a.name < b.name;
}

int main() {
    map<Person, string> people;
    people[{"Alice", 25}] = "Engineer";
    people[{"Bob", 30}] = "Manager";
    people[{"Charlie", 25}] = "Designer";

    for (const auto& [person, job] : people) {
        cout << person.name << " (" << person.age << "): " << job << endl;
    }

    return 0;
}
```

**预期运行结果：**
```
Alice (25): Engineer
Charlie (25): Designer
Bob (30): Manager
```

#### 4. `std::multimap` 简介

如果需要**有序但键可重复**的 map，可以使用 `multimap`：

```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    multimap<string, int> grades;
    grades.insert({"Alice", 85});
    grades.insert({"Alice", 90});     // 允许重复键
    grades.insert({"Bob", 92});

    cout << "multimap 内容:" << endl;
    for (const auto& [name, score] : grades) {
        cout << name << " -> " << score << endl;
    }

    // 注意：multimap 不支持 [] 运算符
    // grades["Alice"] = 95;   // 编译错误！

    return 0;
}
```

**预期运行结果：**
```
multimap 内容:
Alice -> 85
Alice -> 90
Bob -> 92
```

> `multimap` 不支持 `[]` 运算符，只能用 `insert()` 插入。

### 八、完整可运行示例

```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    cout << "========== map 综合示例 ==========" << endl;

    // 应用场景：学生成绩管理系统
    map<string, double> grades;

    // 1. 插入数据
    grades["Alice"] = 85.5;
    grades["Bob"] = 92.0;
    grades["Charlie"] = 78.5;
    grades.insert({"David", 90.0});
    grades["Eve"] = 88.5;

    cout << "所有学生成绩:" << endl;
    for (const auto& [name, score] : grades) {
        cout << "  " << name << ": " << score << endl;
    }
    cout << "共 " << grades.size() << " 名学生" << endl;

    // 2. 查找与更新
    string searchName = "Bob";
    auto it = grades.find(searchName);
    if (it != grades.end()) {
        cout << "\n" << searchName << " 的成绩是: " << it->second << endl;
        // 修改成绩
        it->second = 95.0;
        cout << "修改后 " << searchName << " 的成绩是: " << it->second << endl;
    }

    // 3. 使用 []
    cout << "\nAlice 的成绩: " << grades["Alice"] << endl;

    // 4. 删除
    grades.erase("Eve");
    cout << "\n删除 Eve 后，剩余 " << grades.size() << " 名学生" << endl;

    // 5. 统计各分数段人数
    map<string, int> levelCount;
    for (const auto& [name, score] : grades) {
        if (score >= 90) levelCount["优秀"]++;
        else if (score >= 80) levelCount["良好"]++;
        else levelCount["及格"]++;
    }
    cout << "\n分数段统计:" << endl;
    for (const auto& [level, count] : levelCount) {
        cout << "  " << level << ": " << count << " 人" << endl;
    }

    return 0;
}
```

**预期运行结果：**
```
========== map 综合示例 ==========
所有学生成绩:
  Alice: 85.5
  Bob: 92
  Charlie: 78.5
  David: 90
  Eve: 88.5
共 5 名学生

Bob 的成绩是: 92
修改后 Bob 的成绩是: 95

Alice 的成绩: 85.5

删除 Eve 后，剩余 4 名学生

分数段统计:
  优秀: 2 人
  良好: 1 人
  及格: 1 人
```

### 九、总结

- `map` 是基于红黑树的有序键值对容器，按键自动升序排列
- `[]` 运算符简洁但危险：访问不存在的键会自动创建它
- `at()` 是安全的读取方式，键不存在时抛出 `out_of_range` 异常
- `find()` 是判断键是否存在的最稳妥方式
- C++17 的结构化绑定 `auto [k, v]` 是遍历 map 最优雅的方式
- 有序且键唯一用 `map`；有序且键可重复用 `multimap`；无序用 `unordered_map`
