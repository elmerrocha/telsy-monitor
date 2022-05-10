'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v10.05.2022
Ing. Elmer Rocha Jaime
'''

from time import sleep
from os import system
from subprocess import getoutput
import RPi.GPIO as gpio

xlist = getoutput('xinput list')
index = xlist.find('raspberrypi-ts')
xid = xlist[index:index+70].split('=')[1][0:1]

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
# GPIO pins
LIGHT = 6
LIGHT_LED = 5
HOLD = 26
HOLD_LED = 19
# Status
light_status = False
hold_status  = False
# Setup
gpio.setup(LIGHT, gpio.IN,  pull_up_down=gpio.PUD_UP)
gpio.setup(HOLD, gpio.IN,  pull_up_down=gpio.PUD_UP)
gpio.setup(LIGHT_LED, gpio.OUT, initial=gpio.LOW)
gpio.setup(HOLD_LED, gpio.OUT, initial=gpio.LOW)
# Path brightness in Raspberry Pi OS with Desktop
BACKLIGHT_PATH = '/sys/class/backlight/rpi_backlight/brightness'

try:
    while True:
        light_button = gpio.input(LIGHT)
        hold_button  = gpio.input(HOLD)
        if not light_button:
            if light_status:
                system('bash -c "echo 255 > '+BACKLIGHT_PATH+'"')
                gpio.output(LIGHT_LED, gpio.LOW)
                light_status = False
            else:
                system('bash -c "echo 10 > '+BACKLIGHT_PATH+'"')
                gpio.output(LIGHT_LED, gpio.HIGH)
                light_status = True
            sleep(1)
        if not hold_button:
            if hold_status:
                system('xinput enable '+xid)
                gpio.output(HOLD_LED, gpio.LOW)
                hold_status = False
            else:
                system('xinput disable '+xid)
                gpio.output(HOLD_LED, gpio.HIGH)
                hold_status = True
            sleep(1)
except KeyboardInterrupt:
    system('xinput enable '+xid)
    system('bash -c "echo 255 > '+BACKLIGHT_PATH+'"')
    gpio.cleanup()
except OSError:
    print(OSError)
    system('xinput enable '+xid)
    system('bash -c "echo 255 > '+BACKLIGHT_PATH+'"')
    gpio.cleanup()
