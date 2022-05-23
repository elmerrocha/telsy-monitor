'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v23.05.2022
Ing. Elmer Rocha Jaime
'''

from datetime import datetime
from time import sleep
from uart_io import serial_read, serial_write
from serial import Serial

serial = Serial('/dev/ttyAMA1', 115200)
info = open('nibp_info.txt', 'w')
start_time = datetime.now()
try:
    data = 0
    while True:
        data_ = data
        data = serial.read()
        if ((data_==b'\x01') and (data==b'\x81')):
            serial_write(100)
            sleep(0.5)
            serial_write(35)
            start_time = datetime.now()

        # Cuff pressure
        if data==b'\x20':
            info.write('### Cuff pressure ###\n')
            info.write(serial_read(data)+'\n')
        # NIBP End
        elif data==b'\x21':
            info.write('### NIBP End ###\n')
            info.write(serial_read(data)+'\n')
        # NIBP Results
        elif data==b'\x22':
            info.write('### Cuff Results ###\n')
            info.write(serial_read(data)+'\n')
        # NIBP pulse rate
        elif data==b'\x23':
            info.write('### NIBP pulse rate ###\n')
            info.write(serial_read(data)+'\n')
        # NIBP status
        elif data==b'\x24':
            info.write('### NIBP status ###\n')
            info.write(serial_read(data)+'\n')

        current_time = datetime.now() - start_time
        if current_time.total_seconds() >= 60:
            break
    serial.close()
    info.close()
except KeyboardInterrupt:
    serial.close()
    info.close()
except OSError as exc:
    print(exc)
    serial.close()
    info.close()
