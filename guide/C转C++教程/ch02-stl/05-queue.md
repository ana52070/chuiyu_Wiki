---
title: queue
author: claudecode(deepseekV4flash)
date: 2026-07-20 21:40:45
description: queue
tags:
  - Cpp算法
categories:
  - guide
  - C++算法入门
---

## queue（队列）与 priority_queue（优先队列）

### 一、概念与原理

#### queue（队列）

`queue` 是 C++ STL 中的一种**容器适配器**，它实现了**先进先出（FIFO, First In First Out）**的数据结构。

**生活类比：排队**
- 去银行办业务时，先来的人先办理，后来的人排在队尾
- 新来的人（push）站在队伍末尾
- 办完业务的人（pop）从队首离开
- 你可以看到队伍最前面的人是谁（front），也能看到最后面的人是谁（back）

**核心特性：**
- **先进先出**：元素的插入在队尾（back），删除在队首（front）
- **容器适配器**：基于其他容器（默认是 `deque`）封装
- **不提供迭代器**：queue 不支持遍历

**典型应用场景：**
- 任务调度系统（先来的任务先执行）
- 打印队列
- 消息队列
- 广度优先搜索（BFS）
- 缓冲区处理

**队列的示意图：**
```
                       push(4) →  push(5) →
                                   ┌─────┐
                                   │  5  │  ← back
                                   ┌─────┐
                                   │  4  │
front → pop() →                   ┌─────┐
                   │  3  │
                   └─────┘
                   ┌─────┐
                   │  2  │
                   └─────┘
                   ┌─────┐
                   │  1  │  ← front
                   └─────┘
```

#### priority_queue（优先队列）

`priority_queue` 也是队列适配器的一种变体，但它不是 FIFO，而是**优先级最高的元素先出队**。

- 默认情况下是**大顶堆**（最大堆），即最大的元素在队首
- 内部实现是**二叉堆**（binary heap）
- 插入和删除的时间复杂度为 O(log n)
- 可以自定义比较函数实现小顶堆

### 二、头文件

```cpp
#include <queue>          // 包含 queue 和 priority_queue
```

### 三、创建方式

```cpp
#include <iostream>
#include <queue>
#include <vector>
#include <list>
using namespace std;

int main() {
    // ========== queue 的创建 ==========

    // 1. 默认构造
    queue<int> q1;

    // 2. 基于其他容器的 queue
    queue<int, deque<int>> q2;      // 基于 deque（默认）
    queue<int, list<int>> q3;       // 基于 list

    // 3. 从已有容器构造
    deque<int> d = {1, 2, 3};
    queue<int> q4(d);
    cout << "q4 front = " << q4.front() << ", back = " << q4.back() << endl;  // 输出: 1, 3

    // ========== priority_queue 的创建 ==========

    // 1. 默认构造（大顶堆，最大元素在顶部）
    priority_queue<int> pq1;

    // 2. 指定底层容器（通常用 vector）
    priority_queue<int, vector<int>> pq2;

    // 3. 小顶堆（最小元素在顶部）
    priority_queue<int, vector<int>, greater<int>> pq3;

    // 4. 从已有数据构造
    vector<int> nums = {3, 1, 4, 1, 5, 9};
    priority_queue<int> pq4(nums.begin(), nums.end());
    cout << "pq4 top = " << pq4.top() << endl;                   // 输出: 9

    // 小顶堆从已有数据构造
    priority_queue<int, vector<int>, greater<int>> pq5(nums.begin(), nums.end());
    cout << "pq5 top = " << pq5.top() << endl;                   // 输出: 1

    return 0;
}
```

**预期运行结果：**
```
q4 front = 1, back = 3
pq4 top = 9
pq5 top = 1
```

### 四、queue 常用操作详解

