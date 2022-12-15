'''
Fundación Cardiovascular de Colombia
Dirección de Innovación y Desarrollo Tecnológico
Proyecto Telsy
Telsy Hogar v15.12.2022
Ing. Elmer Rocha Jaime
'''

from os import getcwd, system
from subprocess import Popen, CalledProcessError, PIPE
from django.shortcuts import render
from monitor.raspberry.update import update_info
from monitor.raspberry.measure import disconnect_websocket
from django.views import View
from json import loads
from django.http import JsonResponse

# Pipe of measure subprocess
measure_pipe = 0
# Global variables
last_capacity = 120
last_ac_status = True
measure_type = ''

def is_raspberry_pi_os():
    ''' Return a boolean value if the code is running in Raspberry OS '''
    current_path = getcwd().replace('\\', '/')
    return current_path[0:6] == '/home/'


if is_raspberry_pi_os():
    from monitor.raspberry import raspberry_wifi
    from monitor.raspberry.update import update_firmware
    from monitor.raspberry.information import get_information
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


class Connected(View):
    ''' Connected class '''
    def get(self, request):
        ''' Get view from Connected '''
        return render(request, 'connected.html')

    def post(self, request):
        ''' Post view from Connected '''
        if request.body:
            network_ssid = request.POST['network-ssid']
            password = request.POST['network-password']
        if is_raspberry_pi_os():
            try:
                raspberry_wifi.connect(network_ssid, password)
            except CalledProcessError as exc:
                print(exc)
                return render(request, 'menu.html')
        else:
            print('SSID:', network_ssid, 'Password:', password)
        return render(request, 'connected.html')


def connecting(request):
    ''' Connecting WiFi view '''
    return render(request, 'connecting.html')


def data(request):
    ''' Last telecenter data view '''
    return render(request, 'data.html')


def exercise(request):
    ''' Exercise view '''
    return render(request, 'exercise.html')


def goals(request):
    ''' Goals view '''
    return render(request, 'goals.html')


def goals_details(request):
    ''' Goals details view '''
    return render(request, 'goalsd.html')


def goals_video(request):
    ''' Goals video view '''
    return render(request, 'goalsv.html')


class Home(View):
    ''' Home class '''
    def get(self, request):
        ''' Get view from Home '''
        return render(request, 'home.html')

    def post(self, request):
        ''' Post view from Home '''
        if request.body:
            post_data = request.POST['clock']
            if post_data != '0':
                date = post_data.split('T')
                time = "'"+date[0]+' '+date[1].split('.')[0]+"'"
                print('Current time:', time)
                if is_raspberry_pi_os():
                    system('date --set '+time)
        return render(request, 'home.html')


def index(request):
    ''' Initial index view '''
    return render(request, 'index.html')


def information(request):
    ''' Information view '''
    try:
        info = update_info()
        if is_raspberry_pi_os():
            information = get_information()
            info.update(information)
    except CalledProcessError as exc:
        info = {}
        print(exc)
    return render(request, 'information.html', info)


def login(request):
    ''' Login user view '''
    return render(request, 'login.html')


class Measure(View):
    ''' Measure class '''
    def get(self, request):
        ''' Get view from Measure '''
        global measure_type
        return render(request, 'measure.html', {'measure_type': measure_type})

    def options(self, request):
        ''' Options view from Measure '''
        disconnect_websocket()
        return JsonResponse({'websocket': 'disconnected'})

    def post(self, request):
        ''' Post view from Measure '''
        global measure_type
        if request.body:
            measure_type = request.POST['measure-type']
        return render(request, 'measure.html', {'measure_type': measure_type})


def medicaments(request):
    ''' Medicaments view '''
    return render(request, 'medicaments.html')


def medicine(request):
    ''' Medicine view '''
    return render(request, 'medicine.html')


def menu(request):
    ''' Menu view '''
    return render(request, 'menu.html')


def monitor(request):
    ''' Monitor view '''
    return render(request, 'monitor.html')


def monitoring(request):
    ''' Monitoring view '''
    return render(request, 'monitoring.html')


def monitoring_info(request):
    ''' Monitoring information view '''
    return render(request, 'monitoringinfo.html')


def monitoring_info_video(request):
    ''' Monitoring information video view '''
    return render(request, 'monitoringinfov.html')


def network(request):
    ''' WiFi network view '''
    if is_raspberry_pi_os():
        try:
            networks = raspberry_wifi.scan()
        except IOError as exc:
            print(exc)
            return render(request, 'network.html')
    else:
        networks = ['Red 0', 'Red 1', 'Red 2', 'Red 3', 'Red 4', 'Red 5', 'Red 6', 'Red 7']
    return render(request, 'network.html', {'networks': networks})


def symptoms(request):
    ''' Symptoms view '''
    return render(request, 'symptoms.html')


def update_monitor(request):
    ''' Update firmware view '''
    if is_raspberry_pi_os():
        update_firmware()
        return render(request, 'update.html')
    else:
        return render(request, 'error.html')


def user(request):
    ''' User view '''
    return render(request, 'user.html')


def weight(request):
    ''' Weight view '''
    return render(request, 'weight.html')


def weight_confirmation(request):
    ''' Weight confirmation view '''
    return render(request, 'weightc.html')