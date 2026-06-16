import math
from decimal import Decimal

class ResultadosEletrica:
    def __init__(self,dados):
        self.dados = dados
        

    def densidade_corrente(self,corrente,n_paralelos,area_espira):
        return corrente/(n_paralelos * area_espira)

    def campo_eletrico (self,tensao,parede_iso):
        return (tensao / Decimal((1000 * math.sqrt(3)))) / parede_iso