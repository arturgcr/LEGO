"""
Cabeçalho responsável pelo cálculo do controlador PID.
"""

class PID:
    """
    Classe com os métodos e atributos relacionados ao cálculo do
    controlador PID.
    """
    def __init__(self, kp, kd, ki):
        """
        Método construtor que atribui os valores dos ganhos passados
        para os atributos dos ganhos da classe. Além disso cria outros
        atributos utilizado nos cálculos.

        Self@PID, int ou float, int ou float, int ou float -> None
        """
        # Atributos com os parâmetros do controlador PID
        # Atribui os valores passados nos atributos
        self.kp = kp # Ganho proporcional
        self.ki = ki # Ganho integral
        self.kd = kd # Ganho derivativo

        # Atributos para armazenar o resultado dos termos do algoritmo PID
        self.proporcional = 0
        self.integral     = 0
        self.derivativo   = 0
        
        # Atributo que armazena o erro do último cálculo
        self.erro_anterior = 0

    def calcular_pid(self, erro):
        """
        Método que realiza os cálculos do algoritmo PID.

        - Self@PID, int -> int (caso Kp, Ki e Kd inteiros);
        - Self@PID, int -> float (caso Kp ou Ki ou Kd float);
        - Self@PID, float -> float.
        """
        # Calcula os termos do algoritmo PID
        self.proporcional = self.kp * erro
        self.integral += self.ki * erro
        self.derivativo = self.kd * (erro - self.erro_anterior)

        # Atualiza o atributo que armazena o erro anterior com o valor do erro atual
        self.erro_anterior = erro

        # Retorna a soma dos termos do algoritmo PID
        return self.proporcional + self.integral + self.derivativo

    def resetar_atributos(self):
        """
        Método que reseta os atributos utilizados nos cálculos.

        Self@PID -> None
        """
        self.integral = 0
        self.erro_anterior = 0
