---
author: chuiyu
date: 2026-02-05
description: 第一章 迈向现代C++
tags:
  - Cpp17
---
# 第一章 迈向现代C++
编译环境：本书将使用 clang++ 作为唯一使用的编译器，同时总是在代码中使用 -std=c++2a 编译标志。

```bash
clang++ -v
Apple LLVM version 10.0.1 (clang-1001.0.46.4)
Target: x86_64-apple-darwin18.6.0
Thread model: posix
InstalledDir: /Library/Developer/CommandLineTools/usr/bin
```

>[!NOTE]
>**Clang** 是 **LLVM** 项目的 C/C++ 前端。 **GCC** (GNU Compiler Collection) 是老牌的编译器套件。
>#### 核心原理解析：三维视角
>
>**1. 底层视角 (The C Way): 架构差异**
>
>- **GCC**: 历史上是一个巨大的单体（Monolithic）。很难把它的语法分析器拆出来单独用。
   > 
>- **Clang/LLVM**: 模块化设计。Clang 只是前端，负责把 C++ 翻译成 **LLVM IR** (Intermediate Representation，中间表示)。
   > 
   > - _流向_：`Source Code (.cpp)` -> **Clang** -> `LLVM IR` -> **LLVM Backend** -> `Machine Code (.o)`。
   >     
   > - _优势_：这种架构让它能生成极其精准的错误提示（AST Dump）。GCC 以前报错像天书，Clang 报错直接告诉你“你是不是少了个分号？”。
   >     
>
>**2. 顶层视角 (The Python Way): 交互体验**
>
>- **GCC** 就像 Python 的 C 扩展报错，经常只丢给你一个 `Segmentation fault` 或者莫名其妙的链接错误，你看得云里雾里。
  >  
>- **Clang** 就像 Python 的解释器（Interpreter）加上了 Pylint。它不仅编译代码，还能像 IDE 一样理解你的代码结构。
  >  
>- _类比_：Clang 提供的 `clang-format` (自动格式化) 和 `clang-tidy` (静态分析) 就好比 Python 里的 `Black` 和 `Pylint`。Google Style 严格依赖这些工具。
  >  
>
>**3. 工程实战 (The Embedded Way): 为什么要用它？**
>
>- **交叉编译陷阱**：在 RK3588 上，我们经常遇到 NPU 驱动（librknnrt.so）和系统库版本冲突的问题。
  >  
>- **Sanitizers**：Clang 的 AddressSanitizer (`-fsanitize=address`) 是嵌入式开发的救命稻草。
   > 
  >  - 你以前在 C 语言里写越界了，程序可能跑飞了也不报错，直到在客户现场死机。
   >     
 >   - 用 Clang 加上 Sanitizer，它能像 Python 的 `IndexError` 一样，在运行时直接把你拦截下来，告诉你内存哪里炸了。




## 1.1 被弃用的特性
 

在学习现代 C++ 之前，我们先了解一下从 C++11 开始，被弃用的主要特性：

> **注意**：弃用并非彻底不能用，只是用于暗示程序员这些特性将从未来的标准中消失，应该尽量避免使用。但是，已弃用的特性依然是标准库的一部分，并且出于兼容性的考虑，大部分特性其实会『永久』保留。

- **不再允许字符串字面值常量赋值给一个 `char *`。如果需要用字符串字面值常量赋值和初始化一个 `char *`，应该使用 `const char *` 或者 `auto`。**
    
```cpp
char *str = "hello world!"; // 将出现弃用警告
```
    
- **C++98 异常说明、 `unexpected_handler`、`set_unexpected()` 等相关特性被弃用，应该使用 `noexcept`。**
    
- **`auto_ptr` 被弃用，应使用 `unique_ptr`。**
    
- **`register` 关键字被弃用，可以使用但不再具备任何实际含义。**
    
- **`bool` 类型的 `++` 操作被弃用。**
    
- **如果一个类有析构函数，为其生成拷贝构造函数和拷贝赋值运算符的特性被弃用了。**
    
- **C 语言风格的类型转换被弃用（即在变量前使用 `(convert_type)`），应该使用 `static_cast`、`reinterpret_cast`、`const_cast` 来进行类型转换。**
    
