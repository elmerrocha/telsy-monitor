'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v15.06.2022
Ing. Elmer Rocha Jaime
'''

from uart_io import serial_read, serial_write
from serial import Serial

serial = Serial('/dev/ttyAMA1', 115200)

try:
    data = 0
    while True:
        data_ = data
        data = serial.read()
        if ((data_ == b'\x01') and (data == b'\x81')):
            serial_write(100)

        # Temperature
        if data == b'\x15':
            temp = serial_read(data)
            print(temp.split('S')[0]+' - '+temp.split('S')[1])
    serial.close()
except KeyboardInterrupt:
    serial.close()
except OSError as exc:
    print(exc)
    serial.close()