```cpp
#include <iostream>
#include <queue>
using namespace std;

int main() {
    queue<int> q;

    cout << "初始: empty = " << (q.empty() ? "yes" : "no") << ", size = " << q.size() << endl;

    // push()：入队，将元素放入队尾
    q.push(10);
    cout << "push(10): front = " << q.front() << ", back = " << q.back() << ", size = " << q.size() << endl;

    q.push(20);
    cout << "push(20): front = " << q.front() << ", back = " << q.back() << ", size = " << q.size() << endl;

    q.push(30);
    cout << "push(30): front = " << q.front() << ", back = " << q.back() << ", size = " << q.size() << endl;

    // front()：访问队首元素
    // back()：访问队尾元素
    cout << "\n当前队首: " << q.front() << ", 队尾: " << q.back() << endl;

    // pop()：出队，移除队首元素（不返回值）
    q.pop();
    cout << "pop 后: front = " << q.front() << ", back = " << q.back() << ", size = " << q.size() << endl;

    q.pop();
    cout << "再次 pop 后: front = " << q.front() << ", back = " << q.back() << ", size = " << q.size() << endl;

    // 遍历 queue（会清空队列！）
    cout << "\n=== 通过 pop 遍历 queue ===" << endl;
    queue<int> temp = q;             // 拷贝一份
    while (!temp.empty()) {
        cout << temp.front() << " ";  // 访问队首
        temp.pop();                   // 移除队首
    }
    cout << endl;

    return 0;
}
```

**预期运行结果：**
```
初始: empty = yes, size = 0
push(10): front = 10, back = 10, size = 1
push(20): front = 10, back = 20, size = 2
push(30): front = 10, back = 30, size = 3

当前队首: 10, 队尾: 30
pop 后: front = 20, back = 30, size = 2
再次 pop 后: front = 30, back = 30, size = 1

=== 通过 pop 遍历 queue ===
30
```

### 五、queue 典型应用：模拟打印队列

```cpp
#include <iostream>
#include <queue>
#include <string>
using namespace std;

struct PrintJob {
    string name;
    int pages;
    int id;

    PrintJob(int i, string n, int p) : id(i), name(n), pages(p) {}
};

int main() {
    cout << "========== 打印队列模拟 ==========" << endl;

    queue<PrintJob> printQueue;
    int jobId = 1;

    // 提交打印任务
    auto submitJob = [&](const string& name, int pages) {
        printQueue.push(PrintJob(jobId++, name, pages));
        cout << "提交: \"" << name << "\" (" << pages << " 页)" << endl;
    };

    // 处理下一个打印任务
    auto processNext = [&]() {
        if (printQueue.empty()) {
            cout << "队列为空，没有需要打印的任务" << endl;
            return;
        }

        PrintJob job = printQueue.front();
        printQueue.pop();

        cout << "正在打印: #" << job.id << " \"" << job.name
             << "\" (" << job.pages << " 页)...";

        // 模拟打印耗时（每页 0.1 秒）
        // 这里用循环代替
        cout << " 完成!" << endl;
    };

    // 查看队列状态
    auto showStatus = [&]() {
        if (printQueue.empty()) {
            cout << "打印队列为空" << endl;
        } else {
            cout << "队列中有 " << printQueue.size() << " 个待打印任务" << endl;
            cout << "下一个: \"" << printQueue.front().name << "\""
                 << ", 最后一个: \"" << printQueue.back().name << "\"" << endl;
        }
    };

    // 模拟场景
    submitJob("简历.pdf", 3);
    submitJob("报告.docx", 10);
    submitJob("照片.jpg", 1);
    cout << endl;

    showStatus();
    cout << endl;

    processNext();
    processNext();
    cout << endl;

    showStatus();
    cout << endl;

    submitJob("合同.pdf", 5);
    cout << endl;

    processNext();
    processNext();
    processNext();

    return 0;
}
```

**预期运行结果：**
```
========== 打印队列模拟 ==========
提交: "简历.pdf" (3 页)
提交: "报告.docx" (10 页)
提交: "照片.jpg" (1 页)

队列中有 3 个待打印任务
下一个: "简历.pdf", 最后一个: "照片.jpg"

正在打印: #1 "简历.pdf" (3 页)... 完成!
正在打印: #2 "报告.docx" (10 页)... 完成!

队列中有 1 个待打印任务
下一个: "照片.jpg", 最后一个: "照片.jpg"

提交: "合同.pdf" (5 页)

正在打印: #3 "照片.jpg" (1 页)... 完成!
正在打印: #4 "合同.pdf" (5 页)... 完成!
```

### 六、priority_queue 详解

