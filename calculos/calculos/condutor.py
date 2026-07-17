import math
from decimal import Decimal


class Areas:
    @staticmethod
    def area_quadrado(lado):
        return(lado**2)
    
    @staticmethod
    def area_retangulo(h, b):
        """
        h = altura
        b = base
        """
        return h*b
    
    @staticmethod
    def area_circulo(medida, valor):
        if medida == "raio":
            return math.pow( valor , 2 ) * math.pi()
        if medida == "diametro":
            return math.pow( valor / 4 , 2 ) * math.pi()

class ResultadosCondutor:
    def __init__(self,dados,dados_cond, comprimento_bobina):
        self.dados = dados_cond
        self.l_bobina = comprimento_bobina
        self.altura = self.dados['parametros']['altura']['valor']
        self.largura = self.dados['parametros']['largura']['valor']
        self.altura_iso = self.dados['parametros']['altura isolação']['valor']
        self.largura_iso = self.dados['parametros']['largura isolação']['valor']
        self.densidade = self.dados['parametros']['densidade']['valor']
        self.ranhura = dados['dados_geometricos']['ranhura_b']
        self.n_condutores_espira = dados['dados_estator']['numero_condutores_por_espira']

        self.disp_condutores = self.disposicao_condutores(self.ranhura,self.n_condutores_espira)

        self.area = self.calcular_area()
        
    def calcular_area(self):
        
        area = Areas.area_retangulo(self.altura,self.largura)
        
        return (area)

    def peso (self,volume):

        peso = volume * self.densidade * Decimal("1e-9")

        return peso

    def disposicao_condutores(self, ranhura, cond_esp):
        col = math.floor((ranhura-Decimal(5))/self.largura_iso)

        return {
            'col': col,
            'lin': Decimal(cond_esp/col),
        }