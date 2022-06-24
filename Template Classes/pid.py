class PID:
    
    def __init__(self, kp, kd, ki, sensoriamento):
        
        self.kp = kp
        self.kd = kd
        self.ki = ki

        self.erro = 0
        self.erro_passado = 0

        self.sensoriamento = sensoriamento


    def calcula_erro(self):  # o erro é dado pela diferença entre a medição dos sensores
        for sensor in self.sensoriamento.sensores_direita:
            somaDireita += i
        mediaDireita = somaDireita/len(self.sensoresDireita)

        for i in self.sensoresEsquerda:
            somaEsquerda += i
        mediaEsquerda = somaEsquerda/len(self.sensoresEsquerda)

        self.erro = abs(mediaDireita - mediaEsquerda)/100  # está em cm
        return self.erro

    # junção entre PID e verificaPerto
    def calcula_pid(self):
        if self.erro < 5:
            self.erro = 0
        else:
            self.erro = self.erro - self.erroAnterior        #Adcionado essa linha para inserir novo valor de erro conforme código em blocos
            PID = self.kp * self.erro + self.kd * self.erro 
            self.erroAnterior = self.erro
        return PID