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
                self.motores.giro(100) # temos que testar quantos segundos precisa executar esse movimento
            elif angulo_correcao == -90:
                self.motores.giro(-100)
        else:
            pass
    
    # chama as respectivas ações selecionadas
    def executa_estrategia_inicial(self, estrategia_inicial_selecionada, direcao_estrategia_inicial):
        if estrategia_inicial_selecionada == 'arco':
            self.arco(direcao_estrategia_inicial) # O método já define a direção (esquerda, direita)
        elif estrategia_inicial_selecionada == 'manobra_arco':
            self.manobra_arco()
        elif estrategia_inicial_selecionada == 'armadilha_arco':
            self.armadilha_arco()

    # Executa a estratégia de perseguição com base na leitura do sensores e do PID
    def executa_estrategia_perseguicao(self, direcao_oponente, pid_convertido_pwm):
        self.radar(direcao_oponente, pid_convertido_pwm)
            
    
    # =================================== Estratégias Iniciais =========================================
    def arco(self, direcao):             
        velocidade_linear = 100
        velocidade_angular = 15 * direcao
        giro_sentido_oposto = 100 * -direcao # valor para rotacionar na direção oposto que fez o arco
        self.motores.arco(velocidade_linear, velocidade_angular) # Alterar Vlin e Vang correspondentes ao robo
        wait() # o tempo pode variar para cada robô
        self.motores.giro(giro_sentido_oposto) # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        wait() # o tempo pode variar para cada robô

    def manobra_arco(self, direcao):
        self.motores.giro(100 * direcao) # Alterar pwm correspondente ao robo
        wait(0.28) # alterar tempo (geralmente 0.28) 
        self.motores.arco(Vlin, VAng*self.direcao) # Alterar Vlin e Vang correspondentes ao robo
        wait() # alterar tempo
        self.motores.giro(pwm*self.direcao)        # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        wait()                       # Alterar tempo 
        
    # descobrir se precisa ou nao da func giro em armadilhaInicial
    def armadilha_arco(self):
        locomocao.arco(-Vlin, -VAng*self.direcao) # Alterar Vlin e Vang correspondentes ao robo
        time.sleep(tempo)                         # alterar tempo
        locomocao.giro(pwm*self.direcao)          # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        time.sleep(tempo)                         # Alterar tempo
    
    # ==================================================================================================
    
    # ============================ Estratégias de Perseguição ========================================== 
    # gira ao redor de si até encontrar algo
    def radar(self, direcao_oponente, pwm):
        # Gira no sentido anti-horário com potência determinada pelo PID
        if direcao_oponente < 0:
            self.motores.giro(direcao_oponente * pwm) # direcao_oponente = -1
        # Full frente com potência máxima, desconsiderando PID
        if direcao_oponente == 0:
            self.motores.reta()
        # Gira no sentido horário com potência determinada pelo PID
        if direcao_oponente > 0:
            self.motores.giro(direcao_oponente * pwm) # direcao_oponente = 1
    # ==================================================================================================

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
