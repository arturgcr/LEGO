
#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()


# Write your program here.
ev3.speaker.beep()

#--------------------------------------
# Importar nossas bibliotecas

import sensor
import locomocao
import estrategia
import setup
import time

def main ():
    # Configurações iniciais
    kp = 2
    ki = 0
    kd = 1.2
    _sensor1 = sensor.SensorLEGO('ultrassom', 1, 'esquerda')
    _sensor2 = sensor.SensorLEGO('ultrassom', 2, 'direita')
    _motores = locomocao.Locomocao('CD', 'AB', 'ALL')
    _inicio = setup.Setup(_motores)
    _estrategia = estrategia.Estrategia(_motores)
    # estrategia antes do loop principal e sensoriamento no loop principal
    # Inicia com som + cor vermelha
    brick.sound.beep()
    brick.light(Color.RED)

    # escolher estrategia e direção - Classe Setup
    _inicio.selecionarEstrategia()
    _inicio.selecionarDirecao()
    
    time.sleep(5)

    _inicio.executaEstrategia()
    # Chamar sensores
    _sensoriamento = sensor.Sensoriamento([_sensor1,_sensor2],_inicio.direcao,kp,kd,ki) #listadesensores, vistoUltimo, kp, kd, ki = 0, limiar = 40

    while True:
        pid = _sensoriamento.PID() # Calcula o PID
        _estrategia.radarPID(pid)  # Joga info de PID nos motores
        _sensoriamento.Erro()      # Faz sensoriamento

main()

# -----------------------------------------
#  Nomes de variaveis - classe sensoriamento: erro passado e erro anterior sao IGUAIS
#  Sentido de giro e arco estavam trocados (se neg, girava pra esq em um e pra dir em outro) - padronizar horario com +
#  Invertido era +pwm (inverter isso)
#  Mudar na locomocao, em setup e na main
#  Mudar nomes
#  Testar coisas armadilhas