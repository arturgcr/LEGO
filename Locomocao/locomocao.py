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
      
    def __init__(self, strMotorDireita, strMotorEsquerdo, invertido = 'DEFAULT'):
        # comecei definindo variaveis e pegando motores e respectivas portas (caso venham 2 ou mais motores)
        # ao inves de string, definir como array pois motores ja vem separados: [a, b, c, d]
        # caso nao possa, mudar modo com o qual a função define os motores (acredito que pode e eh mais eficiente)
        self.motores_direita = []
        self.motores_esquerda = []
        self.invertido = invertido

        for porta in strMotorDireita: 
            self.motores_direita.append(Motor.Port(porta))
        for porta in strMotorEsquerdo:
            self.motores_esquerda.append(Motor.Port(porta))

    # Função que inverte o pwm caso os motores de certo lado estejam invertidos.
    # "ALL" - todos invertidos, "DEFAULT" - Nenhum motor invertido.
    # "RIGHT/LEFT" - motores da direita ou da esquerda estão invertidos, respectivamente.
    def controle_sentido_direita(self):
        sentido = 1
        if self.invertido == "ALL" or "RIGHT":
            sentido = -1
            return sentido
    def controle_sentido_esquerda(self):
        sentido = 1
        if self.invertido == "ALL" or "LEFT":
            sentido = -1
            return sentido
    
    # Aplica o valor de pwm [-100, 100] nas rodas do lado esquerdo.
    def AplicarRodaEsquerda ( self, pwm):
        for motor in self.motores_esquerda :
            motor.dc( -pwm * self.controle_sentido_esquerda())

    # Aplica o valor de pwm [-100, 100] nas rodas do lado direito.
    def AplicarRodaDireita ( self, pwm):
        for motor in self.motores_direita :
            motor.dc( -pwm * self.controle_sentido_direita())

    # usando as funcs acima para ir pra frente com a mesma potencia
    def reta( self, pwm = 100 ):
        self.AplicarRodaEsquerda( -pwm )
        self.AplicarRodaDireita ( -pwm )

    # 
    def arco (self, velocidadeLinear = 100, velocidadeAngular=15): # [Vang: que é metade da diferença de potencia entre os motores]
        self.AplicarRodaEsquerda ( velocidadeLinear + velocidadeAngular )
        self.AplicarRodaDireita ( velocidadeLinear - velocidadeAngular )

    # se gira em torno do proprio eixo para direita, motor esq vai pra trás (-1) na potencia pwm, e
    #  motor dir vai pra frente na potencia pwm, o inverso eh valido, ficando:
    def giro(self, pwm = 100):
        self.AplicarRodaEsquerda( -pwm )
        self.AplicarRodaDireita ( pwm )

    # Pára o motor usando fricção e a tensão que este gira na inércia, atua como um freio fraco.
    def Frear (self):
        for motor in self.motores_direita :
            motor.brake()
        for motor in self.motores_esquerda :
            motor.brake()

# Write your program here.
ev3.speaker.beep()

