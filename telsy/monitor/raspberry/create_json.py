'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v25.03.2022
Ing. Elmer Rocha Jaime
'''

from datetime import datetime
from locale import setlocale, LC_ALL
from pytz import timezone

file = open('./monitor/raspberry/data/data.txt','r', encoding='utf-8')
ecg_txt = open('./monitor/raspberry/data/ecg.txt','r', encoding='utf-8')
json_txt = open('./monitor/raspberry/data/data.json','w', encoding='utf-8')
json_txt.write('{')
wave = ecg_txt.read()
ECG_WAVE = wave.rstrip(wave[-1])
ecg_txt.close()

lines_file = file.readlines()
length_file = len(lines_file)-1
file.close()
spo2 = []
rr = []
nibp = []
ecg = []
LOCAL = setlocale(LC_ALL, 'es_CO.UTF-8')
current_date = datetime.now(timezone('America/Bogota')).strftime('%d/%m/%Y')

for i in range(length_file,0,-1):
    if lines_file[i].find('RR') == 0:
        rr.append(lines_file[i].replace('\n','').replace('RR,',''))
    elif lines_file[i].find('SPO2') == 0:
        spo2.append(lines_file[i].replace('\n','').replace('SPO2,',''))
    elif lines_file[i].find('NIBP') == 0:
        nibp.append(lines_file[i].replace('\n','').replace('NIBP,',''))
    ecg.append(int(ECG_WAVE[i*5:(i*5)+4]))

if len(rr) == 0:
    rr.append('0')
if len(spo2) == 0:
    spo2.append('0S0')
if len(nibp) == 0:
    nibp.append('0S0S0')
if int(sum(ecg)/len(ecg)) == 2048:
    ECG_WAVE = '0'

if int(rr[2])>200:
    JSON_RR = '0'
else:
    JSON_RR = rr[2]
if int(spo2[2].split('S')[1]) > 200:
    json_spo2 = ['0','0']
else:
    json_spo2 = spo2[2].split('S')
json_nibp = nibp[0].split('S')

pressure = ',"Systolic":'+json_nibp[0]+',"Diastolic":'+json_nibp[1]+',"MAP":'+json_nibp[2]
json_txt.write('"RR":'+JSON_RR+',"SPO2":'+json_spo2[0]+
',"Pulse":'+json_spo2[1]+pressure+',"Date":"'+current_date+
'","ECG":"'+ECG_WAVE+'"')
json_txt.write('}')
json_txt.close()
