'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v25.04.2022
Ing. Elmer Rocha Jaime
'''

from subprocess import getoutput

def get_information():
    ''' Return Raspberry Pi information '''
    ifconfig = getoutput('ifconfig')
    eth0 = ifconfig.find('eth0:')
    wlan0 = ifconfig.find('wlan0:')
    ethernet = ifconfig[eth0:eth0+250]
    wifi = ifconfig[wlan0:wlan0+250]
    raspberry_ip, raspberry_mac, connection = '', '', False
    if ethernet.find('inet ') > 0:
        connection = True
        inet = ethernet.find('inet ')
        netmask = ethernet.find('  netmask')
        ether = ethernet.find('ether ')
        raspberry_mac = ethernet[ether+6:ether+23]
        raspberry_ip = ethernet[inet+5:netmask]
    elif wifi.find('inet ') > 0:
        connection = True
        inet = wifi.find('inet ')
        netmask = wifi.find('  netmask')
        ether = wifi.find('ether ')
        raspberry_ip = wifi[inet+5:netmask]
        raspberry_mac = wifi[ether+6:ether+23]
    return {'connection':connection, 'ip':raspberry_ip, 'mac':raspberry_mac}
