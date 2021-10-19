## Fundacion Cardiovascular de Colombia
## Proyecto Telsy Hogar
## Ing. Elmer Rocha Jaime

from datetime import datetime
from time import sleep
from Communication import Serial_Read, Serial_Write
from serial import Serial
import RPi.GPIO as GPIO

#Relay enabler
RelayPin = 10#GPIO10
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RelayPin, GPIO.OUT)
sleep(5)

serial = Serial('/dev/ttyAMA1', 115200)
File = open('./monitor/raspberry/data/data.txt','w')
TxtECG = open('./monitor/raspberry/data/ecg.txt','w')
Data = 0
StartTime = datetime.now()
try:
    while True:
        Data2 = Data
        Data = serial.read()
        if((Data2 == b'\x01') and (Data == b'\x81')):
            Serial_Write(0)
            Serial_Write(1)
            StartTime = datetime.now()

        ##### ECG Wave
        if(Data == b'\x05'): TxtECG.write(Serial_Read(Data)+',')
        ##### Respiration rate
        if(Data == b'\x11'): File.write('RR,'+Serial_Read(Data)+'\n')
        ##### SPO2
        if(Data == b'\x17'): File.write('SPO2,'+Serial_Read(Data)+'\n')

        CurrentTime = datetime.now() - StartTime
        if(CurrentTime.total_seconds() >= 60):
            break
    serial.close()
    File.close()
    TxtECG.close()
    GPIO.cleanup()
except KeyboardInterrupt:
    serial.close()
    File.close()
    TxtECG.close()
    GPIO.cleanup()
except Exception:
    serial.close()
    File.close()
    TxtECG.close()
    GPIO.cleanup()
