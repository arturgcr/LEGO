#!/usr/bin/env pybricks-micropython

"""
Módulo responsável pela definição da classe com os métodos e atributos
relacionados às estratégias.
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


class Estrategia():
    """
    Classe com os métodos e atributos relacionados às estratégias. Esta
    classe herda os métodos e atributos da classe Locomocao do módulo
    locomocao.
    """
    def __init__(self, obj_locomocao):
        """
        Método construtor. Executa o método construtor da super classe
        Locomocao.

        Self@Estrategia, list[str], list[str], str -> None
        """
        self.motores = obj_locomocao
    
    def executa_correcao(self, angulo_correcao):
        '''
        Método que recebe um ângulo que, se for diferente de 0, corrige
        o ângulo do robô 90° (para direita ou esquerda) antes de
        executar a estratégia inicial de fato.

        Self@Estrategia, int -> None
        '''
        # Verifica se o ângulo é diferente de 0
        if angulo_correcao != 0:
            # Verifica se o ângulo é igual a 90
            if angulo_correcao == 90:
                # Gira o robô no sentido horário
                self.motores.giro(100)
                wait(3000)
            # Verifica se o ângulo é igual a -90
            elif angulo_correcao == -90:
                # Gira o robô no sentido anti-horário
                self.motores.giro(-100)
                wait(3000)
        # Caso contrário, faz nada
        else:
            pass
    
    def executa_estrategia_inicial(self, estrategia_inicial_selecionada, direcao_estrategia_inicial):
        """
        Método que executa as respectivas ações selecionadas.
        
        Self@Estrategia, str, str -> None
        """
        if estrategia_inicial_selecionada == 'arco':
            self.arco(direcao_estrategia_inicial) # O método já define a direção (esquerda, direita)
        elif estrategia_inicial_selecionada == 'manobra_arco':
            self.manobra_arco(direcao_estrategia_inicial)
        elif estrategia_inicial_selecionada == 'armadilha_arco':
            self.armadilha_arco(direcao_estrategia_inicial)
        elif estrategia_inicial_selecionada == 'moonwalk':
            self.moonwalk(direcao_estrategia_inicial)
        elif estrategia_inicial_selecionada == 'full_frente_honesto':
            self.full_frente_honesto()
        elif estrategia_inicial_selecionada == 'full_re_honesto':
            self.full_re_honesto()

    # Executa a estratégia de perseguição com base na leitura do sensores e do PID
    def executa_estrategia_perseguicao(self, pid_convertido_pwm):
        self.radar(pid_convertido_pwm)
            
    
    # =================================== Estratégias Iniciais =========================================
    def arco(self, direcao):
        """Função que aciona o arco. Neste movimento, o robô deve ser posicionado de lado. Ao selecionar o lado,
        o robô irá percorrer a borda da arena"""
        velocidade_linear = 100
        velocidade_angular = 45 * -direcao
        giro_mesmo_sentido = 100 * -direcao # valor para rotacionar na direção oposto que fez o arco
        self.motores.arco(velocidade_linear, velocidade_angular) # Alterar Vlin e Vang correspondentes ao robo
        wait(1700) # o tempo pode variar para cada robô
        self.motores.giro(giro_mesmo_sentido)
        wait(500)
        
    

    def bixo_piruleta(self, direcao, pwm):
        """"O Robô começa de costas, na linha do adversário. O robo gira no eixo de apenas uma das rodas"""
        self.motores.giro(pwm*direcao)
        wait()

    # Manobra + Arco => segue reto por alguns segundos e executa um arco
    def comunismo(self, direcao):
        '''
        Executa um curto movimento em linha reta e logo em seguida executa um arco e finaliza se voltando para o centro da arena.
        '''
        velocidade_linear = 100
        velocidade_angular = 15 * direcao
        giro_sentido_oposto = 100 * -direcao
        self.motores.reta()
        wait(200)
        self.motores.arco(velocidade_linear, velocidade_angular) # Alterar Vlin e Vang correspondentes ao robo
        wait(1000) # alterar tempo
        self.motores.giro(giro_sentido_oposto) # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente 
        
   
    # Arco de costas --> O robô posicionado de lado faz um arco para trás e depois um giro para o centro da arena
    def moonwalk(self, direcao):
        """Função que aciona o arco. Neste movimento, o robô deve ser posicionado de lado. Ao selecionar o lado,
        o robô irá percorrer a borda da arena de costas"""     
        velocidade_linear = 100
        velocidade_angular = 15 * direcao
        giro_mesmo_sentido = 100 * direcao # valor para girar o robô no mesmo sentido que a direção da estrategia 
        self.motores.arco(-velocidade_linear, velocidade_angular) # Alterar Vlin e Vang correspondentes ao robo
        wait(3500) # Alterar Tempo
        self.motores.giro(giro_mesmo_sentido) # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        
    def full_frente_honesto(self, direcao):
        '''Uma full frente honesta, nada mais nada menos. O robô apenas vai pra frente com tudo, cuidados devem ser tomados
            com essa manobra '''
        velocidade = 100 * abs(direcao)
        self.motores.reta(velocidade)
        wait(5000)
    

    def full_re_honesto(self, direcao):
        '''Uma full frente honesta, nada mais nada menos. O robô apenas vai pra frente com tudo, cuidados devem ser tomados
            com essa manobra '''
        velocidade = -100 * abs(direcao)
        self.motores.reta(velocidade)
        wait(5000)

    # Armadilha reta -
    def baby_come_back(self, pwm):
        """"O robô pode estar posicionado de qualquer forma, mas longe da borda da arena. Inicia dando uma ré, totalmente reta"""
        pass

    # Manobra + Arco invertida
    def capitalismo(self, direcao):
        """"O robô é posicionado de frente um pouco mais no centro na arena. Inicialmente vai para trás ( da ré). 
        Faz o giro para uma direção selecionada (gira) e executa o arco na direção selecionada"""

        velocidade_linear = 100
        velocidade_angular = 15 * direcao
        giro_mesmo_sentido = 100 * direcao
        self.motores.reta(-100)
        wait(200)
        self.motores.arco(-velocidade_linear, velocidade_angular) #
        wait(1000) # alterar tempo
        self.motores.giro(giro_mesmo_sentido) # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        wait() # Alterar tempo

    # ==================================================================================================
    
    # ============================ Estratégias de Perseguição ========================================== 
    # gira ao redor de si até encontrar algo
    def radar(self, pwm):
        # Gira no sentido anti-horário com potência determinada pelo PID
        if pwm != 0:
            self.motores.giro(pwm) # direcao_oponente = -1
        # Full frente com potência máxima, desconsiderando PID
        if pwm == 0:
            self.motores.reta(100)
    # ==================================================================================================

    """ # vai andando em arcos ate encontrar algo
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
            self.motores.reta(100) """