- **特别地，在最新的 C++17 标准中弃用了一些可以使用的 C 标准库，例如 `<ccomplex>`、`<cstdalign>`、`<cstdbool>` 与 `<ctgmath>` 等**
    
- ……等等
    

还有一些其他诸如参数绑定（C++11 提供了 `std::bind` 和 `std::function`）、`export` 等特性也均被弃用。前面提到的这些特性**如果你从未使用或者听说过，也请不要尝试去了解他们，应该向新标准靠拢**，直接学习新特性。毕竟，技术是向前发展的。



## 1.2 与 C 的兼容性


出于一些不可抗力、历史原因，我们不得不在 C++ 中使用一些 C 语言代码（甚至古老的 C 语言代码），例如 Linux 系统调用。在现代 C++ 出现之前，大部分人当谈及『C 与 C++ 的区别是什么』时，普遍除了回答面向对象的类特性、泛型编程的模板特性外，就没有其他的看法了，甚至直接回答『差不多』，也是大有人在。图 1.2 中的韦恩图大致上回答了 C 和 C++ 相关的兼容情况。

![图 1.2: C 和 C++ 互相兼容情况](https://changkun.de/modern-cpp/assets/figures/comparison.png)图 1.2: C 和 C++ 互相兼容情况

从现在开始，你的脑子里应该树立『**C++ 不是 C 的一个超集**』这个观念（而且从一开始就不是，后面的[进一步阅读的参考文献](https://changkun.de/modern-cpp/zh-cn/01-intro/#%E8%BF%9B%E4%B8%80%E6%AD%A5%E9%98%85%E8%AF%BB%E7%9A%84%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE)中给出了 C++98 和 C99 之间的区别）。在编写 C++ 时，也应该尽可能的避免使用诸如 `void*` 之类的程序风格。而在不得不使用 C 时，应该注意使用 `extern "C"` 这种特性，将 C 语言的代码与 C++代码进行分离编译，再统一链接这种做法，例如：
```cpp
// foo.h  
#ifdef __cplusplus  
extern "C" {  
#endif  
  
int add(int x, int y);  
  
#ifdef __cplusplus  
}  
#endif  
  
// foo.c  
int add(int x, int y) {  
    return x+y;  
}  
  
// 1.1.cpp  
#include "foo.h"  
#include <iostream>  
#include <functional>  
  
int main() {  
    [out = std::ref(std::cout << "Result from C code: " << add(1, 2))](){  
        out.get() << ".\n";  
    }();  
    return 0;  
}
```

应先使用 gcc 编译 C 语言的代码：
```bash
gcc -c foo.c
```

编译出 `foo.o` 文件，再使用 `clang++` 将 C++ 代码和 `.o` 文件链接起来（或者都编译为 `.o` 再统一链接）：
```bash
clang++ 1.1.cpp foo.o -std=c++2a -o 1.1
```

当然，你可以使用 Makefile 来编译上面的代码：
```makefile
C = gcc  
CXX = clang++  
  
SOURCE_C = foo.c  
OBJECTS_C = foo.o  
  
SOURCE_CXX = 1.1.cpp  
  
TARGET = 1.1  
LDFLAGS_COMMON = -std=c++2a  
  
all:  
	$(C) -c $(SOURCE_C)  
	$(CXX) $(SOURCE_CXX) $(OBJECTS_C) $(LDFLAGS_COMMON) -o $(TARGET)  
clean:  
	rm -rf *.o $(TARGET)
```

> 注意：`Makefile` 中的缩进是制表符而不是空格符，如果你直接复制这段代码到你的编辑器中，制表符可能会被自动替换掉，请自行确保在 `Makefile` 中的缩进是由制表符完成的。
> 
> 如果你还不知道 `Makefile` 的使用也没有关系，本教程中不会构建过于复杂的代码，简单的在命令行中使用 `clang++ -std=c++2a` 也可以阅读本书。

如果你是首次接触现代 C++，那么你很可能还看不懂上面的那一小段代码，即：
```cpp
[out = std::ref(std::cout << "Result from C code: " << add(1, 2))](){  
    out.get() << ".\n";  
}();
```
不必担心，本书的后续章节将为你介绍这一切。


