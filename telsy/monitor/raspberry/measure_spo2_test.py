'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v18.05.2022
Ing. Elmer Rocha Jaime
'''

from datetime import datetime
from uart_io import serial_read, serial_write
from serial import Serial

serial = Serial('/dev/ttyAMA1', 115200)
spo2_txt = open('./test/spo2_data.txt', 'w')
info = open('./test/spo2_info.txt', 'w')
start_time = datetime.now()
try:
    data = 0
    while True:
        data_ = data
        data = serial.read()
        if ((data_==b'\x01') and (data==b'\x81')):
            serial_write(100)
            start_time = datetime.now()

        # Temperature
        if data==b'\x15':
            info.write('### Temperature ###\n')
            info.write(serial_read(data)+'\n')
        # SPO2 Wave
        elif data==b'\x16':
            tmp = serial_read(data)
            spo2_txt.write(tmp.split('*')[0].split('S')[0]+'\n')
        # SPO2
        elif data==b'\x17':
            info.write('### SPO2 ###\n')
            info.write(serial_read(data)+'\n')

        current_time = datetime.now() - start_time
        if current_time.total_seconds() >= 60:
            break
    serial.close()
    info.close()
    spo2_txt.close()
except KeyboardInterrupt:
    serial.close()
    info.close()
    spo2_txt.close()
except OSError as exc:
    print(exc)
    serial.close()
    info.close()
    spo2_txt.close()
