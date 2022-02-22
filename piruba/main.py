#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import variaveis.py 
import calibracao.py 


ev3 = EV3Brick()
ev3.speaker.beep()


# Calibração dos sensores 

sensorCores = sensorCor()
sensorCores.calibracao()

# Relógios 

relogio1.time()
relogio2.time()




