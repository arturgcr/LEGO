from pybricks.pupdevices import DCMotor
from pybricks.parameters import Port
from pybricks.tools import wait

import variaveis.py

class Motores:
    def __init__(self, stop):

        self.motores = {'motorA'.DCMotor(Port.A), 'motorB'.DCMotor(Port.B), 
                              'motorC'.DCMotor(Port.C)}

        self.stop = stop 

        # velocidade inicial 
        for i in motores:
            self.motores[i].dc(0)

    
    def velocidade(self):

        if stop != 0:
            for i in self.motores:
                self.motores[i].dc(0)
        
        else: # if stop == 0

            if ReguladorVelocidade == True: 

                if tempoVelMax > relogio1:
                    tempo2 = relogio1

                    velMotor = -((tempo2*(-velMax-velocidadeln)/tempoVelMax)+velocidadeln)
                    
                    for i in self.motores:
                        self.motores[i].dc(velMotor)
            
                else: # tempoVelMax < relogio1 

                    for i in self.motores:
                        self.motores[i].dc(velMax)
                        ReguladorVelocidade == False 
            
            else: # ReguladorVelocidade == False 
            

