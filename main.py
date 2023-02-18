from helper import helper
from time import sleep_ms
from machine import I2C, Pin
import ujson, urequests
from ahtx0 import AHT10
'''
I2C object that allows controls communication between micro controller and sensors.
27, 26 are pins on your esp32 board. Feel free to change to another pin.
freq depends on the sensor you are deling with. 40K is a safe ballpark for most sensors.
'''
#I2C object to communicate with sensors
i2c = I2C(0, scl=Pin(27), sda=Pin(26), freq=40000)
temp_sensor = AHT10(i2c)
# Object to use helper methods
helper_obj = helper()

# Connects to wifi and synchronizes device time
sta_if, rtc = helper_obj.self_calibrate('wifi-name', 'wifi-password', 'New_York')

# Checking if wifi connection succeeded
if sta_if:
    print(sta_if.ifconfig())

# Checking if device time is synced
if rtc:
    print(rtc.datetime())
    print(helper_obj.get_time_stamp())

# Add your setup below

# data collection + data storage should go in while loop
while True:
    print('Hello world')
    sleep_ms(1000)
    print(temp_sensor.temperature())
