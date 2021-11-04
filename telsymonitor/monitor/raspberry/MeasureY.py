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
NIBP_Flarg = True
Time_Flarg = True
StartTime = datetime.now()
try:
    while (NIBP_Flarg or Time_Flarg):
        Data2 = Data
        Data = serial.read()
        if((Data2 == b'\x01') and (Data == b'\x81')):
            Serial_Write(0)
            Serial_Write(1)
            Serial_Write(35)
            StartTime = datetime.now()

        ##### ECG Wave
        if((Data == b'\x05') and Time_Flarg): TxtECG.write(Serial_Read(Data)+',')
        ##### Respiration rate
        if((Data == b'\x11') and Time_Flarg): File.write('RR,'+Serial_Read(Data)+'\n')
        ##### SPO2
        if((Data == b'\x17') and Time_Flarg): File.write('SPO2,'+Serial_Read(Data)+'\n')
        ##### NIBP
        if((Data == b'\x22') and NIBP_Flarg):
            File.write('NIBP,'+Serial_Read(Data)+'\n')
            f=open('./monitor/raspberry/data/NIBP.end','w')
            f.close()
            NIBP_Flarg = False
        ##### NIBP End
        # if((Data == b'\x21') and NIBP_Flarg):
        #     print(Serial_Read(Data))
        #     f=open('./monitor/raspberry/data/NIBP.end','w')
        #     f.close()
        #     NIBP_Flarg = False

        CurrentTime = datetime.now() - StartTime
        if((CurrentTime.total_seconds() >= 60) and Time_Flarg):
            Time_Flarg = False
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
