class Sensor():  #acho q o nome verde significa q o nome "sensor" não esta disponivel
    def __init__(self, tipo, porta, lado, tamanhodofiltro=1):

        if porta==1:
            x=port.S1
        if porta==2:
            x=port.S2
        if porta==3:
            x=port.S3
        if porta==4:
            x=port.S4
        #deve ter uma solução mais elegante pra essa parada q eu fiz acima. e provavelmente eu tinha q usar elif

        if tipo == 'ultrasson':
            self.sensor = UltrasonicSensor(x) #"a" e "x" foram nomes meio merda para a variável. mas paciência
        if tipo == 'Infrared': #talvez seja melhor chamr de infravermelho, ou botar clausula para os 2
            self.sensor = InfraredSensor(x)
        #Port.porta não funciona pq tem q se "S1" e não "1", mas o espírito é esse, deve ter um jeito mais prático, 
        #mas se não tiver da pa escrever um if por extenso

        self.LADO =lado
        self.tamanhodofiltro=tamanhodofiltro




    def enxergando(self, limiar): 
    #optei por botar o filtro direto no metodo enxerga, por isso o default do tamanho do filtro é 1. 
    #o método de verificação do filtro sem a lista pode não ser o mais eficiente, na dúvida é só der uma verificada na ironcup virtual
        y=0
        for x < self.tamanhodofiltro:
            if self.sensor.distance() < limiar:
                y+=1
            else:
                y-=1
            

        if y > 0:
            return True
        else:
            return False
#da forma q eu apliquei o metodo enxergando o metodo filtro não é necessário




class Sensoriamento():
    def __init__(self, listadesensores, kp, kd, ki=0, limiar=40):  #ainda não levei em consideração o caso do sensor do meio
    #lembrando q esse sensordireita, sensoresquerda e sensormeio são OBJETOS herdados da classe sensor(talvez seja melho chama-los de sensor 1 2 e 3)
        for i in listadesensores:
            if i.LADO == esquerda:
                #adiciona i à lista da esquerda, lembrando q a lista é um atributo da nova classe
            if i.LADO == direita:
                #adiciona i à lista da direita
                #possívelmente fazer caso para sensor no meio

        self.kp=kp
        self.kd=kd
        self.ki=ki

        self.listadesensores=listadesensores

        self.limiar = limiar   #não vem como argumento da init, então pode entrar direto na classe. no diagram de classes está dizendo q pe default....
                                   #um possível problema para essa abordagem é o fato de q o infravermelho não vem em cm, e o nxt med em cm, não mm
                                   #converter os dados do infravermelho é algo q não implementei em geral

    def verificalado(self):
        x=0
        y=0
        for i in self.sensoresdireita:   #sensoresdireita e sensoresesquerda seriam as listas com os sensores de cada lado
            if i.enxergando(tem q identificar o limiar)==True:
                x+=1
                y=1
        for i in self.sensoresesquerda:    #é importante notar, q da forma como eu optei por montar o filtro aqui haveria uma defasagem de 
            if i.enxergando(tem q identificar o limiar)==True:         #tempo entre as medições, dependendo do tamanho do filtro. pra evitar isto bastria implementar 
                x-=1                       #o filtro no resultado dafunção verifica lado, ao ives de no final da função enxergando, isso é facil de mudar
                y=1
        
        if x>0:
            return 'direita'   #aqui eu mandei retornar uns strings genéricos falando asituação, mas poderia ser uma 
        if x<0:                #manipulação do erro ou tanto faz, o importante é q nessa altura o código ja sabe onde o adversario está
            return 'esquerda'
        if x=0 and and y=1:
            return 'frente'
        if y=0
            retrun 'nãoViu'

        x=0
        y=0


        #ESSA É MAIS CHATA DE FAZER. NÃO PAREI P DEFINIR. 
        #inclusive talvez seja melhor repensar, ao invez de retornar o erro talvez ela cria um atributo erro? não sei...

    def verificaPerto(self): #funcao com limiar menor p garantir o full pa frente, ainda não implementei e não tem no diagrama de classes


    def PID(self, erro, erroAnterior):     #acho q o diagrama de classes tá errado, o PID teria q receber os erros como argumento
        return self.kp * erro + self.kd * (erro - erroAnterior)   #e teria q padronizar o nome dessas variáveis
