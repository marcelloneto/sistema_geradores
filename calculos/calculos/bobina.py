from decimal import Decimal
from calculos.calculos.condutor import ResultadosCondutor
import math

class ResultadosBobinas:
    def __init__(self, dados={}, dados_bobina={},dados_cond={},iso_principal={},iso_cond={},folga={},sobreposicao={},fitas={}):
        self.condutor = dados_cond['parametros']
        self.iso_cond = iso_cond
        self.iso_principal = iso_principal
        self.fitas = fitas
        if self.fitas != {}:

            self.fita_condutiva = self.fitas["fita_condutiva"]["escolhida"]
            self.fita_semicondutiva = self.fitas["fita_semicondutiva"]["escolhida"]
            self.fita_acabamento = self.fitas["fita_acabamento"]["escolhida"]

        
        """
        ===========================================
        dados extraido do banco de dados da bobina 
        ===========================================
        """
        if dados != {}:
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
        if dados and dados_cond != {}:
            res_condutor = ResultadosCondutor(dados,dados_cond,self.calcular_comprimento())

            self.n_col = res_condutor.disp_condutores['col']
            self.n_lin = res_condutor.disp_condutores['lin']
            self.area_condutor = res_condutor.area

        """
        ==============================================
        dados extraidos dos calculos do banco de dados 
        ==============================================
        """
        if self.dados and folga and sobreposicao != {}:

            self.n_cond_esp = dados ['dados_estator']['numero_condutores_por_espira']
            self.n_espiras_bobina = dados['dados_estator']['numero_espiras_por_bobina']
            self.numero_bobinas = dados['dados_estator']['numero_bobinas']
            self.ranhura = dados['dados_geometricos']['ranhura_b']
            self.altura_ranhura = dados['dados_geometricos']['ranhura_c']
            self.folga_ranhura = Decimal(folga)
            self.sobreposicao = Decimal (float(sobreposicao)/100)

        """
        ==================================================
        dados extraidos da fita de isolação entre espiras 
        ==================================================
        """
        if self.iso_cond != {}:
            self.iso_sel_espessura = self.verificar_iso(self.iso_cond)["iso_espessura"]
            self.iso_sel_largura = self.verificar_iso(self.iso_cond)['iso_largura']
            self.iso_sel_comprimento = self.verificar_iso(self.iso_cond)['iso_comprimento']

        """
        ==================================================
        dados extraidos da fita de isolação principal 
        ==================================================
        """
        if self.iso_principal != {}:
   
            self.iso_principal_espessura = self.verificar_iso(self.iso_principal)["iso_espessura"]
            self.iso_principal_largura = self.verificar_iso(self.iso_principal)["iso_largura"]
            self.iso_principal_comprimento = self.verificar_iso(self.iso_principal)["iso_comprimento"]

        """
        ================================================================
        dados extraidos das fitas condutiva, semicondutiva e acabamento 
        ================================================================
        """
        if self.fitas != {}:
            fita_condutiva = self.verificar_iso(self.fita_condutiva)
            fita_semicondutiva = self.verificar_iso(self.fita_semicondutiva)
            fita_acabamento = self.verificar_iso(self.fita_acabamento)

            
            self.espessura_fitas = { 
                "fita_condutiva": fita_condutiva['iso_espessura'],
                "fita_semicondutiva": fita_semicondutiva['iso_espessura'],
                "fita_acabamento": fita_acabamento['iso_espessura'],
            }

            self.largura_fitas = { 
                "fita_condutiva": fita_condutiva['iso_largura'],
                "fita_semicondutiva": fita_semicondutiva['iso_largura'],
                "fita_acabamento": fita_acabamento['iso_largura'],
            }

            self.comprimento_fitas = { 
                "fita_condutiva": fita_condutiva['iso_comprimento'],
                "fita_semicondutiva": fita_semicondutiva['iso_comprimento'],
                "fita_acabamento": fita_acabamento['iso_comprimento'],
            }

        """
        ==============================================
        dados extraidos dos calculos da bobina 
        ==============================================
        """
        if self.condutor != {}:

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

        if self.iso_principal != {}:
            self.voltas_isolacao = self.calcular_voltas_fita(self.calcular_comprimento(),self.sobreposicao,self.iso_principal_largura)
            self.n_camadas_isolacao = self.calcular_camadas(self.parede_iso, self.iso_principal_espessura,self.sobreposicao)
            self.comprimento_fita_isolante_bobina = self.calcular_comprimento_fita_bobina(self.voltas_isolacao, self.perimetro_medio,self.n_camadas_isolacao)
            self.comprimento_fita_isolante_total = self.calcular_comprimento_fita_total(self.comprimento_fita_isolante_bobina,self.numero_bobinas)
            self.rolo_fita_isolante_bobina = self.calcular_rolo_fita(self.comprimento_fita_isolante_bobina,self.iso_principal_comprimento)
            self.rolo_fita_isolante_total = self.calcular_rolo_fita(self.comprimento_fita_isolante_total,self.iso_principal_comprimento)


        """
        ===========================================================
        Cálculos para fitas, condutiva, semicondutiva e acabamento
        ===========================================================
        """
        if self.fitas != {}:

            self.sobreposicao_fitas = {
                "fita_condutiva": self.fitas['fita_condutiva']['sobreposicao'],
                "fita_semicondutiva": self.fitas['fita_semicondutiva']['sobreposicao'],
                "fita_acabamento": self.fitas['fita_acabamento']['sobreposicao'],
            }
            self.camadas_fitas = {
                "fita_condutiva": Decimal(10),
                "fita_semicondutiva": Decimal(1),
                "fita_acabamento": Decimal(1),
            }

            self.comprimento_aplicacao_fitas = {
                "fita_condutiva": self.calcular_comprimento_parte_reta(),
                "fita_semicondutiva": Decimal(100*4),
                "fita_acabamento": self.calcular_comprimento_area_acabamento()
            }

        
            self.resultados_fitas = {}
            
            for fita in self.fitas:
                if self.fitas[fita]['escolhida'] != None:
                    self.resultados_fitas[fita] = {}
                    
                    sobreposicao_fita = Decimal(self.sobreposicao_fitas[fita])/100
                    
                    camadas_fita = self.camadas_fitas[fita]
                    comprimento_aplicacao_fita = self.comprimento_aplicacao_fitas[fita]
                    largura_fita = self.largura_fitas[fita]
                    comprimento_fita = self.comprimento_fitas[fita]

                    self.resultados_fitas[fita]['aplicacao_fita'] = comprimento_aplicacao_fita
                    self.resultados_fitas[fita]['camadas'] = camadas_fita
                    
                    self.resultados_fitas[fita]['n_voltas'] = math.ceil(self.calcular_voltas_fita(comprimento_aplicacao_fita,sobreposicao_fita,largura_fita))
                    self.resultados_fitas[fita]['comprimento_fita_bobina'] = math.ceil(self.calcular_comprimento_fita_bobina(
                                                                                self.resultados_fitas[fita]['n_voltas'],
                                                                                self.perimetro_externo,
                                                                                camadas_fita
                                                                                ))
                    self.resultados_fitas[fita]['rolos_bobina'] = math.ceil(self.calcular_rolo_fita(
                                                                    self.resultados_fitas[fita]['comprimento_fita_bobina'],
                                                                    comprimento_fita
                                                                ))
                    self.resultados_fitas[fita]['comprimento_fita_total'] = math.ceil(self.calcular_comprimento_fita_total(
                                                                                self.resultados_fitas[fita]['comprimento_fita_bobina'],
                                                                                self.numero_bobinas
                                                                            ))
                    self.resultados_fitas[fita]['rolos_total'] = math.ceil(self.calcular_rolo_fita(
                                                                    self.resultados_fitas[fita]['comprimento_fita_total'],
                                                                    comprimento_fita
                                                                ))


    def calcular_comprimento(self):
       return (self.G*2 + self.H*2 + self.I*2 + 2*self.ponta)

    def calcular_comprimento_parte_reta(self):
        return (2*self.H)

    def calcular_comprimento_area_acabamento(self):
        return 2*(self.G + self.I + self.ponta)

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

    def calcular_voltas_fita (self, comprimento, sobreposicao, largura_fita):
        if largura_fita !=0:
            
            return (comprimento / ((1-Decimal(sobreposicao))*largura_fita))
        else:
            print("Largura da fita igual a zero!")
            return 0

    def calcular_comprimento_fita_bobina(self, voltas, perimetro, camadas):
        return voltas*perimetro*camadas

    def calcular_comprimento_fita_total(self, comprimento_bobina, n_bobinas):
        return comprimento_bobina*n_bobinas

    def calcular_rolo_fita(self, comprimento, l_rolo):
        return comprimento/l_rolo

    def calcular_camadas (self, espessura, espessura_fita, sobreposicao):
        if espessura_fita > 0:
            return espessura/(espessura_fita/(1-sobreposicao))
        else:
            return print("espessura da fita igual a zero!")

    def calcular_camadas_olhal(self, camadas_corpo, espessura_iso):
        if espessura_iso > 3:
            return math.ceil(0.65*camadas_corpo)
        else:
            return camadas_corpo

    def verificar_iso(self,iso):
        if iso != -1 and iso is not None and iso != {}:
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
