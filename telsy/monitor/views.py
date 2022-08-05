'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v05.08.2022
Ing. Elmer Rocha Jaime
'''

from os import getcwd, system
from subprocess import Popen, CalledProcessError, PIPE
from time import sleep
from pathlib import Path
from json import load
from django.shortcuts import render
from monitor.raspberry.update import update_info

# Boolean variable to enable membrane keyboard only once
MEMBRANE_KEYBOARD = True
# Boolean variable to start NIBP measurement
NIBP_MEASUREMENT = False
# Path Raspberry folder
RASPI_PATH = './monitor/raspberry/'
# Popen lists
KEYBOARD_GPIO = ['python3', RASPI_PATH+'keyboard_gpio.py']
MEASURE_CANCEL = ['python3', RASPI_PATH+'measure_cancel.py']
MEASURE_NIBP = ['python3', RASPI_PATH+'measure_nibp.py']
MEASURE_ECG = ['python3', RASPI_PATH+'measure_ecg.py']
CREATE_JSON = ['python3', RASPI_PATH+'create_json.py']
# Pipe of measure subprocess
measure_pipe = 0


def is_raspberry_pi_os():
    ''' Return a boolean value if the code is running in Raspberry OS '''
    current_path = getcwd().replace('\\', '/')
    return current_path[0:6] == '/home/'


if is_raspberry_pi_os():
    from monitor.raspberry import raspberry_wifi
    from monitor.raspberry.update import update_firmware
    from monitor.raspberry.information import get_information
    if MEMBRANE_KEYBOARD:
        MEMBRANE_KEYBOARD = False
        try:
            Popen(KEYBOARD_GPIO)
        except CalledProcessError as exc:
            print(exc)


def cancel_measurement(request):
    ''' Cancel monitor measurement '''
    global measure_pipe
    if is_raspberry_pi_os():
        try:
            measure_pipe.kill()
            Popen(MEASURE_CANCEL)
        except CalledProcessError as exc:
            print(exc)
    else:
        print('Cancel measurement')
    return render(request, 'cancel.html')


def connected(request):
    ''' Connected WiFi view '''
    network_ssid = request.POST['NetName']
    password = request.POST['PassNet']
    if is_raspberry_pi_os():
        try:
            raspberry_wifi.connect(network_ssid, password)
        except CalledProcessError as exc:
            print(exc)
            return render(request, 'menu.html')
    else:
        print('SSID:', network_ssid, 'Password:', password)
    return render(request, 'connected.html', {'Net': network_ssid})


def connecting(request, ssid):
    ''' Connecting WiFi view '''
    return render(request, 'connecting.html', {'SSID': ssid})


def data(request):
    ''' Last telecenter data view '''
    return render(request, 'data.html')


def error_400(request, exception):
    ''' Error 400 view '''
    print(exception)
    return render(request, 'error.html', status=400)


def error_403(request, exception):
    ''' Error 403 view '''
    print(exception)
    return render(request, 'error.html', status=403)


def error_404(request, exception):
    ''' Error 404 view '''
    print(exception)
    return render(request, 'error.html', status=404)


def error_500(request):
    ''' Error 500 view '''
    return render(request, 'error.html', status=500)


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


def home(request):
    ''' Main home view '''
    if request.method == 'POST':
        if request.POST['Clock'] != '0':
            date = request.POST['Clock'].split('T')
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


def measuring(request):
    ''' Measuring view '''
    global NIBP_MEASUREMENT, measure_pipe
    NIBP_MEASUREMENT = bool(int(request.POST['NIBP']))
    if is_raspberry_pi_os():
        if NIBP_MEASUREMENT:
            try:
                measure_pipe = Popen(MEASURE_NIBP, stdout=PIPE)
            except CalledProcessError as exc:
                print(exc)
        else:
            try:
                measure_pipe = Popen(MEASURE_ECG, stdout=PIPE)
            except CalledProcessError as exc:
                print(exc)
    else:
        if NIBP_MEASUREMENT:
            print('Monitor will measure NIBP')
        else:
            print('Monitor will not measure NIBP')
    return render(request, 'measuring.html')


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
        networks = ['Red 0', 'Red A', 'Red B', 'Red C', 'Red 4']
    return render(request, 'network.html', {'networks': networks})


def results(request):
    ''' Measurement results view '''
    while (NIBP_MEASUREMENT and not
            Path(RASPI_PATH+'data/nibp.end').is_file()):
        pass
    if is_raspberry_pi_os():
        if Path(RASPI_PATH+'data/nibp.end').is_file():
            try:
                system('rm -f '+RASPI_PATH+'data/nibp.end')
            except CalledProcessError as exc:
                print('File could not be deleted', exc)
        try:
            Popen(CREATE_JSON).wait()
            sleep(1.5)
        except CalledProcessError as exc:
            print(exc)
    try:
        with open(RASPI_PATH+'data/data.json', 'r') as file:
            results_data = load(file)
    except EnvironmentError as exc:
        print(exc)
        results_data = {'RR': 0, 'SPO2': 0, 'Pulse': 0, 'Systolic': 0,
                        'Diastolic': 0, 'MAP': 0, 'Date': '', 'ECG': '0',
                        'Temperature': 0}
    return render(request, 'results.html', results_data)


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
