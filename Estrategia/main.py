#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.




#   STATUS, PROBLEMAS e DUVIDAS:
# - Ver as estrategias possiveis - rastrear inimigo, encontrar, full direcao dele - nao herda de sensores?
# - como aplicar?

# Create your objects here.
ev3 = EV3Brick()

class Estrategia():
      
    def __init__(self, motores):
        self.motores = motores

    def radarSimples(erro):

    #def radarArco (erro):

    #def radarPID (erro):


# Write your program here.
ev3.speaker.beep()
