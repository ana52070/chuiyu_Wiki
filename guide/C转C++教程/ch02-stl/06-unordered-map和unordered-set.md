---
title: unordered-map和unordered-set
author: claudecode(deepseekV4flash)
date: 2026-07-20 21:40:45
description: unordered-map和unordered-set
tags:
  - Cpp算法
categories:
  - guide
  - C++算法入门
---

## unordered_map 和 unordered_set（无序容器）

### 一、概念与原理

`unordered_map` 和 `unordered_set` 是 C++ STL 中**基于哈希表（Hash Table）实现的无序容器**，分别对应 `map` 和 `set` 的无序版本。

#### 哈希表的基本原理

哈希表的核心思想是：通过**哈希函数（hash function）** 将键（key）映射到一个数组的索引（桶，bucket）上，从而实现近似 O(1) 的查找速度。

```
         键(key)               哈希函数              桶(bucket)
        ┌──────┐              ┌──────────┐        ┌─────────┐
        │ "abc" │ ──────────▶  │ hash("abc") │ ──▶ │ [0]     │
        └──────┘              └──────────┘        ├─────────┤
                                                   │ [1]     │
        ┌──────┐              ┌──────────┐        │   ↓     │
        │ "xyz" │ ──────────▶  │ hash("xyz") │ ──▶ │  "abc"  │  ← 冲突
        └──────┘              └──────────┘        │   ↓     │
                                                   │  "xyz"  │
                                                   ├─────────┤
                                                   │ [2]     │
                                                   └─────────┘
```

**关键概念：**

1. **哈希函数**：将任意大小的键映射到固定范围整数（桶索引）的函数
2. **哈希冲突**：两个不同的键被映射到同一个桶的现象
3. **冲突解决方式**：C++ STL 中使用**链地址法（separate chaining）**，即每个桶中维护一个链表，冲突的元素放在同一个桶的链表中
4. **负载因子（load factor）**：元素总数 / 桶数。当负载因子超过阈值时，哈希表会**rehash**（增加桶数并重新分配所有元素）

#### 与有序版本的核心区别

| 特性 | `map` / `set` | `unordered_map` / `unordered_set` |
|------|---------------|----------------------------------|
| 底层结构 | 红黑树（平衡二叉搜索树） | 哈希表 |
| 元素顺序 | **有序**（按键升序） | **无序**（无特定顺序） |
| 查找时间复杂度 | O(log n) | 均摊 O(1)，最坏 O(n) |
| 插入时间复杂度 | O(log n) | 均摊 O(1) |
| 删除时间复杂度 | O(log n) | 均摊 O(1) |
| 内存占用 | 较小（只需树节点） | 较大（桶 + 链表 + 节点） |
| 需要头文件 | `<map>` / `<set>` | `<unordered_map>` / `<unordered_set>` |
| 需要比较函数 | 需要 `operator<` | 需要 `operator==` 和哈希函数 |
| 范围查询 | 支持（lower_bound/upper_bound） | 不支持 |
| 自定义类型支持 | 更容易（只需定义 <） | 较麻烦（需提供 hash 和 ==） |

### 二、头文件

```cpp
#include <unordered_map>
#include <unordered_set>
```

### 三、创建方式

```cpp
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <string>
using namespace std;

int main() {
    // ========== unordered_map ==========

    // 1. 空构造
    unordered_map<string, int> um1;

    // 2. 初始化列表构造
    unordered_map<string, int> um2 = {
        {"Alice", 85},
        {"Bob", 92},
        {"Charlie", 78}
    };
    cout << "um2 size = " << um2.size() << endl;               // 输出: 3

    // 3. 指定桶数（预分配）
    unordered_map<string, int> um3(20);                         // 至少 20 个桶
    cout << "um3 bucket_count = " << um3.bucket_count() << endl;

    // ========== unordered_set ==========

    // 1. 空构造
    unordered_set<int> us1;

    // 2. 初始化列表构造
    unordered_set<int> us2 = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3};
    cout << "us2 (无序+去重): ";
    for (int x : us2) cout << x << " ";
    cout << endl;

    // 3. 指定桶数
    unordered_set<int> us3(50);

    return 0;
}
```

