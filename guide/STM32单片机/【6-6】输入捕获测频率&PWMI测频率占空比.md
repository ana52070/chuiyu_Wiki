---
author: chuiyu
date: 2026-02-04
description: 【6-6】输入捕获测频率&PWMI测频率占空比
tags:
- STM32单片机
---

# 【6-6】输入捕获测频率&PWMI测频率占空比

## 相关库函数

```c
void TIM_ICInit(TIM_TypeDef* TIMx, TIM_ICInitTypeDef* TIM_ICInitStruct);
//函数功能 用结构体配置输入捕获单元的函数,单一的配置一个通道
```

```c
void TIM_PWMIConfig(TIM_TypeDef* TIMx, TIM_ICInitTypeDef* TIM_ICInitStruct);
//函数功能 初始化输入捕获单元,快速配置两个通道,配置为PWMI模式
```

```c
void TIM_ICStructInit(TIM_ICInitTypeDef* TIM_ICInitStruct);
//函数功能: 可以给输入捕获结构体赋一个初始值
```

```c
void TIM_SelectInputTrigger(TIM_TypeDef* TIMx, uint16_t TIM_InputTriggerSource);
//函数功能: 选择输入触发源TRGI,即是从模式的触发源选择,调用这个函数就能选择从模式的触发源了
```

```c
void TIM_SelectOutputTrigger(TIM_TypeDef* TIMx, uint16_t TIM_TRGOSource);
//函数功能: 选择主模式的触发源
```

```c
void TIM_SelectSlaveMode(TIM_TypeDef* TIMx, uint16_t TIM_SlaveMode);
//函数功能: 选择从模式
```

```c
void TIM_SetIC1Prescaler(TIM_TypeDef* TIMx, uint16_t TIM_ICPSC);
void TIM_SetIC2Prescaler(TIM_TypeDef* TIMx, uint16_t TIM_ICPSC);
void TIM_SetIC3Prescaler(TIM_TypeDef* TIMx, uint16_t TIM_ICPSC);
void TIM_SetIC4Prescaler(TIM_TypeDef* TIMx, uint16_t TIM_ICPSC);
//函数功能: 分别单独配置通道1234的分频器
```

```c
uint16_t TIM_GetCapture1(TIM_TypeDef* TIMx);
uint16_t TIM_GetCapture2(TIM_TypeDef* TIMx);
uint16_t TIM_GetCapture3(TIM_TypeDef* TIMx);
uint16_t TIM_GetCapture4(TIM_TypeDef* TIMx);
//函数功能: 分别读取四个通道的CCR
```









