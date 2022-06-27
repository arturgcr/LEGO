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
from setup import Setup
from estrategia import Estrategia
from pid import PID

def main ():
    # ============ Configurações iniciais ============
    
    # -> Constantes para o cálculo do PID:
    kp = 2
    ki = 0
    kd = 1.2
    
    # -> Instanciando Sensores (SensorLEGO):
    _sensor1 = SensorLEGO('ultrassom', 1, 'esquerda')
    _sensor2 = SensorLEGO('ultrassom', 2, 'direita')
    lista_de_sensores = [_sensor1, _sensor2]
    limiar = 40

    # -> Instanciando Motores (Locomocao):
    motores_esquerda = ['A', 'B']
    motores_direita = ['C', 'D']
    servo_motores = [] # Apenas para o caso da Violeta

    _motores = Locomocao(motores_direita, motores_esquerda, 'ALL')
    
    # Instanciando Setup:
    _inicio = Setup(_motores)
    
    # Instanciando Estratégias:
    _estrategia = Estrategia(_motores)
    # ----------------------------------------------------------------------
    
    # Escolhendo estratégias e direções iniciais através da class Setup ----
    _inicio.selecionarEstrategia()
    _inicio.selecionarDirecao()
    
    wait(5) # Função do Pybricks que é similar a time.sleep() do Python
    # ----------------------------------------------------------------------
    
    # Executando estratégia inicial ----------------------------------------
    _inicio.executaEstrategia() # precisa corrigir: isso deveria ser executado por estratégia
    # Se for corrigido, setup entrega o valor que deve ser passado para estratégia executar
    # sua estratégia inicial. Dessa forma, setup não precisa receber motores
    # ----------------------------------------------------------------------

    # Instanciando Sensoriamento -------------------------------------------
    _sensoriamento = Sensoriamento(lista_de_sensores, limiar, _inicio.direcao) #listadesensores, vistoUltimo, kp, kd, ki = 0, limiar = 40
    # ----------------------------------------------------------------------

    # Instanciando PID -----------------------------------------------------
    _pid = PID(kp, kd, ki)
    # ----------------------------------------------------------------------

    # Entra no loop de busca por adversário -----------------------------------------
    while True:
        _sensoriamento.busca_oponente()
        erro = _sensoriamento.erro
        pid = _pid.calcula_pid(erro)
        _estrategia.radarPID(pid)  # Joga info de PID nos motores
    # -------------------------------------------------------------------------------
main()

# -----------------------------------------
#  Nomes de variaveis - classe sensoriamento: erro passado e erro anterior sao IGUAIS
#  Sentido de giro e arco estavam trocados (se neg, girava pra esq em um e pra dir em outro) - padronizar horario com +
#  Invertido era +pwm (inverter isso)
#  Mudar na locomocao, em setup e na main
#  Mudar nomes
#  Testar coisas armadilhas