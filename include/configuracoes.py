"""
Cabeçalho com a definição das variáveis para armazenar o tempo de
execução de cada ação das estratégias.
"""
class Configuracao:
    def __init__(self, nome_do_robo):
        self.tempo_do_full_frente_honesto = 0
        self.tempo_do_full_re_honesto = 0
        self.configurar_estrategias(nome_do_robo)