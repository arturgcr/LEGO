#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO    if porta==1:
        
# Click "Open user guide" on the EV3 extension tab for more information

# Create your objects here.
ev3 = EV3Brick()

class SensorLEGO():

    def __init__(self, tipo, porta, lado, tamanhodofiltro=1):
        
        if porta==1:
            porta=port.S1
        elif porta==2:
            porta=port.S2
        elif porta==3:
            porta=port.S3
        elif porta==4:
            porta=port.S4
        
        if tipo == 'ultrassom' or 'ultrasson':
                self.sensor = UltrasonicSensor(porta)
        if tipo == 'infravermelho' or 'infrared':
                self.sensor = InfraredSensor(porta)    

    self.lado = lado
    self.tamanhoDoFiltro = tamanhodofiltro
    self.listaFiltro = [0] * tamanhodofiltro
    self.index=0
   

     # func que verefica se resultado eh vdd ou falso (sensores naturalmente tem um acumulo
     #  de erros com o tempo, resultando em falsos positivos e falsos negativos)
    def filtro(self):
        
        medicao = self.sensor.distance()
        self.listaFiltro[self.index] = medicao
        
        if self.index < self.tamanhodofiltro:
            self.index +=1
        else:
            self.index=0
            
        for i in self.listaFiltro:
            if i != medicao:
                return False     #funcao retorna true caso o filtro "aprove" o reusltado da medicao e false caso contrario
                
        return True
            
    # se filtro aprovado, confia no resultado e entra em def enxergando; enxergando afirma se ta vendo oponente ou nao    
    def enxergando (self,limiar):
        if self.sensor.distance() < limiar:
            return True
        else:
            return False
            
            
    # em sensoriamento: se filtro aprovado, entrar em def enxergando;

class Sensoriamento():
    def __init__(self, listadesensores, kp, kd, ki=0, limiar=40):
        
        self.sensoresDireita=[]
        self.sensoresEsquerda=[]

        for i in listadesensores:
            if i.lado == self.esquerda:
                self.sensoresEsquerda.append(i)
            if i.lado == self.direita:
                self.sensoresDireita.append(i)
        
        self.kp=kp
        self.kd=kd
        self.ki=ki

        self.listadesensores=listadesensores

        self.limiar = limiar   #não vem como argumento da init, então pode entrar direto na classe. no diagram de classes está dizendo q pe default....
                                   #um possível problema para essa abordagem é o fato de q o infravermelho não vem em cm, e o nxt med em cm, não mm
                                   #converter os dados do infravermelho é algo q não implementei em geral
 

# Write your program here.
ev3.speaker.beep()    