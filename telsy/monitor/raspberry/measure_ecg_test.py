'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v28.04.2022
Ing. Elmer Rocha Jaime
'''

from datetime import datetime
from uart_io import serial_read, serial_write
from serial import Serial

serial = Serial('/dev/ttyAMA1', 115200)
info = open('./test/ecg_info.txt', 'w')
ecg_txt = open('./test/ecg_data.txt', 'w')
rr_txt = open('./test/rr_data.txt', 'w')
start_time = datetime.now()
try:
    data = 0
    while True:
        data_ = data
        data = serial.read()
        if ((data_==b'\x01') and (data==b'\x81')):
            serial_write(0)
            serial_write(1)
            start_time = datetime.now()
        # POST
        if data==b'\x03':
            info.write('### POST ###\n')
            info.write(serial_read(data)+'\n')
        # ECG Wave
        elif data==b'\x05':
            ecg_txt.write(serial_read(data)+'\n')
        # ECG Status
        elif data==b'\x06':
            info.write('### ECG Status ###\n')
            info.write(serial_read(data)+'\n')
        # Heart rate
        elif data==b'\x07':
            info.write('### Heart rate ###\n')
            info.write(serial_read(data)+'\n')
        # Arrhythmia
        elif data==b'\x0A':
            info.write('### Arrhythmia ###\n')
            info.write(serial_read(data)+'\n')
        # ST amplitude
        elif data==b'\x0B':
            info.write('### ST amplitude ###\n')
            info.write(serial_read(data)+'\n')
        # Respiration Wave
        elif data==b'\x10':
            rr_txt.write(serial_read(data)+'\n')
        # Respiration rate
        elif data==b'\x11':
            info.write('### Respiration rate ###\n')
            info.write(serial_read(data)+'\n')
        # Apnea
        elif data==b'\x12':
            info.write('### Apnea ###\n')
            info.write(serial_read(data)+'\n')

        current_time = datetime.now() - start_time
        if current_time.total_seconds() >= 60:
            break
    serial.close()
    info.close()
    rr_txt.close()
    ecg_txt.close()
except KeyboardInterrupt:
    serial.close()
    info.close()
    rr_txt.close()
    ecg_txt.close()
except OSError:
    print(OSError)
    serial.close()
    info.close()
    rr_txt.close()
    ecg_txt.close()
