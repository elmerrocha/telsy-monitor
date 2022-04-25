'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v25.04.2022
Ing. Elmer Rocha Jaime
'''

from serial import Serial
import uart_decoder

serial = Serial('/dev/ttyAMA1', 115200)

def get_length(parameter):
    ''' Returns the number of bytes to read depending on the type of data '''
    parameters = {
        0x01: 2, # Reset
        0x03: 9, # Post
        0x04: 5, # Acknowledge
        0x05: 9, # ECG wave
        0x06: 5, # ECG status
        0x07: 7, # HR
        0x0A: 7, # ARR
        0x0B: 9, # ST
        0x10: 4, # RESP wave
        0x11: 5, # RR
        0x12: 6, # APNEA
        0x15: 8, # TEMP
        0x16: 5, # SPO2 wave
        0x17: 7, # SPO2 value
        0x20: 7, # NIBP cuff
        0x21: 4, # NIBP end
        0x22: 9, # NIBP result1
        0x23: 5, # NIBP result2
        0x24: 8  # NIBP status
    }
    return parameters.get(parameter)-1

def get_int(bytes):
    ''' Converts the data in bytes to integer '''
    return int.from_bytes(bytes, byteorder='big', signed=False)

def serial_read(serial_data):
    ''' Read the serial data sent by the card '''
    data = get_int(serial_data)
    data_length = get_length(data)
    buffer = []
    response = ''
    for _ in range(0, data_length):
        buffer.append(get_int(serial.read()))

    if data==0x03:
        response = uart_decoder.post_module(buffer)
    elif data==0x05:
        response = uart_decoder.ecg_wave(buffer)
    elif data==0x06:
        response = uart_decoder.ecg_status(buffer)
    elif data==0x07:
        response = uart_decoder.heart_rate(buffer)
    elif data==0x0A:
        response = uart_decoder.arrhythmia(buffer)
    elif data==0x0B:
        response = uart_decoder.st_amplitude(buffer)
    elif data==0x10:
        response = uart_decoder.respiration_wave(buffer)
    elif data==0x11:
        response = uart_decoder.respiration_rate(buffer)
    elif data==0x12:
        response = uart_decoder.apnea(buffer)
    elif data==0x15:
        response = uart_decoder.temperature(buffer)
    elif data==0x16:
        response = uart_decoder.spo2_wave(buffer)
    elif data==0x17:
        response = uart_decoder.spo2(buffer)
    elif data==0x20:
        response = uart_decoder.nibp_cuff(buffer)
    elif data==0x21:
        response = uart_decoder.nibp_end(buffer)
    elif data==0x22:
        response = uart_decoder.nibp_results(buffer)
    elif data==0x23:
        response = uart_decoder.nibp_pulse_rate(buffer)
    elif data==0x24:
        response = uart_decoder.nibp_status(buffer)

    return response

    # if data==0x05: return Method.ECG_Wave(buffer)
    # if data==0x06: return Method.ECG_Status(buffer)
    # if data==0x07: return Method.Heart_Rate(buffer)
    # if data==0x0A: return Method.Arrhythmia(buffer)
    # if data==0x0B: return Method.ST_Amplitude(buffer)
    # if data==0x10: return Method.Respiration_Wave(buffer)
    # if data==0x11: return Method.Respiration_Rate(buffer)
    # if data==0x15: return Method.Temperature(buffer)
    # if data==0x16: return Method.SPO2_Wave(buffer)
    # if data==0x17: return Method.SPO2(buffer)
    # if data==0x20: return Method.NIBP_Cuff(buffer)
    # if data==0x21: return Method.NIPB_End(buffer)
    # if data==0x22: return Method.NIBP_Results(buffer)
    # if data==0x23: return Method.NIBP_PulseRate(buffer)

def serial_write(command):
    ''' Sends configuration data to the module via serial '''
    commands = {
        0  : [0x01, 0x81], #Reset Acknowledge
        1  : [0x40, 0xC0], #Request POST
        2  : [0x42, 0x80, 0x00, 0xC2], #Patient type: Adult [default]
        3  : [0x42, 0x80, 0x01, 0xC3], #Patient type: Pediatric
        4  : [0x42, 0x80, 0x02, 0xC4], #Patient type: Adult
        5  : [0x45, 0x80, 0x00, 0xC5], #3/5 lead system: 3 lead
        6  : [0x45, 0x80, 0x01, 0xC6], #3/5 lead system: 5 lead [default]
        7  : [0x46, 0x80, 0x01, 0xC7], #ECG lead mode: lead I
        8  : [0x46, 0x80, 0x02, 0xC8], #ECG lead mode: lead II
        9  : [0x46, 0x80, 0x03, 0xC9], #ECG lead mode: lead III
        10 : [0x47, 0x80, 0x00, 0xC7], #ECG filter mode: Diagnostic (0.05-130Hz) [default]
        11 : [0x47, 0x80, 0x01, 0xC8], #ECG filter mode: Monitor (0.5-40Hz)
        12 : [0x47, 0x80, 0x02, 0xC9], #ECG filter mode: Surgery (1-20Hz)
        13 : [0x48, 0x80, 0x00, 0xC8], #ECG gain: x0.25
        14 : [0x48, 0x80, 0x01, 0xC9], #ECG gain: x0.5
        15 : [0x48, 0x80, 0x02, 0xCA], #ECG gain: x1.0 [default]
        16 : [0x48, 0x80, 0x03, 0xCB], #ECG gain: x2.0
        17 : [0x49, 0x80, 0x00, 0xC9], #ECG Calibration: off [default]
        18 : [0x49, 0x80, 0x01, 0xCA], #ECG Calibration: on
        19 : [0x4A, 0x80, 0x00, 0xCA], #ECG notch: off [default]
        20 : [0x4A, 0x80, 0x01, 0xCB], #ECG notch: on
        21 : [0x4B, 0x80, 0x00, 0xCB], #Pace: off [default]
        22 : [0x4B, 0x80, 0x01, 0xCC], #Pace: on
        23 : [0x50, 0x80, 0x00, 0xD0], #RESP gain: x0.25
        24 : [0x50, 0x80, 0x01, 0xD1], #RESP gain: x0.5
        25 : [0x50, 0x80, 0x02, 0xD2], #RESP gain: x1.0 [default]
        26 : [0x50, 0x80, 0x03, 0xD3], #RESP gain: x2.0
        27 : [0x50, 0x80, 0x04, 0xD4], #RESP gain: x4.0
        28 : [0x51, 0x80, 0x00, 0xD1], #RESP lead: lead I
        29 : [0x51, 0x80, 0x01, 0xD2], #RESP lead: lead II [default]
        30 : [0x53, 0x80, 0x00, 0xD3], #Temp sensor type: 2.5kOhm [default]
        31 : [0x53, 0x80, 0x01, 0xD4], #Temp sensor type: 10kOhm
        32 : [0x54, 0x80, 0x01, 0xD5], #SPO2 sensitivity: High
        33 : [0x54, 0x80, 0x02, 0xD6], #SPO2 sensitivity: Medium [default]
        34 : [0x54, 0x80, 0x03, 0xD7], #SPO2 sensitivity: Low
        35 : [0x55, 0xD5], #NIBP start *************
        36 : [0x56, 0xD6], #NIBP stop
        37 : [0x57, 0x80, 0x00, 0xD7], #NIBP auto period: manual [default]
        38 : [0x57, 0x80, 0x01, 0xD8], #NIBP auto period: 1   minute
        39 : [0x57, 0x80, 0x02, 0xD9], #NIBP auto period: 2   minutes
        40 : [0x57, 0x80, 0x03, 0xDA], #NIBP auto period: 3   minutes
        41 : [0x57, 0x80, 0x04, 0xDB], #NIBP auto period: 4   minutes
        42 : [0x57, 0x80, 0x05, 0xDC], #NIBP auto period: 5   minutes
        43 : [0x57, 0x80, 0x06, 0xDD], #NIBP auto period: 10  minutes
        44 : [0x57, 0x80, 0x07, 0xDE], #NIBP auto period: 15  minutes
        45 : [0x57, 0x80, 0x08, 0xDF], #NIBP auto period: 30  minutes
        46 : [0x57, 0x80, 0x09, 0xE0], #NIBP auto period: 60  minutes
        47 : [0x57, 0x80, 0x0A, 0xE1], #NIBP auto period: 90  minutes
        48 : [0x57, 0x80, 0x0B, 0xE2], #NIBP auto period: 120 minutes
        49 : [0x57, 0x80, 0x0C, 0xE3], #NIBP auto period: 180 minutes
        50 : [0x57, 0x80, 0x0D, 0xE4], #NIBP auto period: 240 minutes
        51 : [0x57, 0x80, 0x0E, 0xE5], #NIBP auto period: 480 minutes
        52 : [0x58, 0xD8], #NIBP calibration
        53 : [0x59, 0xD9], #NIBP reset to default manual mode
        54 : [0x5A, 0xDA], #NIBP pneumatic test
        55 : [0x5B, 0xDB], #Request NIBP status: The module will return NIBP status frame ID=0x24
        56 : [0x5D, 0xDD], #NIBP STAT: Continuous NIBP measurement during 5 minutes
        57 : [0x5E, 0xDE]  #Request NIBP result: Last NIBP result
    }
    for cmd in range(0, len(commands.get(command))):
        serial.write(commands.get(command)[cmd].to_bytes(1, 'big'))
