# CONFIGURAÇÕES INICIAIS - NÃO ESQUECER ---------------
# -> Aqui colocar os valores a serem alterados e separar por cada robo (ex: tempoManobra - treta: 5) 
# -> Treta - Codigo antigo - TESTAR A PARTIR DE:
#    erroBase = 15
#    kp = 2
#    ki = 0
#    kd = 1.2


# ---------------------------------------------------------------------------------------------------------------------------------------------------

#!/usr/bin/env pybricks-micropython
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
        
        # Botões do Brick considerando que o Brick tá de lado e com tela para direita do piloto
        self.botao_direita = Button.UP # Botão para direita é o botão de cima com o Brick de lado
        self.botao_esquerda = Button.DOWN
        self.botao_centro = Button.CENTER
        self.botao_cima = Button.LEFT
        self.botao_baixo = Button.RIGHT

        self.pressionado = 0    # variavel para encerrar loop / se 0, botao nao pressionado, se 1, botao pressionado
        self.tipo_estrategia = 'padrao' # Variável para definir se será estratégia padrão ou de desempate


    def selecionarCorrecao(self):
        ev3.light(Color.PURPLE)  
        
        while (self.pressionado == 0):
            if self.botao_direita in ev3.buttons.pressed(): #Faz uma correção rotacionando 90º sobre o próprio eixo para a direita
                self.pressionado = 1
                self.direcao = 1  # direita
            elif self.botao_centro in ev3.buttons.pressed():
                self.pressionado = 1
            elif self.botao_esquerda in ev3.buttons.pressed():
                self.pressionado = 1
                self.direcao = -1 # esquerda
            elif self.botao_cima in ev3.buttons.pressed():
                self.pressionado = 1
                self.tipo_estrategia = 'desempate'        
        
        time.sleep(1)
        self.pressionado = 0
                
                
    # descobrir botao direcao e estrategia
    def selecionarEstrategia(self):
         
        ev3.light(Color.RED)
        
        while (self.pressionado == 0 and self.tipo_estrategia == 'padrao'):
            if self.botao_direita in ev3.buttons.pressed(): #duvida: buttons.pressed() ou brick.buttons.pressed()
                self.pressionado = 1
                self.estrategia = 'arcoInicial' 
            elif self.botao_esquerda in ev3.buttons.pressed():
                self.pressionado = 1
                self.estrategia = 'manobraInicial' 
            elif self.botao_centro in ev3.buttons.pressed():
                self.pressionado = 1
                self.estrategia = 'armadilhaInicial'
            #elif self.botao_cima
            #elif self.botao_baixo

        time.sleep(1) # espera por 1 segundo
        self.pressionado = 0

    def selecionarDirecaoMovimento(self):
        while (self.pressionado == 0):
            if self.botao_cima in ev3.buttons.pressed():
                self.pressionado = 1
                self.direcao = 1  # direita
            if self.botao_baixo in ev3.buttons.pressed():
                self.pressionado = 1
                self.direcao = -1 # esquerda
    
    def selecionarDirecaoSensoriamento(self):
        while (self.pressionado == 0):
            if self.botao_cima in ev3.buttons.pressed():
                self.pressionado = 1
                self.direcao = 1  # direita
            if self.botao_baixo in ev3.buttons.presses():
                self.pressionado = 1
                self.direcao = -1 #esquerda 


            

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
