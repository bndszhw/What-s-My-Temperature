from machine import Pin, I2C
import ssd1306

import network
import urequests
from machine import enable_irq, disable_irq, idle
import time
from machine import Pin
import machine

        
class AHT21:
    def __init__(self, sda, scl, addr=0x38):
        self.i2c = machine.I2C(sda=machine.Pin(sda), scl=machine.Pin(scl))
        self.addr = addr  # AHT21 的 I2C 地址
        self.init_sensor()

    def init_sensor(self):
        # 初始化传感器
        self.i2c.writeto(self.addr, bytearray([0xBE, 0x08, 0x00]))
        time.sleep(0.02)  # 等待传感器响应

    def read_data(self):
        # 向传感器发送测量命令
        self.i2c.writeto(self.addr, bytearray([0xAC, 0x33, 0x00]))
        time.sleep(0.08)  # 等待测量完成

        # 读取数据
        data = self.i2c.readfrom(self.addr, 6)
        if data[3] & 0x80 == 0:
            # 解析湿度数据
            humidity = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4)) * 100 / (1 << 20)
            # 解析温度数据
            temperature = (((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]) * 200 / (1 << 20) - 50

            return temperature, humidity
        else:
            return None, None

class data_handler:
    
    @staticmethod
    def aht21_get_data(aht21):
        temperature, humidity = aht21.read_data()
        return temperature, humidity


# 初始化 I2C
i2c = I2C(scl=Pin(5), sda=Pin(4))

# 初始化 OLED
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# 初始化 AHT2X
aht21 = AHT21(sda=4, scl=5, addr=0x38)

# 从传感器读取数据


# 在 OLED 上显示数据
while True:
    # 获取温湿度数据
    temperature, humidity = aht21.read_data()
    if temperature is not None and humidity is not None:
        print(f"温度: {temperature:.1f}°C, 湿度: {humidity:.1f}%")
        
        # 在 OLED 上显示数据
        oled.fill(0)  # 清屏
        oled.text("AHT21 Sensor", 0, 0)
        oled.text(f"Temp: {temperature:.1f}C", 0, 16)
        oled.text(f"Humid: {humidity:.1f}%", 0, 32)
        oled.show()
    else:
        print("读取失败，重新尝试...")

    time.sleep(2)  # 每隔 2 秒读取一次
