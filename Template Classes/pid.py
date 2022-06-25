#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()

class PID:
    
    def __init__(self, kp, kd, ki, erro):
        
        self.kp = kp
        self.kd = kd
        self.ki = ki

        self.erro = erro
        self.erro_anterior = 0

    # junção entre PID e verificaPerto
    def calcula_pid(self):
        if self.erro < 5:
            self.erro = 0
        else:
            self.erro = self.erro - self.erro_anterior        #Adicionado essa linha para inserir novo valor de erro conforme código em blocos
            PID = self.kp * self.erro + self.kd * self.erro 
            self.erro_anterior = self.erro
        print(PID)
        return PID