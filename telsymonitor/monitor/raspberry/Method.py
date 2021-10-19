## Fundacion Cardiovascular de Colombia
## Proyecto Telsy Hogar
## Ing. Elmer Rocha Jaime

def Length(Size):
    """ Returns the number of bytes to read depending on the type of data """
    Length = {
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
    return Length.get(Size)-1

def Is_Parameter(Element):
    """ Returns boolean value if the input is a parameter """
    X = Convert(Element)
    Parameters = [
        0x01, #Reset
        0x03, #Post
        0x04, #Acknowledge
        0x05, #ECG wave
        0x06, #ECG status
        0x07, #HR
        0x0A, #ARR
        0x0B, #ST
        0x10, #RESP wave
        0x11, #RR
        0x12, #APNEA
        0x15, #TEMP
        0x16, #SPO2 wave
        0x17, #SPO2 value
        0x20, #NIBP Cuff
        0x21, #NIBP end
        0x22, #NIBP result1
        0x23, #NIBP result2
        0x24  #NIBP status
    ]

    return X in Parameters

def Convert(Data):
    """ Converts the data in bytes to integer """
    return int.from_bytes(Data, byteorder='big', signed=False)

def ECG_Wave(Data):
    """ Returns the waveforms of the ECG signal """
    #Data[0] : HEAD
    #Data[1] : ECG channel 1 wave, high byte
    #Data[2] : ECG channel 1 wave, low byte
    #Data[3] : ECG channel 2 wave, high byte
    #Data[4] : ECG channel 2 wave, low byte
    #Data[5] : ECG channel 3 wave, high byte
    #Data[6] : ECG channel 3 wave, low byte
    #Data[7] : CHECKSUM

    #ECG 1,ECG2, ECG3 wave: unsigned char, wave baseline is 2048, data range: 0-4096.
    #ECG channel 1: lead II, ECG channel 2: lead I, ECG channel 3: lead V.
    #Other ECG lead calculation formula:
    #III = II-I
    #AVR = -(I+II)/2
    #AVL = I-II/2=(I-III)/2
    #AVF = II-I/2=(II+III)/2

    #Pace & beat flag is BIT 7 & 6 in ECG channel 1 wave, high byte:
    #BIT Description
    #7   Pace flag（0: false, 1: true)
    #6   Heart beat flag（0: false, 1: true)

    #0x01 : 0000 0001
    #0x02 : 0000 0010
    #0x04 : 0000 0100
    #0x08 : 0000 1000
    #0x10 : 0001 0000
    #0x20 : 0010 0000
    #0x3F : 0011 1111
    #0x40 : 0100 0000
    #0x7F : 0111 1111
    #################################################################################
    Pace_flarg = Data[0] & 0x01
    Heart_beate_flarg = Data[1] & 0x40
    ECG1_H =   (Data[1] & 0x3F) << 8
    ECG1_L =  ((Data[0] & 0x02)<<6) | (Data[2] & 0x7F)
    ECG2_H = (((Data[0] & 0x04)<<5) | (Data[3] & 0x7F)) << 8
    ECG2_L =  ((Data[0] & 0x08)<<4) | (Data[4] & 0x7F)
    ECG3_H = (((Data[0] & 0x10)<<3) | (Data[5] & 0x7F)) << 8
    ECG3_L =  ((Data[0] & 0x20)<<2) | (Data[6] & 0x7F)
    #################################################################################
    Flargs = str(Pace_flarg) + "S" + str(Heart_beate_flarg)
    #return str(ECG1_H | ECG1_L) + "S" + str(ECG2_H | ECG2_L) + "S" + str(ECG3_H | ECG3_L) + "S" + Flargs
    return str(ECG1_H | ECG1_L)

def ECG_Status(Data):
    """ Return the lead status of ECG """
    #Data[0] : HEAD
    #Data[1] : Status
    #Data[2] : Saturate
    #Data[3] : CHECKSUM

    #Status:
    #BIT     description
    #7:4     Reserved
    #3       V （1: lead off, 0: lead OK）
    #2       RA（1: lead off, 0: lead OK）
    #1       LA（1: lead off, 0: lead OK）
    #0       LL（1: lead off, 0: lead OK）
    #Saturate:
    #BIT     description
    #7:4     Reserved
    #3       Lead V （1: Saturate, 0: lead OK）
    #2       Lead III（1: Saturate, 0: lead OK）
    #1       Lead I（1: Saturate. 0: lead OK）
    #0       Lead II（1: Saturate 0: lead OK

    #0x01 : 0000 0001
    #0x02 : 0000 0010
    #0x04 : 0000 0100
    #0x08 : 0000 1000
    #################################################################################
    Lead_LL = Data[1] & 0x01
    Lead_LA = Data[1] & 0x02
    Lead_RA = Data[1] & 0x04
    Lead_V  = Data[1] & 0x08
    Lead_II = Data[2] & 0x01
    Lead_I  = Data[2] & 0x02
    Lead_III= Data[2] & 0x04
    Lead_V1 = Data[2] & 0x08
    #################################################################################
    LeadTxt1 = str(Lead_LL) + "S" + str(Lead_LA) + "S" + str(Lead_RA) + "S" + str(Lead_V)
    LeadTxt2 = str(Lead_II) + "S" + str(Lead_I) + "S" + str(Lead_III) + "S" + str(Lead_V1)
    return LeadTxt1 + LeadTxt2

def Heart_Rate(Data):
    """ Returns the heart rate value """
    #Data[0] : HEAD
    #Data[1] : HR high byte
    #Data[2] : HR low byte
    #Data[3] : R pos high byte
    #Data[4] : R pos low byte
    #Data[5] : CHECKSUM

    #HR(heart rate): short, data range: adult/pediatric 0-300BPM, neonate: 0-350BPM, -100 means invalid value.
    #R pos: QRS position: short, means the QRS wave time, the unit is 4ms, e.g., 250 mean 1 second before current packet time.

    #0x01 : 0000 0001
    #0x02 : 0000 0010
    #0x04 : 0000 0100
    #0x08 : 0000 1000
    #0x7F : 0111 1111
    #################################################################################
    HR_H = (((Data[0] & 0x01)<<7) | (Data[1] & 0x7F)) << 8
    HR_L =  ((Data[0] & 0x02)<<6) | (Data[2] & 0x7F)
    R_H  = (((Data[0] & 0x04)<<5) | (Data[3] & 0x7F)) << 8
    R_L  =  ((Data[0] & 0x08)<<4) | (Data[4] & 0x7F)
    #################################################################################
    return str(HR_H | HR_L) + "S" + str(R_H | R_L)

def Arrhythmia(Data):
    """ Returns an arrhythmia code and the position in time where it occurs """
    #Data[0] : HEAD
    #Data[1] : ARR type
    #Data[2] : ARR position high byte
    #Data[3] : ARR position low byte
    #Data[4] : CHECKSUM

    #ARR type code:
    #1: Asystole
    #2: Vent Tatchy/FIB
    #3: R on T
    #4: RUN
    #5: Couplet
    #6: PVC
    #7: Bigeminy
    #8: Trigeminy
    #9: Tachy
    #10: Brady
    #11: PNC, Pace not capture
    #12: PNP, Pace no paced
    #13: Miss Beat
    #14: ARR learn
    #15: normal QRS
    #16: Noise
    #17: weak signal
    #ARR position: short, means the arrhythmia event occur time, the unit is 4ms, e.g., 250 mean 1 second before.

    #0x01 : 0000 0001
    #0x02 : 0000 0010
    #0x04 : 0000 0100
    #0x7F : 0111 1111
    #################################################################################
    ARRType  =  ((Data[0] & 0x01)<<7) | (Data[1] & 0x7F)
    ARRPos_H = (((Data[0] & 0x02)<<6) | (Data[2] & 0x7F)) << 8
    ARRPos_L =  ((Data[0] & 0x04)<<5) | (Data[3] & 0x7F)
    #################################################################################
    return str(ARRType) + "S" + str(ARRPos_H | ARRPos_L)

def ST_Amplitude(Data):
    """ Returns the amplitude of the three ECG signal channels """
    #Data[0] : HEAD
    #Data[1] : ST1 high byte
    #Data[2] : ST1 low byte
    #Data[3] : ST2 high byte
    #Data[4] : ST2 low byte
    #Data[5] : ST3 high byte
    #Data[6] : ST3 low byte
    #Data[7] : CHECKSUM

    #0x01 : 0000 0001
    #0x02 : 0000 0010
    #0x04 : 0000 0100
    #0x08 : 0000 1000
    #0x10 : 0001 0000
    #0x20 : 0010 0000
    #0x7F : 0111 1111
    #################################################################################
    ST1_H = (((Data[0] & 0x01)<<7) | (Data[1] & 0x7F)) << 8
    ST1_L =  ((Data[0] & 0x02)<<6) | (Data[2] & 0x7F)
    ST2_H = (((Data[0] & 0x04)<<5) | (Data[3] & 0x7F)) << 8
    ST2_L =  ((Data[0] & 0x08)<<4) | (Data[4] & 0x7F)
    ST3_H = (((Data[0] & 0x10)<<3) | (Data[5] & 0x7F)) << 8
    ST3_L =  ((Data[0] & 0x20)<<2) | (Data[6] & 0x7F)
    #################################################################################
    return str((ST1_H | ST1_L)/100) + "S" + str((ST2_H | ST2_L)/100) + "S" + str((ST3_H | ST3_L)/100)

def Respiration_Wave(Data):
    """ Returns the waveform of the respiration """
    #Data[0] : HEAD
    #Data[1] : RESP wave
    #Data[2] : CHECKSUM

    # RESP wave: data range 0-256, base line is 128.

    #0x01 : 0000 0001
    #0x7F : 0111 1111
    #################################################################################
    RespW = (((Data[0] & 0x01)<<7) | (Data[1] & 0x7F))
    #################################################################################
    return str(RespW)

def Respiration_Rate(Data):
    """ Returns the respiration rate value """
    #Data[0] : HEAD
    #Data[1] : RR high byte
    #Data[2] : RR low byte
    #Data[3] : CHECKSUM

    #RR(respiration rate): short, data range: adult: 0-120BrPM, Pediatric/Neonate 0-150BrPM, 100 means invalid. 0 means apnea.

    #0x01 : 0000 0001
    #0x02 : 0000 0010
    #0x7F : 0111 1111
    #################################################################################
    RR_H = (((Data[0] & 0x01)<<7) | (Data[1] & 0x7F)) << 8
    RR_L =  ((Data[0] & 0x02)<<6) | (Data[2] & 0x7F)
    #################################################################################
    return str(RR_H | RR_L)

def Temperature(Data):
    """ Returns the temperature value """
    #Data[0] : HEAD
    #Data[1] : Sensor states
    #Data[2] : TEMP1 high byte
    #Data[3] : TEMP1 low byte
    #Data[4] : TEMP2 high byte
    #Data[5] : TEMP2 low byte
    #Data[6] : CHECKSUM

    #Sensor  status:
    #BIT     description
    #7:2     Reserved
    #1       Sensor 2 （0 connected, 1 sensor off）
    #0       Sensor 1 （0 connected, 1 sensor off）
    #TEMP1 & TEMP2 value: short, data range: 0-500. Unit: 0.1C. e.g. 204 mean 20.4C. -100 means invalid.

    #0x01 : 0000 0001
    #0x02 : 0000 0010
    #0x04 : 0000 0100
    #0x08 : 0000 1000
    #0x10 : 0001 0000
    #0x7F : 0111 1111
    #################################################################################
    T1_S = Data[1] & 0x01
    T2_S = Data[1] & 0x02
    T1_H = (((Data[0] & 0x02)<<6) | (Data[2] & 0x7F)) << 8
    T1_L =  ((Data[0] & 0x04)<<5) | (Data[3] & 0x7F)
    T2_H = (((Data[0] & 0x08)<<4) | (Data[4] & 0x7F)) << 8
    T2_L =  ((Data[0] & 0x10)<<3) | (Data[5] & 0x7F)
    #################################################################################
    return str(T1_H | T1_L) + "S" + str(T2_H | T2_L) + "S" + str(T1_S) + "S" + str(T2_S)

def SPO2_Wave(Data):
    """ Returns the waveform of the SPO2 signal """
    #Data[0] : HEAD
    #Data[1] : SPO2 wave
    #Data[2] : SPO2 status
    #Data[3] : CHECKSUM

    #SPO2 wave: unsigned char, data range: 0-255.
    #SPO2 status:
    #BIT     description
    #7       SPO2 finger off flag
    #6       Pulse flag
    #5       Search pulse flag
    #4       SPO2 sensor off flag
    #3:0     SPO2 bar graph,0-15

    #0x01 : 0000 0001
    #0x02 : 0000 0010
    #0x0F : 0000 1111
    #0x10 : 0001 0000
    #0x20 : 0010 0000
    #0x40 : 0100 0000
    #0x7F : 0111 1111
    #################################################################################
    SPO2W = ((Data[0] & 0x01)<<7) | (Data[1] & 0x7F)
    BarGraph = Data[2] & 0x0F
    SensorStatus = Data[2] & 0x10
    SearchFlarg = Data[2] & 0x20
    PulseFlarg = Data[2] & 0x40
    Finger = Data[0] & 0x02
    #################################################################################
    return str(SPO2W)+"S"+str(BarGraph)+"S"+str(SensorStatus)+"S"+str(SearchFlarg)+"S"+str(PulseFlarg)+"S"+str(Finger)

def SPO2(Data):
    """ Returns pulse rate and oxygen saturation percentage """
    #Data[0] : HEAD
    #Data[1] : Spo2 information
    #Data[2] : PR high byte
    #Data[3] : PR low byte
    #Data[4] : Spo2
    #Data[5] : CHECKSUM

    #Spo2 information:
    #BIT     description
    #7:6     Reserved
    #5       Spo2 drop flag
    #4       Search too long flag
    #3:0     Signal strength(0-8, 15 means invalid)
    #PR(pulse rate): short, data range: 0-255BPM, -100 means invalid.
    #Spo2: data range: 0～100%, -100 means invalid.

    #0x02 : 0000 0010
    #0x04 : 0000 0100
    #0x08 : 0000 1000
    #0x7F : 0111 1111
    #################################################################################
    PR_H = (((Data[0] & 0x02)<<6) | (Data[2] & 0x7F)) << 8
    PR_L =  ((Data[0] & 0x04)<<5) | (Data[3] & 0x7F)
    SPO2 =  ((Data[0] & 0x08)<<4) | (Data[4] & 0x7F)
    #################################################################################
    return str(SPO2) + "S" + str(PR_H | PR_L)

def NIBP_Cuff(Data):
    """ Returns current cuff pressure """
    #Data[0] : HEAD
    #Data[1] : Cuff high byte
    #Data[2] : Cuff low byte
    #Data[3] : Cuff type wrong flag
    #Data[4] : Measure mode
    #Data[5] : CHECKSUM

    #Cuff pressure: short, data range: 0-300mmHg, -100 means invalid.
    #NIBP Cuff type wrong flag:
    #0: OK; 1: wrong type of Cuff used.
    #Host should stop NIBP measure when received this flag.
    #NIBP measure mode:
    #1: manual mode;
    #2: auto mode;
    #3: STAT mode;
    #4: calibration;
    #5: pneumatic;

    #0x01 : 0000 0001
    #0x02 : 0000 0010
    #0x7F : 0111 1111
    #################################################################################
    Cuff_H = (((Data[0] & 0x01)<<7) | (Data[1] & 0x7F)) << 8
    Cuff_L =  ((Data[0] & 0x02)<<6) | (Data[2] & 0x7F)
    WrongFlag = Data[3] & 0x01
    MeasureMode = Data[3] & 0x7F
    #################################################################################
    return str(Cuff_H | Cuff_L) + "S" + str(WrongFlag) + "S" + str(MeasureMode)

def NIPB_End(Data):
    """ Returns end mode of blood pressure measure """
    #Data[0] : HEAD
    #Data[1] : Data
    #Data[2] : CHECKSUM

    #NIBP end mode:
    #1 : end in manual mode;
    #2 : end in auto mode;
    #3 : end in STAT mode;
    #4 : end in calibration mode;
    #5 : end in pneumatic mode;
    #10: error, detail information in NIBP status frame (0x24)

    #0x01 : 0000 0001
    #0x7F : 0111 1111
    return ((Data[0] & 0x01)<<7) | (Data[1] & 0x7F)

def NIBP_Results(Data):
    """ Returns the NIBP results (systolic, diastolic and mean pressure) """
    #Data[0] : HEAD
    #Data[1] : Systolic high byte
    #Data[2] : Systolic low byte
    #Data[3] : Diastolic high byte
    #Data[4] : Diastolic low byte
    #Data[5] : Mean high byte
    #Data[6] : Mean low byte
    #Data[7] : CHECKSUM

    #Systolic, diastolic, mean: short, data range: 0-300mmHg. -100 means invalid

    #0x01 : 0000 0001
    #0x02 : 0000 0010
    #0x04 : 0000 0100
    #0x08 : 0000 1000
    #0x10 : 0001 0000
    #0x20 : 0010 0000
    #0x7F : 0111 1111
    #################################################################################
    Sys_H = (((Data[0] & 0x01)<<7) | (Data[1] & 0x7F)) << 8
    Sys_L =  ((Data[0] & 0x02)<<6) | (Data[2] & 0x7F)
    Dia_H = (((Data[0] & 0x04)<<5) | (Data[3] & 0x7F)) << 8
    Dia_L =  ((Data[0] & 0x08)<<4) | (Data[4] & 0x7F)
    MeadH = (((Data[0] & 0x10)<<3) | (Data[5] & 0x7F)) << 8
    MeadL =  ((Data[0] & 0x20)<<2) | (Data[6] & 0x7F)
    #################################################################################
    return str(Sys_H | Sys_L) + "S" + str(Dia_H | Dia_L) + "S" + str(MeadH | MeadL)

def NIBP_PulseRate(Data):
    """ Returns the heart rate value by NIBP """
    #Data[0] : HEAD
    #Data[1] : PR high byte
    #Data[2] : PR low byte
    #Data[3] : CHECKSUM

    #PR (pulse rate): short, -100 means invalid

    #0x01 : 0000 0001
    #0x02 : 0000 0010
    #0x7F : 0111 1111
    #################################################################################
    PR_H = (((Data[0] & 0x01)<<7) | (Data[1] & 0x7F)) << 8
    PR_L =  ((Data[0] & 0x02)<<6) | (Data[2] & 0x7F)
    #################################################################################
    return str(PR_H | PR_L)
