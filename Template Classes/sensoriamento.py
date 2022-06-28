#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()

class Sensoriamento():
    
    def __init__(self, lista_sensores, limiar = 40, visto_ultimo = None):
        # lembrando q esse sensordireita, sensoresquerda e sensormeio são OBJETOS herdados da classe sensor
        self.sensores_direita = []
        self.sensores_esquerda = []

        for sensor in lista_sensores:
            if sensor.posicao == 'esquerda':
                self.sensores_esquerda.append(sensor)
            elif sensor.posicao == 'direita':
                self.sensores_direita.append(sensor)

        # não vem como argumento da init, então pode entrar direto na classe. no diagram de classes está dizendo q pe default....
        self.limiar = limiar
        # um possível problema para essa abordagem é o fato de q o infravermelho não vem em cm, e o nxt med em cm, não mm
        # converter os dados do infravermelho é algo q não implementei em geral
        self.visto_ultimo = visto_ultimo
        # recebe o erro na leitura dos sensores
        self.erro = 0

    def busca_oponente(self):
        nao_viu_nada = True     # Varíavel que determina se não vimos o robô inimigo / booleano
        enxergando_inimigo = 0  # Varíavel feita para definir de que lado o robô foi visto positivo direita e negativo esquerda
        # Variável que guarda a distânica vista por cada sensor
        medicoes_sensores_esquerda = []
        medicoes_sensores_direita = []

        for sensor in self.sensores_direita:  # sensoresdireita e sensoresesquerda seriam as listas com os sensores de cada lado
            if sensor.enxergando(self.limiar):   # tem que indentificar o limiar
                enxergando_inimigo += 1
                nao_viu_nada = False
                medicoes_sensores_direita.append(sensor.ultima_medicao_autorizada)

        for sensor in self.sensores_esquerda:
            if sensor.enxergando(self.limiar):
                enxergando_inimigo -= 1
                nao_viu_nada = False
                medicoes_sensores_esquerda.append(sensor.ultima_medicao_autorizada)

        # Se nenhum dos sensores viu, então retorna a direção de visto por último
        if nao_viu_nada:
            if self.visto_ultimo != None:
                return self.visto_ultimo
        else:
            self.visto_ultimo = enxergando_inimigo
            self.erro = self.calcula_erro(medicoes_sensores_esquerda, medicoes_sensores_direita)
            return enxergando_inimigo

    def calcula_erro(self, medicoes_sensores_esquerda, medicoes_sensores_direita):  # o erro é dado pela diferença entre a medição dos sensores
        for medicao in medicoes_sensores_esquerda:
            soma_medicoes_esquerda += medicao
            media_medicoes_esquerda = soma_medicoes_esquerda/len(medicoes_sensores_esquerda)

        for medicao in medicoes_sensores_direita:
            soma_medicoes_direita += medicao
            media_medicoes_direita = soma_medicoes_direita/len(medicoes_sensores_direita)
        
        erro = abs(media_medicoes_esquerda - media_medicoes_direita)/100  # está em cm
        
        return erro
