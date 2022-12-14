'''
Fundación Cardiovascular de Colombia
Dirección de Innovación y Desarrollo Tecnológico
Proyecto Telsy
Telsy Hogar v14.12.2022
Ing. Elmer Rocha Jaime
'''


def post_module(data):  # 0x03
    ''' Return Power on Self Test information about 806c module '''
    # data[0] : HEAD
    # data[1] : POST1
    # data[2] : POST2
    # data[3] : Version
    # data[4] : Module ID 1
    # data[5] : Module ID 2
    # data[6] : Module ID 3
    # data[7] : CHECKSUM

    # Version: version No. x 10, e.g., 10 means version 1.0.
    # Module ID1-3: "808".
    # POST1:
    # BIT     description
    # 7:5     Reserved
    # 4       Watchdog test: 0:, 1: OK
    # 3       A/D test:  (0: Fail, 1: OK)
    # 2       RAM test:  (0: Fail, 1: OK)
    # 1       ROM test:  (0: Fail, 1: OK)
    # 0       CPU test:  (0: Fail, 1: OK)
    # POST2:
    # BIT    description
    # 7:5    Reserved
    # 4      NIBP test:  (0: Fail, 1: OK)
    # 3      SPO2 test:  (0: Fail, 1: OK)
    # 2      TEMP test:  (0: Fail, 1: OK)
    # 1      RESP test:  (0: Fail, 1: OK)
    # 0      ECG test:   (0: Fail, 1: OK)

    # 0x01 : 0000 0001
    # 0x02 : 0000 0010
    # 0x04 : 0000 0100
    # 0x08 : 0000 1000
    # 0x10 : 0001 0000
    # 0x20 : 0010 0000
    # 0x7F : 0111 1111
    ###########################################################################
    cpu_test = str(data[1] & 0x01)
    rom_test = str((data[1] & 0x02) >> 1)
    ram_test = str((data[1] & 0x04) >> 2)
    ad_test = str((data[1] & 0x08) >> 3)
    watchdog = str((data[1] & 0x10) >> 4)
    ecg_test = str(data[2] & 0x01)
    resp_test = str((data[2] & 0x02) >> 1)
    temp_test = str((data[2] & 0x04) >> 2)
    spo2_test = str((data[2] & 0x08) >> 3)
    nibp_test = str((data[2] & 0x10) >> 4)
    version = str(data[3] & 0x7F)
    module_1 = str(data[4] & 0x7F)
    module_2 = str(data[5] & 0x7F)
    module_3 = str(data[6] & 0x7F)
    module_id = module_1+'-'+module_2+'-'+module_3
    post_1 = cpu_test+'S'+rom_test+'S'+ram_test+'S'+ad_test+'S'+watchdog
    post_2 = ecg_test+'S'+resp_test+'S'+temp_test+'S'+spo2_test+'S'+nibp_test
    ###########################################################################
    return post_1+'*'+post_2+'*'+str(version)+module_id


