#!/usr/bin/env pybricks-micropython

"""
Módulo responsável pela definicao da classe com os métodos e atributos
relacionados a locomoção do robô.
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

class Locomocao():
    '''
    Módulo de Locomoção
    -------------------

    Responsável por instanciar motores e controlar seus movimentos.
    '''
    def __init__(self, motores_direita, motores_esquerda, servo_motores = None, invertido = 'ALL'):
        """
        Método construtor que recebe uma lista de strings com as portas
        dos motores da direita, outra lista com os motores da esquerda e
        uma string isolada com o padrão de inversão desses motores
        ('DEFAULT', 'ALL', 'RIGHT' ou 'LEFT'). Os demais métodos dessa
        classe são referentes aos tipos de movimentos que serão
        executados no módulo de Estrategia: reta(), arco(), giro() e
        frear().

        Self@Locomocao, list[str], list[str], str -> None
        """
        # Atributo para armazenar os motores e servo-motores
        self.motores_esquerda = []
        self.motores_direita = []
        self.servo_motores = []

        # Atributo para armazenar se o sentido dos motores é invertido ou não
        self.invertido = invertido

        # Adiciona no atributo "self.motores_esquerda" os motores esquerdos com suas respectivas portas
        for porta in motores_esquerda:
            self.motores_esquerda.append(Motor(self.seleciona_porta(porta)))

        # Adiciona no atributo "self.motores_direita" os motores direitos com suas respectivas portas
        for porta in motores_direita: 
            self.motores_direita.append(Motor(self.seleciona_porta(porta)))

        if servo_motores != None:
            for porta in servo_motores:
                self.servo_motores.append(Motor(self.seleciona_porta(porta)))

        # Controle de inversão dos motores:
        # - "ALL"        -> todos invertidos;
        # - "DEFAULT"    -> Nenhum motor invertido.
        # - "LEFT/RIGHT" -> motores da esquerda ou da direita estão invertidos, respectivamente.
        self.sentido_direita = 1
        if self.invertido == "ALL" or "RIGHT":
            self.sentido_direita = -1

        self.sentido_esquerda = 1
        if self.invertido == "ALL" or "LEFT":
            self.sentido_esquerda = -1

    def seleciona_porta(self, porta):
        """
        Método para selecionar a porta do motor.

        Self@Locomocao, str -> ?
        """
        if porta == 'A':
            return Port.A
        elif porta == 'B':
            return Port.B
        elif porta == 'C':
            return Port.C
        elif porta == 'D':
            return Port.D

    def aplicar_roda_esquerda(self, pwm):
        """
        Método para aplicar o valor de PWM, que varia no intervalo
        [-100, 100], nos motores esquerdos.

        Self@Locomocao, int -> None
        """
        for motor in self.motores_esquerda:
            motor.dc(-pwm * self.sentido_esquerda)

    def aplicar_roda_direita(self, pwm):
        """
        Método para aplicar o valor de PWM, que varia no intervalo
        [-100, 100], nos motores direitos.

        Self@Locomocao, int -> None
        """
        for motor in self.motores_direita:
            motor.dc(-pwm * self.sentido_direita)

    def servo_motor_libera_rampa(self):
        '''
        Move o servo-motor responsável por liberar a rampa da violeta. Atualmente, está configurado para gerar 180° no sentido anti-horário (-180). Com a adição de mais servos-motores, esse método precisará ser revisto.
        '''
        for servo_motor in self.servo_motores:
            servo_motor.angle(-180) # acho que dessa forma, vai girar 180° no sentido anti-horário

    def mapy(self, valor_a_ser_convertido, minimo_da_entrada, maximo_da_entrada, minimo_da_saida,  maximo_da_saida):
        """
        Método com a função map lá do Arduino em sua verdadeira forma, em Python.

        self@Locomocao, int ou float, int ou float, int ou float, int ou float, int ou float -> float
        """
        diferenca_das_entradas = maximo_da_entrada - minimo_da_entrada
        diferenca_das_saidas = maximo_da_saida - minimo_da_saida
        diferenca_do_valor_a_ser_convertido_com_o_minimo_da_entrada = valor_a_ser_convertido - minimo_da_entrada
        return (diferenca_do_valor_a_ser_convertido_com_o_minimo_da_entrada * diferenca_das_saidas) / diferenca_das_entradas + minimo_da_saida

    def mixagem(self, velocidade_linear, velocidade_angular):
        """
        Método que realiza os cálculos da mixagem.

        OBS.: Os parâmetros velocidade linear e angular variam no intervalo [-100, 100].

        self@Locomocao, int, int -> tuple[int, int]
        """
        # Realiza os cálculos da mixagem
        pwm_roda_esquerda = velocidade_linear + velocidade_angular
        pwm_roda_direita  = velocidade_linear - velocidade_angular

        # Converte de volta para o intervalo [-100, 100]
        pwm_roda_esquerda = int(self.mapy(pwm_roda_esquerda, -200, 200, -100, 100))
        pwm_roda_direita  = int(self.mapy(pwm_roda_direita, -200, 200, -100, 100))

        # Retorna uma tupla com a primeira posição o valor de PWM do motor esquerdo e a segunda posição com o valor do motor direito
        return pwm_roda_esquerda, pwm_roda_direita

    def locomover(self, velocidade_linear, velocidade_angular):
        """
        Método que move o robô de acordo com a velocidade linear e
        angular passadas.

        self@Locomocao, int, int -> None
        """
        # Obtém o valor da potência dos motores a partir do cálculo da mixagem
        mixagem = self.mixagem(velocidade_linear, velocidade_angular)

        # Aplica o resultado do cálculo da mixagem nos motores
        self.aplicar_roda_esquerda(mixagem[0])
        self.aplicar_roda_direita(mixagem[1])

    # usando as funcs acima para ir pra frente com a mesma potencia
    def reta(self, pwm = 100):
        """
        Método para mover o robo em linha reta. Para isso, eh colocado a
        velocidade linear com valor de PWM variavel e a velocidade
        angular com valor nulo.

        Self@Locomocao, int -> None
        """
        self.locomover(pwm, 0)

    # talvez arco nao esteja rodando pras duas direcoes, e sim, so pra direita (se sim, criar um if e inverter sinais)
    def arco (self, velocidade_linear = 100, velocidade_angular = 15): # [Vang: que é metade da diferença de potencia entre os motores]
        """
        Método para o robô fazer um movimento de arco. Para isso, eh
        colocado a velocidade linear e angular com valor de PWM
        variavel.

        Self@Locomocao, int, int -> None
        """
        self.locomover(velocidade_linear, velocidade_angular)

    #  Gira em torno do proprio eixo utilizando a função locomover, com o a velocidade linear em 0 e a velocidade angular em 100(pwm)
    #  motor dir vai pra frente na potencia pwm, o inverso eh valido, ficando:
    def giro(self, pwm = 100):
        """
        Método para para o robo girar em reta. Para isso, é colocado a
        velocidade angular com valor de PWM variável e a velocidade
        linear com valor nulo.

        Self@Locomocao, int -> None
        """
        self.locomover(0, pwm)
 
    # Pára o motor usando fricção e a tensão que este gira na inércia, atua como um freio fraco.
    def frear(self):
        """
        Método para frear os motores do robo.

        Self@Locomocao -> None
        """
        for motor in self.motores_direita:
            motor.brake()
        for motor in self.motores_esquerda:
            motor.brake()
