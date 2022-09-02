#!/usr/bin/env pybricks-micropython

'''
Módulo responsável pelo ajuste do robô antes dos segundos iniciais da
luta. Aqui são definidas a direção inicial e a estratégia através do
pressionamento de botões.
'''

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# Definicao do objeto com os métodos e atributos relacionados as peças LEGO
ev3 = EV3Brick()

class Inicializacao():
    '''
    Módulo Inicializacao
    ---------------------
    Responsável pela escolha da estratégia inicial através das informações dos botões apertados no Brick, selecionando o tipo de estratégia, a direção da estratégia e a direção inicial de sensoriamento, além da possibilidade de pequenos ajuste no posicionamento inicial do robô.
    '''
    def __init__(self): # Alterar tempos correspondentes ao robo
        '''
        Metodo construtor. Define os atributos utilizados nas selecoes.

        Self@Inicializacao -> None
        '''

        # Botoes do Brick considerando que o Brick tá de lado e com tela para direita do piloto
        self.botao_central  = Button.CENTER
        self.botao_direito  = Button.UP    # Botão para direita é o botão de cima com o Brick de lado
        self.botao_esquerdo = Button.DOWN  # Botao para esquerda é o botao de baixo  do brick de Lado 
        self.botao_cima     = Button.LEFT  # Botao para cima é o botao da esquerda do brick virado de lado 
        self.botao_baixo    = Button.RIGHT # Botao para baixo é o botao da esquerda do brick virado para o lado direito

        # Atributo que define o angulo que o robo gira na correcao
        self.angulo_correcao = 0
        
        # Atributo que define a estrategia selecionada
        self.estrategia_inicial_selecionada = 'padrao'
        self.direcao_estrategia_inicial = 0

        # Atributo que define o sentido do sensoriamento
        self.direcao_sensoriamento_inicial = 0

    def selecionar_correcao_ou_desempate(self):
        '''
        Seleciona se existe alguma correção a ser feita na posição inicial do robô (ângulo de correção: (-90) `anti-horário`, (90) `horário` ou (0) `mantém posição inicial`, ou ainda se é um round de `desempate`. No caso de ser um round de `desempate`, mudam as estratégias da segunda etapa.
        '''
        # Na selecao da correcao, o brick ira piscar uma luz na cor roxa

        ev3.light.on(Color.ORANGE)
            
        # Enquanto algum botao nao for apertado
        while True:
            # Caso o botao direito tenha sido apertado, o angulo de correcao é de 90 graus para a direita
            if self.botao_direito in ev3.buttons.pressed(): # Faz uma correção rotacionando 90 graus sobre o próprio eixo para a direita
                self.angulo_correcao = 35
                break
            # Caso o botao esquerdo tenha sido apertado, o angulo de correcao é de 90 graus para a esquerda
            elif self.botao_esquerdo in ev3.buttons.pressed():
                self.angulo_correcao = -35
                break
            # Caso o botao do centro tenha sido apertado, o angulo de correcao é de 0 graus
            elif self.botao_central in ev3.buttons.pressed():
                self.angulo_correcao = 0
                break
            # Caso o botao de cima tenha sido apertado, vai para a rodada de desempate
            elif self.botao_baixo in ev3.buttons.pressed():
                self.estrategia_inicial_selecionada = 'desempate'
                break
        wait(500)

    # descobrir botao direcao e estrategia
    def selecionar_estrategia_inicial(self): # Segunda selecao 
        """
        Seleciona a estratégia inicial do robô. No caso de, na etapa anterior, ter sido selecionado que se trata de um round de desempate, muda as opções de estratégia e a cor do led do Brick.
        """

        # Verifica se o modo de estrategia eh padrao
        if self.estrategia_inicial_selecionada == 'padrao':
            # Na selecao das estrategias padroes, o brick ira piscar uma luz na cor ciano

            ev3.light.on(Color.GREEN)

            # Enquanto algum botao nao for apertado
            while True:
                if self.botao_cima in ev3.buttons.pressed():
                    self.estrategia_inicial_selecionada = 'moonwalk'
                    break
                elif self.botao_baixo in ev3.buttons.pressed(): 
                    self.estrategia_inicial_selecionada = 'arco'
                    break
                elif self.botao_esquerdo in ev3.buttons.pressed():
                    self.estrategia_inicial_selecionada  = 'comunismo'
                    break
                elif self.botao_direito in ev3.buttons.pressed():
                    self.estrategia_inicial_selecionada  = 'capitalismo'
                    break

        # Caso contrario, verifica se o modo de estrategia eh desempate
        elif self.estrategia_inicial_selecionada == 'desempate':
            # Na selecao das estrategias de desempate, o brick ira piscar uma luz na cor vermelha

            ev3.light.on(Color.RED)

            # Enquanto algum botao nao for apertado
            while True:
                if self.botao_central in ev3.buttons.pressed():
                    self.estrategia_inicial_selecionada = 'bixo_piruleta'
                    break
        wait(500)

    def selecionar_direcao_movimento(self): # Selecao 3 movimentacao
        '''
        Seleciona a direção para onde a estratégia inicial será executada: (-1) `esquerda` ou (1) `direita`.
        ''' 
        
        ev3.light.on(Color.ORANGE)

        while True:
            if self.botao_direito in ev3.buttons.pressed(): 
                self.direcao_estrategia_inicial = 1  # direita
                if self.estrategia_inicial_selecionado == 'moonwalk':
                    self.direcao_sensoriamento_inicial = 1
                else:
                    self.direcao_sensoriamento_inicial = -1
                break
            elif self.botao_esquerdo in ev3.buttons.pressed():
                self.direcao_estrategia_inicial = -1 # esquerda
                if self.estrategia_inicial_selecionada == 'moonwalk':
                    self.direcao_sensoriamento_inicial = -1
                else:
                    self.direcao_sensoriamento_inicial = 1
                break
            elif self.botao_central in ev3.buttons.pressed():
                self.estrategia_inicial_selecionada = 'radar'
                break
            elif self.botao_baixo in ev3.buttons.pressed():
                self.estrategia_inicial_selecionada = 'full_re_honesto'
                break
            elif self.botao_cima in ev3.buttons.pressed():
                self.estrategia_inicial_selecionada = 'full_frente_honesto'
                break
        wait(500)      
    
    def selecionar_direcao_sensoriamento(self):
        '''
        Seleciona a direção para onde o sensoriamento irá iniciar quando entrar no loop de perseguição do adversário. Essa direção só será utilizada até a primeira detecção do adversário. Essa é a última etapa da seleção de estratégia.
        '''
        ev3.light.on(Color.RED)

        while True:
            if self.botao_esquerdo in ev3.buttons.pressed():
                self.direcao_sensoriamento_inicial = 1  # direita (sentido horario)
                break 
            elif self.botao_direito in ev3.buttons.pressed():
                self.direcao_sensoriamento_inicial = -1 #esquerda (Sentido anti horario) 
                break
            
        ev3.light.on(Color.GREEN)
        wait(500)