def ecg_wave(data):  # 0x05
    ''' Returns the waveforms of the ECG signal '''
    # data[0] : HEAD
    # data[1] : ECG channel 1 wave, high byte
    # data[2] : ECG channel 1 wave, low byte
    # data[3] : ECG channel 2 wave, high byte
    # data[4] : ECG channel 2 wave, low byte
    # data[5] : ECG channel 3 wave, high byte
    # data[6] : ECG channel 3 wave, low byte
    # data[7] : CHECKSUM

    # ECG 1,ECG2, ECG3 wave: unsigned char,
    # wave baseline is 2048, data range: 0-4096.
    # ECG channel 1: lead II, ECG channel 2: lead I,
    # ECG channel 3: lead V.
    # Other ECG lead calculation formula:
    # III = II-I
    # AVR = -(I+II)/2
    # AVL = I-II/2=(I-III)/2
    # AVF = II-I/2=(II+III)/2

    # Pace & beat flag is BIT 7 & 6 in ECG channel 1 wave, high byte:
    # BIT Description
    # 7   Pace flag (0: false, 1: true)
    # 6   Heart beat flag (0: false, 1: true)

    # 0x01 : 0000 0001
    # 0x02 : 0000 0010
    # 0x04 : 0000 0100
    # 0x08 : 0000 1000
    # 0x10 : 0001 0000
    # 0x20 : 0010 0000
    # 0x3F : 0011 1111
    # 0x40 : 0100 0000
    # 0x7F : 0111 1111
    ###########################################################################
    # pace_flarg = data[0] & 0x01
    # heart_beate_flarg = data[1] & 0x40
    # flargs = str(pace_flarg) + 'S' + str(heart_beate_flarg)
    ecg1_h = (data[1] & 0x3F) << 8
    ecg1_l = ((data[0] & 0x02) << 6) | (data[2] & 0x7F)
    ecg2_h = (((data[0] & 0x04) <<5) | (data[3] & 0x7F)) << 8
    ecg2_l =  ((data[0] & 0x08) <<4) | (data[4] & 0x7F)
    ecg3_h = (((data[0] & 0x10) <<3) | (data[5] & 0x7F)) << 8
    ecg3_l =  ((data[0] & 0x20) <<2) | (data[6] & 0x7F)
    ###########################################################################
    return str(ecg1_h | ecg1_l)#+'S'+str(ecg2_h | ecg2_l)+'S'+str(ecg3_h | ecg3_l)


def ecg_status(data):  # 0x06
    ''' Return the lead status of ECG '''
    # data[0] : HEAD
    # data[1] : Status
    # data[2] : Saturate
    # data[3] : CHECKSUM

    # Status:
    # BIT     description
    # 7:4     Reserved
    # 3       V    (1: lead off, 0: lead OK)
    # 2       RA   (1: lead off, 0: lead OK)
    # 1       LA   (1: lead off, 0: lead OK)
    # 0       LL   (1: lead off, 0: lead OK)
    # Saturate:
    # BIT     description
    # 7:4     Reserved
    # 3       Lead V   (1: Saturate, 0: lead OK)
    # 2       Lead III (1: Saturate, 0: lead OK)
    # 1       Lead I   (1: Saturate, 0: lead OK)
    # 0       Lead II  (1: Saturate, 0: lead OK)

    # 0x01 : 0000 0001
    # 0x02 : 0000 0010
    # 0x04 : 0000 0100
    # 0x08 : 0000 1000
    ###########################################################################
    lead_ll = (data[1] & 0x01)
    lead_la = (data[1] & 0x02) >> 1
    lead_ra = (data[1] & 0x04) >> 2
    lead_v = (data[1] & 0x08) >> 3
    lead_ii = (data[2] & 0x01)
    lead_i = (data[2] & 0x02) >> 1
    lead_iii = (data[2] & 0x04) >> 2
    lead_v1 = (data[2] & 0x08) >> 3
    lead_txt1 = str(lead_ll)+'S'+str(lead_la)+'S'+str(lead_ra)+'S'+str(lead_v)
    lead_txt2 = str(lead_ii)+'S'+str(lead_i)+'S'+str(lead_iii)+'S'+str(lead_v1)
    ###########################################################################
    return lead_txt1+'*'+lead_txt2


def heart_rate(data):  # 0x07
    ''' Returns the heart rate value by ECG '''
    # data[0] : HEAD
    # data[1] : HR high byte
    # data[2] : HR low byte
    # data[3] : R pos high byte
    # data[4] : R pos low byte
    # data[5] : CHECKSUM

    # HR(heart rate): short, data range: adult/pediatric 0-300BPM, neonate:
    # 0-350BPM, -100 means invalid value.
    # R pos: QRS position: short, means the QRS wave time, the unit is 4ms,
    # e.g., 250 mean 1 second before current packet time.

    # 0x01 : 0000 0001
    # 0x02 : 0000 0010
    # 0x04 : 0000 0100
    # 0x08 : 0000 1000
    # 0x7F : 0111 1111
    ###########################################################################
    hr_h = (((data[0] & 0x01) << 7) | (data[1] & 0x7F)) << 8
    hr_l = ((data[0] & 0x02) << 6) | (data[2] & 0x7F)
    r_h = (((data[0] & 0x04) << 5) | (data[3] & 0x7F)) << 8
    r_l = ((data[0] & 0x08) << 4) | (data[4] & 0x7F)
    ###########################################################################
    return str(hr_h | hr_l)#+'S'+str(r_h | r_l)


