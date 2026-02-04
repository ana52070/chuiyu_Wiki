---
title: Unity连接Python(Unity连接其它所有的通讯方案)
date: 最新推荐文章于 2025-05-14
tags: [CSDN搬运]
---

# Unity连接Python(Unity连接其它所有的通讯方案)

> 原文链接：[Unity连接Python(Unity连接其它所有的通讯方案)](https://blog.csdn.net/chui_yu666/article/details/145599927)

## 连接思路

Unity通过Socket通信连接本地Python

如何做到Unity连接其它的所有呢？

有了Unity连接本地Python这一方案的话，基于Python强大的胶水语言、网上资料超多的特点，就可以再次用Python去连接更多更多的东西，从而使得Unity可以连接近乎一切你想到的能用Python连接的东西。

下面演示Unity通过Python间接连接阿里云(包含了Unity连接Python的内容)：

因为数字孪生项目需要，楼主最近在捣鼓Unity连接阿里云MQTT服务器时，发现网上的这方面资料很少很少，能找到的比较少的也都只是Unity连接自己的MQTT服务器，而阿里云的服务器往往还需要验证签名什么的。这使得直连这个方案很艰难。

因此楼主毅然决然的选择了Unity通过Socket通信连接本地Python，再用Python连接阿里云服务器的这个间接连接的方案。

下面是思路图

![](https://i-blog.csdnimg.cn/direct/4c79385b561e4e3a88e20d7935ff331b.png)

这样，Unity就可以成功的连接到阿里云服务器了。

下面是连接的相关代码，分为三部分：

1.Python单独连接Unity(Socket)

2.Python单独连接阿里云服务器(MQTT)

3.Unity和阿里云服务器通过Python实现间接连接。

## 1.Python单独连接Unity

### 1.Python部分：link_Unity.py
    
    
    import socket
    import json
    import threading
    from dataclasses import dataclass
    
    # 定义服务器的IP地址和端口号
    host, port = "127.0.0.1", 25001
    
    
    # 定义NPCInfo结构体
    @dataclass
    class NPCInfo:
        temp: float
        humi: int
        bee_state: int
        rader: int
        LED_Lab1: int
        fire: int
        MQ2: int
        voice: int
        check_in: int
        mqtt_state: int
        check_off: int
    
    
    # 处理客户端连接的函数
    def handle_client(client_socket):
        send_thread = threading.Thread(target=send_npc_info, args=(client_socket,))
        receive_thread = threading.Thread(target=receive_npc_info, args=(client_socket,))
    
        send_thread.start()
        receive_thread.start()
    
    
    # 将NPCInfo实例转为JSON格式并发送给客户端
    def send_npc_info(client_socket):
        npc_info = NPCInfo(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)  # 示例数据
        while True:
            user_input = input("输入P发送信息")
            if user_input.lower() == 'p':
                json_data = json.dumps(npc_info.__dict__)  # 转换为JSON格式
                json_data += '\n'  # 添加换行符作为分隔符
                client_socket.sendall(json_data.encode())  # 发送JSON数据
    
    
    # 从客户端接收JSON数据并解码为NPCInfo实例
    def receive_npc_info(client_socket):
        while True:
            received_data = client_socket.recv(1024).decode()  # 接收数据并解码为字符串
            if not received_data:
                break
            # 解码JSON数据为NPCInfo实例
            npc_data = json.loads(received_data)
            npc_info = NPCInfo(**npc_data)
            print("收到Unity信息:", npc_info)
    
    
    # 创建TCP socket并绑定IP地址和端口号
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    
    print(f"正在监听 {host}:{port}")
    
    while True:
        # 等待客户端连接
        client_socket, _ = server_socket.accept()
        print(f"成功连接到客户端 {_}")
    
        # 启动一个线程来处理客户端连接
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

### 2.Unity部分：link_Python.cs

参考代码里，每次需要先运行Python代码才能运行Unity代码，不然就无法正常连接。因此楼主基于资料里多添加了服务器断连重连部分，不需要再考虑先后启动了。
    
    
    using System.IO;
    using System.Net.Sockets;
    using System.Text;
    using UnityEngine;
    
    public class UnityClient : MonoBehaviour
    {
        // 定义NPCInfo结构体
        public struct NPCInfo
        {
            public double temp;
            public int humi;
            public int voice;
            public int MQ2;
            public int check_in;
            public int rader;
            public int check_off;
            public int LED_Lab1;
            public int mqtt_state;
            public int bee_state;
            public int fire;
        }
    
        public string serverIP = "127.0.0.1";
        public int serverPort = 25001;
    
        public NPCInfo MyNPCInfo = new NPCInfo
        {
            temp = 0.0,
            humi = 0,
            voice = 0,
            MQ2 = 0,
            check_in = 0,
            rader = 0,
            check_off = 0,
            LED_Lab1 = 1,
            mqtt_state = 0,
            bee_state = 2,
            fire = 0,
        };
    
        private TcpClient client;
        private NetworkStream stream;
    
        private float reconnectAttemptTime = 0f; // 记录重连尝试的时间
        private float reconnectInterval = 3f; // 设置重连提示的间隔时间
    
        void Start()
        {
            ConnectToServer();
        }
    
        void ConnectToServer()
        {
            if (client != null && client.Connected) return;
    
            try
            {
                client = new TcpClient(serverIP, serverPort);
                stream = client.GetStream();
                Debug.Log("成功连接到服务器");
            }
            catch (SocketException)
            {
                Debug.LogError("连接服务器失败，正在重试...");
                Invoke("Reconnect", 5f); // 等待5秒后重试连接
            }
        }
    
        void Reconnect()
        {
            ConnectToServer();
        }
    
        void Update()
        {
            if (client == null || !client.Connected)
            {
                reconnectAttemptTime += Time.deltaTime; // 增加重连尝试时间
    
                if (reconnectAttemptTime >= reconnectInterval)
                {
                    Debug.LogWarning("未连接到服务器，尝试重连...");
                    reconnectAttemptTime = 0f; // 重置计时器
                    HandleDisconnection();
                }
                return;
            }
    
            if (stream.DataAvailable)
            {
                ReceiveMessage();
            }
    
            if (Input.GetKeyDown(KeyCode.U))
            {
                SendMessage(MyNPCInfo);
            }
        }
    
        void SendMessage(NPCInfo npcInfo)
        {
            if (stream == null) return;
    
            try
            {
                string json = JsonUtility.ToJson(npcInfo);
                byte[] data = Encoding.UTF8.GetBytes(json);
                stream.Write(data, 0, data.Length);
            }
            catch (IOException e)
            {
                Debug.LogError("发送数据失败: " + e.Message);
                HandleDisconnection();
            }
        }
    
        void HandleDisconnection()
        {
            if (stream != null)
            {
                stream.Close();
                stream = null;
            }
            if (client != null)
            {
                client.Close();
                client = null;
            }
            Invoke("Reconnect", 5f); // 等待5秒后重试连接
        }
    
        void ReceiveMessage()
        {
            if (stream != null && stream.DataAvailable)
            {
                byte[] responseData = new byte[1024];
                int bytesRead = stream.Read(responseData, 0, responseData.Length);
                string response = Encoding.UTF8.GetString(responseData, 0, bytesRead);
                DecodeJSON(response);
            }
        }
    
        public void DecodeJSON(string json)
        {
            NPCInfo npcInfo = JsonUtility.FromJson<NPCInfo>(json);
            MyNPCInfo = npcInfo;
    
            Debug.Log("temp：" + MyNPCInfo.temp + "，humi：" + MyNPCInfo.humi + "，voice：" + MyNPCInfo.voice +
                      "，MQ2：" + MyNPCInfo.MQ2 + "，check_in：" + MyNPCInfo.check_in + "，check_off：" + MyNPCInfo.check_off +
                      "，rader：" + MyNPCInfo.rader + "，LED_Lab1：" + MyNPCInfo.LED_Lab1 +
                      "，mqtt_state：" + MyNPCInfo.mqtt_state + "，bee_state：" + MyNPCInfo.bee_state + "，fire：" + MyNPCInfo.fire);
        }
    
        void OnDestroy()
        {
            HandleDisconnection();
        }
    }
    

## 2.Python单独连接阿里云服务器

运行之前，还请先下载TLS证书，在这里建议直接去阿里云官网下载

[如何调用Python的Paho MQTT类库将设备接入物联网平台_物联网平台(IoT)-阿里云帮助中心 (aliyun.com)](<https://help.aliyun.com/zh/iot/use-cases/use-the-paho-mqtt-library-for-python-to-connect-a-device-to-iot-platform?spm=a2c4g.11186623.0.0.8cb042c0EsSmG3> "如何调用Python的Paho MQTT类库将设备接入物联网平台_物联网平台\(IoT\)-阿里云帮助中心 \(aliyun.com\)")

该部分有两个py代码，请分别修改两个py代码中的相关变量

### iot.py

请修改以下数据：

productKey、deviceName、deviceSecret

其它代码请根据自己的定义自己修改。
    
    
    import json
    import time
    import paho.mqtt.client as mqtt
    from MqttSign import AuthIfo
    
    # 设置设备信息，包括产品密钥、设备名称和设备密钥
    productKey = ""
    deviceName = ""
    deviceSecret = ""
    
    # 设置时间戳、客户端ID、订阅主题和发布主题
    timeStamp = str(int(round(time.time() * 1000)))
    clientId = "192.168.****"
    subTopic = f"/{productKey}/{deviceName}/user/get"
    
    # 设置主机地址和端口
    host = f"{productKey}k0lrjXSIdGe.iot-as-mqtt.cn-shanghai.aliyuncs.com"
    port = 1883
    
    # 设置TLS证书和心跳时间
    tls_crt = "root.crt"
    keepAlive = 300
    
    # 全局变量，用于存储传感器值
    temp = None
    humi = None
    bee_state = None
    rader = None
    LED_Lab1 = None
    fire = None
    MQ2 = None
    voice = None
    check_in = None
    mqtt_state = None
    
    # 计算登录认证信息，并将其设置到连接选项中
    m = AuthIfo()
    m.calculate_sign_time(productKey, deviceName, deviceSecret, clientId, timeStamp)
    client = mqtt.Client(m.mqttClientId)
    client.username_pw_set(username=m.mqttUsername, password=m.mqttPassword)
    client.tls_set(tls_crt)
    
    
    def on_connect(client, userdata, flags, rc):
        # 当客户端连接到服务器时的回调函数
        if rc == 0:
            print("成功连接到阿里云物联网云")
        else:
            print(f"连接失败... 错误代码: {rc}")
    
    
    def on_message(client, userdata, msg):
        # 当客户端收到消息时的回调函数
        global temp, humi, bee_state, rader, LED_Lab1, fire, MQ2
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"收到消息 ---------- 主题: {topic}")
        print(f"收到消息 ---------- 负载: {payload}")
    
        try:
            Msg = json.loads(payload)
            items = Msg.get('items', {})
    
            # 从'items'中提取传感器值并将其赋值给全局变量
            temp = items.get('temp', {}).get('value')
            humi = items.get('humi', {}).get('value')
            voice = items.get('voice', {}).get('value')
            MQ2 = items.get('MQ2', {}).get('value')
            check_in = items.get('check_in', {}).get('value')
            rader = items.get('rader', {}).get('value')
            check_off = items.get('check_off', {}).get('value')
            LED_Lab1 = items.get('LED_Lab1', {}).get('value')
            mqtt_state = items.get('mqtt', {}).get('value')
            bee_state = items.get('bee_state', {}).get('value')
            fire = items.get('fire', {}).get('value')
    
            print(f"当前传感器数据: 温度: {temp}, 湿度: {humi}, 声音值:{voice}, 气体传感器: {MQ2}, 签到ID:{check_in}, 雷达: {rader}, 签退ID:{check_off}, 实验室LED: {LED_Lab1}, 服务器状态:{mqtt_state}, 蜂鸣器状态: {bee_state}, 火灾检测: {fire}")
    
        except json.JSONDecodeError:
            # 处理JSON解码错误
            print("JSON 解码失败。")
    
    
    def connect_mqtt():
        # 连接到MQTT服务器
        client.connect(host, port, keepAlive)
        return client
    
    
    def subscribe_topic():
        # 订阅主题
        client.subscribe(subTopic)
        print(f"订阅主题: {subTopic}")
    
    
    import json
    
    def publish_message(bee_state_value, LED_Lab1_value):
        """
        发布消息到指定的固定主题，动态设置 bee_state 和 LED_Lab1 的值。
    
        参数:
        bee_state_value (int): bee_state 的值
        LED_Lab1_value (int): LED_Lab1 的值
        """
        topic = "/sys/k0lrjXSIdGe/SmartLab-app/thing/event/property/post"
    
        # 构造固定格式的 JSON 负载，动态插入 bee_state 和 LED_Lab1 的值
        payload = {
            "id": 1726899778140,
            "params": {
                "bee_state": bee_state_value,
                "LED_Lab1": LED_Lab1_value
            },
            "version": "1.0",
            "method": "thing.event.property.post"
        }
    
        # 将字典转为 JSON 格式的字符串
        payload_str = json.dumps(payload)
    
        # 发布消息到指定主题
        result = client.publish(topic, payload_str)
        # 判断发布结果
        status = result[0]
        if status == 0:
            print(f"成功发布消息到主题 {topic}: {payload_str}")
        else:
            print(f"消息发布失败，状态码: {status}")
    
    
    # 设置连接和消息回调函数
    client.on_connect = on_connect
    client.on_message = on_message
    client = connect_mqtt()
    client.loop_start()
    time.sleep(2)
    
    # 订阅主题
    subscribe_topic()
    
    while True:
        time.sleep(1)
        # 动态发布消息
        publish_message(2, 1)
    

### MqttSign.py

请修改以下数据：

mqttClientId、mqttUsername、mqttPassword

其它代码请根据自己的定义自己修改。
    
    
    import hmac
    from hashlib import sha1
    
    class AuthIfo:
        mqttClientId = ''
        mqttUsername = ''
        mqttPassword = ''
    
        def calculate_sign_time(self, productKey, deviceName, deviceSecret, clientId, timeStamp):
            self.mqttClientId = clientId + "|securemode=2,signmethod=hmacsha1,timestamp=" + timeStamp + "|"
            self.mqttUsername = deviceName + "&" + productKey
            content = "clientId" + clientId + "deviceName" + deviceName + "productKey" + productKey + "timestamp" + timeStamp
            self.mqttPassword = hmac.new(deviceSecret.encode(), content.encode(), sha1).hexdigest()
    
        def calculate_sign(self, productKey, deviceName, deviceSecret, clientId):
            self.mqttClientId = clientId + "|securemode=2,signmethod=hmacsha1|"
            self.mqttUsername = deviceName + "&" + productKey
            content = "clientId" + clientId + "deviceName" + deviceName + "productKey" + productKey
            self.mqttPassword = hmac.new(deviceSecret.encode(), content.encode(), sha1).hexdigest()

## 3.阿里云连Unity

### 1.Python部分：iot_Unity.py

请注意：运行次代码仍然需要阿里云的驱动py文件：MqttSign.py，请去上面部分进行粘贴拷贝。
    
    
    import json
    import time
    import paho.mqtt.client as mqtt
    from MqttSign import AuthIfo
    import socket
    import threading
    from dataclasses import dataclass
    
    """
    Unity与阿里云MQTT服务器的中间通讯
    
    运行思路：
        当阿里云服务器发送数据过来时：回传给Unity
        当Unity发送数据过来时：回传给阿里云
        
        无脑转发
    
    
    """
    
    """-------------------------连接阿里云的数据配置---------------------------------"""
    # 设置设备信息，包括产品密钥、设备名称和设备密钥
    productKey = ""
    deviceName = ""
    deviceSecret = ""
    
    # 设置时间戳、客户端ID、订阅主题和发布主题
    timeStamp = str(int(round(time.time() * 1000)))
    clientId = "192.168.****"
    subTopic = f"/{productKey}/{deviceName}/user/get"
    
    # 设置主机地址和端口
    host = f"{productKey}k0lrjXSIdGe.iot-as-mqtt.cn-shanghai.aliyuncs.com"
    port = 1883
    
    # 设置TLS证书和心跳时间
    tls_crt = "root.crt"
    keepAlive = 300
    
    # 全局变量，用于存储传感器值，合并后，共用数据
    # temp = None
    # humi = None
    # bee_state = None
    # rader = None
    # LED_Lab1 = None
    # fire = None
    # MQ2 = None
    # voice = None
    # check_in = None
    # mqtt_state = None
    
    
    """-------------------------连接Unity部分的数据配置---------------------------------"""
    # 定义服务器的IP地址和端口号
    host_unity, port_unity = "127.0.0.1", 25001
    
    
    # 定义要传输的信息的结构体
    @dataclass
    class NPCInfo:
        temp: float
        humi: int
        bee_state: int
        rader: int
        LED_Lab1: int
        fire: int
        MQ2: int
        voice: int
        check_in: int
        mqtt_state: int
        check_off: int
    
    
    my_message = NPCInfo(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)  # 示例数据
    
    """-------------------------连接阿里云的函数定义---------------------------------"""
    
    
    def on_connect(client, userdata, flags, rc):
        # 当客户端连接到服务器时的回调函数
        if rc == 0:
            print("成功连接到阿里云物联网云")
        else:
            print(f"连接失败... 错误代码: {rc}")
    
    
    def on_message(client, userdata, msg):
        global my_message
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"收到消息 ---------- 主题: {topic}")
        print(f"收到消息 ---------- 负载: {payload}")
    
        try:
            Msg = json.loads(payload)
            items = Msg.get('items', {})
    
            # 从items中提取传感器值并将其赋值给my_message
            my_message.temp = float(items.get('temp', {}).get('value', 0.0)) if items.get('temp') is not None else 0.0
            my_message.humi = int(items.get('humi', {}).get('value', 0)) if items.get('humi') is not None else 0
            my_message.voice = int(items.get('voice', {}).get('value', 0)) if items.get('voice') is not None else 0
            my_message.MQ2 = int(items.get('MQ2', {}).get('value', 0)) if items.get('MQ2') is not None else 0
            my_message.check_in = int(items.get('check_in', {}).get('value', 0)) if items.get('check_in') is not None else 0
            my_message.rader = int(items.get('rader', {}).get('value', 0)) if items.get('rader') is not None else 0
            my_message.check_off = int(items.get('check_off', {}).get('value', 0)) if items.get('check_off') is not None else 0
            my_message.LED_Lab1 = int(items.get('LED_Lab1', {}).get('value', 0)) if items.get('LED_Lab1') is not None else 0
            my_message.mqtt_state = int(items.get('mqtt', {}).get('value', 0)) if items.get('mqtt') is not None else 0
            my_message.bee_state = int(items.get('bee_state', {}).get('value', 0)) if items.get('bee_state') is not None else 0
            my_message.fire = int(items.get('fire', {}).get('value', 0)) if items.get('fire') is not None else 0
    
            print(
                f"当前传感器数据: 温度: {my_message.temp}, 湿度: {my_message.humi}, 声音值: {my_message.voice}, "
                f"气体传感器: {my_message.MQ2}, 签到ID: {my_message.check_in}, 雷达: {my_message.rader}, "
                f"签退ID: {my_message.check_off}, 实验室LED: {my_message.LED_Lab1}, "
                f"服务器状态: {my_message.mqtt_state}, 蜂鸣器状态: {my_message.bee_state}, 火灾检测: {my_message.fire}"
            )
    
            # 发送至Unity
            send_npc_info(client_socket)
    
        except json.JSONDecodeError:
            print("JSON 解码失败。")
    
    def connect_mqtt():
        # 连接到MQTT服务器
        client.connect(host, port, keepAlive)
        return client
    
    
    def subscribe_topic():
        # 订阅主题
        client.subscribe(subTopic)
        print(f"订阅主题: {subTopic}")
    
    
    def publish_message(bee_state_value, LED_Lab1_value):
        """
        发布消息到指定的固定主题，动态设置 bee_state 和 LED_Lab1 的值。
    
        参数:
        bee_state_value (int): bee_state 的值
        LED_Lab1_value (int): LED_Lab1 的值
        """
        topic = "/sys/k0lrjXSIdGe/SmartLab-app/thing/event/property/post"
    
        # 构造固定格式的 JSON 负载，动态插入 bee_state 和 LED_Lab1 的值
        payload = {
            "id": 1726899778140,
            "params": {
                "bee_state": bee_state_value,
                "LED_Lab1": LED_Lab1_value
            },
            "version": "1.0",
            "method": "thing.event.property.post"
        }
    
        # 将字典转为 JSON 格式的字符串
        payload_str = json.dumps(payload)
    
        # 发布消息到指定主题
        result = client.publish(topic, payload_str)
        # 判断发布结果
        status = result[0]
        if status == 0:
            print(f"成功发布消息到主题 {topic}: {payload_str}")
        else:
            print(f"消息发布失败，状态码: {status}")
    
    
    """-------------------------连接Unity的函数定义---------------------------------"""
    
    
    # 处理客户端连接的函数
    def handle_client(client_socket):
        send_thread = threading.Thread(target=send_npc_info, args=(client_socket,))
        receive_thread = threading.Thread(target=receive_npc_info, args=(client_socket,))
    
        send_thread.start()
        receive_thread.start()
    
    
    # 将NPCInfo实例转为JSON格式并发送给客户端
    def send_npc_info(client_socket):
        global my_message
        json_data = json.dumps(my_message.__dict__)  # 转换为JSON格式
        json_data += '\n'  # 添加换行符作为分隔符
        client_socket.sendall(json_data.encode())  # 发送JSON数据
    
    
    # 从客户端接收JSON数据并解码为NPCInfo实例
    def receive_npc_info(client_socket):
        while True:
            received_data = client_socket.recv(1024).decode()  # 接收数据并解码为字符串
            if not received_data:
                break
            # 解码JSON数据为NPCInfo实例
            npc_data = json.loads(received_data)
            npc_info = NPCInfo(**npc_data)
            print("收到Unity信息:", npc_info)
            #发送数据至阿里云
            publish_message(npc_info.bee_state, npc_info.LED_Lab1)
    
    
    """-------------------------连接阿里云的初始化代码---------------------------------"""
    
    # 计算登录认证信息，并将其设置到连接选项中
    m = AuthIfo()
    m.calculate_sign_time(productKey, deviceName, deviceSecret, clientId, timeStamp)
    client = mqtt.Client(m.mqttClientId)
    client.username_pw_set(username=m.mqttUsername, password=m.mqttPassword)
    client.tls_set(tls_crt)
    
    # 设置连接和消息回调函数
    client.on_connect = on_connect
    client.on_message = on_message
    client = connect_mqtt()
    client.loop_start()
    time.sleep(2)
    
    # 订阅主题
    subscribe_topic()
    
    """-------------------------连接Unity的初始化代码---------------------------------"""
    
    # 创建TCP socket并绑定IP地址和端口号
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host_unity, port_unity))
    server_socket.listen(5)
    print(f"正在监听 {host_unity}:{port_unity}")
    
    """-------------------------共用死循环--------------------------------------------"""
    while True:
        # 等待客户端连接
        client_socket, _ = server_socket.accept()
        print(f"成功连接到客户端 {_}")
    
        # 启动一个线程来处理客户端连接
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()
    