```cpp
#include <iostream>
#include <queue>
#include <vector>
using namespace std;

int main() {
    cout << "========== priority_queue 示例 ==========" << endl;

    // 1. 默认大顶堆
    priority_queue<int> maxHeap;

    maxHeap.push(3);
    maxHeap.push(1);
    maxHeap.push(4);
    maxHeap.push(1);
    maxHeap.push(5);
    maxHeap.push(9);

    cout << "大顶堆依次出队: ";
    while (!maxHeap.empty()) {
        cout << maxHeap.top() << " ";      // 输出: 9 5 4 3 1 1
        maxHeap.pop();
    }
    cout << endl;

    // 2. 小顶堆
    priority_queue<int, vector<int>, greater<int>> minHeap;

    minHeap.push(3);
    minHeap.push(1);
    minHeap.push(4);
    minHeap.push(1);
    minHeap.push(5);
    minHeap.push(9);

    cout << "小顶堆依次出队: ";
    while (!minHeap.empty()) {
        cout << minHeap.top() << " ";      // 输出: 1 1 3 4 5 9
        minHeap.pop();
    }
    cout << endl;

    return 0;
}
```

**预期运行结果：**
```
========== priority_queue 示例 ==========
大顶堆依次出队: 9 5 4 3 1 1
小顶堆依次出队: 1 1 3 4 5 9
```

### 七、priority_queue 应用：任务调度

```cpp
#include <iostream>
#include <queue>
#include <string>
#include <vector>
using namespace std;

struct Task {
    string name;
    int priority;     // 优先级数字，越大越紧急

    // priority_queue 默认用 operator<，所以定义 < 运算符
    bool operator<(const Task& other) const {
        return priority < other.priority;   // 优先级高的先出队
    }
};

int main() {
    cout << "========== 优先任务调度 ==========" << endl;

    priority_queue<Task> taskQueue;

    // 提交任务
    taskQueue.push({"编写文档", 2});
    taskQueue.push({"修复紧急Bug", 5});
    taskQueue.push({"代码审查", 3});
    taskQueue.push({"回复邮件", 1});
    taskQueue.push({"上线发布", 5});

    cout << "任务执行顺序:" << endl;
    while (!taskQueue.empty()) {
        Task t = taskQueue.top();
        taskQueue.pop();
        cout << "  [优先级 " << t.priority << "] " << t.name << endl;
    }

    return 0;
}
```

**预期运行结果：**
```
========== 优先任务调度 ==========
任务执行顺序:
  [优先级 5] 修复紧急Bug
  [优先级 5] 上线发布
  [优先级 3] 代码审查
  [优先级 2] 编写文档
  [优先级 1] 回复邮件
```

### 八、性能说明

#### queue 性能

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| `push()` | O(1) | 在队尾插入 |
| `pop()` | O(1) | 移除队首元素 |
| `front()` | O(1) | 访问队首元素 |
| `back()` | O(1) | 访问队尾元素 |
| `size()` | O(1) | 返回元素个数 |
| `empty()` | O(1) | 判断是否为空 |

#### priority_queue 性能

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| `push()` | O(log n) | 插入后需要堆化（上浮） |
| `pop()` | O(log n) | 删除后需要堆化（下沉） |
| `top()` | O(1) | 直接返回堆顶元素 |

### 九、注意事项与常见坑

#### 1. 对空队列进行 front/back/pop 是未定义行为

```cpp
queue<int> q;
// cout << q.front() << endl;   // 崩溃！空队列
// q.pop();                     // 崩溃！空队列

// 安全做法
if (!q.empty()) {
    cout << q.front() << endl;
    q.pop();
}
```

#### 2. pop() 不返回值

与 stack 一样，queue 的 pop() 也不返回值：

```cpp
queue<int> q;
q.push(10);
// int x = q.pop();       // 编译错误！

int x = q.front();        // 先获取值
q.pop();                  // 再移除
```

#### 3. queue 不支持遍历

与 stack 一样，queue **没有迭代器**，不能使用范围 for 或迭代器遍历。

#### 4. priority_queue 的排序与直觉相反

默认的 `priority_queue<T>` 是**大顶堆**，即 `top()` 返回**最大**元素。这和直觉上的"优先级高先处理"一致（优先级数字大表示优先级高），但和 `sort()` 的默认行为（升序）相反。

#### 5. priority_queue 自定义比较函数的写法

```cpp
#include <iostream>
#include <queue>
#include <vector>
using namespace std;

// 小顶堆的两种写法
// 写法一：使用 greater
priority_queue<int, vector<int>, greater<int>> minHeap1;

// 写法二：使用 lambda（C++ 中不能直接用 lambda 作模板参数，需借助 decltype）
auto cmp = [](int a, int b) { return a > b; };    // 返回 true 表示 a 优先级低于 b
priority_queue<int, vector<int>, decltype(cmp)> minHeap2(cmp);
```

