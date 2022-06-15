'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v15.06.2022
Ing. Elmer Rocha Jaime
'''
from uart_io import serial_write
import RPi.GPIO as gpio

serial_write(36)
# GPIO10
RELAY_PIN = 10
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(RELAY_PIN, gpio.OUT)
gpio.cleanup()
