class Locomoção():
  
    motores_esquerda = [Motor.Port(A), Motor.Port(B)]
    motores_direita = [Motor.Port(C), Motor.Port(D)]
    
    def __init__(self, strMotorDireita, strMotorEsquerdo, invertido = 'DEFAULT'):
        
        motores_esquerda = [Motor.Port(A), Motor.Port(B)]
        motores_direita = [Motor.Port(C), Motor.Port(D)]
        
        def controle_sentido(invertido):
            if invertido == 'DEFAULT':
                sentido = 1
                return sentido
            else:
                sentido = -1
                return sentido
        
        #Atributos
        self.dc(pwm * sentido) #Define potência (-100,100) e sentido com que o motor gira 
        self.brake() #Para o motor usando atrito mais a voltagem gerada pelo seu próprio giro.
        self.run_time(velocidade_angular, tempo, then=brake.HOLD, wait=true) #Define uma velocidade angular para o motor em graus centígrados e o tempo em que manterá essa velocidade, definindo então o movimento seguinte


    def controle_sentido(invertido):
        if invertido == 'DEFAULT':
            sentido = 1
            return sentido
        else:
            sentido = -1
            return sentido