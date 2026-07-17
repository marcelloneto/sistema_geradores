from decimal import Decimal
from calculos.calculos.condutor import ResultadosCondutor

class ResultadosBobinas:
    def __init__(self, dados, dados_bobina,dados_cond,iso_principal, iso_sel,folga):
        self.condutor = dados_cond['parametros']
        self.iso_sel = iso_sel
        self.iso_principal = iso_principal
        """
        ===========================================
        dados extraido do banco de dados da bobina 
        ===========================================
        """

        self.dados = dados_bobina

        self.G = self.dados['croqui_j']
        self.H = self.dados ['croqui_k']
        self.I = self.dados ['croqui_l']
        self.g = self.dados ['croqui_g']
        self.h = self.dados ['croqui_h']
        self.i = self.dados ['croqui_i'] 
        self.ponta = self.dados ['croqui_ponta']
        
        """
        ===========================================
        dados extraidos dos calculos do condutor 
        ===========================================
        """

        res_condutor = ResultadosCondutor(dados,dados_cond,self.calcular_comprimento())

        self.n_col = res_condutor.disp_condutores['col']
        self.n_lin = res_condutor.disp_condutores['lin']
        self.area_condutor = res_condutor.area

        """
        ==============================================
        dados extraidos dos calculos do banco de dados 
        ==============================================
        """

        self.n_cond_esp = dados ['dados_estator']['numero_condutores_por_espira']
        self.n_espiras_bobina = dados['dados_estator']['numero_espiras_por_bobina']
        self.ranhura = dados['dados_geometricos']['ranhura_b']
        self.altura_ranhura = dados['dados_geometricos']['ranhura_c']
        self.folga_ranhura = folga

        """
        ==================================================
        dados extraidos da fita de isolação entre espiras 
        ==================================================
        """

        self.iso_sel_espessura = self.verificar_iso(self.iso_sel)["iso_espessura"]
        self.iso_sel_largura = self.verificar_iso(self.iso_sel)['iso_largura']
        self.iso_sel_comprimento = self.verificar_iso(self.iso_sel)['iso_comprimento']


        """
        ==============================================
        dados extraidos dos calculos da bobina 
        ==============================================
        """

        self.altura_espira = self.calcular_medidas_espira_iso(self.condutor,self.n_col,self.n_lin)['h_espira']
        self.largura_espira = self.calcular_medidas_espira_iso(self.condutor,self.n_col,self.n_lin)['b_espira']
        self.area_espira = self.calcular_area_espira(self.area_condutor,self.n_cond_esp)
        self.area_secao_cobre = self.calcular_area_secao_cobre(self.area_espira,self.n_espiras_bobina)
        self.volume_cobre = self.calcular_volume_cobre(self.calcular_comprimento_condutor(),self.area_secao_cobre)
        self.parede_iso = self.calcular_parede_iso(self.largura_espira,self.ranhura, self.folga_ranhura)
        self.altura_bobina = self.calcular_altura_bobina(self.n_espiras_bobina,self.altura_espira,self.iso_sel_espessura)
        self.altura_bobina_iso = self.calcular_altura_bobina_iso(self.altura_bobina,self.parede_iso)
        self.largura_bobina = self.largura_espira
        self.largura_bobina_iso = self.calcular_largura_bobina_iso(self.largura_bobina,self.parede_iso)
        self.espaco_para_calco = self.calcular_espaco_para_calco(self.altura_ranhura,self.altura_bobina_iso)
        self.perimetro_interno = self.calcular_perimetro_int(self.altura_bobina,self.largura_bobina)
        self.perimetro_externo = self.calcular_perimetro_ext(self.altura_bobina_iso,self.largura_bobina_iso)
        self.perimetro_medio = self.calcular_perimetro_medio(self.perimetro_externo,self.perimetro_interno)
        #self.voltas_isolacao = self.calcular_voltas_isolacao(self.calcular_comprimento(),)


    def calcular_comprimento(self):
       return (self.G*2 + self.H*2 + self.I*2 + 2*self.ponta)

    def calcular_comprimento_condutor(self):
        return (self.G*2 + self.H*2 + self.I*2 + 2*self.ponta/3)

    def calcular_medidas_espira_iso (self, condutor, n_col, n_lin):
        
        h_condutor = condutor['altura isolação']['valor']
        b_condutor = condutor['largura isolação']['valor']

        return {
            'h_espira': n_lin * h_condutor,
            'b_espira': n_col * b_condutor
        }

    def calcular_area_espira (self,area_condutor,n_cond_esp):
        return area_condutor * n_cond_esp

    def calcular_area_secao_cobre (self, area_espira, n_espiras):
        return area_espira * n_espiras

    def calcular_volume_cobre (self, comprimento_bobina, area_secao):
        return comprimento_bobina * area_secao

    def calcular_parede_iso(self,largura_espira,largura_ranhura,folga):
        return (largura_ranhura - largura_espira - Decimal(folga))/2

    def calcular_altura_bobina(self, n_esp_b, h_esp,iso_esp=0):
        return n_esp_b * h_esp + (n_esp_b - 1) * iso_esp

    def calcular_altura_bobina_iso(self, h_bobina,iso):
        return 2 * iso + h_bobina

    def calcular_largura_bobina_iso (self, l_bobina, iso):
        return 2 * iso + l_bobina
    
    def calcular_espaco_para_calco(self, altura_ranhura, h_bobina):
        
        return (altura_ranhura - 2* h_bobina)

    def calcular_perimetro_int(self, altura,largura):
        return (altura + largura)*2

    def calcular_perimetro_ext(self, altura_iso,largura_iso):
        return (altura_iso + largura_iso)*2

    def calcular_perimetro_medio(self, perimetro_ext, perimetro_int):
        return (perimetro_ext + perimetro_int)/2

    def calcular_voltas_isolacao (self, comprimento, sobreposicao, largura_fita):
        return (comprimento / (sobreposicao*largura_fita))



    def verificar_iso(self,iso):
        if iso != -1 and iso is not None:
            if 'Espessura' in iso['parametros']:
                iso_espessura = iso['parametros']['Espessura']['valor']
                iso_largura = iso['parametros']['Largura']['valor']
                iso_comprimento = iso['parametros']['Comprimento do rolo']['valor']
            else:
                iso_espessura = Decimal(0)
                iso_largura = Decimal(0)
                iso_comprimento = Decimal(0)
        else:
            iso_espessura = Decimal(0)
            iso_largura = Decimal(0)
            iso_comprimento = Decimal(0)

        return {
            "iso_espessura": iso_espessura, 
            "iso_largura": iso_largura,
            "iso_comprimento": iso_comprimento
        }
