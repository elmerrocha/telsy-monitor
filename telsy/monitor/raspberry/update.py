'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v23.03.2022
Ing. Elmer Rocha Jaime
'''

from subprocess import getoutput
from os import system

# URI = 'https://github.com/elmerrocha/telsy-monitor.git'
URI = 'origin'
LOCAL_VERSION  = getoutput('git rev-parse HEAD')
REMOTE_VERSION = getoutput("git ls-remote "+ URI +" # HEAD | awk '{print $1}'")
UPDATABLE = LOCAL_VERSION!=REMOTE_VERSION

def update_firmware():
    ''' Update firmware searching last commit '''
    if UPDATABLE:
        print("Different version")
        system('git pull origin')
    else:
        print('Same version')

def update_info():
    ''' Return git version information '''
    info = {
            'updatable': UPDATABLE,
            'localVersion': LOCAL_VERSION[0:10],
            'localDate': getoutput('git show -s --format=%ci')[0:10],
            'remoteVersion': REMOTE_VERSION[0:10],
            'remoteDate': getoutput('git log -1 --format=%ci origin')[0:10]
        }
    return info
