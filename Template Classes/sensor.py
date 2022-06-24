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
        self.index = 0

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

        medicao = self.sensor.distance()
        self.lista_filtro[self.index] = medicao

        if self.index < self.tamanho_filtro:
            self.index += 1
        else:
            self.index = 0

        for i in self.lista_filtro:
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
    
    def __init__(self, lista_sensores, visto_ultimo, limiar=40):
        # lembrando q esse sensordireita, sensoresquerda e sensormeio são OBJETOS herdados da classe sensor
        self.sensores_direita = []
        self.sensores_esquerda = []

        for sensor in lista_sensores:
            if sensor.posicao == 'esquerda':
                self.sensores_esquerda.append(sensor)
            elif sensor.posicao == 'direita':
                self.sensores_direita.append(sensor)

        self.lista_sensores = lista_sensores

        # não vem como argumento da init, então pode entrar direto na classe. no diagram de classes está dizendo q pe default....
        self.limiar = limiar
        # um possível problema para essa abordagem é o fato de q o infravermelho não vem em cm, e o nxt med em cm, não mm
        # converter os dados do infravermelho é algo q não implementei em geral
        self.visto_ultimo = visto_ultimo

    def verificado(self):
        ver_inimigo = 0  # Varíavel feita para definir de que lado o robô foi visto positivo direita e negativo esquerda
        ver_nada = 0     # Varíavel que determina se não vimos o robô inimigo
        
        for sensor in self.sensores_direita:  # sensoresdireita e sensoresesquerda seriam as listas com os sensores de cada lado
            if sensor.enxergando(self.limiar) == True:   # tem que indentificar o limiar
                ver_inimigo += 1
                ver_nada = 1

        for sensor in self.sensores_esquerda:
            if sensor.enxergando(self.limiar) == True:
                ver_inimigo -= 1

        for sensor in self.lista_sensores:  # Filtro para validar se realmente o robô viu algo na direção
            if sensor.filtro == False:
                ver_nada == 0

        # Se nenhum dos sensores viu, então retorna a direção de visto por último
        if ver_nada == 0:
            return self.visto_ultimo
        else:
            self.visto_ultimo = ver_inimigo
            return ver_inimigo

