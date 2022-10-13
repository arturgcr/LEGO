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

        # Configurações das estratégias com tempos diferentes
        self.tempo_do_full_frente_honesto = 0
        self.tempo_do_full_re_honesto = 0

    def configurar_estrategias(self, nome_do_robo):
        """
        Função com a definição dos valores das variáveis de tempo de cada
        robô.

        nome_do_robo: str -> None
        """
        # Configurações das estratégias da Violeta
        if nome_do_robo == "Violeta":
            self.tempo_do_full_frente_honesto = 5000
            self.tempo_do_full_re_honesto     = 7000
        # Configurações das estratégias do Treta
        elif nome_do_robo == "Treta":
            self.tempo_do_full_frente_honesto = 1200
            self.tempo_do_full_re_honesto     = 2500
        else:
            self.tempo_do_full_frente_honesto = 6000
            self.tempo_do_full_re_honesto     = 6000 
    
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
            print('ATENCAO! Nenhuma estrategia selecionada')        


    # Executa a estratégia de perseguição com base na leitura do sensores e do PID
    def executa_estrategia_perseguicao(self, pid_convertido_pwm):
        self.radar(pid_convertido_pwm)
            
    
    # =================================== Estratégias Iniciais =========================================
    def arco(self, direcao):
        """Função que aciona o arco. Neste movimento, o robô deve ser posicionado de lado. Ao selecionar o lado,
        o robô irá percorrer a borda da arena"""
        velocidade_linear = 100
        velocidade_angular = 45* -direcao
        giro_mesmo_sentido = 100 * -direcao # valor para rotacionar na direção oposto que fez o arco
        self.motores.arco(velocidade_linear, velocidade_angular) # Alterar Vlin e Vang correspondentes ao robo
        print('iniciou o arco')
        wait(1700) # o tempo pode variar para cada robô
        self.motores.giro(giro_mesmo_sentido)
        wait(550)
        print('girou no msm sentido')

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
        wait(2300) # Alterar Tempo
        self.motores.giro(giro_mesmo_sentido) # Alterar pwm correspondente ao robo - pra virar pro meio da arena novamente
        wait(700)
        
    def full_frente_honesto(self):
        '''Uma full frente honesta, nada mais nada menos. O robô apenas vai pra frente com tudo, cuidados devem ser tomados
            com essa manobra '''
        
        velocidade = 100 
        self.motores.reta(velocidade)
        print('velocidade linear:', velocidade)
        print('estou andando')
        wait(self.tempo_do_full_frente_honesto)
        
    

    def full_re_honesto(self):
        '''Uma full frente honesta, nada mais nada menos. O robô apenas vai pra frente com tudo, cuidados devem ser tomados
            com essa manobra '''
        velocidade = 100 
        self.motores.re(velocidade)
        
        wait(self.tempo_do_full_re_honesto)

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

    # Armadilha
    def de_ladinho(self, direcao):
        """"Armadilha: O robo é posicionado de lado e realiza um curto movimento para trás e logo em seguida inicia o sensoriamento"""
        print("di ladin q é mais gostoso")   
        velocidade_linear = 100
        velocidade_angular = 50 * direcao
        self.motores.arco(-velocidade_linear, velocidade_angular) # Alterar Vlin e Vang correspondentes ao robo
        print('velocidade linear:', velocidade_linear)
        print('velocidade angular:', velocidade_angular)
        wait(800) # Alterar Tempo
  

    def maracutaia(self):
        """"Estratégia feita para robos com defeito. O robo faz curtos movimentos e verifica se o robo adversário se move ou não."""""
        

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
