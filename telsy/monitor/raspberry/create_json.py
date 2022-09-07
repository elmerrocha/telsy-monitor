'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v07.09.2022
Ing. Elmer Rocha Jaime
'''

from datetime import datetime
from locale import setlocale, LC_ALL
from pytz import timezone

file = open('./monitor/raspberry/data/data.txt', 'r')
ecg_txt = open('./monitor/raspberry/data/ecg.txt', 'r')
json_txt = open('./monitor/raspberry/data/data.json', 'w')
json_txt.write('{')
wave = ecg_txt.read()
ecg_wave = wave.rstrip(wave[-1])
ecg_txt.close()

lines_file = file.readlines()
length_file = len(lines_file)-1
file.close()
temp = []
spo2 = []
rr = []
nibp = []
ecg = []
LOCAL = setlocale(LC_ALL, 'es_CO.UTF-8')
current_date = datetime.now(timezone('America/Bogota')).strftime('%d/%m/%Y')

for i in range(length_file, 0, -1):
    if lines_file[i].find('RR') == 0:
        rr.append(lines_file[i].replace('\n', '').replace('RR,', ''))
    elif lines_file[i].find('TEMP') == 0:
        temp.append(lines_file[i].replace('\n', '').replace('TEMP,', ''))
    elif lines_file[i].find('SPO2') == 0:
        spo2.append(lines_file[i].replace('\n', '').replace('SPO2,', ''))
    elif lines_file[i].find('NIBP') == 0:
        nibp.append(lines_file[i].replace('\n', '').replace('NIBP,', ''))
    ecg.append(int(ecg_wave[i*5:(i*5)+4]))

if len(rr) == 0:
    rr.append('0')
    rr.append('0')
    rr.append('0')
if len(temp) ==  0:
    temp.append('0')
    temp.append('0')
    temp.append('0')
if len(spo2) == 0:
    spo2.append('0S0')
    spo2.append('0S0')
    spo2.append('0S0')
if len(nibp) == 0:
    nibp.append('0S0S0')
if len(ecg) > 0:
    if int(sum(ecg)/len(ecg)) == 2048:
        ecg_wave = '0'
else:
    ecg_wave = '0'
if int(rr[2]) > 200:
    JSON_RR = '0'
else:
    JSON_RR = rr[2]
if int(temp[2].split('*')[1].split('S')[0]) == 0:
    if float(temp[2].split('*')[0].split('S')[0]) < 50:
        json_temp = temp[2].split('*')[0].split('S')[0]
    else:
        json_temp = '0'
elif int(temp[2].split('*')[1].split('S')[1]) == 0:
    if float(temp[2].split('*')[0].split('S')[1]) < 50:
        json_temp = temp[2].split('*')[0].split('S')[1]
    else:
        json_temp = '0'
else:
    json_temp = '0'
if int(spo2[2].split('S')[1]) > 200:
    json_spo2 = ['0', '0']
else:
    json_spo2 = spo2[2].split('S')
json_nibp = nibp[0].split('S')

pressure = ',"Systolic":'+json_nibp[0]+',"Diastolic":'
pressure += json_nibp[1]+',"MAP":'+json_nibp[2]
data = '"RR":'+JSON_RR+',"SPO2":'+json_spo2[0]
data += ',"Pulse":'+json_spo2[1]+pressure
data += ',"Temperature":'+json_temp
data += ',"Date":"'+current_date+'","ECG":"'+ecg_wave+'"'
json_txt.write(data)
json_txt.write('}')
json_txt.close()
