"""
Módulo responsável pela definicao da classe com os métodos e atributos
relacionados a locomoção do robô.
"""

from pybricks.ev3devices import Motor
from pybricks.parameters import Port

from include.ferramentas import *

class Locomocao():
    '''
    Módulo de Locomoção
    -------------------

    Responsável por instanciar motores e controlar seus movimentos.
    '''
    def __init__(self, motores_direita, motores_esquerda, servo_motores = None, motores_arma = None, invertido = 'ALL'):
        """
        Método construtor que recebe uma lista de strings com as portas
        dos motores da direita, outra lista com os motores da esquerda e
        uma string isolada com o padrão de inversão desses motores
        ('DEFAULT', 'ALL', 'RIGHT' ou 'LEFT'). Os demais métodos dessa
        classe são referentes aos tipos de movimentos que serão
        executados no módulo de Estrategia: reta(), arco(), giro() e
        frear().

        Self@Locomocao, list[str], list[str], str -> None
        """
        # Atributo para armazenar os motores e servo-motores
        self.motores_esquerda = []
        self.motores_direita = []
        self.servo_motores = []
        self.motores_arma = []

        # Atributo para armazenar se o sentido dos motores é invertido ou não
        self.invertido = invertido

        # Adiciona no atributo "self.motores_esquerda" os motores esquerdos com suas respectivas portas
        for porta in motores_esquerda:
            motor_esquerda = self.instancia_motor(porta)
            self.motores_esquerda.append(motor_esquerda)

        # Adiciona no atributo "self.motores_direita" os motores direitos com suas respectivas portas
        for porta in motores_direita:
            motor_direita = self.instancia_motor(porta)
            self.motores_direita.append(motor_direita)

        if servo_motores != None:
            for porta in servo_motores:
                servo_motor = self.instancia_motor(porta)
                self.servo_motores.append(servo_motor)

        if motores_arma != None:
            for porta in motores_arma:
                motor_arma = self.instancia_motor(porta)
                self.motores_arma.append(motor_arma)

        # Controle de inversão dos motores:
        # - "ALL"        -> todos invertidos;
        # - "DEFAULT"    -> Nenhum motor invertido.
        # - "LEFT/RIGHT" -> motores da esquerda ou da direita estão invertidos, respectivamente.
        self.sentido_direita = 1
        if self.invertido == "ALL" or "RIGHT":
            self.sentido_direita = -1

        self.sentido_esquerda = 1
        if self.invertido == "ALL" or "LEFT":
            self.sentido_esquerda = -1

    def instancia_motor(self, porta):
        """
        Método recebe uma string com o nome da porta, instancia um objeto Port do pybrick e retorna um objeto Motor do pybricks.

        Self@Locomocao, str -> ?
        """
        obj_porta = None

        if porta == 'A':
            obj_porta = Port.A
        elif porta == 'B':
            obj_porta = Port.B
        elif porta == 'C':
            obj_porta = Port.C
        elif porta == 'D':
            obj_porta = Port.D

        motor = Motor(obj_porta)

        return motor

    def aplicar_roda_esquerda(self, pwm):
        """
        Método para aplicar o valor de PWM, que varia no intervalo
        [-100, 100], nos motores esquerdos.

        Self@Locomocao, int -> None
        """
        for motor in self.motores_esquerda:
            motor.dc(pwm * self.sentido_esquerda)

    def aplicar_roda_direita(self, pwm):
        """
        Método para aplicar o valor de PWM, que varia no intervalo
        [-100, 100], nos motores direitos.

        Self@Locomocao, int -> None
        """
        for motor in self.motores_direita:
            motor.dc(pwm * self.sentido_direita)

    def servo_motor_libera_rampa(self):
        '''
        Move o servo-motor responsável por liberar a rampa da violeta. Atualmente, está configurado para gerar 180° no sentido anti-horário (-180). Com a adição de mais servos-motores, esse método precisará ser revisto.
        '''
        for servo_motor in self.servo_motores:
            servo_motor.run_angle(2000,-60) # função que faz o servo motor girar e cair a rampa. 1° parametro é de velocidade em deg/s e o 2° o angulo
        print('roda caiu')

    def ativar_arma(self):
        for motor in self.motores_arma:
            motor.dc(-100)

    def desativar_arma(self):
        for motor in self.motores_arma:
            motor.brake()

    def mixagem(self, velocidade_linear, velocidade_angular):
        """
        Método que realiza os cálculos da mixagem.

        OBS.: Os parâmetros velocidade linear e angular variam no intervalo [-100, 100].

        self@Locomocao, int, int -> tuple[int, int]
        """
        # Realiza os cálculos da mixagem
        pwm_roda_esquerda = velocidade_linear + velocidade_angular
        pwm_roda_direita  = velocidade_linear - velocidade_angular
        
        # Calcula a diferença das mixagens
        diff = abs(abs(velocidade_angular) - abs(velocidade_linear))

        if (pwm_roda_esquerda < 0):
            pwm_roda_esquerda -= diff
        else:
            pwm_roda_esquerda += diff

        if (pwm_roda_direita < 0): 
            pwm_roda_direita -= diff
        else:
            pwm_roda_direita += diff

        # Converte de volta para o intervalo [-100, 100]
        pwm_roda_esquerda = int(ferramentas.mapy(pwm_roda_esquerda, -200, 200, -100, 100))
        pwm_roda_esquerda = ferramentas.constrainpy(pwm_roda_esquerda, -100, 100)
        pwm_roda_direita  = int(ferramentas.mapy(pwm_roda_direita, -200, 200, -100, 100))
        pwm_roda_direita = ferramentas.constrainpy(pwm_roda_direita, -100, 100)

        print('pwm_esquerda: ' + str(pwm_roda_esquerda))
        print('pwm_direita: ' + str(pwm_roda_direita))

        # Retorna uma tupla com a primeira posição o valor de PWM do motor esquerdo e a segunda posição com o valor do motor direito
        return pwm_roda_esquerda, pwm_roda_direita

    def locomover(self, velocidade_linear, velocidade_angular):
        """
        Método que move o robô de acordo com a velocidade linear e
        angular passadas.

        self@Locomocao, int, int -> None
        """
        # Obtém o valor da potência dos motores a partir do cálculo da mixagem
        mixagem = self.mixagem(velocidade_linear, velocidade_angular)

        # Aplica o resultado do cálculo da mixagem nos motores
        self.aplicar_roda_esquerda(mixagem[0])
        self.aplicar_roda_direita(mixagem[1])

    # usando as funcs acima para ir pra frente com a mesma potencia
    def reta(self, pwm = 100):
        """
        Método para mover o robo em linha reta. Para isso, eh colocado a
        velocidade linear com valor de PWM variavel e a velocidade
        angular com valor nulo.

        Self@Locomocao, int -> None
        """
        self.locomover(pwm, 0)

    def re(self, velocidade_linear = 100):
        """
        Empericamente percebemos ums dificuldade em fazer o calculo de mixagem  com velocidade linear 
        negativa e angular nula.
        Portanto criamos a funcao re que eh , essencialmente, um moonwalk com uma pequena velocidade angular
        """
        valor_limiar_angular = 10 # provisorio
        self.arco(-velocidade_linear, valor_limiar_angular)

    # talvez arco nao esteja rodando pras duas direcoes, e sim, so pra direita (se sim, criar um if e inverter sinais)
    def arco (self, velocidade_linear = 100, velocidade_angular = 15): # [Vang: que é metade da diferença de potencia entre os motores]
        """
        Método para o robô fazer um movimento de arco. Para isso, eh
        colocado a velocidade linear e angular com valor de PWM
        variavel.

        Self@Locomocao, int, int -> None
        """
        self.locomover(velocidade_linear, velocidade_angular)

    #  Gira em torno do proprio eixo utilizando a função locomover, com o a velocidade linear em 0 e a velocidade angular em 100(pwm)
    #  motor dir vai pra frente na potencia pwm, o inverso eh valido, ficando:
    def giro(self, pwm = 100):
        """
        Método para para o robo girar em reta. Para isso, é colocado a
        velocidade angular com valor de PWM variável e a velocidade
        linear com valor nulo.

        Self@Locomocao, int -> None
        """
        self.locomover(0, pwm)
 
    # Pára o motor usando fricção e a tensão que este gira na inércia, atua como um freio fraco.
    def frear(self):
        """
        Método para frear os motores do robo.

        Self@Locomocao -> None
        """
        for motor in self.motores_direita:
            motor.brake()
        for motor in self.motores_esquerda:
            motor.brake()
