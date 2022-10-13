#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.tools import wait

from include.estrategia import *
from include.ferramentas import *
from include.inicializacao import *
from include.locomocao import *
from include.pid import *
from include.sensor import *

ev3 = EV3Brick()

def main ():

    # ============ Configurações iniciais ============
    # Configurando parâmetros das estratégias:
    nome_do_robo = "Violeta"
    
    # -> Constantes para o cálculo do PID:
    kp = 0.6
    ki = 0
    kd = 0
    
    # Define os sensores de oponente com suas respectivas portas \ define as portas dos sensores
    sensoresDeOponente = {"esquerdo": 1, "direito": 2}

    # Define o peso de cada sensor  \ define qual sensor ta vendo
    pesoDosSensoresDeOponente = {"esquerdo": -100, "direito": 100}
    
    # Define o objeto dos sensores de oponente
    _sensor_oponente = SensorDeOponente(sensoresDeOponente, pesoDosSensoresDeOponente, 'ultrassonico')


    # -> Instanciando Motores (Locomocao):
    motores_esquerda = ['A', 'B'] # lista com portas dos motores da esquerda
    motores_direita = ['C'] # lista com portas dos motores da direita
    servo_motores = ['D'] # lista com portas dos servo-motores - Apenas para o caso da Violeta
    motores_arma = None
    _motores = Locomocao(motores_direita, motores_esquerda, servo_motores, motores_arma) # precisa comportar servo-motores
    
    # Instanciando Setup:
    _inicio = Inicializacao(ev3)
    
    # Instanciando Estratégias:
    _estrategia = Estrategia(_motores)

    # Configurando estratégias iniciais:
    _estrategia.configurar_estrategias(nome_do_robo)
    
    # ----------------------------------------------------------------------
    
    # Escolhendo estratégia inicial através da class Inicializacao ----
    _inicio.selecionar_correcao_ou_desempate()
    _inicio.selecionar_estrategia_inicial_primeira_etapa()
    _inicio.selecionar_estrategia_inicial_segunda_etapa()
    _inicio.selecionar_direcao_estrategia_inicial()

    # Coletando atributos após as transformações da estapa anterior
    angulo_correcao = _inicio.angulo_correcao
    estrategia_inicial_selecionada = _inicio.estrategia_inicial_selecionada
    direcao_estrategia_inicial = _inicio.direcao_estrategia_inicial
    direcao_sensoriamento_inicial = _inicio.direcao_sensoriamento_inicial
    _sensor_oponente.visto_por_ultimo = direcao_sensoriamento_inicial
    print(direcao_estrategia_inicial)

    # Aguardando 5 segundos para o início da movimentação do robô
    wait(4700) # Função do Pybricks que é similar a time.sleep() do Python
    # ----------------------------------------------------------------------
    print(estrategia_inicial_selecionada)
    print(direcao_estrategia_inicial)
    print(_inicio.direcao_sensoriamento_inicial)
    # Executando estratégia inicial ----------------------------------------

    _motores.servo_motor_libera_rampa() # Assim que a luta se inicia, a rampa cai
    if estrategia_inicial_selecionada != 'radar':
        _estrategia.executa_correcao(angulo_correcao) # se for igual a zero, passa direto sem corrigir
    # Executa a estratégia inicial sem fazer nenhum sensoriamento

        _estrategia.executa_estrategia_inicial(estrategia_inicial_selecionada, direcao_estrategia_inicial)
    # ----------------------------------------------------------------------
    else:
        pass

    # Instanciando PID -----------------------------------------------------
    # Recebe apenas kp, kd e ki -> caso não queira calcular algum, basta colocar 0 no seu valor
    _pid = PID(kp, kd, ki)
    # ----------------------------------------------------------------------

    # Entra no loop de busca por adversário -----------------------------------------
    while True:
        # Lê os sensores de oponente
        _sensor_oponente.lerSensores()

        # Verifica se o oponente foi detectado
        if _sensor_oponente.oponenteDetectado == True:
            # Se foi detectado, calcula o PID e joga na velocidade angular
            pid = _pid.calcular_pid(_sensor_oponente.erro)
            pid_constrained = ferramentas.constrainpy(_pid.calcular_pid(_sensor_oponente.erro), -100, 100)
            _motores.locomover(100, pid_constrained)
        # Caso contrário, faz a busca
        else:
            # Gira no mesmo sentido do sensor que viu o oponente por ultimo
            _motores.locomover(0, 80 * -_sensor_oponente.visto_por_ultimo)

            # Reseta os atributos do PID
            _pid.resetar_atributos()
        print(-_sensor_oponente.visto_por_ultimo)
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
