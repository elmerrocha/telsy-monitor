'''
Fundación Cardiovascular de Colombia
Dirección de Innovación y Desarrollo Tecnológico
Proyecto Telsy
Telsy Hogar v14.12.2022
Ing. Elmer Rocha Jaime
'''

from os import getcwd
from datetime import datetime
from time import sleep
from json import dumps
from monitor.raspberry import uart_decoder
from channels.generic.websocket import WebsocketConsumer

# Relay enabler
# GPIO10
RELAY_PIN = 10
buffer_data = {}
nibp_flarg = True
measure_flarg = True
serial = ''


def is_raspberry_pi_os():
    ''' Return a boolean value if the code is running in Raspberry OS '''
    current_path = getcwd().replace('\\', '/')
    return current_path[0:6] == '/home/'


if is_raspberry_pi_os():
    from serial import Serial
    import RPi.GPIO as gpio


def disconnect_websocket():
    global measure_flarg, nibp_flarg
    print('Websocket disconnection forced :o')
    measure_flarg = False
    nibp_flarg = False


def turn_off_board():
    global serial, measure_flarg, nibp_flarg
    measure_flarg = False
    nibp_flarg = False
    serial_write(36)
    sleep(1)
    serial.close()
    gpio.cleanup()


def turn_on_board():
    global serial, measure_flarg, nibp_flarg
    measure_flarg = True
    nibp_flarg = True
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(RELAY_PIN, gpio.OUT)
    serial = Serial('/dev/ttyAMA0', 115200)


class Spo2Consumer(WebsocketConsumer):
    ''' SpO2 Consumer '''
    def connect(self):
        if is_raspberry_pi_os():
            turn_on_board()
        global serial, buffer_data, measure_flarg
        print('SpO2 Websocket connected :)')
        self.accept()

        if is_raspberry_pi_os():
            try:
                data = 0
                start_time = datetime.now()
                send_data = False
                while measure_flarg:
                    data_ = data
                    data = serial.read()
                    if ((data_ == b'\x01') and (data == b'\x81')):
                        serial_write(100)
                        sleep(1)
                        start_time = datetime.now()
                    # Temperature
                    elif (data == b'\x15'):
                        send_data = True
                        buffer_data = {'type': 'temp', 'value': serial_read(data)}
                    # SpO2
                    elif (data == b'\x17'):
                        send_data = True
                        buffer_data = {'type': 'spo2', 'value': serial_read(data)}
                    # Send data
                    if send_data:
                        send_data = False
                        self.send(dumps(buffer_data))
                    # 60 seconds measurement stop
                    current_time = datetime.now() - start_time
                    if current_time.total_seconds() >= 60:
                        measure_flarg = False
                        self.close()
                        break
            except KeyboardInterrupt as err:
                print(err)
                turn_off_board()
                self.close()
            except OSError as err:
                print(err)
                turn_off_board()
                self.close()
        else:
            sleep(3)
            self.send(dumps({'type': 'websocket', 'value': '99S80S36.0'}))
            print('SpO2 Websocket sended default data <3')
            self.close()

    def disconnect(self, code):
        if is_raspberry_pi_os():
            turn_off_board()
        print('SpO2 Websocket disconnected :(')
        self.close()


class NibpConsumer(WebsocketConsumer):
    ''' NIBP Consumer '''
    def connect(self):
        if is_raspberry_pi_os():
            turn_on_board()
        global serial, buffer_data, measure_flarg, nibp_flarg
        print('NIBP Websocket connected :)')
        self.accept()

        if is_raspberry_pi_os():
            try:
                data = 0
                send_data = False
                while (measure_flarg and nibp_flarg):
                    data_ = data
                    data = serial.read()
                    if ((data_ == b'\x01') and (data == b'\x81')):
                        serial_write(100)
                        sleep(1)
                        serial_write(35)
                    # NIBP cuff
                    elif ((data == b'\x20') and nibp_flarg):
                        send_data = True
                        buffer_data = {'type': 'cuff', 'value': serial_read(data)}
                    # NIBP results
                    elif ((data == b'\x22') and nibp_flarg):
                        send_data = True
                        nibp_flarg = False
                        buffer_data = {'type': 'nibp', 'value': serial_read(data)}
                    # Send data
                    if send_data:
                        send_data = False
                        self.send(dumps(buffer_data))
            except KeyboardInterrupt as err:
                print(err)
                turn_off_board()
                self.close()
            except OSError as err:
                print(err)
                turn_off_board()
                self.close()
        else:
            sleep(3)
            self.send(dumps({'type': 'websocket', 'value': '120S80S93'}))
            print('NIBP Websocket sended default data <3')
            self.close()

    def disconnect(self, code):
        if is_raspberry_pi_os():
            turn_off_board()
        print('NIBP Websocket disconnected :(')
        self.close()


