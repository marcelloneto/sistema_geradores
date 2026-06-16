import math


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
    def __init__(self,dados):
        self.dados = dados
        
    def teste(self,request):
        altura = self.dados['parametros']['altura']['valor']
        largura = self.dados['parametros']['largura']['valor']
        area = Areas.area_retangulo(altura,largura)
        
        return (self.dados)

    