#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

from ferramentas import *

ev3 = EV3Brick()

from sensor import SensorDeOponente
from locomocao import Locomocao
from inicializacao import Inicializacao
from estrategia import Estrategia
from pid import PID

def main ():
    # ============ Configurações iniciais ============
    
    # -> Constantes para o cálculo do PID:
    kp = 2
    ki = 0
    kd = 1.2
    temporizador = StopWatch()
    
    # Define os sensores de oponente com suas respectivas portas \ define as portas dos sensores
    sensoresDeOponente = {"esquerdo": 2, "direito": 1}

    # Define o peso de cada sensor  \ define qual sensor ta vendo
    pesoDosSensoresDeOponente = {"esquerdo": -100, "direito": 100}
    
    # Define o objeto dos sensores de oponente
    _sensor_oponente = SensorDeOponente(sensoresDeOponente, pesoDosSensoresDeOponente, 'nxtultrassonico')


    # -> Instanciando Motores (Locomocao):
    motores_esquerda = ['A', 'B'] # lista com portas dos motores da esquerda
    motores_direita = ['C'] # lista com portas dos motores da direita
    servo_motores = ['D'] # lista com portas dos servo-motores - Apenas para o caso da Violeta
    _motores = Locomocao(motores_direita, motores_esquerda) # precisa comportar servo-motores
    
    # Instanciando Setup:
    _inicio = Inicializacao()
    
    # Instanciando Estratégias:
    _estrategia = Estrategia(_motores)
    # ----------------------------------------------------------------------
    
    # Escolhendo estratégias e direções iniciais através da class Setup ----
    _inicio.selecionar_correcao_ou_desempate()
    _inicio.selecionar_estrategia_inicial()
    _inicio.selecionar_direcao_movimento()
    _inicio.selecionar_direcao_sensoriamento()
    # Coletando atributos após as transformações da estapa anterior
    angulo_correcao = _inicio.angulo_correcao
    estrategia_inicial_selecionada = _inicio.estrategia_inicial_selecionada
    direcao_estrategia_inicial = _inicio.direcao_estrategia_inicial
    direcao_sensoriamento_inicial = _inicio.direcao_sensoriamento_inicial
    _sensor_oponente.visto_por_ultimo = direcao_sensoriamento_inicial
    # Aguardando 5 segundos para o início da movimentação do robô
    wait(5000) # Função do Pybricks que é similar a time.sleep() do Python
    # ----------------------------------------------------------------------
    
    # Executando estratégia inicial ----------------------------------------
    _estrategia.executa_correcao(angulo_correcao) # se for igual a zero, passa direto sem corrigir
    # Executa a estratégia inicial sem fazer nenhum sensoriamento
    _estrategia.executa_estrategia_inicial(estrategia_inicial_selecionada, direcao_estrategia_inicial)
    # ----------------------------------------------------------------------

    # Instanciando PID -----------------------------------------------------
    # Recebe apenas kp, kd e ki -> caso não queira calcular algum, basta colocar 0 no seu valor
    _pid = PID(kp, kd, ki, temporizador)
    # ----------------------------------------------------------------------

    # Entra no loop de busca por adversário -----------------------------------------
    while True:
        # Lê os sensores de oponente
        _sensor_oponente.lerSensores()

        # Verifica se o oponente foi detectado
        if _sensor_oponente.oponenteDetectado == True:
            # Se foi detectado, calcula o PID e joga na velocidade angular
            pid = _pid.calcula_pid(_sensor_oponente.erro)
            pid_constrained = constrainpy(_pid.calcula_pid(_sensor_oponente.erro), -60, 60)
            _motores.locomover(100, pid_constrained)
        # Caso contrário, faz a busca
        else:
            # Faz a busca
            _motores.locomover(0, 80 * _sensor_oponente.visto_por_ultimo)

            # Reseta os atributos do PID
            _pid.resetar_atributos()
    # -------------------------------------------------------------------------------

if __name__ == '__main__':
    main()

# -----------------------------------------
#  Nomes de variaveis - classe sensoriamento: erro passado e erro anterior sao IGUAIS
#  Sentido de giro e arco estavam trocados (se neg, girava pra esq em um e pra dir em outro) - padronizar horario com +
#  Invertido era +pwm (inverter isso)
#  Mudar na locomocao, em setup e na main
#  Mudar nomes
#  Testar coisas armadilhas