def arrhythmia(data):  # 0x0A
    ''' Returns an arrhythmia code and the position in time where it occurs '''
    # data[0] : HEAD
    # data[1] : ARR type
    # data[2] : ARR position high byte
    # data[3] : ARR position low byte
    # data[4] : CHECKSUM

    # ARR type code:
    # 1: Asystole
    # 2: Vent Tatchy/FIB
    # 3: R on T
    # 4: RUN
    # 5: Couplet
    # 6: PVC
    # 7: Bigeminy
    # 8: Trigeminy
    # 9: Tachy
    # 10: Brady
    # 11: PNC, Pace not capture
    # 12: PNP, Pace no paced
    # 13: Miss Beat
    # 14: ARR learn
    # 15: normal QRS
    # 16: Noise
    # 17: weak signal
    # ARR position: short, means the arrhythmia event occur time,
    # the unit is 4ms, e.g., 250 mean 1 second before.

    # 0x01 : 0000 0001
    # 0x02 : 0000 0010
    # 0x04 : 0000 0100
    # 0x7F : 0111 1111
    ###########################################################################
    arr_type = ((data[0] & 0x01) << 7) | (data[1] & 0x7F)
    arr_pos_h = (((data[0] & 0x02) << 6) | (data[2] & 0x7F)) << 8
    arr_pos_l = ((data[0] & 0x04) << 5) | (data[3] & 0x7F)
    ###########################################################################
    return str(arr_type)+'S'+str(arr_pos_h | arr_pos_l)


def st_amplitude(data):  # 0x0B
    ''' Returns the ST amplitude of the three ECG signal channels '''
    # data[0] : HEAD
    # data[1] : ST1 high byte
    # data[2] : ST1 low byte
    # data[3] : ST2 high byte
    # data[4] : ST2 low byte
    # data[5] : ST3 high byte
    # data[6] : ST3 low byte
    # data[7] : CHECKSUM

    # 0x01 : 0000 0001
    # 0x02 : 0000 0010
    # 0x04 : 0000 0100
    # 0x08 : 0000 1000
    # 0x10 : 0001 0000
    # 0x20 : 0010 0000
    # 0x7F : 0111 1111
    ###########################################################################
    st1_h = (((data[0] & 0x01) << 7) | (data[1] & 0x7F)) << 8
    st1_l = ((data[0] & 0x02) << 6) | (data[2] & 0x7F)
    st2_h = (((data[0] & 0x04) << 5) | (data[3] & 0x7F)) << 8
    st2_l = ((data[0] & 0x08) << 4) | (data[4] & 0x7F)
    st3_h = (((data[0] & 0x10) << 3) | (data[5] & 0x7F)) << 8
    st3_l = ((data[0] & 0x20) << 2) | (data[6] & 0x7F)
    st1 = str((st1_h | st1_l)/100)
    st2 = str((st2_h | st2_l)/100)
    st3 = str((st3_h | st3_l)/100)
    ###########################################################################
    return st1+'S'+st2+'S'+st3


def respiration_wave(data):  # 0x10
    ''' Returns the waveform of the respiration '''
    # data[0] : HEAD
    # data[1] : RESP wave
    # data[2] : CHECKSUM

    # RESP wave: data range 0-256, base line is 128.

    # 0x01 : 0000 0001
    # 0x7F : 0111 1111
    ###########################################################################
    resp_wave = ((data[0] & 0x01) << 7) | (data[1] & 0x7F)
    ###########################################################################
    return str(resp_wave)


def respiration_rate(data):  # 0x11
    ''' Returns the respiration rate value '''
    # data[0] : HEAD
    # data[1] : RR high byte
    # data[2] : RR low byte
    # data[3] : CHECKSUM

    # RR(respiration rate): short, data range: adult: 0-120BrPM,
    # Pediatric/Neonate 0-150BrPM, 100 means invalid. 0 means apnea.

    # 0x01 : 0000 0001
    # 0x02 : 0000 0010
    # 0x7F : 0111 1111
    ###########################################################################
    rr_h = (((data[0] & 0x01) << 7) | (data[1] & 0x7F)) << 8
    rr_l = ((data[0] & 0x02) << 6) | (data[2] & 0x7F)
    ###########################################################################
    return str(rr_h | rr_l)


