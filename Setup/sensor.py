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
            self.index +=1
        else:
            self.index=0
            
        for i in self.listaFiltro:
            if i != medicao:
                return False #funcao retorna true caso o filtro "aprove" o resultado da medicao e false caso contrario
                
        return True
            
    # se filtro aprovado, confia no resultado e entra em def enxergando; enxergando afirma se ta vendo oponente ou nao    
    def enxergando (self,limiar):
        if self.sensor.distance() < limiar:
            return True
        else:
            return False
            
            
    # em sensoriamento: se filtro aprovado, entrar em def enxergando;

class Sensoriamento():
    def __init__(self, listadesensores, vistoUltimo, kp, kd, ki = 0, limiar = 40):
    # lembrando q esse sensordireita, sensoresquerda e sensormeio são OBJETOS herdados da classe sensor  
        self.sensoresDireita=[]
        self.sensoresEsquerda=[]
        self.erro = 0
        self.erroPassado = 0 

        for i in listadesensores:
            if i.lado == self.esquerda:
                self.sensoresEsquerda.append(i) #adiciona i à lista da esquerda
            if i.lado == self.direita:
                self.sensoresDireita.append(i) #adiciona i à lista da direita
            if i.lado == self.meio:
                self.sensoresMeio.append(i)
        
        self.kp = kp
        self.kd = kd
        self.ki = ki

        self.listadesensores=listadesensores

        self.limiar = limiar       # não vem como argumento da init, então pode entrar direto na classe. no diagram de classes está dizendo q pe default....
                                   # um possível problema para essa abordagem é o fato de q o infravermelho não vem em cm, e o nxt med em cm, não mm
                                   # converter os dados do infravermelho é algo q não implementei em geral
        self.vistoUltimo = vistoUltimo 

    def verificalado(self):
        x = 0 # Varíavel feita para definir de que lado o robô foi visto
        y = 0 # Varíavel que determina se não vimos o robô inimigo
        for i in self.sensoresDireita: # sensoresdireita e sensoresesquerda seriam as listas com os sensores de cada lado
            
            if i.enxergando == True:   # tem que indentificar o limiar
                x += 1
                y = 1
            if i.filtro == False:
                y == 0 

        for i in self.sensoresEsquerda:   # É importante notar, q da forma como eu optei por montar o filtro aqui haveria uma defasagem de
                                 
            if i.enxergando == True:      # tempo entre as medições, dependendo do tamanho do filtro. pra evitar isto bastria implementar
                x -= 1                    # o filtro no resultado dafunção verifica lado, ao ives de no final da função enxergando, isso é facil de mudar
                y = 1

            if i.filtro == False:
                y == 0 
        
        if y == 0:
            return self.vistoUltimo
        else:
            self.vistoUltimo =  x
            return x

       
    def Erro(self): # o erro é dado pela diferença entre a medição dos sensores 
        for i in self.sensoresDireita:
            somaDireita += i
        mediaDireita = somaDireita/len(self.sensoresDireita) 

        for i in self.sensoresEsquerda:
            somaEsquerda += i
        mediaEsquerda = somaEsquerda/len(self.sensoresEsquerda)

        self.erro = abs(mediaDireita - mediaEsquerda)/100 # está em cm 
        return self.erro 

    # junção entre PID e verificaPerto 
    def PID(self):
        if self.erro < 5:
            self.erro = 0
        else: 
            PID = self.kp * self.erro + self.kd * (self.erro - self.erroAnterior)
            self.erroAnterior = self.erro 
        return PID 
    
    

# Write your program here.
ev3.speaker.beep()    