import math
from decimal import Decimal


class Areas:
    @staticmethod
    def area_quadrado(lado):
        return lado ** 2

    @staticmethod
    def area_retangulo(h, b):
        return h * b

    @staticmethod
    def area_circulo(medida, valor):
        if medida == "raio":
            return Decimal(str(math.pi)) * (valor ** 2)
        if medida == "diametro":
            return Decimal(str(math.pi)) * ((valor / Decimal("2")) ** 2)
        return Decimal("0")


class ResultadosCondutor:
    def __init__(self, dados, dados_cond, comprimento_bobina):
        self.dados = dados_cond
        self.l_bobina = comprimento_bobina
        self.altura = self.dados["altura_mm"]
        self.largura = self.dados["largura_mm"]
        self.altura_iso = self.dados["altura_isolacao_mm"]
        self.largura_iso = self.dados["largura_isolacao_mm"]
        self.densidade = self.dados["densidade_kg_m3"]
        self.ranhura = dados["dados_geometricos"]["ranhura_b"]
        self.n_condutores_espira = dados["dados_estator"]["numero_condutores_por_espira"]

        self.disp_condutores = self.disposicao_condutores(self.ranhura, self.n_condutores_espira)
        self.area = self.calcular_area()

    def calcular_area(self):
        if self.dados.get("forma") == "redondo" and self.dados.get("diametro_mm"):
            return Areas.area_circulo("diametro", self.dados["diametro_mm"])
        return Areas.area_retangulo(self.altura, self.largura)

    def peso(self, volume):
        return volume * self.densidade * Decimal("1e-9")

    def disposicao_condutores(self, ranhura, cond_esp):
        col = math.floor((ranhura - Decimal("5")) / self.largura_iso)
        return {
            "col": col,
            "lin": Decimal(cond_esp) / Decimal(col),
        }