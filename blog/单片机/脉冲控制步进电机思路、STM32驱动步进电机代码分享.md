---
categories:
- 单片机
date: 已于 2025-03-01
tags:
- 单片机
title: 脉冲控制步进电机思路、STM32驱动步进电机代码分享
permalink: /blog/单片机/脉冲控制步进电机思路、STM32驱动步进电机代码分享
---

# 脉冲控制步进电机思路、STM32驱动步进电机代码分享

> 原文链接：[脉冲控制步进电机思路、STM32驱动步进电机代码分享](https://blog.csdn.net/chui_yu666/article/details/145950179)

## 引言

在驱动步进电机的时候，以前都是使用的简单的手写脉冲控制，但是由于之后的项目需求，因此改为了使用PWM波控制，同时添加了定时中断来完成，实现了简单的伪开环位置（放在项目中已然够用）。

因此特将自己的思路和代码分享出来供给大家互相交流学习。

## 目录

1.脉冲驱动步进电机介绍

2.步进电机驱动思路

3.具体实现代码-STM32F103为例

## 脉冲驱动步进电机介绍

步进电机是一种以数字脉冲信号为控制信号的电机，它的运动是由控制器发出的脉冲信号驱动的。步进电机每接收到一个脉冲信号，就会按照固定的步距角度（通常为1.8度或0.9度）运动一步。步进电机由转子和定子两部分组成，转子由磁性材料制成，定子由线圈和磁铁组成。控制器通过改变线圈中电流的方向和大小来实现控制步进电机的转动方向和速度。

所以，想要驱动步进电机，就需要给驱动板发送脉冲就行。

![](https://i-blog.csdnimg.cn/direct/1758a8f0c72c41479783c95c0672aa68.png)

一般来说，使用脉冲控制方式需要单片机接三根信号线：

ENA：使能失能信号线

STP：脉冲信号线

EIR：方向信号线

同时，还需要接地GND分为共阴和共阳接法。

## 步进电机驱动思路

首先，通过使用PWM输出脉冲控制步进电机，随后为其开一个定时中断，在此定时中断中随时监控当前的电机状态，并根据状态进行改变当前PWM的输出情况。

这样既可以做到实现位置环，又不会阻塞主程序的运行，可以说是一举两得。

## 具体实现代码-STM32F103为例

### PWM.c
    
    ```
    #include "stm32f10x.h"                  // Device header
    
    /**
      * 函    数：PWM初始化
      * 参    数：无
      * 返 回 值：无
      */
    void TIM4_PWM_Init(void)
    {
    	/*开启时钟*/
    	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM4, ENABLE);			//开启TIM4的时钟
    	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);			//开启GPIOB的时钟
    	
    	/*GPIO初始化*/
    	GPIO_InitTypeDef GPIO_InitStructure;
    	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
    	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_7 | GPIO_Pin_9 | GPIO_Pin_6;
    	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    	GPIO_Init(GPIOB, &GPIO_InitStructure);							//将PA1引脚初始化为复用推挽输出	
    	
    	
    																//受外设控制的引脚，均需要配置为复用模式
    	
    	/*配置时钟源*/
    	TIM_InternalClockConfig(TIM4);		//选择TIM2为内部时钟，若不调用此函数，TIM默认也为内部时钟
    	
    	/*时基单元初始化*/
    	TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;				//定义结构体变量
    	TIM_TimeBaseInitStructure.TIM_ClockDivision = TIM_CKD_DIV1;     //时钟分频，选择不分频，此参数用于配置滤波器时钟，不影响时基单元功能
    	TIM_TimeBaseInitStructure.TIM_CounterMode = TIM_CounterMode_Up; //计数器模式，选择向上计数
    	TIM_TimeBaseInitStructure.TIM_Period = 100 - 1;				//计数周期，即ARR的值
    	TIM_TimeBaseInitStructure.TIM_Prescaler = 36 - 1;				//预分频器，即PSC的值
    	TIM_TimeBaseInitStructure.TIM_RepetitionCounter = 0;            //重复计数器，高级定时器才会用到
    	TIM_TimeBaseInit(TIM4, &TIM_TimeBaseInitStructure);             //将结构体变量交给TIM_TimeBaseInit，配置TIM2的时基单元
    	
    	/*输出比较初始化*/ 
    	TIM_OCInitTypeDef TIM_OCInitStructure;							//定义结构体变量
    	TIM_OCStructInit(&TIM_OCInitStructure);                         //结构体初始化，若结构体没有完整赋值
    	                                                                //则最好执行此函数，给结构体所有成员都赋一个默认值
    	                                                                //避免结构体初值不确定的问题
    	TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM1;               //输出比较模式，选择PWM模式1
    	TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_High;       //输出极性，选择为高，若选择极性为低，则输出高低电平取反
    	TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable;   //输出使能
    	TIM_OCInitStructure.TIM_Pulse = 0;								//初始的CCR值
    	TIM_OC2Init(TIM4, &TIM_OCInitStructure);                        //将结构体变量交给TIM_OC2Init，配置TIM2的输出比较通道2
    	TIM_OC4Init(TIM4, &TIM_OCInitStructure);  
    	TIM_OC1Init(TIM4, &TIM_OCInitStructure); 
    	
    	/*TIM使能*/
    	TIM_Cmd(TIM4, ENABLE);			//使能TIM2，定时器开始运行
    	
    }
    
    
    
    
    /**
      * 函    数：PWM设置CCR
      * 参    数：Compare 要写入的CCR的值，范围：0~100
      * 返 回 值：无
      * 注意事项：CCR和ARR共同决定占空比，此函数仅设置CCR的值，并不直接是占空比
      *           占空比Duty = CCR / (ARR + 1)
      */
    void TIM4_PWM_SetCompare2(uint16_t Compare)
    {
    	TIM_SetCompare2(TIM4, Compare);		//设置CCR2的值
    }
    
    void TIM4_PWM_SetCompare4(uint16_t Compare)
    {
    	TIM_SetCompare4(TIM4, Compare);		//设置CCR2的值
    }
    
    void TIM4_PWM_SetCompare1(uint16_t Compare)
    {
    	TIM_SetCompare1(TIM4, Compare);		//设置CCR2的值
    }
    ```

### PWM.h
    
    ```
    #ifndef __PWM_H
    #define __PWM_H
    
    void TIM4_PWM_Init(void);
    void TIM4_PWM_SetCompare2(uint16_t Compare);
    void TIM4_PWM_SetCompare4(uint16_t Compare);
    void TIM4_PWM_SetCompare3(uint16_t Compare);
    
    
    #endif
    ```

### Timer.c
    
    ```
    #include "stm32f10x.h"                  // Device header
    
    /**
      * 函    数：定时中断初始化
      * 参    数：无
      * 返 回 值：无
      */
    void Timer2_Init(void)
    {
    	/*开启时钟*/
    	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);			//开启TIM2的时钟
    	
    	/*配置时钟源*/
    	TIM_InternalClockConfig(TIM2);		//选择TIM2为内部时钟，若不调用此函数，TIM默认也为内部时钟
    	
    	/*时基单元初始化*/
    	TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;				//定义结构体变量
    	TIM_TimeBaseInitStructure.TIM_ClockDivision = TIM_CKD_DIV1;		//时钟分频，选择不分频，此参数用于配置滤波器时钟，不影响时基单元功能
    	TIM_TimeBaseInitStructure.TIM_CounterMode = TIM_CounterMode_Up;	//计数器模式，选择向上计数
    	TIM_TimeBaseInitStructure.TIM_Period = 100 - 1;				//计数周期，即ARR的值
    	TIM_TimeBaseInitStructure.TIM_Prescaler = 7200 - 1;				//预分频器，即PSC的值
    	TIM_TimeBaseInitStructure.TIM_RepetitionCounter = 0;			//重复计数器，高级定时器才会用到
    	TIM_TimeBaseInit(TIM2, &TIM_TimeBaseInitStructure);				//将结构体变量交给TIM_TimeBaseInit，配置TIM2的时基单元	
    	
    	/*中断输出配置*/
    	TIM_ClearFlag(TIM2, TIM_FLAG_Update);						//清除定时器更新标志位
    																//TIM_TimeBaseInit函数末尾，手动产生了更新事件
    																//若不清除此标志位，则开启中断后，会立刻进入一次中断
    																//如果不介意此问题，则不清除此标志位也可
    	
    	TIM_ITConfig(TIM2, TIM_IT_Update, ENABLE);					//开启TIM2的更新中断
    	
    	/*NVIC中断分组*/
    	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);				//配置NVIC为分组2
    																//即抢占优先级范围：0~3，响应优先级范围：0~3
    																//此分组配置在整个工程中仅需调用一次
    																//若有多个中断，可以把此代码放在main函数内，while循环之前
    																//若调用多次配置分组的代码，则后执行的配置会覆盖先执行的配置
    	
    	/*NVIC配置*/
    	NVIC_InitTypeDef NVIC_InitStructure;						//定义结构体变量
    	NVIC_InitStructure.NVIC_IRQChannel = TIM2_IRQn;				//选择配置NVIC的TIM2线
    	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;				//指定NVIC线路使能
    	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 2;	//指定NVIC线路的抢占优先级为2
    	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;			//指定NVIC线路的响应优先级为1
    	NVIC_Init(&NVIC_InitStructure);								//将结构体变量交给NVIC_Init，配置NVIC外设
    	
    	/*TIM使能*/
    	TIM_Cmd(TIM2, ENABLE);			//使能TIM2，定时器开始运行
    }
    
    /* 定时器中断函数，可以复制到使用它的地方
    void TIM2_IRQHandler(void)
    {
    	if (TIM_GetITStatus(TIM2, TIM_IT_Update) == SET)
    	{
    		
    		TIM_ClearITPendingBit(TIM2, TIM_IT_Update);
    	}
    }
    */
    ```

### Timer.h
    
    ```
    #ifndef __TIMER_H
    #define __TIMER_H
    
    void Timer2_Init(void);
    
    
    #endif
    ```

### Step.c
    
    ```
    #include "stm32f10x.h"                  // Device header
    #include "Step.h"
    #include "PWM.h"
    #include "Timer.h"
    
    
    //全局变量
    uint16_t step1_now_location;
    uint16_t step2_now_location;
    uint16_t step1_spin_time_flag;
    uint16_t step2_spin_time_flag;
    uint8_t step1_spin_run_flag;
    uint8_t step2_spin_run_flag;
    
    
    /**
      * 函    数：步进电机初始化(包括步进电机1、2)
      * 参    数：无
      * 返 回 值：无
      */
    void Step_Init(void)
    {
    	
    	RCC_APB2PeriphClockCmd(Step1_GPIO_Clock, ENABLE);
    	RCC_APB2PeriphClockCmd(Step2_GPIO_Clock, ENABLE);
    	GPIO_InitTypeDef GPIO_InitStructure;
    	
    	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
    	GPIO_InitStructure.GPIO_Pin = Step1_DIR_Pin | Step1_ENA_Pin;
    	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    	GPIO_Init(Step1_GPIO_Port, &GPIO_InitStructure);
    	
    	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
    	GPIO_InitStructure.GPIO_Pin = Step2_DIR_Pin | Step2_ENA_Pin;
    	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    	GPIO_Init(Step2_GPIO_Port, &GPIO_InitStructure);
    	
    	GPIO_ResetBits(Step1_GPIO_Port,Step1_DIR_Pin | Step1_ENA_Pin);//全设置低电平
    	GPIO_ResetBits(Step2_GPIO_Port,Step2_DIR_Pin | Step2_ENA_Pin);//全设置低电平
    	
    	TIM4_PWM_Init();
    
    	
    	Timer2_Init();
    	
    }
    
    
    /**
      * 函    数：步进电机使能
      * 参    数：步进电机编号：1  2
      * 返 回 值：无
      */
    void Step_Enable(uint8_t Step_ID)
    {
    	if(Step_ID == 1)
    	{
    		GPIO_SetBits(Step1_GPIO_Port,Step1_ENA_Pin);
    	}
    	else if(Step_ID == 2)
    	{
    		GPIO_SetBits(Step2_GPIO_Port,Step2_ENA_Pin);
    	}
    }
    
    /**
      * 函    数：步进电机失能
      * 参    数：步进电机编号：1  2
      * 返 回 值：无
      */
    void Step_Disable(uint8_t Step_ID)
    {
    	if(Step_ID == 1)
    	{
    		GPIO_ResetBits(Step1_GPIO_Port,Step1_ENA_Pin);
    	}
    	else if(Step_ID == 2)
    	{
    		GPIO_ResetBits(Step2_GPIO_Port,Step2_ENA_Pin);
    	}
    }
    
    /**
      * 函    数：步进电机旋转
      * 参    数：	步进电机编号：1  2
    				旋转方向：1--正传	0--反转
    				旋转时间：0-1000000	单位：ms
      * 返 回 值：无
      */
    void spin_Step(uint8_t Step_ID ,uint8_t diraction , uint16_t spin_time)
    {
    
    	
    	if(Step_ID == 1)
    	{
    		if(diraction == 1)
    		{
    			//正传
    			GPIO_ResetBits(Step1_GPIO_Port,Step1_DIR_Pin);
    			
    		}
    		else if(diraction == 0)
    		{
    			//反转
    			GPIO_SetBits(Step1_GPIO_Port,Step1_DIR_Pin);
    		}
    		
    		step1_spin_run_flag = 1;
    		//置标志位
    		step1_spin_time_flag = spin_time;
    		
    	}
    	else if(Step_ID == 2)
    	{
    		if(diraction == 1)
    		{
    			//正传
    			GPIO_ResetBits(Step2_GPIO_Port,Step2_DIR_Pin);
    		}
    		else if(diraction == 0)
    		{
    			//反转
    			GPIO_SetBits(Step2_GPIO_Port,Step2_DIR_Pin);
    		}
    		step2_spin_run_flag = 1;
    		step2_spin_time_flag = spin_time;
    	}
    }
    
    
    /**
      * 函    数：步进电机旋转到指定编码位置
      * 参    数：	步进电机编号：1  2
    				旋转位置：0-1000000	单位：ms，
      * 给 值 参 考：值给160为步进电机转一圈
    				35步进电机(2)的到最底端的值为580
      * 返 回 值：无
      */
    void Set_Step_location(uint8_t Step_ID , uint16_t location)
    {
    
    	
    	
    	if(Step_ID == 1)
    	{
    		//获得当前的location:step1_now_location
    		//计算要转动的location大小
    		if(location - step1_now_location > 0)
    		{
    			//正转
    			spin_Step(1,0,(location - step1_now_location));
    			step1_now_location = location;
    			
    		}
    		else if(location - step1_now_location < 0)
    		{
    			//反转
    			spin_Step(1,1,(step1_now_location - location));
    			step1_now_location = location;
    			
    		}
    		else if(location - step1_now_location == 0)
    			return;
    		
    	}
    	else if(Step_ID == 2)
    	{
    		//获得当前的location:step1_now_location
    		//计算要转动的location大小
    		if(location - step2_now_location > 0)
    		{
    			//正转
    			spin_Step(2,0,(location - step2_now_location));
    			step2_now_location = location;
    			
    		}
    		else if(location - step2_now_location < 0)
    		{
    			//反转
    			spin_Step(2,1,(step2_now_location - location));
    			step2_now_location = location;
    		}
    		else if(location - step2_now_location == 0)
    			return;
    	}
    }
    
    
    
    
    /**
      * 函    数：TIM2定时中断函数，用于配合步进电机旋转使用，避免拥塞
      * 参    数：无
      * 返 回 值：无
      */
    void TIM2_IRQHandler(void)
    {
    	if (TIM_GetITStatus(TIM2, TIM_IT_Update) == SET)
    	{
    		if(step1_spin_run_flag == 1)
    		{
    			TIM4_PWM_SetCompare4(50);
    			if(step1_spin_time_flag > 0)
    			{
    				step1_spin_time_flag  = step1_spin_time_flag - 10;
    			}
    			else if(step1_spin_time_flag <= 0)
    			{
    				TIM4_PWM_SetCompare4(0);
    				step1_spin_run_flag = 0;
    			}
    		}
    
    		if(step2_spin_run_flag == 1)
    		{		
    			TIM4_PWM_SetCompare2(50);
    			if(step2_spin_time_flag > 0)
    			{
    				step2_spin_time_flag  = step2_spin_time_flag - 10;
    			}
    			else if(step2_spin_time_flag <= 0)
    			{
    				TIM4_PWM_SetCompare2(0);
    				step2_spin_run_flag = 0;
    			}
    		}
    		
    		
    		TIM_ClearITPendingBit(TIM2, TIM_IT_Update);
    	}
    }
    ```
    

### Step.h
    
    ```
    #ifndef __STEP_H
    #define __STEP_H
    
    #include "stm32f10x.h"                  // Device header
    
    
    #define Step1_GPIO_Clock		RCC_APB2Periph_GPIOB
    #define Step2_GPIO_Clock		RCC_APB2Periph_GPIOB
    
    
    #define Step1_GPIO_Port		GPIOB
    #define Step2_GPIO_Port		GPIOB
    
    
    //#define Step1_PUL_Pin		GPIO_Pin_9
    #define Step1_DIR_Pin		GPIO_Pin_12
    #define Step1_ENA_Pin		GPIO_Pin_13
    
    //#define Step2_PUL_Pin		GPIO_Pin_7
    #define Step2_DIR_Pin		GPIO_Pin_14
    #define Step2_ENA_Pin		GPIO_Pin_15
    
    
    extern uint16_t step1_now_location;
    extern uint16_t step2_now_location;
    extern uint16_t step1_spin_time_flag;
    extern uint16_t step2_spin_time_flag;
    
    void Step_Init(void);
    void Step_Enable(uint8_t Step_ID);
    void Step_Disable(uint8_t Step_ID);
    void spin_Step(uint8_t Step_ID ,uint8_t diraction , uint16_t spin_time);
    void Set_Step_location(uint8_t Step_ID , uint16_t location);
    
    
    #endif
    ```

### main.c
    
    ```
    #include "stm32f10x.h"                  // Device header
    #include "Delay.h"
    #include "Step.h"
    #include "PWM.h"
    
    
    
    int main(void)
    {
    	Step_Init();
    	Step_Enable(1);
    	Step_Enable(2);
    
    	Set_Step_location(1,600);
    	while (1)
    	{
    
    		Set_Step_location(2,200);
    		Delay_ms(2000);
    		Set_Step_location(2,580);
    		Set_Step_location(1,400);
    		Delay_ms(3000);
    		Set_Step_location(2,0);
    		Set_Step_location(1,200);
    		Delay_ms(3000);
    
    	}
    }
	```
