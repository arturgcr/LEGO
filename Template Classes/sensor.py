#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()


class SensorLEGO():
    '''
    Módulo de SensorLEGO
    --------------------
    Responsável por instanciar um sensor, definindo: tipo (str: `ultrassonico` ou `infravermelho`), porta (int: `1`, `2`, `3` ou `4`), a posição (str: `esquerda` ou `direita`) e o tamanho do filtro (`int`, por padrão recebe `None`)do sensor.
    '''
    def __init__(self, tipo, porta, posicao, tamanho_filtro=1):

        # Instanciando classe Port de acordo com a porta recebida no construtor
        if porta == 1:
            porta = Port.S1
        elif porta == 2:
            porta = Port.S2
        elif porta == 3:
            porta = Port.S3
        elif porta == 4:
            porta = Port.S4
        
        # Instanciando a classe correspondente ao sensor, cedendo a Port selecionada como argumento
        if tipo == 'ultrassonico' or 'ultrasonic':
            self.sensor = UltrasonicSensor(porta)
        if tipo == 'infravermelho' or 'infrared':
            self.sensor = InfraredSensor(porta)

        self.posicao = posicao
        self.filtro = self.criando_filtro(tamanho_filtro)

    # Recebe o tamanho do filtro e cria uma lista de tamanho igual
    def criando_filtro(self, tamanho_filtro):
        if tamanho_filtro != 0:
            filtro = [0] * tamanho_filtro
            return filtro
        else:
            return None
    
    # func que verefica se resultado eh vdd ou falso (sensores naturalmente tem um acumulo
    # de erros com o tempo, resultando em falsos positivos e falsos negativos)
    def filtrar(self):
        for leitura_filtro in range(self.lista_filtro):
            medicao = self.sensor.distance()
            if medicao == 0: # Converte o resultado para booleano, pq oq nos interessa é a presença apenas
                medicao = False
            elif medicao != 0:
                medicao = True
            self.lista_filtro[leitura_filtro] = medicao
            if self.lista_filtro[leitura_filtro] != self.lista_filtro[0]:
                break
        if False not in self.lista_filtro:
            return True
        else:
            return False
    
    # se filtro aprovado, confia no resultado e entra em def enxergando; enxergando afirma se ta vendo oponente ou nao
    def enxergando(self, limiar):
        if self.sensor.distance() < limiar:
            if self.filtro != None:
                if self.filtrar():
                    return True
                else:
                    return False
            return True
        else:
            return False