**预期运行结果：**
```
um2 size = 3
um3 bucket_count = 23
us2 (无序+去重): 9 3 4 5 6 1 2        （注意：实际顺序取决于哈希函数，可能不同）
```

> **注意**：unordered 容器的输出顺序可能因编译器、运行环境不同而不同。这正是"无序"的含义——不要依赖任何特定顺序。

### 四、unordered_map 的常用操作

unordered_map 的接口与 map 基本一致，但内部实现不同导致行为差异：

```cpp
#include <iostream>
#include <unordered_map>
#include <string>
using namespace std;

int main() {
    cout << "========== unordered_map 示例 ==========" << endl;

    unordered_map<string, int> scores;

    // 1. 插入
    scores["Alice"] = 85;
    scores["Bob"] = 92;
    scores.insert({"Charlie", 78});
    scores.emplace("David", 90);        // C++11，直接构造，避免拷贝

    // 2. 访问
    cout << "Alice: " << scores["Alice"] << endl;      // 使用 []
    cout << "Bob: " << scores.at("Bob") << endl;       // 使用 at()

    // 3. 查找
    auto it = scores.find("Charlie");
    if (it != scores.end()) {
        cout << "Charlie: " << it->second << endl;
    }

    // 使用 count 判断是否存在
    if (scores.count("Eve") == 0) {
        cout << "Eve 不存在" << endl;
    }

    // 4. 删除
    scores.erase("David");

    // 5. 遍历（注意：无序！）
    cout << "\n所有键值对（无序）:" << endl;
    for (const auto& [name, score] : scores) {
        cout << "  " << name << " -> " << score << endl;
    }

    // 6. 查看哈希表信息
    cout << "\n哈希表统计:" << endl;
    cout << "  size = " << scores.size() << endl;
    cout << "  bucket_count = " << scores.bucket_count() << endl;
    cout << "  load_factor = " << scores.load_factor() << endl;
    cout << "  max_load_factor = " << scores.max_load_factor() << endl;

    // 7. 按桶查看
    cout << "\n各桶中的元素:" << endl;
    for (size_t i = 0; i < scores.bucket_count(); i++) {
        size_t bucketSize = scores.bucket_size(i);
        if (bucketSize > 0) {
            cout << "  桶 " << i << " (" << bucketSize << " 个元素): ";
            for (auto it = scores.begin(i); it != scores.end(i); ++it) {
                cout << it->first << " ";
            }
            cout << endl;
        }
    }

    return 0;
}
```

**预期运行结果（顺序可能不同）：**
```
========== unordered_map 示例 ==========
Alice: 85
Bob: 92
Charlie: 78
Eve 不存在

所有键值对（无序）:
  Charlie -> 78
  Bob -> 92
  Alice -> 85

哈希表统计:
  size = 3
  bucket_count = 23
  load_factor = 0.130435
  max_load_factor = 1

各桶中的元素:
  桶 2 (1 个元素): Charlie
  桶 5 (1 个元素): Bob
  桶 6 (1 个元素): Alice
```

### 五、unordered_set 的常用操作

