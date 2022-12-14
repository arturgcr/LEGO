"""
#TODO: Fazer o cabeçalho.
"""

from pybricks.ev3devices import InfraredSensor, UltrasonicSensor # Sensor ultrassônico EV3
from pybricks.nxtdevices import UltrasonicSensor as nxtUltrasonicSensor # Sensor ultrassônico NXT
from pybricks.parameters import Port

class SensorDeOponente():
    """
    Módulo de SensorLEGO
    --------------------
    Responsável por instanciar um sensor, definindo: tipo (str: `ultrassonico` ou `infravermelho`), porta (int: `1`, `2`, `3` ou `4`), a posição (str: `esquerda` ou `direita`) e o tamanho do filtro (`int`, por padrão recebe `None`)do sensor.
    """
    def __init__(self, sensores, pesos, tipo, tamanho_filtro=1):
        """
        Self, dict[str, int], dict[str, int], str -> None
        """
        # Atributo para armazenar os sensores de oponente
        self.sensores = sensores

        # Atributo para armazenar os pesos dos sensores de oponente
        self.pesoDosSensores = pesos

        # Atributo para armazenar o tipo dos sensores de oponente
        self.tipo = tipo

        # Atributo para armazenar as leituras dos sensores
        self.leituraDosSensores = {}
        # Inicia todos os sensores como "False"
        for sensor in sensores:
            self.leituraDosSensores[sensor] = False

        # Atributo que armazena se o oponente foi detectado ou não
        self.oponenteDetectado = False

        # Atributo que armazena o erro dos sensores
        self.erro = 0

        # Define as portas de cada sensor
        for sensor in sensores:
            if self.sensores[sensor] == 1:
                self.sensores[sensor] = Port.S1
            elif self.sensores[sensor] == 2:
                self.sensores[sensor] = Port.S2
            elif self.sensores[sensor] == 3:
                self.sensores[sensor] = Port.S3
            elif self.sensores[sensor] == 4:
                self.sensores[sensor] = Port.S4

        # Define o objeto de cada sensor
        if self.tipo == "ultrassonico":
            for sensor in sensores:
                self.sensores[sensor] = UltrasonicSensor(self.sensores[sensor])
        elif self.tipo == "nxtultrassonico":
            for sensor in sensores:
                self.sensores[sensor] = nxtUltrasonicSensor(self.sensores[sensor])
        elif self.tipo == "infravermelho":
            for sensor in sensores:
                self.sensores[sensor] = InfraredSensor(self.sensores[sensor])

        # guarda a última direção que foi detectado
        self.visto_por_ultimo = -1
        # guarda o valor que será usado para o tamanho do filtro durante a leitura dos sensores
        self.tamanho_filtro = tamanho_filtro
        # guarda o valor numérico da última medição autorizada pelos filtros
        self.ultima_distancia_autorizada = 0 # essencial para organizar o cálculo do erro

    def lerSensores(self, limiar = 400):
        # Passa por todos os sensores e verifica se o oponente foi detectado ou não
        for sensor in self.sensores:
            filtro = [0] * self.tamanho_filtro
            leitura = bool(self.sensores[sensor].distance() < limiar) 
            if leitura:
                for leitura_filtro in filtro:
                    nova_leitura = bool(self.sensores[sensor].distance() < limiar)
                    if nova_leitura == False:
                        self.leituraDosSensores[sensor] = False
                self.leituraDosSensores[sensor] = True
            else:
                self.leituraDosSensores[sensor] = False
                
        print("dist:", self.sensores[sensor].distance())
        
        # Atualiza o atributo que armazena se o oponente foi detectado ou não
        self.oponenteDetectado = True in self.leituraDosSensores.values()

        # Caso o oponente tenha sido detectado, calcula o erro dos sensores
        if self.oponenteDetectado == True:
            self.erro = self.calcularErro()

    def calcularErro(self):
        # Variável para armazenar a soma dos pesos dos sensores que detectaram o oponente
        soma = 0

        # Variável para armazenar o número de sensores que detectaram o oponente
        numeroDeDeteccoes = 0

        # Passa por todos os sensores
        for sensor in self.sensores:
            # Verifica se o sensor detectou o oponente
            if self.leituraDosSensores[sensor] == True:
                # Soma o peso do sensor na soma dos pesos dos sensores que detectaram o oponente
                soma += self.pesoDosSensores[sensor]

                # Incrementa 1 no número de detecções
                numeroDeDeteccoes += 1
        self.visto_por_ultimo = soma
        # Retorna a média ponderada dos sensores que detectaram o oponente
        return soma / numeroDeDeteccoes

    # # Recebe o tamanho do filtro e cria uma lista de tamanho igual
    # # Caso receba 0, não cria o filtro
    # def criando_filtro(self, tamanho_filtro):
    #     if tamanho_filtro != 0:
    #         filtro = [0] * tamanho_filtro
    #         return filtro
    #     else:
    #         return None
    
    # # Função que vai decidir como vai ser a medição do sensor, tornando a classe modular
    # # Não está funcionando
    # def medicao(self):
    #     if isinstance(self.sensor, (UltrasonicSensor, InfraredSensor)):
    #         distancia = self.sensor.distance()
    #         return distancia
    
    # # funcão que verifica se o resultado eh vdd ou falso (sensores naturalmente tem um acumulo
    # # de erros com o tempo, resultando em falsos positivos e falsos negativos)
    # def filtrar(self):
    #     for leitura_filtro in range(len(self.filtro)):
    #         distancia = self.distancia()
    #         if distancia == 0: # Converte o resultado para booleano, pq oq nos interessa é a presença apenas
    #             distancia = False
    #         elif distancia != 0:
    #             distancia = True
    #         self.filtro[leitura_filtro] = distancia
    #         if self.filtro[leitura_filtro] != self.filtro[0]:
    #             break
    #     if False not in self.filtro:
    #         return True
    #     else:
    #         return False
    
    # # se filtro aprovado, confia no resultado e entra em def enxergando; enxergando afirma se ta vendo oponente ou nao
    # def enxergando(self, limiar):
    #     distancia = self.sensor.distance()
    #     if distancia < limiar:
    #         if self.filtro != None:
    #             if self.filtrar():
    #                 self.ultima_distancia_autorizada = distancia
    #                 return True
    #             else:
    #                 return False
    #         return True
    #     else:
    #         return False
