#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information

# Create your objects here.
ev3 = EV3Brick()

class Locomocao():
    '''
    Módulo de Locomoção
    -------------------
    Responsável por instanciar motores e controlar seus movimentos. Recebe como construtor uma lista de strings com as portas dos motores da direita, outra lista com os motores da esquerda e uma string isolada com o padrão de inversão desses motores ('DEFAULT', 'ALL', 'RIGHT' ou 'LEFT'). Os demais métodos dessa classe são referentes aos tipos de movimentos que serão executados no módulo de Estrategia: reta(), arco(), giro() e frear().
    '''
    def __init__(self, motores_direita, motores_esquerda, invertido = 'DEFAULT'):
        # comecei definindo variaveis e pegando motores e respectivas portas (caso venham 2 ou mais motores)
        # ao inves de string, definir como array pois motores ja vem separados: [a, b, c, d]
        # caso nao possa, mudar modo com o qual a função define os motores (acredito que pode e eh mais eficiente)
        self.motores_direita = []
        self.motores_esquerda = []
        self.invertido = invertido

        for porta in motores_direita: 
            self.motores_direita.append(Motor(porta))
        for porta in motores_esquerda:
            self.motores_esquerda.append(Motor(porta))

        # Controle de inversão dos motores
        # "ALL" - todos invertidos, "DEFAULT" - Nenhum motor invertido.
        # "RIGHT/LEFT" - motores da direita ou da esquerda estão invertidos, respectivamente.
        # Possivelmente, esse bloco pode ser removido (junto dos locais onde é chamado) e podemos manter o sentido definido pelo valor do pwm.
        
        self.sentido_direita = 1
        if self.invertido == "ALL" or "RIGHT":
            self.sentido_direita = -1
            
        
        self.sentido_esquerda = 1
        if self.invertido == "ALL" or "LEFT":
            self.sentido_esquerda = -1
            
    # Aplica o valor de pwm [-100, 100] nas rodas do lado esquerdo.
    def aplicar_roda_esquerda(self, pwm):
        for motor in self.motores_esquerda:
            motor.dc(-pwm * self.sentido_esquerda)

    # Aplica o valor de pwm [-100, 100] nas rodas do lado direito.
    def aplicar_roda_direita(self, pwm):
        for motor in self.motores_direita:
            motor.dc(-pwm * self.sentido_direita)

    # usando as funcs acima para ir pra frente com a mesma potencia
    def reta(self, pwm = 100):
        self.aplicar_roda_esquerda(-pwm)
        self.aplicar_roda_direita(-pwm)

    # talvez arco nao esteja rodando pras duas direcoes, e sim, so pra direita (se sim, criar um if e inverter sinais)
    def arco (self, velocidade_linear = 100, velocidade_angular = 15): # [Vang: que é metade da diferença de potencia entre os motores]
        self.aplicar_roda_esquerda(velocidade_linear + velocidade_angular) # segundo a documentação do pyblocks, isso provavelmente vai quebrar, já que Motor.dc() recebe valores entre [-100,100]
        self.aplicar_roda_direita(velocidade_linear - velocidade_angular)

    #  se gira em torno do proprio eixo para direita, motor esq vai pra trás (-1) na potencia pwm, e
    #  motor dir vai pra frente na potencia pwm, o inverso eh valido, ficando:
    def giro(self, pwm = 100):
        self.aplicar_roda_esquerda(pwm)
        self.aplicar_roda_direita(-pwm)
 
    # Pára o motor usando fricção e a tensão que este gira na inércia, atua como um freio fraco.
    def frear(self):
        for motor in self.motores_direita:
            motor.brake()
        for motor in self.motores_esquerda:
            motor.brake()
