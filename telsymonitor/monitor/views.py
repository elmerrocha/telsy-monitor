from django.shortcuts import render
from json import load
from subprocess import Popen
from time import sleep
from os import getcwd, system
from pathlib import Path
TakeNIBP = False
keyboardFlarg = True

def IsRaspbian():
    CurrentPath = getcwd().replace('\\','/')
    if (CurrentPath[0:6] == '/home/'): return True
    else: return False
if IsRaspbian():
    from monitor.raspberry import WiFi
    from monitor.raspberry.X728 import readCapacity
    if keyboardFlarg:
        Popen(['python3', './monitor/raspberry/KeyboardGPIO.py'])
        keyboardFlarg = False
def Cancel(request):
    if IsRaspbian():
        Popen(['python3', './monitor/raspberry/MeasureC.py'])
    else:
        print('Cancel')
    return render(request,'cancel.html')

def Connected(request):
    Net = request.POST["NetName"]
    Pass = request.POST["PassNet"]
    if IsRaspbian():
        try:
            WiFi.Connect(Net,Pass)
        except Exception:
            return render(request, 'menu.html')
    else:
        print(Net,Pass)
    WiFiNets = {"Net":Net}
    return render(request,'connected.html', WiFiNets)

def Connecting(request, net):
    WiFiNetwork = {"SSID":net}
    return render(request,'connecting.html',WiFiNetwork)

def Data(request):
    return render(request,'data.html')

def Exercise(request):
    return render(request,'exercise.html')

def Goals(request):
    return render(request,'goals.html')

def GoalsD(request):
    return render(request,'goalsd.html')

def GoalsV(request):
    return render(request,'goalsv.html')

def Home(request):
    if request.method=='POST':
        if (request.POST['Clock'] != '0'):
            Data = request.POST['Clock'].split('T')
            Time = "'"+Data[0]+' '+Data[1].split('.')[0]+"'"
            print(Time)
            if IsRaspbian(): system('date --set '+Time)
    if IsRaspbian():
        try:
            cap:readCapacity()
        except Exception:
            cap = 100
        return render(request,'home.html',{"BatteryCap":cap})
    else: return render(request,'home.html',{"BatteryCap":100})

def Index(request):
    return render(request,'index.html')

def Login(request):
    return render(request,'login.html')

def Measuring(request):
    global TakeNIBP
    TakeNIBP = bool(int(request.POST["NIBP"]))
    if IsRaspbian():
        if TakeNIBP:
            Popen(['python3', './monitor/raspberry/MeasureY.py'])
        else:
            Popen(['python3', './monitor/raspberry/MeasureN.py'])
    else:
        if TakeNIBP:
            print("It will take NIBP")
        else:
            print("It won't take NIBP")
    return render(request,'measuring.html')

def Medicaments(request):
    return render(request,'medicaments.html')

def Medicine(request):
    return render(request,'medicine.html')

def Menu(request):
    return render(request,'menu.html')

def Monitor(request):
    return render(request,'monitor.html')

def Monitoring(request):
    return render(request,'monitoring.html')

def MonitoringInfo(request):
    return render(request,'monitoringinfo.html')

def MonitoringInfoV(request):
    return render(request,'monitoringinfov.html')

def Network(request):
    if IsRaspbian():
        try:
            networks = WiFi.Scan()
        except Exception:
            sleep(2)
            return render(request, 'network.html')
    else:
        networks = ["Red 0", "Red A", "Red X", "Red F", "Red 4", "Red 5", "Red 6", "Red 7", "Red 8", "Red 9", "Red 10"]
    WiFiNetworks = {"networks":networks}
    return render(request,'network.html', WiFiNetworks)

def Results(request):
    while (TakeNIBP and not Path('./monitor/raspberry/data/NIBP.end').is_file()):
        pass
    if IsRaspbian():
        if(Path('./monitor/raspberry/data/NIBP.end').is_file()): system('rm -f ./monitor/raspberry/data/NIBP.end')
        Popen(['python3', './monitor/raspberry/CreateJSON.py']).wait()
        sleep(1.5)
    with open('./monitor/raspberry/data/data.json') as file:
        ResultsData = load(file)
    return render(request,'results.html',ResultsData)

def Symptoms(request):
    return render(request,'symptoms.html')

def User(request):
    return render(request,'user.html')

def Weigth(request):
    return render(request,'weigth.html')

def WeigthC(request):
    return render(request,'weigthc.html')