def apnea(data):  # 0x12
    ''' Returns apnea alarm '''
    # data[0] : HEAD
    # data[1] : Apnea
    # data[2] : Reserved
    # data[3] : Reserved
    # data[4] : CHECKSUM

    # Apnea alarm: 0: false; 1: true;

    # 0x01 : 0000 0001
    ###########################################################################
    apnea_alarm = data[1] & 0x01
    ###########################################################################
    return str(apnea_alarm)


def temperature(data):  # 0x15
    ''' Returns the temperature value '''
    # data[0] : HEAD
    # data[1] : Sensor states
    # data[2] : TEMP1 high byte
    # data[3] : TEMP1 low byte
    # data[4] : TEMP2 high byte
    # data[5] : TEMP2 low byte
    # data[6] : CHECKSUM

    # Sensor  status:
    # BIT     description
    # 7:2     Reserved
    # 1       Sensor 2 (0 connected, 1 sensor off)
    # 0       Sensor 1 (0 connected, 1 sensor off)
    # TEMP1 & TEMP2 value: short, data range: 0-500.
    # Unit: 0.1C. e.g. 204 mean 20.4C. -100 means invalid.

    # 0x01 : 0000 0001
    # 0x02 : 0000 0010
    # 0x04 : 0000 0100
    # 0x08 : 0000 1000
    # 0x10 : 0001 0000
    # 0x7F : 0111 1111
    ###########################################################################
    t1_s = (data[1] & 0x01)
    t2_s = (data[1] & 0x02) >> 1
    t1_h = (((data[0] & 0x02) << 6) | (data[2] & 0x7F)) << 8
    t1_l = ((data[0] & 0x04) << 5) | (data[3] & 0x7F)
    t2_h = (((data[0] & 0x08) << 4) | (data[4] & 0x7F)) << 8
    t2_l = ((data[0] & 0x10) << 3) | (data[5] & 0x7F)
    status = str(t1_s)+'S'+str(t2_s)
    ###########################################################################
    return str((t1_h | t1_l)/10)#+'S'+str((t2_h | t2_l)/10)+'*'+status


def spo2_wave(data):  # 0x16
    ''' Returns the waveform of the SPO2 signal '''
    # data[0] : HEAD
    # data[1] : SPO2 wave
    # data[2] : SPO2 status
    # data[3] : CHECKSUM

    # SPO2 wave: unsigned char, data range: 0-255.
    # SPO2 status:
    # BIT     description
    # 7       SPO2 finger off flag
    # 6       Pulse flag
    # 5       Search pulse flag
    # 4       SPO2 sensor off flag
    # 3:0     SPO2 bar graph,0-15

    # 0x01 : 0000 0001
    # 0x02 : 0000 0010
    # 0x0F : 0000 1111
    # 0x10 : 0001 0000
    # 0x20 : 0010 0000
    # 0x40 : 0100 0000
    # 0x7F : 0111 1111
    ###########################################################################
    spo2_wave = ((data[0] & 0x01) << 7) | (data[1] & 0x7F)
    # bar_graph = data[2] & 0x0F
    # sensor_status = str((data[2] & 0x10) >> 4)
    # search_flarg = str((data[2] & 0x20) >> 5)
    # pulse_flarg = str((data[2] & 0x40) >> 6)
    # finger = str(data[0] & 0x02)
    # spo2_1 = str(spo2_wave)+'S'+str(bar_graph)
    # spo2_2 = sensor_status+'S'+search_flarg+'S'+pulse_flarg+'S'+finger
    ###########################################################################
    # return spo2_1+'*'+spo2_2
    return str(spo2_wave)


