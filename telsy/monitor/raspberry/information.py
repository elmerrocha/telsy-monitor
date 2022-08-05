'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v05.08.2022
Ing. Elmer Rocha Jaime
'''

from subprocess import getoutput


def get_information():
    ''' Return Raspberry Pi information '''
    ifconfig = getoutput('ifconfig')
    eth0 = ifconfig.find('eth0:')
    wlan0 = ifconfig.find('wlan0:')
    wwan0 = ifconfig.find('wwan0:')
    ethernet = ifconfig[eth0:eth0+250]
    wifi = ifconfig[wlan0:wlan0+250]
    gprs_4g = ifconfig[wwan0:wwan0+250]
    type, raspberry_ip, raspberry_mac, connection = '', '', '', False
    if ethernet.find('inet ') > 0:
        type = 'ethernet'
        connection = True
        inet = ethernet.find('inet ')
        netmask = ethernet.find('  netmask')
        ether = ethernet.find('ether ')
        raspberry_mac = ethernet[ether+6:ether+23]
        raspberry_ip = ethernet[inet+5:netmask]
    elif wifi.find('inet ') > 0:
        type = 'wifi'
        connection = True
        inet = wifi.find('inet ')
        netmask = wifi.find('  netmask')
        ether = wifi.find('ether ')
        raspberry_ip = wifi[inet+5:netmask]
        raspberry_mac = wifi[ether+6:ether+23]
    elif gprs_4g.find('inet ') > 0:
        type = 'gprs'
        connection = True
        inet = ethernet.find('inet ')
        netmask = ethernet.find('  netmask')
        raspberry_ip = ethernet[inet+5:netmask]
    response = {
        'type': type,
        'connection': connection,
        'ip': raspberry_ip,
        'mac': raspberry_mac
    }
    return response
