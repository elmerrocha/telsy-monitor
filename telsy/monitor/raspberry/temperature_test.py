'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v28.04.2022
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
        if ((data_==b'\x01') and (data==b'\x81')):
            serial_write(0)
            serial_write(1)

        # Temperature
        if data==b'\x15':
            temp = serial_read(data)
            print(temp.split('S')[0])
    serial.close()
except KeyboardInterrupt:
    serial.close()
except OSError:
    print(OSError)
    serial.close()
