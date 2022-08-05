'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v05.08.2022
Ing. Elmer Rocha Jaime
'''

from django.http import JsonResponse
from os import getcwd

# Global variables
last_capacity = 120
last_ac_status = True


def is_raspberry_pi_os():
    ''' Return a boolean value if the code is running in Raspberry OS '''
    current_path = getcwd().replace('\\', '/')
    return current_path[0:6] == '/home/'


if is_raspberry_pi_os():
    from monitor.raspberry.geekworm_x728 import read_capacity, power_supply_status


def battery(request):
    ''' Battery capacity and power supply status view '''
    global last_capacity, last_ac_status
    if is_raspberry_pi_os():
        try:
            current_capacity = read_capacity()
            current_ac_status = power_supply_status()
            res = {
                'capacity': current_capacity,
                'power_ac': current_ac_status
            }
            last_capacity = current_capacity
            last_ac_status = current_ac_status
        except OSError as exc:
            print(exc)
            res = {
                'capacity': last_capacity,
                'power_ac': last_ac_status
            }
    else:
        res = {
                'capacity': last_capacity,
                'power_ac': last_ac_status
        }
    return JsonResponse(res)
