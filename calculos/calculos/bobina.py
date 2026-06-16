from decimal import Decimal

class ResultadosBobinas:
    def __init__(self, dados):
        self.dados = dados
        self.G = self.dados['croqui_j']
        self.H = self.dados ['croqui_k']
        self.I = self.dados ['croqui_l']
        self.g = self.dados ['croqui_g']
        self.h = self.dados ['croqui_h']
        self.i = self.dados ['croqui_i'] 
        self.ponta = self.dados ['croqui_ponta']

    def comprimento(self):
       return (self.G*2 + self.H*2 + self.I*2 + self.ponta/3)

    def medidas_espira_iso (self, condutor, n_col, n_lin):
        
        h_condutor = condutor['altura isolação']['valor']
        b_condutor = condutor['largura isolação']['valor']

        return {
            'h_espira': n_lin * h_condutor,
            'b_espira': n_col * b_condutor
        }

    def area_espira (self,area_condutor,n_cond_esp):
        return area_condutor * n_cond_esp

    def area_secao_cobre (self, area_espira, n_espiras):
        return area_espira * n_espiras

    def volume_cobre (self, comprimento_bobina, area_secao):
        return comprimento_bobina * area_secao

    def parede_iso(self,largura_espira,largura_ranhura):
        return (largura_ranhura - largura_espira - Decimal(0.4))/2


