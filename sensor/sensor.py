
class Sensor():
    def __init__(self):
   
    sensores = {sensor1 : UltrasonicSensor(Port.S1), sensor2 : UltrasonicSensor(Port.S2)}

    # armazenando o valor da distância fornecida pelos sensores 
    distanciaEsquerda = sensor2.distance()
    distanciaDireita = sensor1.distance()


    def varredura(int limiar):

        # retorna um booleano que vai dizer se o obstáculo está próximo ou não 
        def proximidade_esq(limiar):
            resultado_proximidade =  distanciaEsquerda < limiar
        return resultado_proximidade_esq

        def proximidade_dir(limiar):
            resultado_proximidade_dir = distanciaDireita < limiar
        return resultado_proximidade_dir  

        erro_esq = 15
        erro_dir = 15 
        
        # Retorna: -1 - Viu apenas com sensor direito.
        #           0 - Viu com os dois sensores ou com nenhum.
        #           1 - Viu apenas com o sensor esquerdo.

        visaoDireita = resultado_proximidade_dir  * erro_esq 
        visaoEsquerda = resultado_proximidade_esq * erro_dir 
        visao = visaoEsquerda - visaoDireita
        return visao


        
