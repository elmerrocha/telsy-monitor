from struct import unpack, pack
from smbus import SMBus

bus = SMBus(1)
address = 0x36
def readVoltage(bus):
    read = bus.read_word_data(address, 2)
    swapped = unpack("<H", pack(">H", read))[0]
    voltage = swapped * 1.25 /1000/16
    return voltage
def readCapacity():
    read = bus.read_word_data(address, 4)
    swapped = unpack("<H", pack(">H", read))[0]
    capacity = int(swapped/256)
    return capacity