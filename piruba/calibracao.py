from pybricks.pupdevices import ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait

class sensorCor:
    def __init__(self):

        sensorCor = {'esquerdaFrente': ColorSensor(Port.S1), 'direitaFrente': ColorSensor(Port.S2),
        'direitaTras' : ColorSensor(Port.S3), 'esquerdaTras' : ColorSensor(Port.S4)}
        
        self.valoresPreto = []
        self.valoresBranco = []
    
    def calibracao(self):

        verde = Color(h=120, s=100, v=100)

        print('Coloca no preto!')
        for i in sensorCor:
            self.valoresPreto.append(sensorCor[i].reflection())
            wait(5000)
            light.blink(verde, 200)
        return(self.valoresPreto)
        
## perguntar se a luz acende em paralelo 

        print('Coloca no branco!')
        for i in sensorCor:
            self.valoresBranco.append(sensorCor[i].reflection())
            wait(5000)
            light.blink(verde, 200)
        return(self.valoresBranco)