import RPi.GPIO as GPIO
from time import sleep
from os import system, popen

Xlist = popen('xinput list').read()
index = Xlist.find('raspberrypi-ts')
Xid = Xlist[index:index+70].split('=')[1][0:1]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO pins
Light     = 6
Light_LED = 5
Hold      = 26
Hold_LED  = 19
#Status
Light_Status = False
Hold_Status  = False
#Setup
GPIO.setup(Light,     GPIO.IN,  pull_up_down=GPIO.PUD_UP)
GPIO.setup(Hold,      GPIO.IN,  pull_up_down=GPIO.PUD_UP)
GPIO.setup(Light_LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Hold_LED,  GPIO.OUT, initial=GPIO.LOW)

try:
    while True:
        Light_Button = GPIO.input(Light)
        Hold_Button  = GPIO.input(Hold)
        if not Light_Button:
            if Light_Status:
                system('bash -c "echo 255 > /sys/class/backlight/rpi_backlight/brightness"')
                GPIO.output(Light_LED, GPIO.LOW)
                Light_Status = False
            else:
                system('bash -c "echo 10 > /sys/class/backlight/rpi_backlight/brightness"')
                GPIO.output(Light_LED, GPIO.HIGH)
                Light_Status = True
            sleep(1)
        if not Hold_Button:
            if Hold_Status:
                system('xinput enable '+Xid)
                GPIO.output(Hold_LED, GPIO.LOW)
                Hold_Status = False
            else:
                system('xinput disable '+Xid)
                GPIO.output(Hold_LED, GPIO.HIGH)
                Hold_Status = True
            sleep(1)
except KeyboardInterrupt:
    system('xinput enable '+Xid)
    system('bash -c "echo 255 > /sys/class/backlight/rpi_backlight/brightness"')
    GPIO.cleanup()
except Exception as e:
    system('xinput enable '+Xid)
    system('bash -c "echo 255 > /sys/class/backlight/rpi_backlight/brightness"')
    GPIO.cleanup()