def spo2(data):  # 0x17
    ''' Returns pulse rate and oxygen saturation percentage '''
    # data[0] : HEAD
    # data[1] : Spo2 information
    # data[2] : PR high byte
    # data[3] : PR low byte
    # data[4] : Spo2
    # data[5] : CHECKSUM

    # Spo2 information:
    # BIT     description
    # 7:6     Reserved
    # 5       Spo2 drop flag
    # 4       Search too long flag
    # 3:0     Signal strength(0-8, 15 means invalid)

    # PR(pulse rate): short, data range: 0-255BPM, -100 means invalid.

    # Spo2: data range: 0～100%, -100 means invalid.

    # 0x02 : 0000 0010
    # 0x04 : 0000 0100
    # 0x08 : 0000 1000
    # 0x0F : 0000 1111
    # 0x10 : 0001 0000
    # 0x20 : 0010 0000
    # 0x7F : 0111 1111
    ###########################################################################
    # signal = (data[1] & 0x0F)
    # search = (data[1] & 0x10) >> 4
    # drop   = (data[1] & 0x20) >> 5
    # information = str(signal)+'S'+str(search)+'S'+str(drop)
    pr_h = (((data[0] & 0x02) << 6) | (data[2] & 0x7F)) << 8
    pr_l = ((data[0] & 0x04) << 5) | (data[3] & 0x7F)
    spo2 = ((data[0] & 0x08) << 4) | (data[4] & 0x7F)
    ###########################################################################
    return str(spo2)+'S'+str(pr_h | pr_l)
    # return str(pr_h | pr_l)


def nibp_cuff(data):  # 0x20
    ''' Returns current cuff pressure '''
    # data[0] : HEAD
    # data[1] : Cuff high byte
    # data[2] : Cuff low byte
    # data[3] : Cuff type wrong flag
    # data[4] : Measure mode
    # data[5] : CHECKSUM

    # Cuff pressure: short, data range: 0-300mmHg, -100 means invalid.

    # NIBP Cuff type wrong flag:
    # 0: OK; 1: wrong type of Cuff used.

    # Host should stop NIBP measure when received this flag.

    # NIBP measure mode:
    # 1: manual mode;
    # 2: auto mode;
    # 3: STAT mode;
    # 4: calibration;
    # 5: pneumatic;

    # 0x01 : 0000 0001
    # 0x02 : 0000 0010
    # 0x7F : 0111 1111
    ###########################################################################
    cuff_h = (((data[0] & 0x01) << 7) | (data[1] & 0x7F)) << 8
    cuff_l = ((data[0] & 0x02) << 6) | (data[2] & 0x7F)
    wrong_flag = data[3] & 0x01
    measure_mode = data[3] & 0x7F
    ###########################################################################
    return str(cuff_h | cuff_l)#+'S'+str(wrong_flag)+'S'+str(measure_mode)


def nibp_end(data):  # 0x21
    ''' Returns end mode of blood pressure measure '''
    # data[0] : HEAD
    # data[1] : data
    # data[2] : CHECKSUM

    # NIBP end mode:
    # 1 : end in manual mode;
    # 2 : end in auto mode;
    # 3 : end in STAT mode;
    # 4 : end in calibration mode;
    # 5 : end in pneumatic mode;
    # 10: error, detail information in NIBP status frame (0x24)

    # 0x01 : 0000 0001
    # 0x7F : 0111 1111
    return ((data[0] & 0x01) << 7) | (data[1] & 0x7F)


def nibp_results(data):  # 0x22
    ''' Returns the NIBP results (systolic, diastolic and mean pressure) '''
    # data[0] : HEAD
    # data[1] : Systolic high byte
    # data[2] : Systolic low byte
    # data[3] : Diastolic high byte
    # data[4] : Diastolic low byte
    # data[5] : Mean high byte
    # data[6] : Mean low byte
    # data[7] : CHECKSUM

    # Systolic, diastolic, mean: short, data range: 0-300mmHg.
    # -100 means invalid

    # 0x01 : 0000 0001
    # 0x02 : 0000 0010
    # 0x04 : 0000 0100
    # 0x08 : 0000 1000
    # 0x10 : 0001 0000
    # 0x20 : 0010 0000
    # 0x7F : 0111 1111
    ###########################################################################
    sys_h = (((data[0] & 0x01) << 7) | (data[1] & 0x7F)) << 8
    sys_l = ((data[0] & 0x02) << 6) | (data[2] & 0x7F)
    dia_h = (((data[0] & 0x04) << 5) | (data[3] & 0x7F)) << 8
    dia_l = ((data[0] & 0x08) << 4) | (data[4] & 0x7F)
    mean_h = (((data[0] & 0x10) << 3) | (data[5] & 0x7F)) << 8
    mean_l = ((data[0] & 0x20) << 2) | (data[6] & 0x7F)
    ###########################################################################
    return str(sys_h | sys_l)+'S'+str(dia_h | dia_l)+'S'+str(mean_h | mean_l)