```cpp
#include <iostream>
#include <unordered_set>
#include <string>
using namespace std;

int main() {
    cout << "========== unordered_set 示例 ==========" << endl;

    unordered_set<string> us;

    // 1. 插入
    us.insert("apple");
    us.insert("banana");
    us.insert("cherry");
    us.insert("apple");              // 重复，被忽略

    cout << "size: " << us.size() << endl;              // 输出: 3

    // 2. 查找
    if (us.find("banana") != us.end()) {
        cout << "banana 存在" << endl;
    }

    // count 对于 unordered_set 只能是 0 或 1
    cout << "apple count: " << us.count("apple") << endl;   // 输出: 1
    cout << "durian count: " << us.count("durian") << endl; // 输出: 0

    // 3. 删除
    us.erase("cherry");
    cout << "删除 cherry 后 size: " << us.size() << endl;   // 输出: 2

    // 4. 遍历（无序）
    cout << "所有元素（无序）: ";
    for (const string& s : us) {
        cout << s << " ";
    }
    cout << endl;

    // 5. 与 set 的性能对比演示
    cout << "\n--- 性能对比提示 ---" << endl;
    cout << "unordered_set find(): O(1) 均摊" << endl;
    cout << "set find(): O(log n)" << endl;
    cout << "数据量大时 unordered_set 明显更快" << endl;

    return 0;
}
```

**预期运行结果（顺序可能不同）：**
```
========== unordered_set 示例 ==========
size: 3
banana 存在
apple count: 1
durian count: 0
删除 cherry 后 size: 2
所有元素（无序）: banana apple

--- 性能对比提示 ---
unordered_set find(): O(1) 均摊
set find(): O(log n)
数据量大时 unordered_set 明显更快
```

### 六、时间复杂度对比

| 操作 | `map` / `set` | `unordered_map` / `unordered_set` |
|------|---------------|----------------------------------|
| 插入 | O(log n) | **均摊 O(1)**，最坏 O(n) |
| 查找 | O(log n) | **均摊 O(1)**，最坏 O(n) |
| 删除 | O(log n) | **均摊 O(1)**，最坏 O(n) |
| 遍历 | O(n)（有序） | O(n)（无序） |
| lower/upper_bound | O(log n) | **不支持** |

> **"均摊 O(1)"** 的含义：大多数时候是 O(1)，但在 rehash（扩容）时需要 O(n) 重新分配所有元素，不过 rehash 不频繁，平均下来每个操作是 O(1)。

> **"最坏 O(n)"** 的含义：如果哈希函数设计不佳（大量冲突），所有元素都落在同一个桶里，退化为链表，查找变成 O(n)。实践中，标准库的哈希函数质量很高，很少出现这种情况。

### 七、什么时候用哪个？

#### 选择指南

| 场景 | 推荐容器 | 原因 |
|------|---------|------|
| 需要按键排序遍历 | `map` / `set` | 有序版本自然支持 |
| 需要范围查询（如找 [a, z) 之间的键） | `map` / `set` | 支持 lower_bound / upper_bound |
| 只需要快速插入/查找，不关心顺序 | `unordered_map` / `unordered_set` | O(1) 性能 |
| 算法刷题中出现超时 | 尝试替换为 unordered 版本 | 常数优化明显 |
| 键是自定义类型且不想写哈希函数 | `map` / `set` | 更容易上手 |
| 内存受限的环境 | `map` / `set` | 哈希表占用更多内存 |
| 数据量极大（百万级以上） | `unordered_map` / `unordered_set` | O(log n) 在大数据量下有明显差异 |

#### 一个实测对比

```cpp
#include <iostream>
#include <map>
#include <unordered_map>
#include <chrono>
using namespace std;
using namespace chrono;

int main() {
    const int N = 1000000;          // 100 万次操作

    // === map 插入性能 ===
    map<int, int> m;
    auto start = high_resolution_clock::now();
    for (int i = 0; i < N; i++) {
        m[i] = i;
    }
    auto end = high_resolution_clock::now();
    auto mapTime = duration_cast<milliseconds>(end - start).count();

    // === unordered_map 插入性能 ===
    unordered_map<int, int> um;
    start = high_resolution_clock::now();
    for (int i = 0; i < N; i++) {
        um[i] = i;
    }
    end = high_resolution_clock::now();
    auto umTime = duration_cast<milliseconds>(end - start).count();

    cout << "插入 " << N << " 个元素:" << endl;
    cout << "  map:             " << mapTime << " ms" << endl;
    cout << "  unordered_map:   " << umTime << " ms" << endl;
    cout << "  差距: unordered_map 快了约 " << (mapTime * 100 / max(umTime, 1L)) / 100.0 << " 倍" << endl;

    return 0;
}
```

