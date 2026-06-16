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
    def __init__(self,dados, bobina):
        self.dados = dados
        self.l_bobina = bobina.comprimento()
        self.altura = self.dados['parametros']['altura']['valor']
        self.largura = self.dados['parametros']['largura']['valor']
        self.densidade = self.dados['parametros']['densidade']['valor']
        
    def area(self):
        
        area = Areas.area_retangulo(self.altura,self.largura)
        
        return (area)

    def peso (self,volume):

        peso = volume * self.densidade * Decimal("1e-9")

        return peso