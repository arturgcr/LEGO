"""
Módulo responsável pela definição da classe com os métodos e atributos
relacionados às estratégias.
"""

from pybricks.tools import wait

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
        self.nome_robo = "Robo Genérico"

        # Configurações das estratégias com tempos diferentes
        self.tempo_arco = 0
        self.tempo_capitalismo = 0
        self.tempo_comunismo = 0
        self.tempo_de_ladinho = 0
        self.tempo_full_frente_honesto = 0
        self.tempo_full_re_honesto = 0
        self.tempo_moonwalk = 0

    def configurar_estrategias(self, nome_robo):
        """
        Função com a definição dos valores das variáveis de tempo de cada
        robô.

        nome_do_robo: str -> None
        """

        # Configurações da Violeta (1 motor de um lado e 2 motores do outro)
        if nome_robo == "Violeta":
            self.nome_robo = nome_robo
            self.tempo_arco                = 2000
            self.tempo_capitalismo         = 1700
            self.tempo_comunismo           = 1500
            self.tempo_de_ladinho          = 1000
            self.tempo_full_frente_honesto = 1800
            self.tempo_full_re_honesto     = 1800
            self.tempo_moonwalk            = 2300
            # add correções para: "arco", "comunismo", "capitalismo", "moonwalk" e "de_ladinho"

        # Configurações do Treta (2 motores de cada lado)
        elif nome_robo == "Treta":
            self.nome_robo = nome_robo
            self.tempo_arco                = 1700
            self.tempo_capitalismo         = 1700
            self.tempo_comunismo           = 1200
            self.tempo_de_ladinho          = 1000
            self.tempo_full_frente_honesto = 1200
            self.tempo_full_re_honesto     = 1600
            self.tempo_moonwalk            = 2300
        
        # Configurações do Picasso (1 motor de cada lado)
        elif nome_robo == "Picasso":
            self.nome_robo = nome_robo
            self.tempo_arco                = 2200
            self.tempo_capitalismo         = 2000
            self.tempo_comunismo           = 1500
            self.tempo_de_ladinho          = 1500
            self.tempo_full_frente_honesto = 2000
            self.tempo_full_re_honesto     = 2000
            self.tempo_moonwalk            = 2500
        
        else:
            self.nome_robo = nome_robo
            self.tempo_full_frente_honesto = 6000
            self.tempo_full_re_honesto     = 6000
    
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
                wait(250)
            # Verifica se o ângulo é igual a -90
            elif angulo_correcao == -35:
                # Gira o robô no sentido anti-horário
                self.motores.giro(-100)
                wait(250)
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
        elif estrategia_inicial_selecionada == 'bixo_piruleta': #Pronto
            self.bixo_piruleta()
        elif estrategia_inicial_selecionada == 'de_ladinho': #A ser feito
            self.de_ladinho(direcao_estrategia_inicial)
        elif estrategia_inicial_selecionada == 'maracutaia': #A ser feito
            self.maracutaia()
        else:
            pass           
    
    # =================================== Estratégias Iniciais =========================================
    def arco(self, direcao):
        """Função que aciona o arco. Neste movimento, o robô deve ser posicionado de lado. Ao selecionar o lado,
        o robô irá percorrer a borda da arena"""
        # Verifica se a Violeta está usando os motores mais potentes e se está no sentido anti-horário
        velocidade_linear = 100
        velocidade_angular = 45 * -direcao
        giro_mesmo_sentido = 100 * -direcao

        if self.nome_robo == "Violeta":
            if direcao < 0:
                velocidade_angular = 30 * -direcao
            if direcao > 0:
                velocidade_angular = 35 * -direcao
        
        if self.nome_robo == "Treta":
            velocidade_angular = 35 * -direcao
        
        self.motores.arco(velocidade_linear, velocidade_angular)
        wait(self.tempo_arco)
        self.motores.giro(giro_mesmo_sentido)
        wait(550)

    def bixo_piruleta(self):
        """"O Robô começa de costas, na linha do adversário. O robo gira no eixo de apenas uma das rodas"""
        self.motores.giro(100)
        wait(800)

    # Manobra + Arco => segue reto por alguns segundos e executa um arco
    def comunismo(self, direcao):
        '''
        Executa um curto movimento em linha reta e logo em seguida executa um arco e finaliza se voltando para o centro da arena.
        '''
        velocidade_linear = 100
        velocidade_angular = 50 * -direcao
        giro_sentido_oposto = 100 * -direcao
        giro_mesmo_sentido = 100 * direcao
        tempo_reta = 200
        tempo_giro_mesmo_sentido = 350
        tempo_giro_sentido_oposto = 250
        
        if self.nome_robo == "Violeta":
            tempo_reta = 500
            if direcao > 0:
                velocidade_angular = 30 * -direcao

        elif self.nome_robo == "Picasso":
            tempo_reta = 500
            if direcao > 0:
                velocidade_linear = 100
                velocidade_angular = 60 * -direcao

        self.motores.reta() #frente
        wait(tempo_reta)
        self.motores.giro(giro_mesmo_sentido) #angulo
        wait(tempo_giro_mesmo_sentido)
        self.motores.arco(velocidade_linear+20, velocidade_angular ) # Alterar Vlin e Vang correspondentes ao robo
        wait(self.tempo_comunismo) # alterar tempo
        self.motores.giro(giro_sentido_oposto) #angulo
        wait(tempo_giro_sentido_oposto)
        
   
    # Arco de costas --> O robô posicionado de lado faz um arco para trás e depois um giro para o centro da arena
    def moonwalk(self, direcao):
        """Função que aciona o arco. Neste movimento, o robô deve ser posicionado de lado. Ao selecionar o lado,
        o robô irá percorrer a borda da arena de costas"""
        velocidade_linear = 200
        velocidade_angular = 150 * direcao
        giro_mesmo_sentido = 100 * -direcao # valor para girar o robô no mesmo sentido que a direção da estrategia 
        self.motores.arco(-velocidade_linear, velocidade_angular) # Alterar Vlin e Vang correspondentes ao robo
        wait(self.tempo_moonwalk) # Alterar Tempo
        self.motores.giro(giro_mesmo_sentido) # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        wait(700)
        
    def full_frente_honesto(self):
        '''Uma full frente honesta, nada mais nada menos. O robô apenas vai pra frente com tudo, cuidados devem ser tomados
            com essa manobra '''  
        velocidade = 100 
        self.motores.reta(velocidade)
        wait(self.tempo_full_frente_honesto)
        
    def full_re_honesto(self):
        '''Uma full ré honesta, nada mais nada menos. O robô apenas vai pra trás com tudo, cuidados devem ser tomados
            com essa manobra '''
        velocidade = 100
        # Essa verificação é necessária pq a violeta precisa corrigir para não fazer um arco
        if self.nome_robo == "Violeta":
            self.motores.re(velocidade, 10)
        else:
            self.motores.re(velocidade)
        wait(self.tempo_full_re_honesto)

    # Manobra + Arco invertida
    def capitalismo(self, direcao):
        """"O robô é posicionado de frente um pouco mais no centro na arena. Inicialmente vai para trás ( da ré). 
        Faz o giro para uma direção selecionada (gira) e executa o arco na direção selecionada"""
        
        velocidade_linear = 100
        velocidade_angular = 50 * -direcao
        tempo_re = 450
        giro_mesmo_sentido = 100 * direcao
        giro_sentido_oposto = 100 * -direcao

        if self.nome_robo == "Picasso":
            velocidade_angular = 60 * -direcao
            tempo_re = 200
        
        self.motores.re(velocidade_linear)
        wait(tempo_re)
        self.motores.giro(giro_mesmo_sentido)
        wait(350)
        self.motores.arco(velocidade_linear +20, velocidade_angular) #
        wait(self.tempo_capitalismo) # alterar tempo
        self.motores.giro(giro_sentido_oposto) # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        wait(500) # Alterar tempo

    # Armadilha
    def de_ladinho(self, direcao):
        """"Armadilha: O robo é posicionado de lado e realiza um curto movimento para trás e logo em seguida inicia o sensoriamento"""   
        velocidade_linear = 100
        velocidade_angular = 80 * -direcao
        self.motores.arco(-velocidade_linear, velocidade_angular) # Alterar Vlin e Vang correspondentes ao robo
        wait(self.tempo_de_ladinho) # Alterar Tempo

    def maracutaia(self):
        """"Estratégia feita para robos com defeito. O robo faz curtos movimentos e verifica se o robo adversário se move ou não."""""
        pass

    # ==================================================================================================
    
    # ============================ Estratégias de Perseguição ========================================== 
    # gira ao redor de si até encontrar algo
    def radar(self):
        pass
    # ==================================================================================================
