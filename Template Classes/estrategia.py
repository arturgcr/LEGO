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
            if angulo_correcao == 35:
                # Gira o robô no sentido horário
                self.motores.giro(100)
                wait(500)
            # Verifica se o ângulo é igual a -90
            elif angulo_correcao == -35:
                # Gira o robô no sentido anti-horário
                self.motores.giro(-100)
                wait(500)
        # Caso contrário, faz nada
        else:
            pass
    
    def executa_estrategia_inicial(self, estrategia_inicial_selecionada, direcao_estrategia_inicial):
        """
        Método que executa as respectivas ações selecionadas.
        
        Self@Estrategia, str, str -> None
        """
        if estrategia_inicial_selecionada == 'arco': #Pronto
            self.arco(direcao_estrategia_inicial) # O método já define a direção (esquerda, direita)
        elif estrategia_inicial_selecionada == 'comunismo': #Pronto
            self.comunismo(direcao_estrategia_inicial)
        elif estrategia_inicial_selecionada == 'capitalismo': #Pronto
            self.capitalismo(direcao_estrategia_inicial)
        elif estrategia_inicial_selecionada == 'moonwalk': #Pronto
            self.moonwalk(direcao_estrategia_inicial)
        elif estrategia_inicial_selecionada == 'full_frente_honesto': #Pronto
            self.full_frente_honesto()
        elif estrategia_inicial_selecionada == 'full_re_honesto': #Pronto
            self.full_re_honesto()
        else:
            print('ATENCAO! Nenhuma estrategia selecionada')        


    # Executa a estratégia de perseguição com base na leitura do sensores e do PID
    def executa_estrategia_perseguicao(self, pid_convertido_pwm):
        self.radar(pid_convertido_pwm)
            
    
    # =================================== Estratégias Iniciais =========================================
    def arco(self, direcao):
        """Função que aciona o arco. Neste movimento, o robô deve ser posicionado de lado. Ao selecionar o lado,
        o robô irá percorrer a borda da arena"""
        velocidade_linear = 100
        velocidade_angular = 50* -direcao
        giro_mesmo_sentido = 100 * -direcao # valor para rotacionar na direção oposto que fez o arco
        self.motores.arco(velocidade_linear, velocidade_angular) # Alterar Vlin e Vang correspondentes ao robo
        print('iniciou o arco')
        wait(2000) # o tempo pode variar para cada robô
        self.motores.giro(giro_mesmo_sentido)
        wait(550)
        print('girou no msm sentido')

    # def andarUmPouquinho():
    # a violeta ja abaixa a rampa oq mostra p juiz que ela ta viva
    # mas o treta nao
    # poderiamos fazer ele andar pouquinho mas isso n abaixaria o chifre
    # nao abaixar o chifre --> sensoria o proprio chifre
    # Ftreta

    # def maracutaia(self):
    #     distancia_min = 100 #mudar
    #     distancia_max = 400 #mudar
    #     distancia_de_ataque = 20 #mudar
     
    #     ataque_do_oponente = False
    #     distancia = 0
    
    #     while ataque_do_oponente == False:
    #         distancia_antiga = distancia
    #         distancia = self.sensores[sensor].distance()

    #         if distancia <= distancia_min:
    #             break

    #         if distancia > distancia_max:
    #             #procurar ate achar
                  #SO PROCURAR
    #             continue
            
    #         wait(50)
    #         andarUmPouquinho()
    #         wait(50) #breve tempo em que ele vai ficar parado por loop
            
    #         if (distancia - distancia_antiga) > distancia_de_ataque :
    #             #diferenca de ditancia / tempo no wait = velocidade
    #             #se for muito rapido eh ataque
    #             ataque_do_oponente = True
         

    def bixo_piruleta(self, direcao, pwm):
        """"O Robô começa de costas, na linha do adversário. O robo gira no eixo de apenas uma das rodas"""
        self.motores.giro(pwm*direcao)
        wait(1500)

    # Manobra + Arco => segue reto por alguns segundos e executa um arco
    def comunismo(self, direcao):
        '''
        Executa um curto movimento em linha reta e logo em seguida executa um arco e finaliza se voltando para o centro da arena.
        '''
        velocidade_linear = 100
        velocidade_angular = 50 * -direcao
        giro_sentido_oposto = 100 * -direcao
        giro_mesmo_sentido = 100 * direcao
        self.motores.reta() #frente
        wait(200)
        self.motores.giro(giro_mesmo_sentido) #angulo
        wait(350)
        self.motores.arco(velocidade_linear+20, velocidade_angular ) # Alterar Vlin e Vang correspondentes ao robo
        wait(1200) # alterar tempo
        self.motores.giro(giro_sentido_oposto) #angulo
        wait(250)
        
   
    # Arco de costas --> O robô posicionado de lado faz um arco para trás e depois um giro para o centro da arena
    def moonwalk(self, direcao):
        """Função que aciona o arco. Neste movimento, o robô deve ser posicionado de lado. Ao selecionar o lado,
        o robô irá percorrer a borda da arena de costas"""  
        print("Meu nome é Michael Jackson!")   
        velocidade_linear = 200
        velocidade_angular = 150 * direcao
        giro_mesmo_sentido = 100 * -direcao # valor para girar o robô no mesmo sentido que a direção da estrategia 
        self.motores.arco(-velocidade_linear, velocidade_angular) # Alterar Vlin e Vang correspondentes ao robo
        print('velocidade linear:', velocidade_linear)
        print('velocidade angular:', velocidade_angular)
        wait(2500) # Alterar Tempo
        self.motores.giro(giro_mesmo_sentido) # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        wait(700)
        
    def full_frente_honesto(self):
        '''Uma full frente honesta, nada mais nada menos. O robô apenas vai pra frente com tudo, cuidados devem ser tomados
            com essa manobra '''
        
        velocidade = 100 
        self.motores.reta(velocidade)
        wait(5000)
    

    def full_re_honesto(self):
        '''Uma full frente honesta, nada mais nada menos. O robô apenas vai pra frente com tudo, cuidados devem ser tomados
            com essa manobra '''
        velocidade = 100 
        self.motores.re(velocidade)
        wait(7000)

    # Armadilha reta -
    def baby_come_back(self, pwm):
        """"O robô pode estar posicionado de qualquer forma, mas longe da borda da arena. Inicia dando uma ré, totalmente reta"""
        pass

    # Manobra + Arco invertida
    def capitalismo(self, direcao):
        """"O robô é posicionado de frente um pouco mais no centro na arena. Inicialmente vai para trás ( da ré). 
        Faz o giro para uma direção selecionada (gira) e executa o arco na direção selecionada"""

        velocidade_linear = 100
        velocidade_angular = 50 * -direcao
        giro_mesmo_sentido = 100 * direcao
        giro_sentido_oposto = 100 * -direcao
        #self.motores.reta(-velocidade_linear)
        self.motores.re(velocidade_linear)
        wait(450)
        self.motores.giro(giro_mesmo_sentido)
        wait(350)
        self.motores.arco(velocidade_linear +20, velocidade_angular) #
        wait(1700) # alterar tempo
        self.motores.giro(giro_sentido_oposto) # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        wait(500) # Alterar tempo

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
