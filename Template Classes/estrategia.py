#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# Create your objects here.
ev3 = EV3Brick()

# Estamos aplicando PID em algum lugar?
class Estrategia():

    def __init__(self, motores):
        self.motores = motores
 
    # chama as respectivas ações selecionadas
    def executa_estrategia_inicial(self, estrategia_selecionada):
        if estrategia_selecionada == 'arcoInicial':
            self.arcoInicial() # colocar valores Numericos padronizados de cada robo
        elif estrategia_selecionada == 'manobraInicial':
            self.manobraInicial()
        elif estrategia_selecionada == 'armadilhaInicial':
            self.armadilhaInicial()
            
    # girar ao redor de si ate encontrar algo
    # 100 eh valor arbitrario, teremos q testar e descobrir o real
    # na main, chamar tudo e botar loop pra recalcular sensores sempre ate achar oponente, full frente;
    def radarSimples(self,erro):
        if erro < 0:
            self.motores.giro(-100)
        if erro == 0:
            self.motores.reta(100)
        if erro > 0:
            self.motores.giro(100) 

    # vai andando em arcos ate encontrar algo
    # 100 e 15 eh valor arbitrario, teremos q testar e descobrir o real
    def radarArco (self,erro):
        if erro < 0:
            self.motores.arco(100,-15)
        if erro == 0:
            self.motores.reta(100)
        if erro > 0:
            self.motores.arco(100,15) 

    # vai andando em arcos ate encontrar algo
    def radarPID (self, erro, vLin=0):
        # na func arco - primeiro argumento: Vlin; segundo argumento: erro;
        if erro != 0:
            self.motores.arco(vLin,erro)
        if erro == 0:
            self.motores.reta(100)

    def manobraArco():
        pass

    def moonwalk():
        pass

    #def arco_de_costas

    #def full_frente_honesta():



    def arcoInicial(self):             
        locomocao.arco(Vlin, VAng*self.direcao) # Alterar Vlin e Vang correspondentes ao robo
        time.sleep(tempo)                       # Alterar tempo
        locomocao.giro(pwm*self.direcao)        # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        time.sleep(tempo)                       # Alterar tempo

    def manobraInicial(self):
        locomocao.giro(-pwm*self.direcao)       # Alterar pwm correspondente ao robo
        time.sleep(tempo)                       # Alterar tempo (geralmente 0.28) 
        locomocao.arco(Vlin, VAng*self.direcao) # Alterar Vlin e Vang correspondentes ao robo
        time.sleep(tempo)                       # alterar tempo
        locomocao.giro(pwm*self.direcao)        # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        time.sleep(tempo)                       # Alterar tempo 
        
    # descobrir se precisa ou nao da func giro em armadilhaInicial
    def armadilhaInicial(self):
        locomocao.arco(-Vlin, -VAng*self.direcao) # Alterar Vlin e Vang correspondentes ao robo
        time.sleep(tempo)                         # alterar tempo
        locomocao.giro(pwm*self.direcao)          # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        time.sleep(tempo)                         # Alterar tempo
