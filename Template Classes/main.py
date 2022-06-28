#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()

from sensor import SensorLEGO
from sensoriamento import Sensoriamento
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
    
    # -> Instanciando e listando Sensores (SensorLEGO):
    _sensor1 = SensorLEGO('ultrassom', 1, 'esquerda')
    _sensor2 = SensorLEGO('ultrassom', 2, 'direita')
    lista_de_sensores = [_sensor1, _sensor2]
    limiar = 40

    # -> Instanciando Motores (Locomocao):
    motores_esquerda = ['A', 'B'] # lista com portas dos motores da esquerda
    motores_direita = ['C', 'D'] # lista com portas dos motores da direita
    servo_motores = [] # lista com portas dos servo-motores - Apenas para o caso da Violeta
    _motores = Locomocao(motores_direita, motores_esquerda, 'ALL') # precisa comportar servo-motores
    
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

    angulo_correcao = _inicio.angulo_correcao
    estrategia_inicial_selecionada = _inicio.estrategia_inicial_selecionada
    direcao_estrategia_inicial = _inicio.direcao_estrategia_inicial
    direcao_sensoriamento_inicial = _inicio.direcao_sensoriamento_inicial
    
    wait(5) # Função do Pybricks que é similar a time.sleep() do Python
    # ----------------------------------------------------------------------
    
    # Executando estratégia inicial ----------------------------------------
    _estrategia.executa_correcao(angulo_correcao) # se for igual a zero, passa direto sem corrigir
    _estrategia.executa_estrategia_inicial(estrategia_inicial_selecionada, direcao_estrategia_inicial)
    # ----------------------------------------------------------------------

    # Instanciando Sensoriamento -------------------------------------------
    _sensoriamento = Sensoriamento(lista_de_sensores, limiar, direcao_sensoriamento_inicial) #listadesensores, vistoUltimo, kp, kd, ki = 0, limiar = 40
    # ----------------------------------------------------------------------

    # Instanciando PID -----------------------------------------------------
    _pid = PID(kp, kd, ki)
    # ----------------------------------------------------------------------

    # Entra no loop de busca por adversário -----------------------------------------
    while True:
        direcao_oponente = _sensoriamento.busca_oponente() # retorna a direção em que o oponente foi detectado
        # erro vai de [0,limiar], já que no cálculo ficamos apenas com o valor absoluto
        erro = _sensoriamento.erro
        # calcula_pid recebe erro [0,limiar]
        pid = _pid.calcula_pid(erro)
        # Convertendo PID [0, erro * kp] para PWM [0, 100]
        pid_convertido_pwm = _pid.converte_pid_para_pwm(pid)
        # Recebe a direcao_oponente (-1, 0, 1) e valor pid convertido para pwm [0, 100]
        # O sentido de rotação será decidido (direção_oponente != 0 * pid_convertido_pwm)
        _estrategia.executa_estrategia_perseguicao(direcao_oponente, pid_convertido_pwm)
    # -------------------------------------------------------------------------------
main()

# -----------------------------------------
#  Nomes de variaveis - classe sensoriamento: erro passado e erro anterior sao IGUAIS
#  Sentido de giro e arco estavam trocados (se neg, girava pra esq em um e pra dir em outro) - padronizar horario com +
#  Invertido era +pwm (inverter isso)
#  Mudar na locomocao, em setup e na main
#  Mudar nomes
#  Testar coisas armadilhas