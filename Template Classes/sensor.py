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

    def __init__(self, tipo, porta, lado, tamanhodofiltro=1):

        if porta == 1:
            porta = Port.S1
        elif porta == 2:
            porta = Port.S2
        elif porta == 3:
            porta = Port.S3
        elif porta == 4:
            porta = Port.S4

        if tipo == 'ultrassom' or 'ultrasson':
            self.sensor = UltrasonicSensor(porta)
        if tipo == 'infravermelho' or 'infrared':
            self.sensor = InfraredSensor(porta)

        self.lado = lado
        self.tamanhoDoFiltro = tamanhodofiltro
        self.listaFiltro = [0] * tamanhodofiltro
        self.index = 0

    # func que verefica se resultado eh vdd ou falso (sensores naturalmente tem um acumulo
    # de erros com o tempo, resultando em falsos positivos e falsos negativos)
    def filtro(self):

        medicao = self.sensor.distance()
        self.listaFiltro[self.index] = medicao

        if self.index < self.tamanhodofiltro:
            self.index += 1
        else:
            self.index = 0

        for i in self.listaFiltro:
            if i != medicao:
                return False  # funcao retorna true caso o filtro "aprove" o resultado da medicao e false caso contrario

        return True

    # se filtro aprovado, confia no resultado e entra em def enxergando; enxergando afirma se ta vendo oponente ou nao
    def enxergando(self, limiar):
        if self.sensor.distance() < limiar:
            return True
        else:
            return False

    # em sensoriamento: se filtro aprovado, entrar em def enxergando;


class Sensoriamento():
    def __init__(self, lista_sensores, vistoUltimo, limiar=40):
        # lembrando q esse sensordireita, sensoresquerda e sensormeio são OBJETOS herdados da classe sensor
        self.sensores_direita = []
        self.sensores_esquerda = []

        for sensor in lista_sensores:
            if sensor.lado == 'esquerda':
                # adiciona i à lista da esquerda
                self.sensores_esquerda.append(sensor)
            if sensor.lado == 'direita':
                self.sensores_direita.append(sensor)  # adiciona i à lista da direita

        self.listadesensores = lista_sensores

        # não vem como argumento da init, então pode entrar direto na classe. no diagram de classes está dizendo q pe default....
        self.limiar = limiar
        # um possível problema para essa abordagem é o fato de q o infravermelho não vem em cm, e o nxt med em cm, não mm
        # converter os dados do infravermelho é algo q não implementei em geral
        self.vistoUltimo = vistoUltimo

    def verificado(self):
        verInimigo = 0  # Varíavel feita para definir de que lado o robô foi visto positivo direita e negativo esquerda
        verNada = 0     # Varíavel que determina se não vimos o robô inimigo
        for i in self.sensores_direita:  # sensoresdireita e sensoresesquerda seriam as listas com os sensores de cada lado

            if i.enxergando(self.limiar) == True:   # tem que indentificar o limiar
                verInimigo += 1
                verNada = 1

        for i in self.sensores_esquerda:

            if i.enxergando(self.limiar) == True:
                verInimigo -= 1

        for i in self.listadesensores:  # Filtro para validar se realmente o robô viu algo na direção
            if i.filtro == False:
                verNada == 0

        if verNada == 0:
            return self.vistoUltimo
        else:
            self.vistoUltimo = verInimigo
            return verInimigo

#   def PID(self):
#         if self.erro < 5:
#             self.erro = 0
#         else:
#             PID = self.kp * self.erro + self.kd * \
#                 (self.erro - self.erroAnterior)
#             self.erroAnterior = self.erro
#         return PID 
