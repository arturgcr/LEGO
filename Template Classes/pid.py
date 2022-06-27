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
    
    def __init__(self, kp, kd, ki):
        # Definindo as constantes
        self.kp = kp # constante proporcional
        self.ki = ki # constante integral
        self.kd = kd # constante derivativa

        # variáveis pra o cálculo do PID
        self.proporcional = 0
        self.integral = 0
        self.derivativa = 0
        
        self.erro_anterior = 0 # erro da iteração anterior
        self.tempo_anterior = 0 # tempo para o cálculo da variação de tempo

    # junção entre PID e verificaPerto
    def calcula_pid(self, erro):
        # Marca o tempo atual menos o tempo anterior para encontrar a variação de tempo entre iterações
        diferenca_tempo = StopWatch.time() - self.tempo_anterior
        
        # Calcula novos valores para as variáveis com base no novo erro
        self.proporcional = self.kp * erro
        self.integral += self.ki * erro * diferenca_tempo
        self.derivativa = (self.kd * (erro - self.erro_anterior)) / diferenca_tempo
        PID = self.proporcional + self.integral + self.derivativa
            
        # Redefine erro e tempo anterior para o cálculo da próxima iteração
        self.erro_anterior = erro # erro atual passa a ser o erro anterior
        self.tempo_anterior = StopWatch.time() # marca um novo tempo para o tempo anterior

        # Retorna o valor de PID
        return PID