#### 6. deque 作为默认底层容器

queue 默认使用 `deque`（双端队列）作为底层容器，而不是 `vector`。原因是 deque 在两端插入删除都是 O(1)，而 vector 在头部插入是 O(n)。

### 十、完整可运行示例：排队系统

```cpp
#include <iostream>
#include <queue>
#include <string>
#include <cstdlib>
#include <ctime>
using namespace std;

int main() {
    cout << "========== 银行排队系统模拟 ==========" << endl;

    queue<int> customerQueue;
    int nextCustomerId = 1;
    int currentTime = 0;

    // 模拟顾客到达（随机到达）
    srand(time(nullptr));

    // 模拟 10 个时间单位的运行
    for (int t = 1; t <= 10; t++) {
        cout << "\n=== 时间 T = " << t << " ===" << endl;

        // 随机到达 0~2 个新顾客
        int arriveCount = rand() % 3;
        for (int i = 0; i < arriveCount; i++) {
            int id = nextCustomerId++;
            customerQueue.push(id);
            cout << "  顾客 #" << id << " 到达，排队人数: " << customerQueue.size() << endl;
        }

        // 每 2 个时间单位处理一个顾客
        if (t % 2 == 0 && !customerQueue.empty()) {
            int served = customerQueue.front();
            customerQueue.pop();
            cout << "  >> 顾客 #" << served << " 办理完毕，离开队伍" << endl;
        } else if (t % 2 == 0) {
            cout << "  队列为空，暂无顾客可服务" << endl;
        }

        // 显示排队情况
        if (!customerQueue.empty()) {
            cout << "  当前排队: " << customerQueue.size() << " 人";
            cout << " (队首: #" << customerQueue.front();
            cout << ", 队尾: #" << customerQueue.back() << ")" << endl;
        } else {
            cout << "  当前没有顾客排队" << endl;
        }
    }

    cout << "\n========== 模拟结束 ==========" << endl;
    cout << "共服务 " << (nextCustomerId - 1) << " 位顾客" << endl;
    cout << "剩余排队: " << customerQueue.size() << " 人" << endl;

    return 0;
}
```

**预期运行结果（随机，示例）：**
```
========== 银行排队系统模拟 ==========

=== 时间 T = 1 ===
  顾客 #1 到达，排队人数: 1
  顾客 #2 到达，排队人数: 2
  当前排队: 2 人 (队首: #1, 队尾: #2)

=== 时间 T = 2 ===
  >> 顾客 #1 办理完毕，离开队伍
  当前排队: 1 人 (队首: #2, 队尾: #2)

=== 时间 T = 3 ===
  当前没有顾客排队

=== 时间 T = 4 ===
  顾客 #3 到达，排队人数: 1
  顾客 #4 到达，排队人数: 2
  >> 顾客 #2 办理完毕，离开队伍
  当前排队: 1 人 (队首: #3, 队尾: #4)

...

========== 模拟结束 ==========
共服务 7 位顾客
剩余排队: 2 人
```

### 十一、queue 与 priority_queue 对比

| 特性 | `queue` | `priority_queue` |
|------|---------|-----------------|
| 出队顺序 | FIFO（先进先出） | 优先级最高的先出 |
| 常用操作 | push, pop, front, back | push, pop, top |
| 访问队尾 | 支持 `back()` | 不支持 |
| push 复杂度 | O(1) | O(log n) |
| 底层结构 | deque（默认） | vector（默认） |
| 迭代器 | 无 | 无 |
| 适用场景 | BFS、任务队列、缓冲区 | 贪心算法、任务调度、Top-K |

### 十二、总结

- `queue` 是 FIFO（先进先出）的容器适配器，核心操作 `push()`、`pop()`、`front()`、`back()` 均为 O(1)
- `priority_queue` 是优先队列，默认大顶堆（最大元素优先输出），`push` 和 `pop` 为 O(log n)
- `pop()` 不返回值，需要先 `front()` / `top()` 再 `pop()`
- 对空队列进行操作是未定义行为（可能崩溃）
- queue 不支持遍历和迭代器
- BFS（广度优先搜索）普遍使用 queue 作为核心数据结构