**预期运行结果（参考值，实际因环境而异）：**
```
插入 1000000 个元素:
  map:             1234 ms
  unordered_map:   456 ms
  差距: unordered_map 快了约 2.71 倍
```

### 八、自定义类型与 unordered 容器

自定义类型需要在 unordered 容器中使用时，需要提供：
1. **哈希函数**：`hash<T>` 的特化或自定义函数对象
2. **等价判断**：`operator==`

```cpp
#include <iostream>
#include <unordered_set>
#include <string>
using namespace std;

struct Person {
    string name;
    int age;

    // 需要 operator==
    bool operator==(const Person& other) const {
        return name == other.name && age == other.age;
    }
};

// 自定义哈希函数
struct PersonHash {
    size_t operator()(const Person& p) const {
        // 组合哈希：使用标准库的 hash<string> 和 hash<int>
        return hash<string>()(p.name) ^ (hash<int>()(p.age) << 1);
    }
};

int main() {
    unordered_set<Person, PersonHash> people;

    people.insert({"Alice", 25});
    people.insert({"Bob", 30});
    people.insert({"Alice", 25});        // 重复，被忽略

    cout << "size = " << people.size() << endl;    // 输出: 2

    for (const auto& p : people) {
        cout << p.name << " (" << p.age << ")" << endl;
    }

    // 查找
    Person target = {"Bob", 30};
    if (people.find(target) != people.end()) {
        cout << "找到了 Bob (30)" << endl;
    }

    return 0;
}
```

**预期运行结果：**
```
size = 2
Alice (25)
Bob (30)
找到了 Bob (30)
```

### 九、注意事项与常见坑

#### 1. 不要依赖任何顺序

unordered 容器不保证元素顺序，而且顺序可能因为 rehash 而改变：

```cpp
unordered_map<int, string> um;
um[1] = "one";
um[2] = "two";
um[3] = "three";

// 下面的输出顺序是不确定的
for (const auto& [k, v] : um) cout << k << " ";

um.rehash(100);     // 强制 rehash

// rehash 后顺序可能改变了！
for (const auto& [k, v] : um) cout << k << " ";
```

#### 2. 关键字不能用 `[]` 读取

与 map 一样，使用 `[]` 访问不存在的键会**默认创建**它。要读取不存在的键且不创建，使用 `at()` 或 `find()`。

#### 3. 性能退化

如果哈希函数质量差，最坏情况下 unordered 容器退化为链表，性能变成 O(n)。不过这种情况极罕见，标准库的哈希函数通常足够好。

#### 4. 内存开销

```cpp
// 对于小数据量，有序版本可能更快
// 因为哈希表的管理开销可能超过红黑树的 O(log n) 查找
unordered_map<int, int> um;
map<int, int> m;
// 当只有几十个元素时，两者的性能差异几乎可以忽略
```

#### 5. reserve() 和 rehash

```cpp
#include <iostream>
#include <unordered_map>
using namespace std;

int main() {
    unordered_map<int, int> um;

    // 如果预知元素数量，提前 reserve 可以避免 rehash
    um.reserve(10000);          // 预留 10000 个元素的空间

    cout << "reserve 后 bucket_count: " << um.bucket_count() << endl;
    cout << "reserve 后 max_load_factor: " << um.max_load_factor() << endl;

    for (int i = 0; i < 10000; i++) {
        um[i] = i;              // 不会触发 rehash
    }

    cout << "最终 load_factor: " << um.load_factor() << endl;

    return 0;
}
```

**预期运行结果：**
```
reserve 后 bucket_count: 11071
reserve 后 max_load_factor: 1
最终 load_factor: 0.903259
```

