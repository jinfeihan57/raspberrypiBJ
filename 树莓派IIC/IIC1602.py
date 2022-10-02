import pigpio
import time

class I2c1602Display():
    '''I2C 1602液晶显示器驱动'''
    def __init__(self, pi, blen = 1, i2cBus = 1, addr = 0x27):
        self.pi = pi
        self._addr = addr
        self._blen = blen
        self._handle = pi.i2c_open(i2cBus, self._addr)
        print(self._handle)
        try:
            self.SendCommand(0x33) # 必须先初始化为8行模式   110011 Initialise
            time.sleep(0.005)
            self.SendCommand(0x32) # 然后初始化为4行模式   110010 Initialise
            time.sleep(0.005)
            self.SendCommand(0x28) # 4位总线，双行显示，显示5×8的点阵字符。
            time.sleep(0.005)
            self.SendCommand(0x0C) # 打开显示屏，不显示光标，光标所在位置的字符不闪烁
            time.sleep(0.005)
            self.SendCommand(0x01) # 清屏幕指令，将以前的显示内容清除
            time.sleep(0.005)
            self.SendCommand(0x06) # 设置光标和显示模式，写入新数据后光标右移，显示不移动
        except Exception as e:
            print(e)
            exit()
        else:
            print('i2c init success!')

    def __del__(self):
        pi.i2c_close(self._handle)
        print('close 1602')
    
    def WriteByte(self, bData):
        temp = bData
        if self._blen == 1:
            temp |= 0x08  #0x08=0000 1000，表开背光
        else:
            temp &= 0xF7  #0xF7=1111 0111，表关闭背光
        pi.i2c_write_byte(self._handle, temp)
    
    def SendCommand(self, cmd):
        # Send bit7-4 firstly
        buf = cmd & 0xF0   #与运算，取高四位数值
        #由于4位总线的接线是接到P0口的高四位，传送高四位不用改
        buf |= 0x04    #buf |= 0x04等价于buf = buf | 0x04(按位或)0x04=0000 0100
        # RS = 0, RW = 0, EN = 1 低四位为控制管脚
        self.WriteByte(buf)  #高4位加控制写入
        time.sleep(0.002)
        buf &= 0xFB    #buf &= 0xFB等价于buf = buf & 0xFB(按位与)0xFB=1111 1011
        # Make EN = 0，EN从1——>0，下降沿，确认写入
        self.WriteByte(buf)

        # Send bit3-0 secondly
        buf = (cmd & 0x0F) << 4  #与运算，取低四位数值，
        #由于4位总线的接线是接到P0口的高四位，所以要再左移4位
        buf |= 0x04               
        # RS = 0, RW = 0, EN = 1 写入命令
        self.WriteByte(buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.WriteByte(buf)

    def SendByte(self, byte):
        # Send bit7-4 firstly
        buf = byte & 0xF0
        buf |= 0x05               # RS = 1, RW = 0, EN = 1 写入数据
        self.WriteByte(buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.WriteByte(buf)

        # Send bit3-0 secondly
        buf = (byte & 0x0F) << 4
        buf |= 0x05               # RS = 1, RW = 0, EN = 1 写入数据
        self.WriteByte(buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.WriteByte(buf)

    def Clear(self):
        self.SendCommand(0x01)

    def DisPlay(self, x, y, str):
        if x < 0:   #LCD1602只有16列显示，2行显示，小于第0列的数据要做修正
            x = 0
        if x > 15:  #LCD1602只有16列显示，2行显示，大于第15列的数据要做修正
            x = 15
        if y <0:    #LCD1602只有16列显示，2行显示，小于第0行的数据要做修正
            y = 0
        if y > 1:   #LCD1602只有16列显示，2行显示，大于第1行的数据要做修正
            y = 1

        # 移动光标
        coordinate = 0x80 + 0x40 * y + x
        #第一行第一位的地址为0x00，加上D7恒为1，所以第一行第一位的地址为0x80
        #第二行第一位是0x40，加上D7恒为1，所以第二行第一位的地址为0x80加上0x40，最后为0xC0
        self.SendCommand(coordinate)       #设置显示位置

        for chr in str:
            #ord()函数以一个字符（长度为1的字符串）作为参数，
            #返回对应的 ASCII 数值，或者 Unicode 数值
            self.SendByte(ord(chr))  #发送显示内容
    
    def MoveLeft(self):
        self.SendCommand(0x18)
  
    def MoveRight(self):
        self.SendCommand(0x1C)

if __name__ == '__main__':
    pi = pigpio.pi()
    if not pi.connected:
        print("pigpio connect failed.")
        exit()
    display = I2c1602Display(pi)
    # 第二个参数1表示打开LCD背光，若是0则关闭背光
    display.DisPlay(3, 0, 'Hello')  #3，0参数指显示的起始位置为第3列，第0行
    display.DisPlay(3, 1, 'pigpio i2c!') #3，1参数指显示的起始位置为第3列，第1行
    i = 0
    while i < 40: # 1602有40个位的缓存，朝一个y方向移动40次。就会回到原点
        time.sleep(1)
        display.MoveLeft()
        i += 1
    i = 0
    while i < 40:
        time.sleep(1)
        display.MoveRight()
        i += 1

    display.Clear()
    del display
