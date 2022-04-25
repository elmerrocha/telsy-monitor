'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v25.04.2022
Ing. Elmer Rocha Jaime
'''

from struct import unpack, pack
from smbus import SMBus

# I2C x728 address
ADDRESS = 0x36
bus = SMBus(1)

def read_voltage():
    ''' Return the value voltage battery '''
    read = bus.read_word_data(ADDRESS, 2)
    swapped = unpack("<H", pack(">H", read))[0]
    voltage = swapped * 1.25 /1000/16
    return voltage
def read_capacity():
    ''' Return the percentage battery '''
    read = bus.read_word_data(ADDRESS, 4)
    swapped = unpack("<H", pack(">H", read))[0]
    capacity = int(swapped/256)
    return capacity