def nibp_pulse_rate(data):  # 0x23
    ''' Returns the pulse rate value by NIBP '''
    # data[0] : HEAD
    # data[1] : PR high byte
    # data[2] : PR low byte
    # data[3] : CHECKSUM

    # PR (pulse rate): short, -100 means invalid

    # 0x01 : 0000 0001
    # 0x02 : 0000 0010
    # 0x7F : 0111 1111
    ###########################################################################
    pr_h = (((data[0] & 0x01) << 7) | (data[1] & 0x7F)) << 8
    pr_l = ((data[0] & 0x02) << 6) | (data[2] & 0x7F)
    ###########################################################################
    return str(pr_h | pr_l)


def nibp_status(data):  # 0x24
    ''' Returns the NIBP measurement information '''
    # data[0] : HEAD
    # data[1] : NIBP status
    # data[2] : NIBP auto period
    # data[3] : Error code
    # data[4] : Next measure time high
    # data[5] : Next measure time low
    # data[6] : CHECKSUM

    # NIBP status:
    # BIT    description
    # 7:6    Reserved
    # 5:4    Patient type, 00: adult; 01: pediatric, 02: neonate.
    # 3:0    0: NIBP reset OK;
    # 1      manual mode;
    # 2      manual mode;
    # 3      STAT mode;
    # 4      calibration;
    # 5      pneumatic;
    # 6      NIBP resetting;
    # 10     error, details see Error code.

    # NIBP auto period:
    # 0: manual mode;             8: 30 minute in auto mode;
    # 1: 1 minute in auto mode;   9: 1 hour in auto mode;
    # 2: 1 minute in auto mode;   10: 1.5 hour in auto mode;
    # 3: 3 minute in auto mode;   11: 2 hour in auto mode;
    # 4: 4 minute in auto mode;   12: 3 hour in auto mode;
    # 5: 5 minute in auto mode;   13: 4 hour in auto mode;
    # 6: 10 minute in auto mode;  14: 8 hour in auto mode;
    # 7: 15 minute in auto mode;  15: STAT mode.

    # NIBP error code:
    # Code    Description
    # 0       No error
    # 1       Cuff loose
    # 2       Leakage
    # 3       Pressure wrong
    # 4       Weak signal
    # 5       Data range error
    # 6       Arm movement
    # 7       Over pressure
    # 8       Signal saturate
    # 9       Pneumatic test fail
    # 10      Fatal error
    # 11      Over time

    # NIBP next measure time: short, unit: second.

    # 0x01 : 0000 0001
    # 0x02 : 0000 0010
    # 0x04 : 0000 0100
    # 0x08 : 0000 1000
    # 0x0F : 0000 1111
    # 0x10 : 0001 0000
    # 0x20 : 0010 0000
    # 0X30 : 0011 0000
    # 0x40 : 0100 0000
    # 0x7F : 0111 1111
    ###########################################################################
    nibp_status = str(data[1] & 0x0F)
    patient_type = str((data[1] & 0x30) >> 4)
    auto_period = str(data[2] & 0x0F)
    error_code = str(data[3] & 0x0F)
    next_measure_h = ((data[0] & 0x08) << 4) | (data[4] & 0x7F) << 8
    next_measure_l = ((data[0] & 0x10) << 3) | (data[5] & 0x7F)
    status = nibp_status+'S'+patient_type+'S'+auto_period+error_code
    ###########################################################################
    return str(next_measure_h | next_measure_l)+'*'+status
