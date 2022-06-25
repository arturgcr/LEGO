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
    
    def __init__(self, kp, kd, ki, sensoriamento):
        
        self.kp = kp
        self.kd = kd
        self.ki = ki

        self.erro = 0
        self.erro_passado = 0

        self.sensoriamento = sensoriamento


    def calcula_erro(self):  # o erro é dado pela diferença entre a medição dos sensores
        for sensor in self.sensoriamento.sensores_direita:
            somaDireita += sensor.distance()
        mediaDireita = somaDireita/len(self.sensoresDireita)

        for sensor in self.sensoriamento.sensoresEsquerda:
            somaEsquerda += sensor.distance()
        mediaEsquerda = somaEsquerda/len(self.sensoresEsquerda)

        self.erro = abs(mediaDireita - mediaEsquerda)/100  # está em cm
        return self.erro

    # junção entre PID e verificaPerto
    def calcula_pid(self):
        if self.erro < 5:
            self.erro = 0
        else:
            self.erro = self.erro - self.erroAnterior        #Adicionado essa linha para inserir novo valor de erro conforme código em blocos
            PID = self.kp * self.erro + self.kd * self.erro 
            self.erroAnterior = self.erro
        print(PID)
        return PID