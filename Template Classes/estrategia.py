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
    
    def executa_correcao(self, angulo_correcao):
        '''
        Recebe um angulo_correcao que, se for diferente de 0, corrige o ângulo do robô 90° (para direita ou esquerda) antes de executar a estratégia inicial de fato.
        '''
        if angulo_correcao != 0:
            if angulo_correcao == 90:
                self.motores.giro(100)
            elif angulo_correcao == -90:
                self.motores.giro(-100)
        else:
            pass
    
    # chama as respectivas ações selecionadas
    def executa_estrategia_inicial(self, estrategia_inicial_selecionada, direcao_estrategia_inicial):
        if estrategia_inicial_selecionada == 'arco':
            self.arco() # colocar valores Numericos padronizados de cada robo
        elif estrategia_inicial_selecionada == 'manobra_arco':
            self.manobra_arco()
        elif estrategia_inicial_selecionada == 'armadilha_arco':
            self.armadilha_arco()

    # Executa a estratégia de perseguição com base na leitura do sensores e do PID
    def executa_estrategia_perseguicao(self, direcao_oponente, pid):
        self.radar(direcao_oponente, pid)
            
    # girar ao redor de si ate encontrar algo
    # 100 eh valor arbitrario, teremos q testar e descobrir o real
    # na main, chamar tudo e botar loop pra recalcular sensores sempre ate achar oponente, full frente;
    def radar(self, direcao_oponente, pid):
        if direcao_oponente < 0:
            self.motores.giro(direcao_oponente * pid)
        if direcao_oponente == 0:
            self.motores.reta(100)
        if direcao_oponente > 0:
            self.motores.giro(direcao_oponente * pid) 

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



    def arco(self):             
        locomocao.arco(Vlin, VAng*self.direcao) # Alterar Vlin e Vang correspondentes ao robo
        time.sleep(tempo)                       # Alterar tempo
        locomocao.giro(pwm*self.direcao)        # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        time.sleep(tempo)                       # Alterar tempo

    def manobra_arco(self):
        locomocao.giro(-pwm*self.direcao)       # Alterar pwm correspondente ao robo
        time.sleep(tempo)                       # Alterar tempo (geralmente 0.28) 
        locomocao.arco(Vlin, VAng*self.direcao) # Alterar Vlin e Vang correspondentes ao robo
        time.sleep(tempo)                       # alterar tempo
        locomocao.giro(pwm*self.direcao)        # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        time.sleep(tempo)                       # Alterar tempo 
        
    # descobrir se precisa ou nao da func giro em armadilhaInicial
    def armadilha_arco(self):
        locomocao.arco(-Vlin, -VAng*self.direcao) # Alterar Vlin e Vang correspondentes ao robo
        time.sleep(tempo)                         # alterar tempo
        locomocao.giro(pwm*self.direcao)          # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        time.sleep(tempo)                         # Alterar tempo