class EcgConsumer(WebsocketConsumer):
    ''' ECG Consumer '''
    def connect(self):
        if is_raspberry_pi_os():
            turn_on_board()
        global serial, buffer_data, measure_flarg, ecg_wave
        print('ECG Websocket connected :)')
        self.accept()

        if is_raspberry_pi_os():
            try:
                data = 0
                start_time = datetime.now()
                send_data = False
                while measure_flarg:
                    data_ = data
                    data = serial.read()
                    if ((data_ == b'\x01') and (data == b'\x81')):
                        serial_write(100)
                        sleep(1)
                        start_time = datetime.now()
                    # ECG wave
                    elif (data == b'\x05'):
                        send_data = True
                        buffer_data = {'type': 'ecg', 'value': serial_read(data)}
                    # Heart_rate
                    elif (data == b'\x07'):
                        send_data = True
                        buffer_data = {'type': 'hr', 'value': serial_read(data)}
                    # Respiration rate
                    elif (data == b'\x11'):
                        send_data = True
                        buffer_data = {'type': 'rr', 'value': serial_read(data)}
                    # Send data
                    if send_data:
                        send_data = False
                        self.send(dumps(buffer_data))
                    # 60 seconds measurement stop
                    current_time = datetime.now() - start_time
                    if current_time.total_seconds() >= 60:
                        measure_flarg = False
                        self.close()
                        break
            except KeyboardInterrupt as err:
                print(err)
                turn_off_board()
                self.close()
            except OSError as err:
                print(err)
                turn_off_board()
                self.close()
        else:
            sleep(3)
            self.send(dumps({'type': 'websocket', 'value': '80S30', 'ecg_wave':ecg_wave}))
            print('ECG Websocket sended default data <3')
            self.close()

    def disconnect(self, code):
        if is_raspberry_pi_os():
            turn_off_board()
        print('ECG Websocket disconnected :(')
        self.close()


class MonitorConsumer(WebsocketConsumer):
    ''' Monitor Consumer '''
    def connect(self):
        if is_raspberry_pi_os():
            turn_on_board()
        global serial, buffer_data, measure_flarg, nibp_flarg, ecg_wave
        print('Monitor Websocket connected :)')
        self.accept()

        if is_raspberry_pi_os():
            data = 0
            try:
                start_time = datetime.now()
                send_data = False
                while (measure_flarg or nibp_flarg):
                    data_ = data
                    data = serial.read()
                    if ((data_ == b'\x01') and (data == b'\x81')):
                        serial_write(100)
                        sleep(1)
                        serial_write(35)
                        start_time = datetime.now()
                    # ECG wave
                    elif ((data == b'\x05') and measure_flarg):
                        send_data = True
                        buffer_data = {'type': 'ecg', 'value': serial_read(data)}
                    # Heart rate
                    elif ((data == b'\x07') and measure_flarg):
                        send_data = True
                        buffer_data = {'type': 'hr', 'value': serial_read(data)}
                    # Respiration rate
                    elif ((data == b'\x11') and measure_flarg):
                        send_data = True
                        buffer_data = {'type': 'rr', 'value': serial_read(data)}
                    # Temperature
                    elif ((data == b'\x15') and measure_flarg):
                        send_data = True
                        buffer_data = {'type': 'temp', 'value': serial_read(data)}
                    # SpO2
                    elif ((data == b'\x17') and measure_flarg):
                        send_data = True
                        buffer_data = {'type': 'spo2', 'value': serial_read(data)}
                    # NIBP cuff
                    elif ((data == b'\x20') and nibp_flarg):
                        send_data = True
                        buffer_data = {'type': 'cuff', 'value': serial_read(data)}
                    # NIBP results
                    elif ((data == b'\x22') and nibp_flarg):
                        send_data = True
                        nibp_flarg = False
                        buffer_data = {'type': 'nibp', 'value': serial_read(data)}
                    # Send data
                    if send_data:
                        send_data = False
                        self.send(dumps(buffer_data))
                    # 60 seconds measurement stop
                    current_time = datetime.now() - start_time
                    if current_time.total_seconds() >= 60:
                        measure_flarg = False
                        self.close()
                        break
            except KeyboardInterrupt as err:
                print(err)
                turn_off_board()
                self.close()
            except OSError as err:
                print(err)
                turn_off_board()
                self.close()
        else:
            sleep(3)
            self.send(dumps({'type': 'websocket', 'value': '80S30S99S80S36.0S120S80S93', 'ecg_wave':ecg_wave}))
            print('Monitor Websocket sended default data <3')
            self.close()

    def disconnect(self, code):
        if is_raspberry_pi_os():
            turn_off_board()
        print('Monitor Websocket disconnected :(')
        self.close()




