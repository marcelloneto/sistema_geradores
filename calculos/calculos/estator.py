

class ResultadosEstator:
    def __init__(self,dados):
        self.dados = dados

    def area_espira(self, area_condutor):
        n_cond_espiras = self.dados['numero_condutores_por_espira']
        area = area_condutor

        return area * n_cond_espiras