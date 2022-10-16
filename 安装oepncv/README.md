## 安装opencv

树莓派4B bullseye 已经更换清华源

### 不知道是否必须，但是我做了的步骤

```
sudo raspi-config
# 选择Advanced Options进入，然后选择Expand Filesystem，确定后选择Finish，重启。
sudo apt-get install aptitude # 这一步应该是没有意义的
```

## 必须要做的

建议大家从这一步开始，不行在回到上面的步骤

```
sudo pip3 install opencv-python
```

## 验证opencv

```
pi@raspberrypi:~ $ python
Python 3.9.2 (default, Feb 28 2021, 17:03:44)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>> cv2.__version__
'4.6.0'
>>> exit()
pi@raspberrypi:~ $
```

## 优化opencv

此时opencv虽然能用，但是可能存在摄像头视频延时高，有卡顿等问题。

mobaxterm通过ssh链接树莓派，可以显示opencv的show。因此采用此方法或者vnc链接树莓派时，如果发现摄像头视频卡顿，请先把电脑和树莓派都采用有线的方式接入网络。（wifi 极大可能造成树莓派摄像头视频卡顿）

解决方案：

```
#安装libv4l-dev库
sudo apt-get install libv4l-dev
#安装 opencv-contrib-python
pip install opencv-contrib-python
```

## cv2验证

```
python opencv2camera.py
```

