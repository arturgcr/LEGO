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
    
    def __init__(self, kp, kd, ki, temporizador):
        # Definindo as constantes
        self.kp = kp # constante proporcional
        self.ki = ki # constante integral
        self.kd = kd # constante derivativa

        # variáveis pra o cálculo do PID
        self.proporcional = 0
        self.integral = 0
        self.derivativa = 0
        
        self.temporizador = temporizador
        self.erro_anterior = 0 # erro da iteração anterior
        self.tempo_anterior = 0 # tempo para o cálculo da variação de tempo

    # junção entre PID e verificaPerto
    def calcula_pid(self, erro):
        # Marca o tempo atual menos o tempo anterior para encontrar a variação de tempo entre iterações
        diferenca_tempo = self.temporizador.time() - self.tempo_anterior
        
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

    # Vai converter pid para pwm de [0,100], pois o sinal do pwm será determinado pela direção do oponente
    # No cálculo do erro em Sensoriamento, o valor do erro é absoluto e de [0,limiar] (limiar=40)
    # A direção do oponente será -1 ou 1, caso ela seja 0, o PID não será considerado no full frente 
    def converte_pid_para_pwm(self, pid, pid_min = 0, pid_max = 40, pwm_min = 0,  pwm_max = 100):
        pid_min = 0 # temporário, precisamos corrigir isso para ser automatizado
        pid_max = pid_max * self.kp # mesmo problema de cima
        variacao_pid_min_max = pid_max - pid_min
        variacao_pwm_min_max = pwm_max - pwm_min
        variacao_pid_a_ser_convertido_com_pid_min = pid - pid_min
        pid_convertido_pwm = (variacao_pid_a_ser_convertido_com_pid_min * variacao_pwm_min_max) / variacao_pid_min_max + pwm_min
        return pid_convertido_pwm