---
author: chuiyu
date: 2026-09-07
description: 07-const
tags:
  - cpp
---
const 在cpp中相当于#define 即 可以看作一个宏定义。



```cpp

#include <iostream>


using namespace std;

#define MAX1 150

int main()
{
    const int MAX2 = 150;

    cout << MAX1 << endl;

    cout << MAX2 << endl;


    return 0;
}




```