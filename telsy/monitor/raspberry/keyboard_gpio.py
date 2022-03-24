'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v23.03.2022
Ing. Elmer Rocha Jaime
'''

from time import sleep
from os import system
from subprocess import getoutput
import RPi.GPIO as gpio

# xlist = getoutput('xinput list')
# index = xlist.find('raspberrypi-ts')
# xid = xlist[index:index+70].split('=')[1][0:1]

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
# GPIO pins
LIGHT     = 6
LIGHT_LED = 5
# HOLD      = 26
# HOLD_LED  = 19
# Status
LIGHT_STATUS = False
# HOLD_STATUS  = False
# Setup
gpio.setup(LIGHT,     gpio.IN,  pull_up_down=gpio.PUD_UP)
# gpio.setup(HOLD,      gpio.IN,  pull_up_down=gpio.PUD_UP)
gpio.setup(LIGHT_LED, gpio.OUT, initial=gpio.LOW)
# gpio.setup(HOLD_LED,  gpio.OUT, initial=gpio.LOW)
# Path brightness in Raspberry Pi OS Lite
BACKLIGHT_PATH = '/sys/class/backlight/10-0045/brightness'

try:
    while True:
        LIGHT_BUTTON = gpio.input(LIGHT)
        # HOLD_BUTTON  = gpio.input(HOLD)
        if not LIGHT_BUTTON:
            if LIGHT_STATUS:
                system('bash -c "echo 255 > '+BACKLIGHT_PATH+'"')
                gpio.output(LIGHT_LED, gpio.LOW)
                LIGHT_STATUS = False
            else:
                system('bash -c "echo 10 > '+BACKLIGHT_PATH+'"')
                gpio.output(LIGHT_LED, gpio.HIGH)
                LIGHT_STATUS = True
            sleep(1)
        # if not HOLD_BUTTON:
        #     if HOLD_STATUS:
        #         system('xinput enable '+xid)
        #         gpio.output(HOLD_LED, gpio.LOW)
        #         HOLD_STATUS = False
        #     else:
        #         system('xinput disable '+xid)
        #         gpio.output(HOLD_LED, gpio.HIGH)
        #         HOLD_STATUS = True
        #     sleep(1)
except KeyboardInterrupt:
    # system('xinput enable '+xid)
    system('bash -c "echo 255 > '+BACKLIGHT_PATH+'"')
    gpio.cleanup()
except OSError:
    print(OSError)
    # system('xinput enable '+xid)
    system('bash -c "echo 255 > '+BACKLIGHT_PATH+'"')
    gpio.cleanup()
