#!/usr/bin/env pybricks-micropython
from re import X
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

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------



# Objetivo: Classe que ajusta robo antes dos segundos iniciais da luta - definindo direcao inicial e estrategia atraves do pressionamento de botoes
class Setup():
    
    def __init__(self, motores):
        self.motores = motores 

    # descobrir botao direcao e estrategia e executar estrategia
    def selecionarEstrategia(self): 
        while true:
            if buttons.pressed()[0] = X
                self.estrategia = (arcoInicial ou outro)
            
        wait 1000

        while true:
            if buttons.pressed()[0] = X
                self.direcao = (direita ou outro)

    def executaEstrategia(self):
        if self.estrategia = arcoInicial:
            # chama arcoInicial por exemplo

    def arcoInicial(self,tempo):
        if self.direcao = esquerda
        #infos oq motores fazem
    def manobraInicial(self,tempo):

    def armadilhaInicial(self,tempo):

    


# Write your program here.
ev3.speaker.beep()    