> `reserve(n)` 会预分配足够的桶，使得 n 个元素可以在不触发 rehash 的情况下全部插入。当数据量很大时，这是一个重要的性能优化。

### 十、完整可运行示例

```cpp
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <string>
#include <vector>
using namespace std;

int main() {
    cout << "========== unordered_map + unordered_set 综合示例 ==========" << endl;

    // 场景：统计一篇文章中单词出现的频率，并找出出现次数 >= 2 的单词

    // 模拟文章单词
    vector<string> words = {
        "the", "quick", "brown", "fox", "jumps",
        "over", "the", "lazy", "dog", "the",
        "fox", "jumps", "high", "over", "the",
        "lazy", "cat"
    };

    // 1. 使用 unordered_map 统计词频
    unordered_map<string, int> freq;

    for (const string& word : words) {
        freq[word]++;               // [] 在 key 不存在时自动创建（值为 0），然后 ++
    }

    cout << "单词频率统计:" << endl;
    for (const auto& [word, count] : freq) {
        cout << "  \"" << word << "\": " << count << " 次" << endl;
    }

    // 2. 使用 unordered_set 找出出现次数 >= 2 的单词（去重）
    unordered_set<string> frequentWords;

    for (const auto& [word, count] : freq) {
        if (count >= 2) {
            frequentWords.insert(word);
        }
    }

    cout << "\n出现 >= 2 次的单词: ";
    for (const string& word : frequentWords) {
        cout << word << " ";
    }
    cout << endl;

    // 3. 验证快速查找
    string query = "fox";
    auto it = freq.find(query);
    if (it != freq.end()) {
        cout << "\n\"" << query << "\" 出现了 " << it->second << " 次" << endl;
    }

    // 4. 检查 key 是否在 set 中
    if (frequentWords.count("fox") > 0) {
        cout << "\"fox\" 是高频词（出现 >= 2 次）" << endl;
    }

    // 5. 查看哈希表信息
    cout << "\n词频哈希表统计:" << endl;
    cout << "  不同单词数: " << freq.size() << endl;
    cout << "  桶数: " << freq.bucket_count() << endl;
    cout << "  负载因子: " << freq.load_factor() << endl;

    return 0;
}
```

**预期运行结果（顺序可能不同）：**
```
========== unordered_map + unordered_set 综合示例 ==========
单词频率统计:
  "dog": 1 次
  "over": 2 次
  "fox": 2 次
  "high": 1 次
  "lazy": 2 次
  "the": 4 次
  "quick": 1 次
  "brown": 1 次
  "jumps": 2 次
  "cat": 1 次

出现 >= 2 次的单词: lazy jumps the over fox

"fox" 出现了 2 次
"fox" 是高频词（出现 >= 2 次）

词频哈希表统计:
  不同单词数: 10
  桶数: 23
  负载因子: 0.434783
```

### 十一、性能建议

1. **大数据量（>10万）优先用 unordered 版本**：O(1) vs O(log n) 的差异在数据量大时非常明显
2. **小数据量（<100）两者差异不大**：选择更符合语义的版本即可
3. **如果需要有序输出**：可以用 unordered_map 统计，然后拷贝到 vector 中排序
4. **预知元素大数时使用 reserve()**：避免多次 rehash 带来的性能损失
5. **自定义类型优先用有序版本**：除非确信需要极高性能，否则 map/set 更易用

### 十二、总结

- `unordered_map` 和 `unordered_set` 基于**哈希表**实现，查找/插入/删除**均摊 O(1)**
- 元素**无序**，不要依赖任何特定的遍历顺序
- 接口与 `map`/`set` 基本一致，但不支持 `lower_bound`/`upper_bound` 等范围查询
- 内存占用比有序版本大（需要额外的桶和链表结构）
- 用 `reserve()` 预分配空间可以避免 rehash，提升性能
- 需要顺序用 `map`/`set`，追求性能用 unordered 版本
- 自定义类型用于 unordered 容器需要提供哈希函数和 `operator==`
