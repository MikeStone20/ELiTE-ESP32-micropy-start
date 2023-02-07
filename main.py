from helper import helper
from time import sleep_ms
import ujson, urequests

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
