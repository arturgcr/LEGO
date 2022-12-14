import pytest

from template_classes.locomocao import Locomocao


class TestLocomocao:
    
    @pytest.fixture
    def motores_direita(self):
        return ['A', 'B']

    @pytest.fixture
    def motores_esquerda(self):
        return ['C', 'D']

    @pytest.fixture
    def invertido(self):
        return 'ALL'

    def test_instanciando_Locomocao_sem_estourar_erro(self, motores_direita, motores_esquerda, invertido):
        try:
            _motores = Locomocao(motores_direita, motores_esquerda, invertido)
        except Exception:
            pytest.fail('Erro inesperado ao tentar instanciar a class Locomocao()')

    def test_metodo_arco_com_valores_acima_de_100_apos_somar_vlin_e_vang(self, motores_direita, motores_esquerda, invertido):
        try:
            _motores = Locomocao(motores_direita, motores_esquerda, invertido)
            _motores.arco()
        except Exception:
            pytest.fail('Ocorreu um erro durante a execução do método erro')