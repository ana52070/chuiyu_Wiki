---
title: ROS2串口通信-连接STM32等下位机/串口模块调用
date: 已于 2025-03-26
tags: [CSDN搬运]
---

# ROS2串口通信-连接STM32等下位机/串口模块调用

> 原文链接：[ROS2串口通信-连接STM32等下位机/串口模块调用](https://blog.csdn.net/chui_yu666/article/details/146533466)

## **前言**

阅读此博客需要有基础的ROS2知识，再次不做讲解。

## **开启开发板串口**

由于每个开发板的串口开启方式都不一样，这里不做过多讲解，根据自己的开发板寻找教程开启串口即可。我这里使用的是鲁班猫4的开发板，这里分享一下鲁班猫4的串口开启教程： [6\. 串口通讯 — 快速使用手册—基于LubanCat-RK3588系列板卡 文档](<https://doc.embedfire.com/linux/rk3588/quick_start/zh/latest/quick_start/40pin/uart/uart.html> "6. 串口通讯 — 快速使用手册—基于LubanCat-RK3588系列板卡 文档")

## **测试串口通讯**

将下面的测试代码保存至开发板并运行：
    
    
     import serial
     import time
     ​
     def serial_communication():
         ser = None
         try:
             # 配置串口参数
             ser = serial.Serial(
                 port='/dev/ttyS0',        # 根据系统修改串口设备
                 baudrate=115200,          # 波特率
                 bytesize=serial.EIGHTBITS,# 数据位
                 parity=serial.PARITY_NONE,# 校验位
                 stopbits=serial.STOPBITS_ONE, # 停止位
                 timeout=1                 # 读取超时时间
             )
     ​
             if ser.is_open:
                 print(f"成功打开串口: {ser.port}")
                 try:
                     while True:
                         # 检查接收缓冲区是否有数据
                         if ser.in_waiting > 0:
                             # 读取所有可用数据
                             received_data = ser.read(ser.in_waiting)
                             
                             # 打印原始字节数据和解码后的文本
                             print(f"接收到原始数据: {received_data}")
                             try:
                                 decoded_data = received_data.decode('utf-8').strip()
                                 print(f"解码后文本: {decoded_data}")
                             except UnicodeDecodeError:
                                 print("接收到非文本数据")
                             
                             # 将接收到的数据原样返回
                             ser.write(received_data)
                             print("已回传数据")
     ​
                         # 短暂休眠降低CPU占用
                         time.sleep(0.01)
     ​
                 except KeyboardInterrupt:
                     print("\n用户中断，关闭串口")
                 
                 except serial.SerialException as e:
                     print(f"串口通信错误: {e}")
                 
                 finally:
                     if ser.is_open:
                         ser.close()
                         print("串口已关闭")
             else:
                 print("无法打开串口")
         
         except serial.SerialException as e:
             print(f"串口操作失败: {e}")
         
         except Exception as e:
             print(f"发生未知错误: {e}")
     ​
     if __name__ == "__main__":
         serial_communication()

注意需要先将USB转串口连接开发板和电脑,具体连接引脚根据开发板而定。

![](https://i-blog.csdnimg.cn/direct/99ed8d0d6f214e0199871ed6e1ea576e.jpeg)

然后运行该代码，运行命令为：
    
    
     python3 代码路径

例如我的为：
    
    
     python3 mypython/python_code/serial_test.py

如果遇到提示serial未安装的报错，

![](https://i-blog.csdnimg.cn/direct/4ae05359ef4f495cb3efc9dd905ea828.png)

则可以安装一下： 当然还是建议创建一个虚拟环境来安装
    
    
     pip install pyserial

![](https://i-blog.csdnimg.cn/direct/4785a235fa2e438cb437294963b597de.png)

此时再次执行该python脚本

![](https://i-blog.csdnimg.cn/direct/4a9b89ccbdbd474f95b3fe76af7317a0.png)

此时，我们打开对应的串口助手：

![](https://i-blog.csdnimg.cn/direct/86ead3d4cccf4653ba7332a5a597eeba.png)

串口的配置如截图，当然如果需要更改可到代码中进行修改。

现在我们给开发板发送一个helloworld进行测试：

![](https://i-blog.csdnimg.cn/direct/638ad5a602d248df9062a304d1717a1e.png)

可以看到，开发板给了相同的回复

并且在终端正确的输出了日志：

![](https://i-blog.csdnimg.cn/direct/4e013b3eb5a44aa285c0a3f701abf925.png)

测试完成

按Ctrl+C终止代码运行

![](https://i-blog.csdnimg.cn/direct/bcbc6c45b193405a9d8ef7c0f7c926d2.png)

## **Ros2串口测试**

Ros2中我准备了如下节点：

topic_serial_pub:串口发布者,该节点通过开启串口通讯 1.如若接收到串口，则将串口数据发送至·serial_data·话题 2.如果监听到·serial_send·话题数据，则将数据发送至串口

topic_serial_sub:串口接收测试节点 1.监听·serial_data·话题，如果监听到则将数据输出到控制台。

topic_serial_sendtest:串口发送测试节点| 1.定时将字符串发送至·serial_send·话题。

### **源码拷贝**

下面是各节点源码：

topic_serial_pub
    
    
     #!/usr/bin/env python3
     # -*- coding: utf-8 -*-
     ​
     import rclpy
     from rclpy.node import Node
     from std_msgs.msg import String
     import serial
     import serial.tools.list_ports
     import threading
     import time
     ​
     class SerialPublisher(Node):
         def __init__(self, name):
             super().__init__(name)
     ​
             # 创建发布者和订阅者
             self.publisher_ = self.create_publisher(String, 'serial_data', 10)
             self.subscription = self.create_subscription(
                 String,
                 'serial_send',
                 self.send_serial_callback,
                 10)
     ​
             # 初始化串口
             self.serial_port = None
             self.init_serial('/dev/ttyS0', 115200)  # 根据实际设备修改
     ​
             # 启动串口读取线程
             if self.serial_port and self.serial_port.is_open:
                 self.read_thread = threading.Thread(target=self.read_serial_async)
                 self.read_thread.daemon = True
                 self.read_thread.start()
     ​
         def init_serial(self, port, baudrate):
             """初始化串口连接"""
             try:
                 self.serial_port = serial.Serial(
                     port=port,
                     baudrate=baudrate,
                     bytesize=serial.EIGHTBITS,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     timeout=0.01
                 )
                 if self.serial_port.is_open:
                     self.get_logger().info(f"成功打开串口 {port}")
             except Exception as e:
                 self.get_logger().error(f"打开串口失败: {str(e)}")
     ​
         def read_serial_async(self):
             """在单独线程中读取串口数据"""
             while rclpy.ok() and self.serial_port and self.serial_port.is_open:
                 try:
                     # 检查接收缓冲区是否有数据
                     if self.serial_port.in_waiting > 0:
                         time.sleep(0.1)  # 短暂休眠确保数据完整接收
                         # 读取所有可用数据
                         data = self.serial_port.read(self.serial_port.in_waiting)
                         if data:
                             # self.get_logger().info(f"接收到原始数据: {data}")
                             try:
                                 # 使用 UTF-16 解码
                                 decoded_data = data.decode('utf-16').strip()
                                 self.data_received_callback(decoded_data)
                             except UnicodeDecodeError:
                                 self.get_logger().warn("接收到非UTF-16格式数据")
                 except Exception as e:
                     self.get_logger().error(f"串口读取错误: {str(e)}")
     ​
         def data_received_callback(self, data):
             """串口数据接收回调函数"""
             msg = String()
             msg.data = data
             self.publisher_.publish(msg)
             self.get_logger().info(f"发布数据: {data}")
     ​
         def send_serial_callback(self, msg):
             """话题数据接收回调函数"""
             if self.serial_port and self.serial_port.is_open:
                 try:
                     # 添加换行符保证数据完整性
                     send_data = msg.data + '\n'
                     # 使用 UTF-16 编码发送数据
                     self.serial_port.write(send_data.encode('utf-8'))
                     self.get_logger().info(f"发送数据: {msg.data}")
                 except Exception as e:
                     self.get_logger().error(f"串口发送失败: {str(e)}")
             else:
                 self.get_logger().warn("尝试发送数据时串口未打开")
     ​
         def destroy_node(self):
             """节点销毁时关闭串口"""
             if self.serial_port and self.serial_port.is_open:
                 self.serial_port.close()
                 self.get_logger().info("串口已关闭")
             super().destroy_node()
     ​
     def main(args=None):
         rclpy.init(args=args)
         node = SerialPublisher("serial_publisher")
         try:
             rclpy.spin(node)
         except KeyboardInterrupt:
             pass
         finally:
             node.destroy_node()
             rclpy.shutdown()
     ​
     if __name__ == "__main__":
         main()

topic_serial_sub
    
    
     #!/usr/bin/env python3
     # -*- coding: utf-8 -*-
     ​
     ​
     ​
     import rclpy                                     # ROS2 Python接口库
     from rclpy.node   import Node                    # ROS2 节点类
     from std_msgs.msg import String                  # ROS2标准定义的String消息
     ​
     """
     创建一个订阅者节点
     """
     class SubscriberNode(Node):
         
         def __init__(self, name):
             super().__init__(name)                                    # ROS2节点父类初始化
             self.sub = self.create_subscription(\
                 String, "serial_data", self.listener_callback, 10)        # 创建订阅者对象（消息类型、话题名、订阅者回调函数、队列长度）
     ​
         def listener_callback(self, msg):                             # 创建回调函数，执行收到话题消息后对数据的处理
             self.get_logger().info('I heard: "%s"' % msg.data)        # 输出日志信息，提示订阅收到的话题消息
             
     def main(args=None):                                 # ROS2节点主入口main函数
         rclpy.init(args=args)                            # ROS2 Python接口初始化
         node = SubscriberNode("topic_serial_sub")    # 创建ROS2节点对象并进行初始化
         rclpy.spin(node)                                 # 循环等待ROS2退出
         node.destroy_node()                              # 销毁节点对象
         rclpy.shutdown()                                 # 关闭ROS2 Python接口
     ​

topic_serial_sendtest
    
    
     #!/usr/bin/env python3
     # -*- coding: utf-8 -*-
     ​
     ​
     import rclpy                                     # ROS2 Python接口库
     from rclpy.node import Node                      # ROS2 节点类
     from std_msgs.msg import String                  # 字符串消息类型
     ​
     """
     创建一个发布者节点
     """
     class PublisherNode(Node):
         
         def __init__(self, name):
             super().__init__(name)                                    # ROS2节点父类初始化
             self.pub = self.create_publisher(String, "serial_send", 10)   # 创建发布者对象（消息类型、话题名、队列长度）
             self.timer = self.create_timer(0.5, self.timer_callback)  # 创建一个定时器（单位为秒的周期，定时执行的回调函数）
             self.num = 0
             
         def timer_callback(self):                                     # 创建定时器周期执行的回调函数
             msg = String()                                            # 创建一个String类型的消息对象
             msg.data = f'hello im3588 test{self.num}'                                  # 填充消息对象中的消息数据
             self.num += 1
             self.pub.publish(msg)                                     # 发布话题消息
             self.get_logger().info('Publishing: "%s"' % msg.data)     # 输出日志信息，提示已经完成话题发布
             
     def main(args=None):                                 # ROS2节点主入口main函数
         rclpy.init(args=args)                            # ROS2 Python接口初始化
         node = PublisherNode("topic_serial_sendtest")     # 创建ROS2节点对象并进行初始化
         rclpy.spin(node)                                 # 循环等待ROS2退出
         node.destroy_node()                              # 销毁节点对象
         rclpy.shutdown()                                 # 关闭ROS2 Python接口
     ​

将其放入到你的功能包里面，并且在setup.py里进行配置：
    
    
     entry_points={
         'console_scripts': [
             'topic_serial_pub        = main_package.topic_serial_pub:main',
             'topic_serial_sub        = main_package.topic_serial_sub:main',
             'topic_serial_sendtest   = main_package.topic_serial_sendtest:main',
         ],

接下来，编译功能包
    
    
     colcon build

![](https://i-blog.csdnimg.cn/direct/be8919b681664ab786cca6ffc5073b64.png)

### **ROS2串口发送测试**

首先打开两个终端，将终端进入工作空间内：

注意：下面的操作是两个终端都需要进行的操作：

注意：下面的操作是两个终端都需要进行的操作：

注意：下面的操作是两个终端都需要进行的操作：

例如我的为：
    
    
     cd ProjectTrain/

然后，配置环境变量
    
    
     source install/setup.bash

![](https://i-blog.csdnimg.cn/direct/08aedafc4e32495b8c750cecf266b921.png)

接下来就可以开始开启Ros节点了：

终端1执行：
    
    
     ros2 run main_package topic_serial_pub

终端2执行：
    
    
     ros2 run main_package topic_serial_sendtest

此时，就可以开始观察现象了： 终端1现象:

![](https://i-blog.csdnimg.cn/direct/3c083677a8434c4da6649a24521eecb2.png)

终端2现象：

![](https://i-blog.csdnimg.cn/direct/7d24e8698605445f908a751478227b98.png)

电脑串口助手现象：

![](https://i-blog.csdnimg.cn/direct/14e77108b17c454387a2f937d9f63fd7.png)

此时，ROS2成功将串口发送。

在实际开发中，如若有需要通过串口发送出去给下位机等指令时，只需在`serial_send`话题发送数据即可。

### **ROS2串口接收测试**

首先打开两个终端，将终端进入工作空间内：

注意：下面的操作是两个终端都需要进行的操作：

注意：下面的操作是两个终端都需要进行的操作：

注意：下面的操作是两个终端都需要进行的操作：

例如我的为：
    
    
     cd ProjectTrain/

然后，配置环境变量
    
    
     source install/setup.bash

![](https://i-blog.csdnimg.cn/direct/b0c570b5f9464362b7da852d56770714.png)

接下来就可以开始开启Ros节点了：

终端1执行：
    
    
     ros2 run main_package topic_serial_pub

终端2执行：
    
    
     ros2 run main_package topic_serial_sendsub

此时，就可以开始观察现象了：

我们在串口助手里依次发送数据

![](https://i-blog.csdnimg.cn/direct/60a00bbd22dc484fa912b7a97eb7c240.png)

终端1现象：

![](https://i-blog.csdnimg.cn/direct/165c321ff3824c1d92fd7831185044a3.png)

终端2现象：

![](https://i-blog.csdnimg.cn/direct/c435cb9cc0684fa49471a976bc2257e8.png)

此时，ROS2成功接收到串口。

在实际开发中，如若有需要通过串口读取下位机数据时，只需监听`serial_data`即可。

