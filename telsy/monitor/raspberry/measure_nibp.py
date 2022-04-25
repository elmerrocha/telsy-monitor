'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v25.04.2022
Ing. Elmer Rocha Jaime
'''

from datetime import datetime
from time import sleep
from uart_io import serial_read, serial_write
from serial import Serial
import RPi.GPIO as gpio

#Relay enabler
RELAY_PIN = 10 #GPIO10
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(RELAY_PIN, gpio.OUT)
sleep(5)

serial = Serial('/dev/ttyAMA1', 115200)
file = open('./monitor/raspberry/data/data.txt','w')
ecg_txt = open('./monitor/raspberry/data/ecg.txt','w')
data = 0
NIBP_FLARG = True
TIME_FLARG = True
start_time = datetime.now()
try:
    while (NIBP_FLARG or TIME_FLARG):
        data_ = data
        data = serial.read()
        if ((data_==b'\x01') and (data==b'\x81')):
            serial_write(0)
            serial_write(1)
            serial_write(35)
            start_time = datetime.now()

        # ECG Wave
        if ((data==b'\x05') and TIME_FLARG):
            ecg_txt.write(serial_read(data)+',')
        # Respiration rate
        if ((data==b'\x11') and TIME_FLARG):
            file.write('RR,'+serial_read(data)+'\n')
        # SPO2
        if ((data==b'\x17') and TIME_FLARG):
            file.write('SPO2,'+serial_read(data)+'\n')
        # NIBP
        if ((data==b'\x22') and NIBP_FLARG):
            file.write('NIBP,'+serial_read(data)+'\n')
            f=open('./monitor/raspberry/data/nibp.end','w')
            f.close()
            NIBP_FLARG = False
        current_time = datetime.now() - start_time
        if ((current_time.total_seconds() >= 60) and TIME_FLARG):
            TIME_FLARG = False
    serial.close()
    file.close()
    ecg_txt.close()
    gpio.cleanup()
except KeyboardInterrupt:
    serial.close()
    file.close()
    ecg_txt.close()
    gpio.cleanup()
except OSError:
    print(OSError)
    serial.close()
    file.close()
    ecg_txt.close()
    gpio.cleanup()