#### UART methods ####
def get_length(parameter):
    ''' Returns the number of bytes to read depending on the type of data '''
    parameters = {
        0x01: 2,  # Reset
        0x03: 9,  # Post
        0x04: 5,  # Acknowledge
        0x05: 9,  # ECG wave
        0x06: 5,  # ECG status
        0x07: 7,  # HR
        0x0A: 7,  # ARR
        0x0B: 9,  # ST
        0x10: 4,  # RESP wave
        0x11: 5,  # RR
        0x12: 6,  # APNEA
        0x15: 8,  # TEMP
        0x16: 5,  # SPO2 wave
        0x17: 7,  # SPO2 value
        0x20: 7,  # NIBP cuff
        0x21: 4,  # NIBP end
        0x22: 9,  # NIBP result1
        0x23: 5,  # NIBP result2
        0x24: 8  # NIBP status
    }
    return parameters.get(parameter)-1


def get_int(bytes):
    ''' Converts the data in bytes to integer '''
    return int.from_bytes(bytes, byteorder='big', signed=False)


def serial_read(serial_data):
    ''' Read the serial data sent by the card '''
    global serial
    data = get_int(serial_data)
    data_length = get_length(data)
    buffer = []
    response = ''
    for _ in range(0, data_length):
        buffer.append(get_int(serial.read()))

    if data == 0x03:
        response = uart_decoder.post_module(buffer)
    elif data == 0x05:
        response = uart_decoder.ecg_wave(buffer)
    elif data == 0x06:
        response = uart_decoder.ecg_status(buffer)
    elif data == 0x07:
        response = uart_decoder.heart_rate(buffer)
    elif data == 0x0A:
        response = uart_decoder.arrhythmia(buffer)
    elif data == 0x0B:
        response = uart_decoder.st_amplitude(buffer)
    elif data == 0x10:
        response = uart_decoder.respiration_wave(buffer)
    elif data == 0x11:
        response = uart_decoder.respiration_rate(buffer)
    elif data == 0x12:
        response = uart_decoder.apnea(buffer)
    elif data == 0x15:
        response = uart_decoder.temperature(buffer)
    elif data == 0x16:
        response = uart_decoder.spo2_wave(buffer)
    elif data == 0x17:
        response = uart_decoder.spo2(buffer)
    elif data == 0x20:
        response = uart_decoder.nibp_cuff(buffer)
    elif data == 0x21:
        response = uart_decoder.nibp_end(buffer)
    elif data == 0x22:
        response = uart_decoder.nibp_results(buffer)
    elif data == 0x23:
        response = uart_decoder.nibp_pulse_rate(buffer)
    elif data == 0x24:
        response = uart_decoder.nibp_status(buffer)

    return response


