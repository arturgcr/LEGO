#!/usr/bin/env pybricks-micropython
from re import X
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()

# ---------------------------------------------------------------------------------------------------------------------------------------------------



# Objetivo: Classe que ajusta robo antes dos segundos iniciais da luta - definindo direcao inicial e estrategia atraves do pressionamento de botoes
import time
import estrategia
import sensor
class Setup():
    
    def __init__(self, motores):
        self.motores = motores
        self.pressionado = 0 #variavel para encerrar loop / se 0, botao nao pressionado, se 1, botao pressionado
    

    # descobrir botao direcao e estrategia
    def selecionarEstrategia(self): 
        while (pressionado == 0):
            if Button.RIGHT in buttons.pressed(): #duvida: buttons.pressed() ou brick.buttons.pressed()
                pressionado = 1
                self.estrategia = 1 # arcoInicial
            elif Button.LEFT in buttons.pressed():
                pressionado = 1
                self.estrategia = 0 # manobraInicial
            elif Button.CENTER in buttons.pressed():
                pressionado = 1
                self.estrategia = -1 # armadilhaInicial

        time.sleep(1) # espera por 1 segundo
        pressionado = 0

        while (pressionado == 0):
            if Button.UP in buttons.pressed():
                pressionado = 1
                self.direcao = 1 # direita
            if Button.DOWM in buttons.pressed():
                pressionado = 1
                self.direcao = -1 # esquerda
            

    # chama as respectivas acoes selecionadas
    def executaEstrategia(self):
        if self.estrategia == 1:
            self.arcoInicial(self,tempo)
        elif self.estrategia == 0:
            self.manobraInicial(self,tempo)
        elif self.estrategia == -1:
            self.armadilhaInicial(self,tempo)


    # def arcoInicial(self,tempo):
    #     if self.direcao == 1: #direita
    #     #infos oq motores fazem
    #     elif self.direcao == -1: #esquerda
   
   
    # def manobraInicial(self,tempo):
    #     if self.direcao == 1: #direita
    #     #infos oq motores fazem
    #     elif self.direcao == -1: #esquerda
   
  
    # def armadilhaInicial(self,tempo):
    #     if self.direcao == 1: #direita
    #     #infos oq motores fazem
    #     elif self.direcao == -1: #esquerda
    


# Write your program here.
ev3.speaker.beep()    
