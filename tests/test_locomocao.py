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

    def test_instanciando_motores_sem_retornar_erro(self, motores_direita, motores_esquerda, invertido):
        with not pytest.raises(Exception):
            _motores = Locomocao(motores_direita, motores_esquerda, invertido)