def serial_write(command):
    ''' Sends configuration data to the module via serial '''
    commands = {
        0: [0x01, 0x81],  # Reset Acknowledge
        1: [0x40, 0xC0],  # Request POST
        2: [0x42, 0x80, 0x80, 0xC2],  # Patient type: Adult *
        3: [0x42, 0x80, 0x81, 0xC3],  # Patient type: Pediatric
        4: [0x42, 0x80, 0x82, 0xC4],  # Patient type: Adult
        5: [0x45, 0x80, 0x80, 0xC5],  # 3/5 lead system: 3 lead
        6: [0x45, 0x80, 0x81, 0xC6],  # 3/5 lead system: 5 lead *
        7: [0x46, 0x80, 0x81, 0xC7],  # ECG lead mode: lead I
        8: [0x46, 0x80, 0x82, 0xC8],  # ECG lead mode: lead II
        9: [0x46, 0x80, 0x83, 0xC9],  # ECG lead mode: lead III
        10: [0x47, 0x80, 0x80, 0xC7],  # ECG filter: Diagnostic (0.05-130Hz) *
        11: [0x47, 0x80, 0x81, 0xC8],  # ECG filter: Monitor (0.5-40Hz)
        12: [0x47, 0x80, 0x82, 0xC9],  # ECG filter: Surgery (1-20Hz)
        13: [0x48, 0x80, 0x80, 0xC8],  # ECG gain: x0.25
        14: [0x48, 0x80, 0x81, 0xC9],  # ECG gain: x0.5
        15: [0x48, 0x80, 0x82, 0xCA],  # ECG gain: x1.0 *
        16: [0x48, 0x80, 0x83, 0xCB],  # ECG gain: x2.0
        17: [0x49, 0x80, 0x80, 0xC9],  # ECG Calibration: off *
        18: [0x49, 0x80, 0x81, 0xCA],  # ECG Calibration: on
        19: [0x4A, 0x80, 0x80, 0xCA],  # ECG notch: off *
        20: [0x4A, 0x80, 0x81, 0xCB],  # ECG notch: on
        21: [0x4B, 0x80, 0x80, 0xCB],  # Pace: off *
        22: [0x4B, 0x80, 0x81, 0xCC],  # Pace: on
        23: [0x50, 0x80, 0x80, 0xD0],  # RESP gain: x0.25
        24: [0x50, 0x80, 0x81, 0xD1],  # RESP gain: x0.5
        25: [0x50, 0x80, 0x82, 0xD2],  # RESP gain: x1.0 *
        26: [0x50, 0x80, 0x83, 0xD3],  # RESP gain: x2.0
        27: [0x50, 0x80, 0x84, 0xD4],  # RESP gain: x4.0
        28: [0x51, 0x80, 0x80, 0xD1],  # RESP lead: lead I
        29: [0x51, 0x80, 0x81, 0xD2],  # RESP lead: lead II *
        30: [0x53, 0x80, 0x80, 0xD3],  # Temp sensor type: 2.5kOhm *
        31: [0x53, 0x80, 0x81, 0xD4],  # Temp sensor type: 10kOhm
        32: [0x54, 0x80, 0x81, 0xD5],  # SPO2 sensitivity: High
        33: [0x54, 0x80, 0x82, 0xD6],  # SPO2 sensitivity: Medium *
        34: [0x54, 0x80, 0x83, 0xD7],  # SPO2 sensitivity: Low
        35: [0x55, 0xD5],  # NIBP start
        36: [0x56, 0xD6],  # NIBP stop
        37: [0x57, 0x80, 0x80, 0xD7],  # NIBP auto period: manual *
        38: [0x57, 0x80, 0x81, 0xD8],  # NIBP auto period: 1   minute
        39: [0x57, 0x80, 0x82, 0xD9],  # NIBP auto period: 2   minutes
        40: [0x57, 0x80, 0x83, 0xDA],  # NIBP auto period: 3   minutes
        41: [0x57, 0x80, 0x84, 0xDB],  # NIBP auto period: 4   minutes
        42: [0x57, 0x80, 0x85, 0xDC],  # NIBP auto period: 5   minutes
        43: [0x57, 0x80, 0x86, 0xDD],  # NIBP auto period: 10  minutes
        44: [0x57, 0x80, 0x87, 0xDE],  # NIBP auto period: 15  minutes
        45: [0x57, 0x80, 0x88, 0xDF],  # NIBP auto period: 30  minutes
        46: [0x57, 0x80, 0x89, 0xE0],  # NIBP auto period: 60  minutes
        47: [0x57, 0x80, 0x8A, 0xE1],  # NIBP auto period: 90  minutes
        48: [0x57, 0x80, 0x8B, 0xE2],  # NIBP auto period: 120 minutes
        49: [0x57, 0x80, 0x8C, 0xE3],  # NIBP auto period: 180 minutes
        50: [0x57, 0x80, 0x8D, 0xE4],  # NIBP auto period: 240 minutes
        51: [0x57, 0x80, 0x8E, 0xE5],  # NIBP auto period: 480 minutes
        52: [0x58, 0xD8],  # NIBP calibration
        53: [0x59, 0xD9],  # NIBP reset to default manual mode
        54: [0x5A, 0xDA],  # NIBP pneumatic test
        55: [0x5B, 0xDB],  # Request NIBP status:  return NIBP status
        56: [0x5D, 0xDD],  # NIBP STAT: Continuous during 5 minutes
        57: [0x5E, 0xDE]  # Request NIBP result: Last NIBP result
        # * Default mode
    }
    DEFAULT_COMMANDS = [0, 1, 36, 11, 20, 30, 53]
    if command == 100:
        for default_cmd in DEFAULT_COMMANDS:
            for cmd in range(0, len(commands.get(default_cmd))):
                serial.write(commands.get(default_cmd)[cmd].to_bytes(1, 'big'))
    else:
        for cmd in range(0, len(commands.get(command))):
            serial.write(commands.get(command)[cmd].to_bytes(1, 'big'))

## ECG Wave
ecg_txt = open('./monitor/raspberry/data/ecg.txt', 'r')
wave = ecg_txt.read()
ecg_wave = wave.rstrip(wave[-1]).split(',')
ecg_txt.close()
