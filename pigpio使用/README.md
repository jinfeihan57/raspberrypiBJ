# pigpio 使用

关于树莓派的GPIO使用，网上有大量资料都过于老旧。

pigpio是一个较为新的树莓派gpio控制库，但是这个库的使用资料都比较简单，或者上来就教大家pwm波的使用。因此我想再此做一个基础系统的pigpio库的使用方法。

文档主要以python语言为主做pigpio的介绍媒介。

## pigpio的特性

- hardware timed sampling and time-stamping of GPIO 0-31 every 5 us
- hardware timed PWM on all of GPIO 0-31
- hardware timed servo pulses on all of GPIO 0-31
- callbacks on GPIO 0-31 level change (time accurate to a few us)
- notifications via pipe on GPIO 0-31 level change
- callbacks at timed intervals
- reading/writing all of the GPIO in a bank (0-31, 32-53) as a single operation
- GPIO reading, writing, modes, and internal pulls
- socket and pipe interfaces for the bulk of the functionality
- waveforms to generate GPIO level changes (time accurate to a few us)
- software serial links using any user GPIO
- rudimentary permission control through the socket and pipe interfaces
- creating and running scripts on the pigpio daemon
- 支持远程访问，默认端口 8888

## pigpio的安装

采用源码安装（命令行安装的方式自行百度）

```
git clone https://github.com/joan2937/pigpio.git -b v79 #我做整理的时候最新版本是这个，后续有新的建议用最新的
cd pigpio
make
sudo make install
# test
sudo x_pigpio
sudo pigpiod #启动pigpio后台服务，否则后续的测试会失败
./x_pigpio.py
./x_pigs
./x_pipe
```

使用pigpio的时候，需要保证后台进程pigpiod是在运行的。

```
sudo systemctl enable pigpiod
```

## 指导文档

本文把[官方指导文档](http://abyz.me.uk/rpi/pigpio/index.html)作为主体，一步步深入学习pigpio的使用方法。

## 点亮LED（控制GPIO输出高低电平）

点亮led就和，hello world一样重要和基础。所以我们的学习由点亮LED灯开始。

由于是第一次使用我会详细介绍每一行，

```
pi@raspberrypi:~/gpio/pigpio-79 $ python
Python 3.9.2 (default, Feb 28 2021, 17:03:44)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pigpio #导入 pigpio 模块
>>> pi = pigpio.pi() #启动客户端链接pigpiod 我这里使用的默认参数，也可以指定pigpio.pi("hostname", port)
>>> pi.connected #判断客户端链接是否成功
True
>>> led_ctl = 17 #设置led的控制管脚为 gpio17 也就是排针的11阵脚，并且由于我手上没有led灯，我是用的是激光。控制原理一样的
>>> pi.set_mode(led_ctl, pigpio.OUTPUT)#设置led_ctl为输出属性
0
>>> pi.write(led_ctl, 1)#高电平输出
0
>>> pi.write(led_ctl, 0)#低电平输出
0
>>> pi.stop()
>>> exit()
```

![](./demo.jpg)

激光头侧，**红色为底线，黑色为正极**，紫色为控制线。

## 读取按键输入（读取GPIO的电平状态）

这里因为没有复位按键可以直接采用管脚接地和接高电平测试。

```
pi@raspberrypi:~/gpio/pigpio-79 $ python
Python 3.9.2 (default, Feb 28 2021, 17:03:44)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pigpio
>>> pi = pigpio.pi()
>>> pi.connected
True
>>> bt_ctl = 17 #依然是gpio17
>>> pi.set_mode(bt_ctl, pigpio.INPUT) #设置属性为输入
0
>>> pi.set_pull_up_down(bt_ctl, pigpio.PUD_DOWN) #设置拉低属性（也是默认的属性）也可以设置拉高
0
>>> pi.read(bt_ctl)
0
>>> pi.read(bt_ctl)
1
>>> pi.read(bt_ctl)
0
>>> pi.read(bt_ctl)
1
>>> pi.stop()
>>> exit()
```

## 串口通信

pigpio支持硬件串口通信，需要提前打开树莓派的串口。打开方式参见[树莓派串口](https://github.com/jinfeihan57/raspberrypiBJ/tree/main/%E6%A0%91%E8%8E%93%E6%B4%BE%E4%B8%B2%E5%8F%A3)。pigpio实现了硬件的串口通信，但是硬件的串口通信是有数量（在树莓派4B之前的版本，树莓派3和3+上都是稀缺资源）的并且要求使用指定的 io 口。因此pigpio同时实现了软件串口（bb_serial_read_open）通信的读，**仅支持读**。推荐使用硬件的串口，支持更多的设置，可判断待读信息的大小。

串口2自通信接线图

![](./串口2自通信.jpg)

```
pi@raspberrypi:~ $ python
Python 3.9.2 (default, Feb 28 2021, 17:03:44)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pigpio
>>> pi = pigpio.pi()
>>> pi.connected
True
>>> u2 = pi.serial_open("/dev/ttyAMA1", 19200)
>>> pi.serial_write(u2, b"hello u2")
0
>>> (c, d) = pi.serial_read(u2, 100)
>>> print(c)
8
>>> print(d)
bytearray(b'hello u2')
>>> pi.serial_write(u2, "hello u2")
0
>>> (c, d) = pi.serial_read(u2, 100)
>>> print(c)
8
>>> print(d)
bytearray(b'hello u2')
>>> pi.serial_write(u2, "hello u2")
0
>>> pi.serial_data_available(u2)
8
>>> (c, d) = pi.serial_read(u2, 8)
>>> print(d)
bytearray(b'hello u2')
>>> pi.serial_write_byte(u2, 96)
0
>>> pi.serial_data_available(u2)
1
>>> (c, d) = pi.serial_read(u2, 1)
>>> print(c)
1
>>> print(d)
bytearray(b'`')
>>> pi.serial_close(u2)
0
>>> pi.stop()
>>> exit()
pi@raspberrypi:~ $
```

采用模拟串口接收功能实现任意gpio的串口读功能，读出的结果被存放在一个环形缓存中（具体缓存大小待测）。

串口2发送信息，gpio26接受信息接线图

![](./串口2tx_io26rx.jpg)

```
pi@raspberrypi:~ $ python
Python 3.9.2 (default, Feb 28 2021, 17:03:44)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pigpio
>>> pi = pigpio.pi()
>>> pi.connected
True
>>> u2 = pi.serial_open("/dev/ttyAMA1", 19200)
>>> rxio = 26
>>> pi.bb_serial_read_open(rxio, 19200)
0
>>> pi.serial_write(u2, b'hello gpio26')
0
>>> (c, d) = pi.bb_serial_read(rxio)
>>> print(c)
12
>>> print(d)
bytearray(b'hello gpio26')
>>> pi.serial_write_byte(u2, 0)
0
>>> (c, d) = pi.bb_serial_read(rxio)
>>> print(c)
1
>>> print(d)
bytearray(b'\x00')
>>> pi.stop()
>>> exit()
pi@raspberrypi:~ $
```

