from network import WLAN, STA_IF
from machine import RTC
import urequests
from time import sleep_ms

class helper:
    station = None
    rtc = None
    
    def __init__(self):
        self.station = WLAN(STA_IF)
        self.rtc = RTC()
    
    '''If connected to internet, synchronize datetime based on time zone (America)
       city (str): the city we want the timezone of
       return: RTC object with local datetime, None if sync fails
    '''
    def synchronize_date_time(self, city : str) -> RTC:
        if not self.station.isconnected():
            print('Wifi not connected. Synchronization failed')
            return None
        api_response = urequests.get('http://worldtimeapi.org/api/timezone/America/' + city)
        raw_date_time = api_response.json()['datetime']
        date, time = raw_date_time.split('T')
        year, month, day = date.split('-')
        hours, mins, seconds = time.split(':')[:3]
        seconds = seconds.split('.')[0]

        date_time_tup = (int(year), int(month), int(day), 0, int(hours), int(mins), int(seconds), 0)
        self.rtc.datetime(date_time_tup)
        return self.rtc
    
    '''Connect to wifi
       ssid (str): wifi name
       password (str): wifi password
       return: WLAN object on success None on failure
    '''
    def wifi_connect(self, ssid : str, password: str) -> WLAN:
       if self.station.isconnected():
           self.station.disconnect()
       print('attempting to connect to network...')
       self.station.active(True)
       self.station.connect(ssid, password)
       retries = 0
       while not self.station.isconnected() and retries < 30:
           sleep_ms(1000)
           retries += 1
       if not self.station.isconnected():
           print('unable to connect to access point. Attempt timeout.')
           return None
       print('Connected!')
       return self.station
            
    
    ''' Connect to wifi and synchronize time
        city (str): the city we want the timezone of
        return Tuple(sta_if object, RTC object), (None, None) on failure
    '''
    def self_calibrate(self, ssid : str, password: str, city: str) -> Tuple[WLAN, RTC]:
        return (self.wifi_connect(ssid, password), self.synchronize_date_time(city))
    
    ''' Format a timestamp string using RTC
        rtc (RTC): real time clock object that has been synced
        return: timestamp string format y-m-dTh:m:s
    '''
    def get_time_stamp(self):
        dt_tup = self.rtc.datetime()
        timestamp = str(dt_tup[0]) + '-' + str(dt_tup[1]) + '-' + str(dt_tup[2]) + 'T' + str(dt_tup[4]) + ':' + str(dt_tup[5]) + ':' + str(dt_tup[6])
        return timestamp