"""
Módulo responsável pelo ajuste do robô antes dos segundos iniciais da
luta. Aqui são definidas a direção inicial e a estratégia através do
pressionamento de botões.
"""

from pybricks.parameters import Button, Color
from pybricks.tools import wait

class Inicializacao():
    """
    Módulo Inicializacao
    ---
    Responsável pela escolha da estratégia inicial através das informações dos botões apertados no Brick. Com os cliques, são selecionados: o tipo, a estratégia inicial em si, sua direção e o sentido do sensoriamento, além da possibilidade de pequenos ajuste no posicionamento inicial do robô.
    """
    def __init__(self, objeto_EV3): # Alterar tempos correspondentes ao robo
        """
        Metodo construtor. Define os atributos utilizados nas selecoes.

        Self@Inicializacao, EV3Brick -> None
        """
        # Atributo com o objeto da classe EV3Brick
        self.ev3 = objeto_EV3

        # Botoes do Brick considerando que o Brick tá de lado e com tela para direita do piloto
        self.botao_central  = Button.CENTER
        self.botao_direito  = Button.UP    # Botão para direita é o botão de cima com o Brick de lado
        self.botao_esquerdo = Button.DOWN  # Botao para esquerda é o botao de baixo  do brick de Lado 
        self.botao_cima     = Button.LEFT  # Botao para cima é o botao da esquerda do brick virado de lado 
        self.botao_baixo    = Button.RIGHT # Botao para baixo é o botao da esquerda do brick virado para o lado direito

        # Atributo que define o angulo que o robo gira na correcao
        self.angulo_correcao = 0
        
        # Atributo que define os parâmetros da estratégia inicial selecionada
        self.tipo_de_estrategia_inicial = 'padrao'
        self.estrategia_inicial_selecionada = 'radar'
        self.direcao_estrategia_inicial = 0
        self.direcao_sensoriamento_inicial = -1

    def selecionar_correcao_ou_desempate(self):
        """
        selecionar_correcao_ou_desempate()
        ---
        Seleciona se será feita alguma `correção na posição inicial do robô` (ângulo de correção: (-90) `anti-horário`, (90) `horário` ou (0) `mantém posição inicial`, ou ainda se é um round de `desempate`. No caso de ser um round de `desempate`, mudam as estratégias da segunda etapa.
        """

        self.ev3.light.on(Color.ORANGE)
            
        # Enquanto algum botao nao for apertado
        while True:
            # Caso o botao direito tenha sido apertado, o angulo de correcao é de 90 graus para a direita
            if self.botao_direito in self.ev3.buttons.pressed(): # Faz uma correção rotacionando 90 graus sobre o próprio eixo para a direita
                self.angulo_correcao = 35
                break
            # Caso o botao esquerdo tenha sido apertado, o angulo de correcao é de 90 graus para a esquerda
            elif self.botao_esquerdo in self.ev3.buttons.pressed():
                self.angulo_correcao = -35
                break
            # Caso o botao do centro tenha sido apertado, o angulo de correcao é de 0 graus
            elif self.botao_central in self.ev3.buttons.pressed():
                self.angulo_correcao = 0
                break
            # Caso o botao de cima tenha sido apertado, vai para a rodada de desempate
            elif self.botao_baixo in self.ev3.buttons.pressed():
                self.tipo_de_estrategia_inicial = 'desempate'
                break
        wait(500)

    # descobrir botao direcao e estrategia
    def selecionar_estrategia_inicial_primeira_etapa(self): # Segunda selecao 
        """
        selecionar_estrategia_inicial_primeira_etapa()
        ---
        Seleciona 1 das 4 estratégias iniciais. Elas podem ser do tipo `padrao` ou `desempate`. Caso na etapa anterior tenha sido selecionado que se trata de um round de `desempate`, muda as opções de estratégia e a cor do led do Brick. O botão central pula para a próxima etapa.
        """

        # Verifica se o modo de estrategia eh padrao
        if self.tipo_de_estrategia_inicial == 'padrao':

            self.ev3.light.on(Color.GREEN)

            # Etapa de escolha de estratégia, enquanto algum botao nao for apertado a tela do brick fica verde
            while True:
                if self.botao_cima in self.ev3.buttons.pressed():
                    self.estrategia_inicial_selecionada = 'moonwalk'
                    break
                elif self.botao_baixo in self.ev3.buttons.pressed(): 
                    self.estrategia_inicial_selecionada = 'arco'
                    break
                elif self.botao_esquerdo in self.ev3.buttons.pressed():
                    self.estrategia_inicial_selecionada  = 'comunismo'
                    break
                elif self.botao_direito in self.ev3.buttons.pressed():
                    self.estrategia_inicial_selecionada  = 'capitalismo'
                    break
                # Botão central - simplesmente avança para as próximas estratégias
                elif self.botao_central in self.ev3.buttons.pressed():
                    break

        # Caso contrario, verifica se o modo de estrategia eh desempate
        elif self.tipo_de_estrategia_inicial == 'desempate':

            self.ev3.light.on(Color.RED)

            # Etapa de escolha de estrategia de desempate, enquanto algum botao nao for apertado a tela do brick fica vermelha
            while True:
                if self.botao_central in self.ev3.buttons.pressed():
                    self.estrategia_inicial_selecionada = 'bixo_piruleta'
                    break
                elif self.botao_baixo in self.ev3.buttons.pressed():
                    self.estrategia_inicial_selecionada = 'full_re_honesto'
                    break
        
        wait(500)

    def selecionar_estrategia_inicial_segunda_etapa(self):
        """
        selecionar_estrategia_inicial_segunda_etapa()
        ---
        Seleciona 1 das 2 estratégias que não estão na primeira etapa. Apenas tipo Padrão
        """
        
        if self.tipo_de_estrategia_inicial == 'padrao':
            
            self.ev3.light.on(Color.ORANGE)
            
            # Etapa de escolha de outras estratégia, enquanto algum botao nao for apertado a tela do brick fica laranja
            while True:
                if self.botao_cima in self.ev3.buttons.pressed():
                    self.estrategia_inicial_selecionada = 'maracutaia'
                    break
                elif self.botao_baixo in self.ev3.buttons.pressed():
                    self.estrategia_inicial_selecionada = 'maracutaia'
                    break
                elif self.botao_esquerdo in self.ev3.buttons.pressed():
                    self.estrategia_inicial_selecionada = 'de_ladinho'
                    break
                elif self.botao_direito in self.ev3.buttons.pressed():
                    self.estrategia_inicial_selecionada = 'de_ladinho'
                    break
                # Botão central - simplesmente avança para as próximas estratégias
                elif self.botao_central in self.ev3.buttons.pressed():
                    break

        if self.tipo_de_estrategia_inicial == 'desempate':
            pass
            
        wait(500)

    def selecionar_direcao_estrategia_inicial(self): # Selecao 3 movimentacao
        """
        selecionar_direcao_estrategia_inicial()
        ---
        Seleciona a direção de movimendo da estratégia inicial. Por padrão, o sentido de sensoriamento é o contrário do sentido do movimento da estratégia, exceto no 'moonwalk'.
        """ 
        
        self.ev3.light.on(Color.RED)

        while True:
            # Pressionando o botão direito a estratégia será executada para direita
            if self.botao_direito in self.ev3.buttons.pressed(): 
                self.direcao_estrategia_inicial = 1  # direita
                # O sentido do sensoriamento, por padrão, vai ser o contrário, exceto no 'moonwalk'
                if self.tipo_de_estrategia_inicial == 'moonwalk':
                    self.direcao_sensoriamento_inicial = self.direcao_estrategia_inicial # direita
                else:
                    self.direcao_sensoriamento_inicial = -self.direcao_estrategia_inicial # esquerda
                break
            
            # Pressionando o botão esquerdo a estratégia será executada para esquerda
            elif self.botao_esquerdo in self.ev3.buttons.pressed():
                self.direcao_estrategia_inicial = -1 # esquerda
                # O sentido do sensoriamento, por padrão, vai ser o contrário, exceto no 'moonwalk'
                if self.estrategia_inicial_selecionada == 'moonwalk':
                    self.direcao_sensoriamento_inicial = self.direcao_estrategia_inicial # esquerda
                else:
                    self.direcao_sensoriamento_inicial = -self.direcao_estrategia_inicial # direita
                break

            # Ignora as estratégias selecionadas anteriormente e faz simplemente o 'radar'
            elif self.botao_central in self.ev3.buttons.pressed():
                self.estrategia_inicial_selecionada = 'radar'
                break
            
            # Ignora as estratégias selecionadas anteriormente e vai 'full_re_honesto'
            elif self.botao_baixo in self.ev3.buttons.pressed():
                self.estrategia_inicial_selecionada = 'full_re_honesto'
                break

            # Ignora as estratégias selecionadas anteriormente e vai 'full_frente'
            elif self.botao_cima in self.ev3.buttons.pressed():
                self.estrategia_inicial_selecionada = 'full_frente_honesto'
                break

        self.ev3.light.on(Color.GREEN)    
        wait(500)      
