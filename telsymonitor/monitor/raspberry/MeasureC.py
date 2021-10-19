## Fundacion Cardiovascular de Colombia
## Proyecto Telsy Hogar
## Ing. Elmer Rocha Jaime

import RPi.GPIO as GPIO
from Communication import Serial_Write

Serial_Write(36)

RelayPin = 10#GPIO10
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RelayPin, GPIO.OUT)
GPIO.cleanup()