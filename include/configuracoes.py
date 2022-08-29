"""
Cabeçalho com a definição das variáveis para armazenar o tempo de
execução de cada ação das estratégias.
"""

# Variável para armazenar o nome do robô
nomeDoRobo = "AlterarONomeNaMain"

# Configurações das estratégias da Violeta
if nomeDoRobo == "Violeta":
    tempo_do_full_frente_honesto = 5000
    tempo_do_full_re_honesto     = 7000
# Configurações das estratégias do Treta
elif nomeDoRobo == "Treta":
    tempo_do_full_frente_honesto = 1200
    tempo_do_full_re_honesto     = 2500
else:
    tempo_do_full_frente_honesto = 0
    tempo_do_full_re_honesto     = 0
