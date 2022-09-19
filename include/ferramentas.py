"""
Cabecalho com definições de funções úteis para qualquer parte do código.
"""

class Ferramentas:
    """
    Classe com os métodos úteis para qualquer parte do código.
    """
    def mapy(self, valor_a_ser_convertido, minimo_da_entrada, maximo_da_entrada, minimo_da_saida,  maximo_da_saida):
        """
        Função map do Arduino em sua verdadeira forma, em Python. Ela
        remapeia um número de um intervalo para outro.

        Self@Ferramentas, int ou float, int ou float, int ou float, int ou float, int ou float -> float
        """
        diferenca_das_entradas = maximo_da_entrada - minimo_da_entrada
        diferenca_das_saidas = maximo_da_saida - minimo_da_saida
        diferenca_do_valor_a_ser_convertido_com_o_minimo_da_entrada = valor_a_ser_convertido - minimo_da_entrada
        return (diferenca_do_valor_a_ser_convertido_com_o_minimo_da_entrada * diferenca_das_saidas) / diferenca_das_entradas + minimo_da_saida

    def constrainpy(self, valor, minimo, maximo):
        """
        Função constrain do Arduino em sua verdadeira forma, em Python. Ela
        restringe um número a ficar dentro de um intervalo.

        - Self@Ferramentas, int, int, int -> int;
        - Self@Ferramentas, float, float, float -> float
        - Self@Ferramentas, float, int, int -> int ou float (depende dos valores passados);
        - Self@Ferramentas, int, float, int -> int ou float (depende dos valores passados);
        - Self@Ferramentas, int, int, float -> int ou float (depende dos valores passados);
        - Self@Ferramentas, float, float, int -> int ou float (depende dos valores passados);
        - Self@Ferramentas, float, int, float -> int ou float (depende dos valores passados);
        - Self@Ferramentas, int, float, float -> int ou float (depende dos valores passados).
        """
        if valor > maximo:
            return maximo
        elif valor < minimo:
            return minimo
        else:
            return valor

# Definição do objeto da classe Ferramentas
ferramentas = Ferramentas();
