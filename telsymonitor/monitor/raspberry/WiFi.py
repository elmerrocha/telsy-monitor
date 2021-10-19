## Fundacion Cardiovascular de Colombia
## Proyecto Telsy Hogar
## Ing. Elmer Rocha Jaime

""" Here it looks for nearby networks and creates the permanent WiFi connection on the Raspberry """
from subprocess import Popen, PIPE
from wifi import Cell
from os import system
from time import sleep

def Connect(ssid, passkey):
	""" Establish Wi-Fi connection """
	p1 = Popen(["wpa_passphrase", ssid, passkey], stdout=PIPE)
	p2 = Popen(["sudo", "tee", "-a", "/etc/wpa_supplicant/wpa_supplicant.conf", "./monitor/raspberry/data/>", "/dev/null"], stdin=p1.stdout, stdout=PIPE)
	p1.stdout.close()
	#err = p2.communicate()
	system("sudo wpa_cli -i wlan0 reconfigure > /dev/null")

def Scan():
	""" Search nearby networks """
	Networks = []
	nets = list(Cell.all('wlan0'))

	for x in nets:
		r = str(x).replace(")","").replace("Cell(ssid=","")
		Networks.append(r)

	return Networks
