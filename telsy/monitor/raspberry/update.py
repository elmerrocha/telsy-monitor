'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v29.03.2022
Ing. Elmer Rocha Jaime
'''

from subprocess import getoutput
from os import system
from time import sleep

URI = 'https://github.com/elmerrocha/telsy-monitor.git'
# URI = 'origin'

def update_firmware():
    ''' Update firmware searching last commit '''
    local_version  = getoutput('git rev-parse HEAD')
    remote_version = getoutput('git ls-remote '+URI).split('\t')[0]
    updatable = local_version!=remote_version
    if updatable:
        print("Different version")
        # system('git reset --hard')
        system('git pull origin')
    else:
        print('Same version')

def update_info():
    ''' Return git version information '''
    local_version  = getoutput('git rev-parse HEAD')
    remote_version = getoutput('git ls-remote '+URI).split('\t')[0]
    updatable = local_version!=remote_version
    system('git fetch --all')
    info = {
            'updatable': updatable,
            'localVersion': local_version[0:10],
            'localDate': getoutput('git show -s --format=%cD')[0:25],
            'remoteVersion': remote_version[0:10],
            'remoteDate': getoutput('git log -1 --format=%cD origin')[0:25]
        }
    return info
