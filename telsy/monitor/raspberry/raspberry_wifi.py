'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v25.04.2022
Ing. Elmer Rocha Jaime
'''
from os import system
from subprocess import Popen, PIPE
from wifi import Cell

WPA = '/etc/wpa_supplicant/wpa_supplicant.conf'
PATH = './monitor/raspberry/data/>'

def connect(ssid, passkey):
    ''' Creates the permanent WiFi connection '''
    pipe1 = Popen(['wpa_passphrase', ssid, passkey], stdout=PIPE)
    Popen(['sudo', 'tee', '-a', WPA, PATH, '/dev/null'], stdin=pipe1.stdout, stdout=PIPE)
    pipe1.stdout.close()
    #err = p2.communicate()
    system('sudo wpa_cli -i wlan0 reconfigure > /dev/null')

def scan():
    ''' Search nearby WiFi networks '''
    networks = []
    nets = list(Cell.all('wlan0'))
    for net in nets:
        replace = str(net).replace(')','').replace('Cell(ssid=','')
        networks.append(replace)
    return networks
