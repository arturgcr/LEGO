# CONFIGURAÇÕES INICIAIS - NÃO ESQUECER ---------------
# -> Aqui colocar os valores a serem alterados e separar por cada robo (ex: tempoManobra - treta: 5) 
# -> Treta - Codigo antigo - TESTAR A PARTIR DE:
#    erroBase = 15
#    kp = 2
#    ki = 0
#    kd = 1.2


# ---------------------------------------------------------------------------------------------------------------------------------------------------

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
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# Objetivo: Classe que ajusta robo antes dos segundos iniciais da luta - definindo direcao inicial e estrategia atraves do pressionamento de botoes
import time
import locomocao
class Setup():
    
    def __init__(self, motores): # # Alterar tempos correspondentes ao robo
        self.motores = motores  # Motores: objeto vindo de Locomoção
        self.pressionado = 0    # variavel para encerrar loop / se 0, botao nao pressionado, se 1, botao pressionado
    

    # descobrir botao direcao e estrategia
    def selecionarEstrategia(self): 
        while (pressionado == 0):
            if Button.RIGHT in ev3.buttons.pressed(): #duvida: buttons.pressed() ou brick.buttons.pressed()
                pressionado = 1
                self.estrategia = 'arcoInicial' 
            elif Button.LEFT in ev3.buttons.pressed():
                pressionado = 1
                self.estrategia = 'manobraInicial' 
            elif Button.CENTER in ev3.buttons.pressed():
                pressionado = 1
                self.estrategia = 'armadilhaInicial' 

        time.sleep(1) # espera por 1 segundo
        pressionado = 0

    def selecionarDirecao(self):
        while (pressionado == 0):
            if Button.UP in ev3.buttons.pressed():
                pressionado = 1
                self.direcao = 1  # direita
            if Button.DOWM in ev3.buttons.pressed():
                pressionado = 1
                self.direcao = -1 # esquerda
            

    # chama as respectivas ações selecionadas
    def executaEstrategia(self):
        if self.estrategia == 'arcoInicial':
            self.arcoInicial() # colocar valores Numericos padronizados de cada robo
        elif self.estrategia == 'manobraInicial':
            self.manobraInicial()
        elif self.estrategia == 'armadilhaInicial':
            self.armadilhaInicial()


    def arcoInicial(self):             
        locomocao.arco(Vlin, VAng*self.direcao)   # Alterar Vlin e Vang correspondentes ao robo
        time.sleep(tempo)                         # alterar tempo
        locomocao.giro(pwm*self.direcao)         # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        time.sleep(tempo)                         # Alterar tempo     

    def manobraInicial(self):
        locomocao.giro(-pwm*self.direcao)         # Alterar pwm correspondente ao robo
        time.sleep(tempo)                         # Alterar tempo (geralmente 0.28) 
        locomocao.arco(Vlin, VAng*self.direcao)   # Alterar Vlin e Vang correspondentes ao robo
        time.sleep(tempo)                         # alterar tempo
        locomocao.giro(pwm*self.direcao)         # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        time.sleep(tempo)                         # Alterar tempo 
        
    # descobrir se precisa ou nao da func giro em armadilhaInicial
    def armadilhaInicial(self):
        locomocao.arco(-Vlin, -VAng*self.direcao) # Alterar Vlin e Vang correspondentes ao robo
        time.sleep(tempo)                         # alterar tempo
        locomocao.giro(pwm*self.direcao)         # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        time.sleep(tempo)                         # Alterar tempo