### Unity部分：link_Python.cs
    
    
    using System.IO;
    using System.Net.Sockets;
    using System.Text;
    using UnityEngine;
    
    public class UnityClient : MonoBehaviour
    {
        // 定义NPCInfo结构体
        public struct NPCInfo
        {
            public double temp;
            public int humi;
            public int voice;
            public int MQ2;
            public int check_in;
            public int rader;
            public int check_off;
            public int LED_Lab1;
            public int mqtt_state;
            public int bee_state;
            public int fire;
        }
    
        public string serverIP = "127.0.0.1";
        public int serverPort = 25001;
    
        public NPCInfo MyNPCInfo = new NPCInfo
        {
            temp = 0.0,
            humi = 0,
            voice = 0,
            MQ2 = 0,
            check_in = 0,
            rader = 0,
            check_off = 0,
            LED_Lab1 = 1,
            mqtt_state = 0,
            bee_state = 2,
            fire = 0,
        };
    
        private TcpClient client;
        private NetworkStream stream;
    
        private float reconnectAttemptTime = 0f; // 记录重连尝试的时间
        private float reconnectInterval = 3f; // 设置重连提示的间隔时间
    
        void Start()
        {
            ConnectToServer();
        }
    
        void ConnectToServer()
        {
            if (client != null && client.Connected) return;
    
            try
            {
                client = new TcpClient(serverIP, serverPort);
                stream = client.GetStream();
                Debug.Log("成功连接到服务器");
            }
            catch (SocketException)
            {
                Debug.LogError("连接服务器失败，正在重试...");
                Invoke("Reconnect", 5f); // 等待5秒后重试连接
            }
        }
    
        void Reconnect()
        {
            ConnectToServer();
        }
    
        void Update()
        {
            if (client == null || !client.Connected)
            {
                reconnectAttemptTime += Time.deltaTime; // 增加重连尝试时间
    
                if (reconnectAttemptTime >= reconnectInterval)
                {
                    Debug.LogWarning("未连接到服务器，尝试重连...");
                    reconnectAttemptTime = 0f; // 重置计时器
                    HandleDisconnection();
                }
                return;
            }
    
            if (stream.DataAvailable)
            {
                ReceiveMessage();
            }
    
            if (Input.GetKeyDown(KeyCode.U))
            {
                SendMessage(MyNPCInfo);
            }
        }
    
        void SendMessage(NPCInfo npcInfo)
        {
            if (stream == null) return;
    
            try
            {
                string json = JsonUtility.ToJson(npcInfo);
                byte[] data = Encoding.UTF8.GetBytes(json);
                stream.Write(data, 0, data.Length);
            }
            catch (IOException e)
            {
                Debug.LogError("发送数据失败: " + e.Message);
                HandleDisconnection();
            }
        }
    
        void HandleDisconnection()
        {
            if (stream != null)
            {
                stream.Close();
                stream = null;
            }
            if (client != null)
            {
                client.Close();
                client = null;
            }
            Invoke("Reconnect", 5f); // 等待5秒后重试连接
        }
    
        void ReceiveMessage()
        {
            if (stream != null && stream.DataAvailable)
            {
                byte[] responseData = new byte[1024];
                int bytesRead = stream.Read(responseData, 0, responseData.Length);
                string response = Encoding.UTF8.GetString(responseData, 0, bytesRead);
                DecodeJSON(response);
            }
        }
    
        public void DecodeJSON(string json)
        {
            NPCInfo npcInfo = JsonUtility.FromJson<NPCInfo>(json);
            MyNPCInfo = npcInfo;
    
            Debug.Log("temp：" + MyNPCInfo.temp + "，humi：" + MyNPCInfo.humi + "，voice：" + MyNPCInfo.voice +
                      "，MQ2：" + MyNPCInfo.MQ2 + "，check_in：" + MyNPCInfo.check_in + "，check_off：" + MyNPCInfo.check_off +
                      "，rader：" + MyNPCInfo.rader + "，LED_Lab1：" + MyNPCInfo.LED_Lab1 +
                      "，mqtt_state：" + MyNPCInfo.mqtt_state + "，bee_state：" + MyNPCInfo.bee_state + "，fire：" + MyNPCInfo.fire);
        }
    
        void OnDestroy()
        {
            HandleDisconnection();
        }
    }
    

