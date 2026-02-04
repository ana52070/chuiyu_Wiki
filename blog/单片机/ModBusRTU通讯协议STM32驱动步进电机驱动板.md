---
title: ModBusRTU通讯协议/STM32驱动步进电机驱动板
date: 已于 2025-03-02
tags: [CSDN搬运]
---

# ModBusRTU通讯协议/STM32驱动步进电机驱动板

> 原文链接：[ModBusRTU通讯协议/STM32驱动步进电机驱动板](https://blog.csdn.net/chui_yu666/article/details/145950116)

## 目录

1.RS485介绍

2.ModBus通讯协议介绍

3.步进电机驱动板介绍

4.stm32f103控制步进电机驱动板代码

## 1.RS485介绍

下面是本人自己的简单的一句话介绍RS485：TTL串口的升级版，通过将传统的线（0V逻辑低电平、3.3V逻辑高电平）升级为差分线（A、B之间的正电平在+2～+6V，是一个逻辑状态，负电平在-2～6V），这样计算电压差不仅能够增强防干扰能力，还可以少了GND这一根线。

关于RS485更详细但又简单通俗易懂的视频链接：非常推荐去看一看！！才几分钟

【5分钟看懂!串口RS232 RS485最本质的区别！】 [5分钟看懂!串口RS232 RS485最本质的区别！_哔哩哔哩_bilibili](<https://www.bilibili.com/video/BV1PD4y147ts/?share_source=copy_web&vd_source=800b0cce2dee97823e91fad6181bdec5> "5分钟看懂!串口RS232 RS485最本质的区别！_哔哩哔哩_bilibili")  
  
RS485一般用在PLC领域，MCU领域一般只有TTL串口外设。因此若我们需要用MCU驱动RS485，需要一个TTL转RS485模块。  
可以淘宝买一个：

![](https://i-blog.csdnimg.cn/direct/c5266f9e465e480db2cb75538186f2be.png)

也可以自己画一个（该电路已经经过实测可用）：  


![](https://i-blog.csdnimg.cn/direct/f2e928020c7e4c95b937bfffb71a6d66.png)

## 2.ModBus通讯协议介绍

下面是本人自己的简单的一句话介绍ModBus：就是一个业界大家都商量好的一个报文格式而已，我们都约定俗成好了，这样的话就能够互相听得懂对方发送的消息并作出正确的回应了。

关于RS485更详细的博客链接：（下面的介绍主要来源于该博客，推荐去看原文）

[大神带你秒懂Modbus通信协议-CSDN博客](<https://blog.csdn.net/tiandiren111/article/details/118347661> "大神带你秒懂Modbus通信协议-CSDN博客")

#### **1、帧结构**

**帧结构 = 地址 + 功能码+ 数据 + 校验**

  * **地址** : 占用一个字节，范围0-255，其中有效范围是1-247，其他有特殊用途，比如255是广播地址(广播地址就是应答所有地址，正常的需要两个设备的地址一样才能进行查询和回复)。

  * **功能码** ：占用一个字节，功能码的意义就是，知道这个指令是干啥的，比如你可以查询从机的数据，也可以修改数据，所以不同功能码对应不同功能。

  * **数据** ：根据功能码不同，有不同结构，在下面的实例中有说明。

  * **校验** ：为了保证数据不错误，增加这个，然后再把前面的数据进行计算看数据是否一致，如果一致，就说明这帧数据是正确的，我再回复；如果不一样，说明你这个数据在传输的时候出了问题，数据不对的，所以就抛弃了。




#### 2、发送数据解析

![](https://i-blog.csdnimg.cn/direct/e237bef3a26e499181c24dca7c2d48b4.png)

01-地址，也就是你传感器的地址

03-功功能码，03代表查询功能，查询传感器的数据

00 00-代表查询的起始寄存器地址.说明从0x0000开始查询。这里需要说明以下，Modbus把数据存放在寄存器中，通过查询寄存器来得到不同变量的值，一个寄存器地址对应2字节数据

00 01-代表查询了一个寄存器.结合前面的00 00,意思就是查询从0开始的1个寄存器值

84 0A-循环冗余校验,是modbus的校验公式,从首个字节开始到84前面为止;

#### 3、回复数据解析![](https://i-blog.csdnimg.cn/direct/e3deec873002446790767773025bba7a.png)

01-地址，也就是你传感器的地址

03-功功能码，03代表查询功能，查询传感器的数据。这里要注意的是注意发给从机的功能码是啥，从机就要回复同样的功能码，如果不一样说明这一帧数据有错误

02-代表后面数据的字节数,因为上面说到,一个寄存器有2个字节,所以后面的字节数肯定是2*查询的寄存器个数;

19 98-寄存器的值是19 98,结合发送的数据看出,01这个寄存器的值为19 98

B2 7E-循环冗余校验

## 3.步进电机驱动板介绍

步进电机主要用两款：1.张大头 2.巧克力

关于步进电机驱动板的详细介绍在这里就不多展开了，有需要可自行去了解。

简单来说就是：

步进电机+步进电机驱动板+MCU

通过MCU与步进电机驱动板的交互即可实现步进电机的驱动。  
  
MCU与步进电机驱动板的交互有多种：  
脉冲、脉宽、UART串口、RS485、CAN等等

## 4.stm32f103控制步进电机驱动板代码

本博客代码主要针对于通过使用RS485通讯方式、ModBus通讯协议驱动巧克力驱动板。将分为两部分：1.ModBus底层代码 2.巧克力驱动代码

### 1.ModBus底层代码

使用了STM32F103的串口2来完成，可根据需求自行修改为其它串口。

#### sys.h

由于本工程是移植于其它来自于正点原子的工程代码而来，所以需要带上正点原子的底层封装代码。但实际对开发无任何影响，还是和江科大工程一样。
    
    
    #ifndef __SYS_H
    #define __SYS_H	
    #include "stm32f10x.h"
    //////////////////////////////////////////////////////////////////////////////////	 
    //本程序只供学习使用，未经作者许可，不得用于其它任何用途
    //ALIENTEK STM32开发板		   
    //正点原子@ALIENTEK
    //技术论坛:www.openedv.com
    //修改日期:2012/8/18
    //版本：V1.7
    //版权所有，盗版必究。
    //Copyright(C) 广州市星翼电子科技有限公司 2009-2019
    //All rights reserved
    ////////////////////////////////////////////////////////////////////////////////// 	 
    
    //0,不支持ucos
    //1,支持ucos
    #define SYSTEM_SUPPORT_OS		0		//定义系统文件夹是否支持UCOS
    																	    
    	 
    //位带操作,实现51类似的GPIO控制功能
    //具体实现思想,参考<<CM3权威指南>>第五章(87页~92页).
    //IO口操作宏定义
    #define BITBAND(addr, bitnum) ((addr & 0xF0000000)+0x2000000+((addr &0xFFFFF)<<5)+(bitnum<<2)) 
    #define MEM_ADDR(addr)  *((volatile unsigned long  *)(addr)) 
    #define BIT_ADDR(addr, bitnum)   MEM_ADDR(BITBAND(addr, bitnum)) 
    //IO口地址映射
    #define GPIOA_ODR_Addr    (GPIOA_BASE+12) //0x4001080C 
    #define GPIOB_ODR_Addr    (GPIOB_BASE+12) //0x40010C0C 
    #define GPIOC_ODR_Addr    (GPIOC_BASE+12) //0x4001100C 
    #define GPIOD_ODR_Addr    (GPIOD_BASE+12) //0x4001140C 
    #define GPIOE_ODR_Addr    (GPIOE_BASE+12) //0x4001180C 
    #define GPIOF_ODR_Addr    (GPIOF_BASE+12) //0x40011A0C    
    #define GPIOG_ODR_Addr    (GPIOG_BASE+12) //0x40011E0C    
    
    #define GPIOA_IDR_Addr    (GPIOA_BASE+8) //0x40010808 
    #define GPIOB_IDR_Addr    (GPIOB_BASE+8) //0x40010C08 
    #define GPIOC_IDR_Addr    (GPIOC_BASE+8) //0x40011008 
    #define GPIOD_IDR_Addr    (GPIOD_BASE+8) //0x40011408 
    #define GPIOE_IDR_Addr    (GPIOE_BASE+8) //0x40011808 
    #define GPIOF_IDR_Addr    (GPIOF_BASE+8) //0x40011A08 
    #define GPIOG_IDR_Addr    (GPIOG_BASE+8) //0x40011E08 
     
    //IO口操作,只对单一的IO口!
    //确保n的值小于16!
    #define PAout(n)   BIT_ADDR(GPIOA_ODR_Addr,n)  //输出 
    #define PAin(n)    BIT_ADDR(GPIOA_IDR_Addr,n)  //输入 
    
    #define PBout(n)   BIT_ADDR(GPIOB_ODR_Addr,n)  //输出 
    #define PBin(n)    BIT_ADDR(GPIOB_IDR_Addr,n)  //输入 
    
    #define PCout(n)   BIT_ADDR(GPIOC_ODR_Addr,n)  //输出 
    #define PCin(n)    BIT_ADDR(GPIOC_IDR_Addr,n)  //输入 
    
    #define PDout(n)   BIT_ADDR(GPIOD_ODR_Addr,n)  //输出 
    #define PDin(n)    BIT_ADDR(GPIOD_IDR_Addr,n)  //输入 
    
    #define PEout(n)   BIT_ADDR(GPIOE_ODR_Addr,n)  //输出 
    #define PEin(n)    BIT_ADDR(GPIOE_IDR_Addr,n)  //输入
    
    #define PFout(n)   BIT_ADDR(GPIOF_ODR_Addr,n)  //输出 
    #define PFin(n)    BIT_ADDR(GPIOF_IDR_Addr,n)  //输入
    
    #define PGout(n)   BIT_ADDR(GPIOG_ODR_Addr,n)  //输出 
    #define PGin(n)    BIT_ADDR(GPIOG_IDR_Addr,n)  //输入
    
    //以下为汇编函数
    void WFI_SET(void);		//执行WFI指令
    void INTX_DISABLE(void);//关闭所有中断
    void INTX_ENABLE(void);	//开启所有中断
    void MSR_MSP(u32 addr);	//设置堆栈地址
    
    #endif
    

#### crc16.c

该部分用于ModBus通讯中的CRC校验计算
    
    
    /*************************************************************************************
    文件名称：crc16.c
    版    本：V1.0
    日    期：2020-5-11
    编    著：Eric Xie
    说    明：CRC校验表
    修改日志：
    
    
    
    **************************************************************************************/
    #include "crc16.h"
    
    const unsigned char TabH[] = {  //CRC高位字节值表
            0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,  
            0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,  
            0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,  
            0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,  
            0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1,  
            0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41,  
            0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1,  
            0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,  
            0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,  
            0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40,  
            0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1,  
            0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,  
            0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,  
            0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40,  
            0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,  
            0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,  
            0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,  
            0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,  
            0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,  
            0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,  
            0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,  
            0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40,  
            0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1,  
            0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,  
            0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,  
            0x80, 0x41, 0x00, 0xC1, 0x81, 0x40  
        } ;  
    const unsigned char TabL[] = {  //CRC低位字节值表
            0x00, 0xC0, 0xC1, 0x01, 0xC3, 0x03, 0x02, 0xC2, 0xC6, 0x06,  
            0x07, 0xC7, 0x05, 0xC5, 0xC4, 0x04, 0xCC, 0x0C, 0x0D, 0xCD,  
            0x0F, 0xCF, 0xCE, 0x0E, 0x0A, 0xCA, 0xCB, 0x0B, 0xC9, 0x09,  
            0x08, 0xC8, 0xD8, 0x18, 0x19, 0xD9, 0x1B, 0xDB, 0xDA, 0x1A,  
            0x1E, 0xDE, 0xDF, 0x1F, 0xDD, 0x1D, 0x1C, 0xDC, 0x14, 0xD4,  
            0xD5, 0x15, 0xD7, 0x17, 0x16, 0xD6, 0xD2, 0x12, 0x13, 0xD3,  
            0x11, 0xD1, 0xD0, 0x10, 0xF0, 0x30, 0x31, 0xF1, 0x33, 0xF3,  
            0xF2, 0x32, 0x36, 0xF6, 0xF7, 0x37, 0xF5, 0x35, 0x34, 0xF4,  
            0x3C, 0xFC, 0xFD, 0x3D, 0xFF, 0x3F, 0x3E, 0xFE, 0xFA, 0x3A,  
            0x3B, 0xFB, 0x39, 0xF9, 0xF8, 0x38, 0x28, 0xE8, 0xE9, 0x29,  
            0xEB, 0x2B, 0x2A, 0xEA, 0xEE, 0x2E, 0x2F, 0xEF, 0x2D, 0xED,  
            0xEC, 0x2C, 0xE4, 0x24, 0x25, 0xE5, 0x27, 0xE7, 0xE6, 0x26,  
            0x22, 0xE2, 0xE3, 0x23, 0xE1, 0x21, 0x20, 0xE0, 0xA0, 0x60,  
            0x61, 0xA1, 0x63, 0xA3, 0xA2, 0x62, 0x66, 0xA6, 0xA7, 0x67,  
            0xA5, 0x65, 0x64, 0xA4, 0x6C, 0xAC, 0xAD, 0x6D, 0xAF, 0x6F,  
            0x6E, 0xAE, 0xAA, 0x6A, 0x6B, 0xAB, 0x69, 0xA9, 0xA8, 0x68,  
            0x78, 0xB8, 0xB9, 0x79, 0xBB, 0x7B, 0x7A, 0xBA, 0xBE, 0x7E,  
            0x7F, 0xBF, 0x7D, 0xBD, 0xBC, 0x7C, 0xB4, 0x74, 0x75, 0xB5,  
            0x77, 0xB7, 0xB6, 0x76, 0x72, 0xB2, 0xB3, 0x73, 0xB1, 0x71,  
            0x70, 0xB0, 0x50, 0x90, 0x91, 0x51, 0x93, 0x53, 0x52, 0x92,  
            0x96, 0x56, 0x57, 0x97, 0x55, 0x95, 0x94, 0x54, 0x9C, 0x5C,  
            0x5D, 0x9D, 0x5F, 0x9F, 0x9E, 0x5E, 0x5A, 0x9A, 0x9B, 0x5B,  
            0x99, 0x59, 0x58, 0x98, 0x88, 0x48, 0x49, 0x89, 0x4B, 0x8B,  
            0x8A, 0x4A, 0x4E, 0x8E, 0x8F, 0x4F, 0x8D, 0x4D, 0x4C, 0x8C,  
            0x44, 0x84, 0x85, 0x45, 0x87, 0x47, 0x46, 0x86, 0x82, 0x42,  
            0x43, 0x83, 0x41, 0x81, 0x80, 0x40  
        } ;
    
    /*************************************************************************************
     * 函数说明: CRC16校验
     * 入口参数：u8 *ptr,u8 len
     * 出口参数：u16
     * 函数功能：根据入口参数数组的值计算crc16校验值 并返回
    **************************************************************************************/
    unsigned int GetCRC16(unsigned char *pPtr,unsigned char ucLen)
    { 
        unsigned int  uiIndex;
        unsigned char ucCrch = 0xFF;  		//高CRC字节
        unsigned char ucCrcl = 0xFF;  		//低CRC字节 
        while (ucLen --)  			//计算指定长度CRC
        {
            uiIndex = ucCrch ^ *pPtr++;
            ucCrch  = ucCrcl ^ TabH[uiIndex];
            ucCrcl  = TabL[uiIndex];
        }
        
        return ((ucCrch << 8) | ucCrcl);  
    } 
    
    

#### crc16.h

该部分用于ModBus通讯中的CRC校验计算
    
    
    #ifndef _CRC16_H
    #define _CRC16_H
    
    #include "sys.h"
    
    unsigned int GetCRC16(unsigned char *pPtr,unsigned char ucLen);	/* 获得CRC16校验值 */
    
    #endif 
    
    

#### Timer.c

该部分主要用来配合串口通过使用定时中断的方式接收ModBus报文
    
    
    //模块导入
    #include "stm32f10x.h"   // 包含STM32F10x系列微控制器的头文件
    #include "Timer.h"       // 包含定时器相关函数的头文件
    
    
    
    
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
    	TIM_TimeBaseInitStructure.TIM_Period = 1000 - 1;				//计数周期，即ARR的值
    	TIM_TimeBaseInitStructure.TIM_Prescaler = 72 - 1;				//预分频器，即PSC的值
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
    
    
    
    
    

#### Timer.h

该部分主要用来配合串口通过使用定时中断的方式接收ModBus报文
    
    
    #ifndef __TIMER_H
    #define __TIMER_H
    
    
    
    void Timer2_Init(void);
    
    
    
    
    
    #endif
    
    

#### RS485.c

该部分主要是ModBus的驱动代码
    
    
    /*************************************************************************************
    文件名称：RS485.c
    版    本：V1.0
    日    期：2020-5-11
    编    著：Eric Xie
    说    明：串口相关设置
    修改日志：
    
    modbus协义基本格式说明：
    	1.主机对从机写数据操作，从机接收到报文后对报文进行解析，然后执行相应的处理，同时需要向主机应答
    	  为什么要应答？因为主机需要确认从机是否收到报文，然后可向从机发送其它的数据，执行其它的操作，
    	  有些操作是基于上一次操作而产生的，所以需要应答，以保证系统的健壮性和稳定性。当然也可不理会
    	  
    	例：主机向从机发送一条报文格式如下(16进制)
    		01		  06	 00 01	   00 17	 98 04
    	  从机地址	功能号	数据地址	数据	CRC校验码	
    	解：主机向地址为01的从机 寄存器地址为0001的地方 写入数据0017
    	    从机可把这条报文原样返回作为应答，主机收到后表示写数据成功，可执行下一条操作
    	
    	2.主机对从机进行读数据操作，从机接收到报文后进行解析，然后根据报文的内容，把需要返回给主机的数
    	  据返回给主机，返回的报文即同等于应答。
    	
    	例：主机向从机发送一条报文格式如下(16进制)
    		 01		  03	 00 01		   00 01		 d5 ca
    	  从机地址	功能号	数据地址	读取数据个数	CRC校验码
    	解：假设从机寄存器组0001的地方存放的数据为aa，那么返回给主机的数据为 01 03 02 00 aa 38 3b
    		主机收到后对这条报文解析或把读到的数据保存在指定的变量中即可。
    		
    备注说明：以上是基本通讯格式，这些数据可通过其它方式逻辑实现更多的功能，具体请自行研究
    
    **************************************************************************************/   
    #include "rs485.h"	 
    #include "Delay.h"
    #include "crc16.h"
    #include "Serial.h"
    
    
    
    /* 通讯标志 主机发送数据后置1 接收到应答后清零 */
    u8 RS485Busy = 0;
    /* 接收缓存区 */
    u8 RS485_RX_BUF[64];  	//接收缓冲,最大64个字节.
    /* 用于保存读命令获得的数据 */
    u16 ReadDateVal = 0;
    
    /***************************************************************************************************
     * 函数说明: 485串口初始化
     * 入口参数：u32 bound
     * 出口参数：
     * 函数功能：初始化串口2 用于485通讯 
     *			 波特率要和从机的波特率一致
     *			 具体设置可以rs485.h是查看设置 对应硬件
    ***************************************************************************************************/ 
    void RS485_Init(u32 bound)
    {  
    	GPIO_InitTypeDef GPIO_InitStructure;
    	USART_InitTypeDef USART_InitStructure;
    	NVIC_InitTypeDef NVIC_InitStructure;
    	
    	RCC_APB2PeriphClockCmd(RS485_GPIO_RCC | RS485_MODE_RCC, ENABLE);	//打开串口GPIO时钟 RS485控制引脚GPIO时钟 
    	RCC_APB1PeriphClockCmd(RS485_USART_RCC,ENABLE);				//使能对应使用串口时钟
    	RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO,ENABLE);			//复用功能时钟，如果串口引脚为复用功能即需要有这一条
    
    	GPIO_InitStructure.GPIO_Pin   = RS485_MODE_Pin;				//RS485模式控制引脚
    	GPIO_InitStructure.GPIO_Mode  = GPIO_Mode_Out_PP; 			//推挽输出
    	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;			//翻转速度50MHz
    	GPIO_Init(RS485_MODE_PROT, &GPIO_InitStructure);
    
    	GPIO_InitStructure.GPIO_Pin   = RS485_TX_Pin;				//TXD引脚
    	GPIO_InitStructure.GPIO_Mode  = GPIO_Mode_AF_PP;			//复用推挽
    	GPIO_Init(RS485_PROT, &GPIO_InitStructure);
    
    	GPIO_InitStructure.GPIO_Pin   = RS485_RX_Pin;				//RXD引脚
    	GPIO_InitStructure.GPIO_Mode  = GPIO_Mode_IN_FLOATING; 		//浮空输入
    	GPIO_Init(RS485_PROT, &GPIO_InitStructure);  
    	
    	NVIC_InitStructure.NVIC_IRQChannel = USART2_IRQn; 			//使能串口2中断
    	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 3; 	//先占优先级2级
    	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 2; 			//从优先级2级
    	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE; 			//使能外部中断通道
    	NVIC_Init(&NVIC_InitStructure); 							//根据NVIC_InitStruct中指定的参数初始化外设NVIC寄存器
     
    	USART_InitStructure.USART_BaudRate = bound;					//波特率设置
    	USART_InitStructure.USART_WordLength = USART_WordLength_8b;//8位数据长度
    	USART_InitStructure.USART_StopBits = USART_StopBits_1;		//一个停止位
    	USART_InitStructure.USART_Parity = USART_Parity_No;			//无奇偶校验位
    	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;//无硬件数据流控制
    	USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;//收发模式
    
    	USART_Init(RS485_USART_NUM, &USART_InitStructure); ; 		//初始化串口
    	USART_ITConfig(RS485_USART_NUM, USART_IT_RXNE, ENABLE);		//开启中断
    	USART_Cmd(RS485_USART_NUM, ENABLE);                    		//使能串口 
    
    }
    
    /****************************************************************************************************
     * 函数名称： void Send_Data(u8 *buf,u8 len)
     * 入口参数：u8 *buf u8 len
     * 返回  值：无
     * 功能说明：串口发送数据
     * 			 buf:发送区首地址
     *			 len:发送的字节数(为了和本代码的接收匹配,这里建议不要超过64个字节)
     ***************************************************************************************************/
    void Send_Data(u8 *buf,u8 len)
    {
    	u8 t;
    	Delay_ms(1);
    	for(t=0;t<len;t++)		//循环发送数据
    	{		   
    		while(USART_GetFlagStatus(RS485_USART_NUM, USART_FLAG_TC) == RESET);	  
    		USART_SendData(USART2,buf[t]);
    	}	 
    
    }
    
    
    
    /****************************************************************************************************
     * 函数名称：void RS485_RW_Opr(u8 ucAddr,u8 ucCmd,u16 ucReg,u16 uiDate)
     * 入口参数：u8 ucAddr,u8 ucCmd,u16 ucReg,u16 uiDate
     * 			 ucAddr：从机地址
     *			 ucCmd ：功能码 03->读	06->写
     *			 ucReg ：寄存器地址
     *			 uiDate：写操作即是发送的数据 读操作即是读取数据个数
     * 返回  值：无
     * 功能说明：485读写操作函数
     ***************************************************************************************************/   
    void RS485_RW_Opr(u8 ucAddr,u8 ucCmd,u16 ucReg,u16 uiDate)
    {
    	unsigned int crc;
    	unsigned char crcl;
    	unsigned char crch;	
    	unsigned char ucBuf[8];
    	
    	ucBuf[0] = ucAddr;				/* 从机地址 */
    	ucBuf[1] = ucCmd;				/* 命令 06 写 03 读 */
    	ucBuf[2] = ucReg >> 8;			/* 寄存器地址高位 */
    	ucBuf[3] = ucReg;				/* 寄存器地址低位 */
    	
    	
    	ucBuf[4] = uiDate >> 8;			/* 数据高8位 */
    	ucBuf[5] = uiDate;				/* 数据低8位 */
    	crc      = GetCRC16(ucBuf,6);   /* 计算CRC校验值 */
    	crch     = crc >> 8;    		/* crc高位 */
    	crcl     = crc &  0xFF;			/* crc低位 */
    	ucBuf[6] = crch;				/* 校验高8位 */
    	ucBuf[7] = crcl;				/* 校验低8位 */
    	
    	Send_Data(ucBuf,8);				/* 发送数据 */
    }
    
    
    
    
    
    uint8_t Serial2_RxPacket[9];//7
    uint8_t Serial2_RxFlag;					//定义接收数据包标志位
    uint8_t Rx_Modbus_data[5];
    
    void USART2_IRQHandler(void)
    {
    
    	static uint8_t Rx2State = 0;		//定义表示当前状态机状态的静态变量
    	static uint8_t pRx2Packet = 0;	//定义表示当前接收数据位置的静态变量
    	if (USART_GetITStatus(USART2, USART_IT_RXNE) == SET)		//判断是否是USART1的接收事件触发的中断
    	{
    		uint8_t Rx2Data = USART_ReceiveData(USART2);				//读取数据寄存器，存放在接收的数据变量
    
    		/*使用状态机的思路，依次处理数据包的不同部分*/
    		if(Rx2State == 0 &&  Serial2_RxFlag == 0)
    		{
    			if(Rx2Data == 1)
    			{
    				Serial2_RxPacket[pRx2Packet] = Rx2Data;	//将数据存入数据包数组的指定位置
    				pRx2Packet ++;				//数据包的位置自增
    				Rx2State = 1;	//状态1：接收第二个字节
    			}
    		}
    		else if(Rx2State == 1)
    		{
    			Serial2_RxPacket[pRx2Packet] = Rx2Data;	//将数据存入数据包数组的指定位置
    			pRx2Packet ++;				//数据包的位置自增
    			Rx2State = 2;
    		}
    		
    		else if(Rx2State == 2)
    		{
    			if(Rx2Data == 4)	//若为四字节型接收
    			{
    				Serial2_RxPacket[pRx2Packet] = Rx2Data;	//将数据存入数据包数组的指定位置
    				pRx2Packet ++;				//数据包的位置自增
    				Rx2State = 3;		//四字节型接收状态位
    			}
    			else if(Rx2Data == 2)	//若为二字节型接收
    			{
    				Serial2_RxPacket[pRx2Packet] = Rx2Data;	//将数据存入数据包数组的指定位置
    				pRx2Packet ++;				//数据包的位置自增
    				Rx2State = 4;		//二字节型接收状态位
    			}
    
    		}
    		
    		else if(Rx2State == 3)
    		{
    			if(pRx2Packet <= 8)//6
    			{
    				Serial2_RxPacket[pRx2Packet] = Rx2Data;	//将数据存入数据包数组的指定位置
    				pRx2Packet ++;				//数据包的位置自增
    			}
    			else
    			{
    				pRx2Packet = 0;
    				Rx2State = 0;
    				Serial2_RxFlag = 1;
    			}
    
    		}
    		else if(Rx2State == 4)
    		{
    			if(pRx2Packet <= 6)
    			{
    				Serial2_RxPacket[pRx2Packet] = Rx2Data;	//将数据存入数据包数组的指定位置
    				pRx2Packet ++;				//数据包的位置自增
    			}
    			else
    			{
    				pRx2Packet = 0;
    				Rx2State = 0;
    				Serial2_RxFlag = 1;
    			}
    
    		}
    		USART_ClearITPendingBit(USART2, USART_IT_RXNE);		//清除标志位
    	}											 
    } 
    
    uint8_t ModBus_RxFlag;					//定义接收数据包标志位
    void TIM2_IRQHandler(void)
    {
        if (TIM_GetITStatus(TIM2, TIM_IT_Update) == SET)
        {
            if(Serial2_RxFlag == 1)  // 判断是否接收到报文
            {
                /*
                格式解析：
                1,3,2,0,1,121,132
                1: 从机地址
                3: 命令号
                2: 数据字节数
                0,1: 数据
                121,132: CRC校验
                */
                // 创建用于存放数据的数组
    
                uint8_t data[7];
    			unsigned char crch;
    			if(Serial2_RxPacket[2] == 2)	//2字节数据形式
    			{
    				// 使用 for 循环将前 5 个数据存放到 data 数组
    				for (int i = 0; i < 5; i++) 
    				{
    					data[i] = Serial2_RxPacket[i];  // 将 Serial2_RxPacket 中的数据复制到 data 数组
    				}
    				// 计算 CRC 校验值
    				unsigned int calculated_crc = GetCRC16(data, 5);
    				crch=calculated_crc  >> 8;    										//crc高位
    				//crcl=calculated_crc  &  0xFF;										//crc低位
    				
    				// 输出计算的 CRC 和期望的 CRC 进行比较
    				if (Serial2_RxPacket[5] == crch)
    				{
    					// CRC 校验成功
    					Rx_Modbus_data[0] = Serial2_RxPacket[3];
    					Rx_Modbus_data[1] = Serial2_RxPacket[4];
    					ModBus_RxFlag = 2;  // 设置为 2，表示数据接收成功
    				} 
    				else
    				{
    					ModBus_RxFlag = 251;
    				}
    			}
    			
    			if(Serial2_RxPacket[2] == 4)	//4字节数据形式
    			{
    				// 使用 for 循环将前 7 个数据存放到 data 数组
    				for (int i = 0; i < 7; i++) 
    				{
    					data[i] = Serial2_RxPacket[i];  // 将 Serial2_RxPacket 中的数据复制到 data 数组
    				}
    				// 计算 CRC 校验值
    				unsigned int calculated_crc = GetCRC16(data, 7);
    				crch=calculated_crc  >> 8;    										//crc高位
    				//crcl=calculated_crc  &  0xFF;										//crc低位
    				
    				// 输出计算的 CRC 和期望的 CRC 进行比较
    				if (Serial2_RxPacket[7] == crch) 
    				{
    					// CRC 校验成功
    					Rx_Modbus_data[0] = Serial2_RxPacket[3];
    					Rx_Modbus_data[1] = Serial2_RxPacket[4];
    					Rx_Modbus_data[2] = Serial2_RxPacket[5];
    					Rx_Modbus_data[3] = Serial2_RxPacket[6];
    					ModBus_RxFlag = 4;  // 设置为 4，表示数据接收成功
    				}
    				else
    				{
    					ModBus_RxFlag = 250;
    				}
    			}
    
                // 清除接收标志
                Serial2_RxFlag = 0;  // 将接收标志位清除，以便下一次接收
            }
            TIM_ClearITPendingBit(TIM2, TIM_IT_Update);  // 清除定时器中断标志
        }
    }
    
    
    int32_t bytes_to_int32(uint8_t byte1, uint8_t byte2, uint8_t byte3, uint8_t byte4) 
    {
        // 按照大端字节序组合四个字节
        int32_t result = (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | byte4;
        return result;
    }
    
    int16_t bytes_to_int16(uint8_t byte1, uint8_t byte2) 
    {
        // 按照大端字节序组合两个字节
        int16_t result = (byte1 << 8) | byte2;
        return result;
    }
    
    
    _Bool ModBus_ReadCommand(u8 ucAddr,u16 ucReg,u16 uiDate,int32_t data)
    {
    	RS485_RW_Opr(ucAddr, READ, ucReg,uiDate);
    	uint8_t time = 200;
    	while(time--)
    	{	
    		if(ModBus_RxFlag == 4)							//如果收到数据
    		{	
    			int32_t result = bytes_to_int32(Rx_Modbus_data[0],Rx_Modbus_data[1],Rx_Modbus_data[2],Rx_Modbus_data[3]);
    			if(result == data)		//如果检索到关键词
    			{
    				return 0;
    			}
    		}
    		else if(ModBus_RxFlag == 2)							//如果收到数据
    		{	
    			int32_t result = bytes_to_int16(Rx_Modbus_data[0],Rx_Modbus_data[1]);
    			if(result == data)		//如果检索到关键词
    			{
    				return 0;
    			}
    		}
    		Delay_ms(1);
    	}
    	return 1;
    }
    
    
    int32_t ModBus_ReadData(u8 ucAddr,u16 ucReg,u16 uiDate)
    {
    	RS485_RW_Opr(ucAddr, READ, ucReg,uiDate);
    	uint8_t time = 200;
    	while(time--)
    	{	
    		if(ModBus_RxFlag == 4)							//如果收到数据
    		{	
    			int32_t result = bytes_to_int32(Rx_Modbus_data[0],Rx_Modbus_data[1],Rx_Modbus_data[2],Rx_Modbus_data[3]);
    			return result;
    		}
    		else if(ModBus_RxFlag == 2)							//如果收到数据
    		{	
    			int32_t result = bytes_to_int16(Rx_Modbus_data[0],Rx_Modbus_data[1]);
    			return result;
    		}
    		Delay_ms(1);
    	}
    	return 1;
    }
    
    
    
    
    
    
    
    
    
    
    
    

#### RS485.h
    
    
    #ifndef __RS485_H
    #define __RS485_H			
    
    #include "sys.h"	 								  
    
    
    /* 串口相关设置，如需更换串口更改下面这几项即可 */
    #define	RS485_PROT		GPIOA					//串口端口
    #define RS485_GPIO_RCC	RCC_APB2Periph_GPIOA	//串口端口GPIO时钟
    #define RS485_TX_Pin	GPIO_Pin_2				//串口TXD引脚
    #define RS485_RX_Pin	GPIO_Pin_3				//串口RXD引脚
    #define RS485_USART_RCC	RCC_APB1Periph_USART2	//串口功能时钟
    #define RS485_USART_NUM	USART2					//串口通道
    
    /* 485模式控制引脚设置 如需更换更改下面这几项即可 */
    #define	RS485_MODE_PROT	GPIOA					//RS485模式控制端口
    #define RS485_MODE_Pin	GPIO_Pin_1				//RS485模式控制引脚
    #define RS485_MODE_RCC	RCC_APB2Periph_GPIOA	//RS485模式控制端口GPIO时钟
    #define RS485_TX_EN		PAout(1)				//485模式控制.0,接收;1,发送
    
    /* 如果想串口中断接收，请不要注释以下宏定义 */
    #define EN_USART2_RX 	1						//0,不接收;1,接收.
    
    #define READ	0x03
    #define WRITE	0X06
    
    
    extern u8 RS485Busy ;
    extern u16 ReadDateVal;
    extern u8 USART2_RX_BUF[64];
    
    extern uint8_t Serial2_RxPacket[];
    extern uint8_t Serial2_RxFlag;
    extern uint8_t Rx_Modbus_data[];
    
    extern uint8_t ModBus_RxFlag;
    
    void RS485_Init(u32 bound);
    void RS485_RW_Opr(u8 ucAddr,u8 ucCmd,u16 ucReg,u16 uiDate);
    
    
    int32_t bytes_to_int32(uint8_t byte1, uint8_t byte2, uint8_t byte3, uint8_t byte4);
    int16_t bytes_to_int16(uint8_t byte1, uint8_t byte2);
    _Bool ModBus_ReadCommand(u8 ucAddr,u16 ucReg,u16 uiDate,int32_t data);
    int32_t ModBus_ReadData(u8 ucAddr,u16 ucReg,u16 uiDate);
    
    
    #endif	   
    
    

### 2.巧克力驱动板的驱动代码

#### Step.c
    
    
    #include "stm32f10x.h"                  // Device header
    #include "Delay.h"
    #include "RS485.h"
    #include "ESP8266.h"
    #include <stdio.h>
    #include "LED.h"
    #include "Timer.h"
    u16 high,low;
    
    char Send_Data2[200];
    
    
    // 将32位有符号整数转换为两个16位无符号整数
    void convertToModbusRegisters(int32_t value, u16* highRegister, u16* lowRegister) 
    {
        // 直接拆分为高16位和低16位
        *highRegister = (u16)(value >> 16);        // 高16位
        *lowRegister = (u16)(value & 0xFFFF);      // 低16位
    }
    
    
    void Step_Init(void)
    {
    	RS485_Init(115200);	
    	Timer2_Init();
    //	convertToModbusRegisters(-512000,&high,&low);
    //	RS485_RW_Opr(0x01, WRITE, 0X68, high);
    //	RS485_RW_Opr(0x01, WRITE, 0X69, low);
    }
    
    
    
    
    
    void Step_Return_zreo(void)
    {
    	//设置堵转速度	210(D2)
    	convertToModbusRegisters(180000,&high,&low);
    	RS485_RW_Opr(0x01, WRITE, 0XD2, high);
    	RS485_RW_Opr(0x01, WRITE, 0XD3, low);
    	
    	//设置堵转时间	212(D4)
    //	convertToModbusRegisters(5,&high,&low);
    //	RS485_RW_Opr(0x01, WRITE, 0XD4, 0x00);
    //	RS485_RW_Opr(0x01, WRITE, 0XD5, 0x05);
    	
    	//设置归零速度	247(F7)
    	convertToModbusRegisters(180000,&high,&low);
    	RS485_RW_Opr(0x01, WRITE, 0XF7, high);
    	RS485_RW_Opr(0x01, WRITE, 0XF8, low);
    	//设置回转间隙	251(FB)
    	convertToModbusRegisters(-352000,&high,&low);
    	RS485_RW_Opr(0x01, WRITE, 0XFB, high);
    	RS485_RW_Opr(0x01, WRITE, 0XFC, low);
    	
    	//开启归零	
    	RS485_RW_Opr(0x01, WRITE, 0XFD, 0x01);
    	
    	//归零检测
    	while(ModBus_ReadCommand(0X01,0XF5,0X01,1))
    		Delay_ms(200);
    	while(ModBus_ReadCommand(0X01,0XF5,0X01,2))
    		Delay_ms(200);
    	while(ModBus_ReadCommand(0X01,0XF5,0X01,0))
    		Delay_ms(200);
    	
    	//置相对位置为0	236(EC)
    	RS485_RW_Opr(0x01, WRITE, 0XEC, 0x00);
    	while(ModBus_ReadCommand(0X01,0XEC,0X02,0))
    	{
    		Delay_ms(200);
    		RS485_RW_Opr(0x01, READ, 0XEC, 0x00);
    	}
    
    }
    
    
    
    
    void Step_distance_command(float distance)
    {
    	//计算位置	12800 = 1cm
        // 计算对应的编码值，假设每1cm对应12800
        int32_t encoder_value = (distance - 10) * 12800;
    
    	convertToModbusRegisters(encoder_value,&high,&low);
    	//去到指定的位置
    	RS485_RW_Opr(0x01, WRITE, 0XEE, high);
    	RS485_RW_Opr(0x01, WRITE, 0XEF, low);
    }
    
    
    
    float encoder_value_to_distance(int32_t encoder_value) {
        // 根据公式反转计算距离
        float distance = (float)encoder_value / 12800 + 10;
        return distance;
    }
    
    float Step_distance_get(void)
    {
    	//读取编码值
    	float result = encoder_value_to_distance(ModBus_ReadData(0X01, 0XEE ,0X02));
    	
    	return result;
    	
    }
    
    
    
    

#### Step.h
    
    
    #ifndef __STEP_H
    #define __STEP_H			
    
    #include "sys.h"	 								  
    #include "stm32f10x.h"                  // Device header
    #include "Delay.h"
    #include "RS485.h"
    
    // 输入一个十进制数，返回两个 u16 类型的十六进制数
    void decimalToTwoHex(int decimal, u16* high, u16* low);
    
    void convertToModbusRegisters(int32_t value, u16* highRegister, u16* lowRegister) ;
    
    void Step_Init(void);
    
    
    
    
    
    void Step_Return_zreo(void);
    void Step_distance_command(float distance);
    
    float Step_distance_get(void);
    
    #endif	   

