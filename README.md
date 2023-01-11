# ELiTE-ESP32-micropy-start
A guide to setting up esp32 with micropython and populating sensor data into database.

# Setting up Thonny

# Setting up Firebase account
Firebase is a cloud platform that has specialized tools that help developers grow and build their apps.
Sepcifically we are interested in using the [RTDB](https://en.wikipedia.org/wiki/Real-time_database) tool.

Steps:
  1. Visit https://firebase.google.com/ and sign in (you can sign up quickly using your gmail)
  2. After signing in. Click on ***Go to console*** in the top right.
  3. Webpage should redirect to homepage. Click ***Create a project*** and come up with an appropriate and unique name for your project. Click ***Continue***.
  4. Optional: Enable/Disable gooogle analytics. Click ***Continue***
  5. Expand the left-toolbar by clicking the arrow.
  6. Once expanded, click ***Build** and then ***Real Time Database***.
  7. Click ***Create Database*** and make sure Database location is set to ***United States (us-central1)***.
  8. By default, the database is going to start in ***locked mode***. Make sure to check ***Start in test mode*** instead.
  9. That's it! Your RTD is now ready for use. You should see a link on your screen in the form ***https://[name-of-project].firebaseio.com*** this is going to be the link we use to reference the database. Make sure to not share with anyone!

# Helper.py Documentation
Helper.py is a class that contains a few helper methods that make life a bit more easier.
Functionality includes connecting to wifi, synchronizing date and time, and timestamp generation.

### Helper Instance Vars
The helper class has two instance variables ***station*** and ***rtc*** which keep track of internet connection and time respectively. It is very unlikely that one needs to modify these vars directly and it is recommended that you ***don't***

### Helper Constructor
By default, the helper class will initialize station and rtc to default values. Station will have reference a WLAN object (wireless local area network aka wifi) that isn't connected to the internet and rtc will have a default time and date which most likely will be January 1, 2015.

### wifi_connect
A helper method that connects your micro-controller to the internet. It takes 2 string params, ***ssid*** (name of wifi) and ***password*** (password for wifi network). The method will attempt to connect to the network for 30 seconds. 

On success you will see ***Connected!*** print to console and the method will return a WLAN object. On failure, an error message will be printed and the method will return ***None***.

Things to Note:
  - ESP32 can only connect to a 2.4 Ghz network. If you have 5ghz or more (which most internet providers do) the esp32 will not be able to connect. If avilable connect to your 2.4 Ghz network. Optionally, mobile hotspots can also be an alternative.
  - Sometimes even if network speed, name, and password are correct the esp32 may take too long to connect causing it to fail connection. Pressing the reset button and trying again tends to fix the issue.
  
Example Usage:
```
from helper import helper
helper_methods = helper()

sta_if = helper_methods.wifi_connect('wifi-name', 'my wifi password')

if sta_if is None:
  # Wifi connection failed :(
else:
  # Wifi connection succeeded :)
```

### synchronize_date_time
A helper method that synchronizes the date and time of your micro controller. It takes a single string param ***city*** which is the name of the city your controller is in. It uses an [api]() to get the current time. This method ***will not*** work if your device is not connected to the internet.

On success, the method returns a synchronized RTC (real time clock) object. On failure it will return ***None***.

Example Usage:
```
from helper import helper
helper_methods = helper()

rtc = helepr.synchronize_date_time('New_York')

if rtc is None:
  # Sync failed :(
 else:
  # Sync succeeded :)
```

### self_calibrate
A helper method that connects to wifi and attempts to synchronize device clock. It takes 3 string params ***ssid**, ***password***, and ***city***. This is essentially a function that calls both wifi_connect and syncrhonize_date_time.

On success, the method will return a tuple (WLAN object, RTC object). On failure it will return a tuple (***None***, ***None***). If the wifi the device connects but synchronization fails it will instead return (WLAN object, ***None**). For quick setup using this function is recommended over calling wifi_connect and synchronize_date_time separately.

Example Usage:
```
from helper import helper
helper_methods = helper()

sta_if, rtc = helper_methods.self_calibrate('my wifi name', 'my wifi pass', 'New_York')

if sta_if is None:
  # Wifi connection failed :(
else:
  # Wifi connection succeeded :)
  
if rtc is None:
  # Clock sync failed :(
else:
  # Clock sync succeeded :)

```

### get_time_stamp
A helper method that returns a datetime string in y-m-dTh\:m\:s format. Ex Jan 10 2023, 10:30:05 would be formatted to 2023-1-10T10:30:05. This is helpful to timestamp the data your sensors collect before storing them into a database. Make sure your device clock is synchronized by calling ***self_calibrate***, or ***synchronize_date_time*** first!

Example Usage:
```
from helper import helper
helper_methods = helper()

current_time_stamp = helper_methods.get_time_stamp()
```

# Main.py Documentation
The main file where you will write the bulk of your micro-controller code for data collection.
The file already has some boiler plate code that helps you get quickly setup. All of the starting methods are defined in Helper.py.

Things to do:
  - replace ***'wifi_name'*** with the name of the wifi you are connecting to.
  - replace ***'wifi-password'*** with network's password
  - replace ***'New_York'*** if your device won't be in the east coast.
  - run your code to make sure your device is able to connect and synchronize itself.

If everything works, then you are all set! From here is getting your sensors to collect data and then storing it somewhere.

# Adding a sensor driver
Since we are working with low level controllers. Normally we would need to write low level code to interact with sensors. Luckily, there are some smart people out there who have already written some drivers (interface) that makes using sensors quick and easy.

Sensor Drivers:
 - [Temprature Sensor](https://github.com/MikeStone20/micropython_ahtx0) (AHT 10)

Adding Sensor Driver:
  1. Download the driver file. Normally the driver looks like ***sensor_name.py***.
  2. Make sure your microcontroller is plugged in, and that you have followed the instructions under [Setting up Thonny](#setting-up-thonny)
  3. In Thonny click ***File*** which is located on the top toolbar and then ***open***. Open the sensor driver file you just downloaded.
  4. Once the file is open in Thonny. Click ***File*** and then ***Save As***. Thonny will ask you if you want to save to your PC or to the microcontroller. Choose the microcontroller.
  5. Done! Now you can import the sensor driver and use it.

# Storing into Firebase

# Getting your data from Firebase
