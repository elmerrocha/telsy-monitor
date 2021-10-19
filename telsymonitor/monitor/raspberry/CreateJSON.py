## Fundacion Cardiovascular de Colombia
## Proyecto Telsy Hogar
## Ing. Elmer Rocha Jaime

from datetime import datetime
from locale import setlocale, LC_ALL
from pytz import timezone

File = open('./monitor/raspberry/data/data.txt','r')
TxtECG = open('./monitor/raspberry/data/ecg.txt','r')
TxtJSON = open('./monitor/raspberry/data/data.json','w')
TxtJSON.write('{')
Wave = TxtECG.read()
ECGWave = Wave.rstrip(Wave[-1])
TxtECG.close()

FileLines = File.readlines()
FileLength = len(FileLines)-1
File.close()
SPO2 = []
RR = []
NIBP = []
ECG = []
Local = setlocale(LC_ALL, 'es_CO.UTF-8')
Date = datetime.now(timezone("America/Bogota")).strftime("%d/%m/%Y")

for i in range(FileLength,0,-1):
    if(FileLines[i].find('RR') == 0):
        RR.append(FileLines[i].replace('\n','').replace('RR,',''))
    elif(FileLines[i].find('SPO2') == 0):
        SPO2.append(FileLines[i].replace('\n','').replace('SPO2,',''))
    elif(FileLines[i].find('NIBP') == 0):
        NIBP.append(FileLines[i].replace('\n','').replace('NIBP,',''))
    ECG.append(int(ECGWave[i*5:(i*5)+4]))

if(len(RR) == 0): RR.append('0')
if(len(SPO2) == 0): SPO2.append('0S0')
if(len(NIBP) == 0): NIBP.append('0S0S0')
if(int(sum(ECG)/len(ECG)) == 2048): ECGWave = '0'

if(int(RR[2])>200): JRR = '0'
else: JRR = RR[2]
if(int(SPO2[2].split('S')[1])>200): JSPO2 = ['0','0']
else: JSPO2 = SPO2[2].split('S')
JNIPB = NIBP[0].split('S')

Pressure = ',"Systolic":'+JNIPB[0]+',"Diastolic":'+JNIPB[1]+',"MAP":'+JNIPB[2]
TxtJSON.write('"RR":'+JRR+',"SPO2":'+JSPO2[0]+',"Pulse":'+JSPO2[1]+Pressure+',"Date":"'+Date+'","ECG":"'+ECGWave+'"')
TxtJSON.write('}')
TxtJSON.close()
