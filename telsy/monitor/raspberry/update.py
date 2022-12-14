'''
Fundación Cardiovascular de Colombia
Dirección de Innovación y Desarrollo Tecnológico
Proyecto Telsy
Telsy Hogar v14.12.2022
Ing. Elmer Rocha Jaime
'''

from subprocess import getoutput
from os import system
from monitor.raspberry.gitlab_key import get_gitlab_key

URI = 'https://telsyupdate:'+get_gitlab_key()+'@gitlab.com/businesslab/telsy-monitor.git'
# URI = 'origin'


def update_firmware():
    ''' Update firmware searching last commit '''
    local_version = getoutput('git rev-parse HEAD')
    remote_version = getoutput('git ls-remote '+URI+' | grep dev').split('\t')[0]
    updatable = local_version != remote_version
    if updatable:
        system('git reset --hard')
        system('rm -rf ~/.cache/chromium/')
        system('git pull origin')


def update_info():
    ''' Return git version information '''
    local_version = getoutput('git rev-parse HEAD')
    remote_version = getoutput('git ls-remote '+URI+' | grep dev').split('\t')[0]
    updatable = local_version != remote_version
    can_update = updatable and (remote_version[0:10] != 'fatal: una')
    system('git fetch --all')
    info = {
        'updatable': can_update,
        'localVersion': local_version[0:10],
        'localDate': translate(getoutput('git show -s --format=%cD')),
        'remoteVersion': remote_version[0:10],
        'remoteDate': translate(getoutput('git log -1 --format=%cD origin/dev'))
    }
    return info


def translate(date_to_translate):
    ''' Returns date in Spanish language '''
    day = date_to_translate.split(' ')[0].replace(',','')
    month = date_to_translate.split(' ')[2]
    days = {
        'Mon': 'Lun',
        'Tue': 'Mar',
        'Wed': 'Mié',
        'Thu': 'Jue',
        'Fri': 'Vie',
        'Sat': 'Sáb',
        'Sun': 'Dom'
    }
    months = {
        'Jan': 'Ene',
        'Feb': 'Feb',
        'Mar': 'Mar',
        'Apr': 'Abr',
        'May': 'May',
        'Jun': 'Jun',
        'Jul': 'Jul',
        'Aug': 'Ago',
        'Sep': 'Sep',
        'Oct': 'Oct',
        'Nov': 'Nov',
        'Dec': 'Dic'
    }
    new_date = date_to_translate[0:25]
    if (day in days):
        new_date = new_date.replace(day, days.get(day))
    if (month in months):
        new_date = new_date.replace(month, months.get(month))
    return new_date
