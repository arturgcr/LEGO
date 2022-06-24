class Sensoriamento():
    
    def __init__(self, lista_sensores, visto_ultimo, limiar=40):
        # lembrando q esse sensordireita, sensoresquerda e sensormeio são OBJETOS herdados da classe sensor
        self.sensores_direita = []
        self.sensores_esquerda = []

        for sensor in lista_sensores:
            if sensor.posicao == 'esquerda':
                self.sensores_esquerda.append(sensor)
            elif sensor.posicao == 'direita':
                self.sensores_direita.append(sensor)

        # não vem como argumento da init, então pode entrar direto na classe. no diagram de classes está dizendo q pe default....
        self.limiar = limiar
        # um possível problema para essa abordagem é o fato de q o infravermelho não vem em cm, e o nxt med em cm, não mm
        # converter os dados do infravermelho é algo q não implementei em geral
        self.visto_ultimo = visto_ultimo

    def verificado(self):
        ver_inimigo = 0  # Varíavel feita para definir de que lado o robô foi visto positivo direita e negativo esquerda
        nao_viu_nada = True     # Varíavel que determina se não vimos o robô inimigo / booleano
        
        for sensor in self.sensores_direita:  # sensoresdireita e sensoresesquerda seriam as listas com os sensores de cada lado
            if sensor.enxergando(self.limiar):   # tem que indentificar o limiar
                ver_inimigo += 1
                nao_viu_nada = False

        for sensor in self.sensores_esquerda:
            if sensor.enxergando(self.limiar):
                ver_inimigo -= 1
                nao_viu_nada = False

        # Se nenhum dos sensores viu, então retorna a direção de visto por último
        if nao_viu_nada:
            return self.visto_ultimo
        else:
            self.visto_ultimo = ver_inimigo
            return ver_inimigo

