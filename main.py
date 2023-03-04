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

# Object to use helper methods
helper_obj = helper()

# Build an AHT10 object
temp_sensor = AHT10(i2c)

# Connects to wifi and synchronizes device time
sta_if, rtc = helper_obj.self_calibrate('', '', 'New_York')

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
    print(temp_sensor.temperature())
    current_time = helper_obj.get_time_stamp()
    temp = temp_sensor.temperature()
    humidity = temp_sensor.relative_humidity()
    temp_package = ujson.dumps({'timestamp': current_time, 'temp': temp})
    humidity_package = ujson.dumps({'timestamp': current_time, 'humidity': humidity})
    
    if not sta_if.isconnected():
        print('Wifi got disconnected. Attempting to reconnect.')
        helper_obj.wifi_connect('', '')
    
    res_humidity = None
    try:
        res_humidity = urequests.post('https://codenextchat-1ff54.firebaseio.com/sensor_data/aht10/temperature.json', data=temp_package)
    except:
        print('Unable to connect to database.')
            
    finally:
        if res_humidity:
            res_humidity.close()
    
    res_temp = None
    try:
        res_temp = urequests.post('https://codenextchat-1ff54.firebaseio.com/sensor_data/aht10/humidity.json', data=humidity_package)
    except:
            print('Unable to connect to database.')
    finally:
        if res_temp:
            res_temp.close()
    sleep_ms(10000)
    print(current_time)
