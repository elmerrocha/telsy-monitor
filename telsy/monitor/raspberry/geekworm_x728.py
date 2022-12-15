'''
Fundación Cardiovascular de Colombia
Dirección de Innovación y Desarrollo Tecnológico
Proyecto Telsy
Telsy Hogar v15.12.2022
Ing. Elmer Rocha Jaime
'''

from struct import unpack, pack
from smbus import SMBus
import RPi.GPIO as gpio

# I2C x728 address
ADDRESS = 0x36
bus = SMBus(1)
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# GPIO pin
POWER = 18
# Setup
gpio.setup(POWER, gpio.IN, pull_up_down=gpio.PUD_DOWN)


def read_voltage():
    ''' Return the value voltage battery '''
    read = bus.read_word_data(ADDRESS, 2)
    swapped = unpack("<H", pack(">H", read))[0]
    voltage = swapped * 1.25/1000/16
    return voltage


def read_capacity():
    ''' Return the percentage battery '''
    read = bus.read_word_data(ADDRESS, 4)
    swapped = unpack("<H", pack(">H", read))[0]
    capacity = int(swapped/256)
    return capacity


def power_supply_status():
    ''' Return a boolean value of AC power supply connection '''
    power_wire = gpio.input(POWER)
    return not bool(power_wire)
