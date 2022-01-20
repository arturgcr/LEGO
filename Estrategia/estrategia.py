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



# Create your objects here.
ev3 = EV3Brick()

class Estrategia():

    def __init__(self, motores):
        self.motores = motores

    # girar ao redor de si ate encontrar algo
    # 100 eh valor arbitrario, teremos q testar e descobrir o real
    # na main, chamar tudo e botar loop pra recalcular sensores sempre ate achar oponente, full frente;
    def radarSimples(self,erro):
        if erro < 0:
            self.motores.giro(-100)
        if erro == 0:
            self.motores.reta(100)
        if erro > 0:
            self.motores.giro(100) 

    # vai andando em arcos ate encontrar algo
    # 100 e 15 eh valor arbitrario, teremos q testar e descobrir o real
    def radarArco (self,erro):
        if erro < 0:
            self.motores.arco(100,-15)
        if erro == 0:
            self.motores.reta(100)
        if erro > 0:
            self.motores.arco(100,15) 

    # vai andando em arcos ate encontrar algo
    def radarPID (self, erro, vLin=0):
        # na func arco - primeiro argumento: Vlin; segundo argumento: erro;
        if erro != 0:
            self.motores.arco(vLin,erro)
        if erro == 0:
            self.motores.reta(100)


# Write your program here.
ev3.speaker.beep()
