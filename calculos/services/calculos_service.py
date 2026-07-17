from calculos.services.dados_maquina_service import DadosMaquinaService
from calculos.services.dados_material_service import DadosMaterialService
from django.forms.models import model_to_dict
from calculos.calculos.condutor import ResultadosCondutor
from calculos.calculos.estator import ResultadosEstator
from calculos.calculos.bobina import ResultadosBobinas
from calculos.calculos.eletrica import ResultadosEletrica
from decimal import Decimal

class Verificacao:
    @staticmethod
    def validar_valores(material):
        PARAMETROS = [
            'altura',
            'largura',
            'altura isolação',
            'largura isolação',
            'densidade',
        ]

        for parametro in PARAMETROS:
            if parametro in material['parametros']:
                pass
            else:
                mensagem = "Material não possui dados registrados"
                print(parametro)
                return mensagem

    def chamar_calculos(request,escolhido):
        ver = Verificacao.validar_valores(escolhido)
        if escolhido is None:
            print("nenhum condutor registrado")
            return "nenhum condutor registrado"
        elif ver:
            print(ver)
            return ver
        else:
            return True


class Filtros:
    def __init__(self, dados,iso_sel={},condutor={},iso_principal={},folga=0.4):
        self.dados = dados
        self.condutor_sel = condutor
        self.iso_principal = iso_principal
        self.iso_sel = iso_sel
        
        self.estator = ResultadosEstator(dados['dados_estator'])
        if self.validar_dados(self.condutor_sel) is True:
            self.bobinas = ResultadosBobinas(self.dados,dados['dados_bobina'], condutor, iso_principal, iso_sel,folga)
            self.condutor = ResultadosCondutor(self.dados,condutor,self.bobinas.calcular_comprimento())
        self.eletrica = ResultadosEletrica(dados)

    def validar_dados(self,secao):
        if 'parametros' in secao and secao['parametros'] != {}:
            return True
        else:
            return False


    def calcularcondutor(self, coef,folga):
        
        if self.validar_dados(self.condutor_sel) is True:

            area_condutor = self.condutor.area
            n_condutores_espira = self.dados['dados_estator']['numero_condutores_por_espira']
            n_espiras_bobina = self.dados['dados_estator']['numero_espiras_por_bobina']
            area_espira = self.bobinas.area_espira
            area_total_espiras = self.bobinas.area_secao_cobre
            comprimento_bobina = self.bobinas.calcular_comprimento_condutor()
            volume_condutor_bobina = self.bobinas.volume_cobre
            peso_condutor_bobina = self.condutor.peso(volume_condutor_bobina)
            numero_bobinas = self.dados['dados_estator']['numero_bobinas']
            peso_total_condutor = peso_condutor_bobina * numero_bobinas
            peso_com_seguranca = peso_total_condutor * Decimal(float(str(coef).replace(",",".")))

            n_paralelos = self.dados['dados_estator']['numero_paralelos']
            corrente = self.dados['maquina']['corrente_a']

            densidade = self.eletrica.densidade_corrente(corrente,n_paralelos,area_espira)
            largura_ranhura = self.dados['dados_geometricos']['ranhura_b']
            
            
            espessura_iso = self.bobinas.parede_iso

            tensao = self.dados['maquina']['tensao_v']

            campo_eletrico = self.eletrica.campo_eletrico(tensao,espessura_iso) 
            espaco_calco = self.bobinas.espaco_para_calco

            return {
                "Área do Condutor": [area_condutor,'mm²'],
                "Quantidade de condutores por espira": [n_condutores_espira, ''],
                "Área da Espira": [area_espira,'mm²'],
                "Quantidade de espiras por bobina": [n_espiras_bobina, ''],
                "Área Total Espiras": [area_total_espiras,'mm²'],
                "Comprimento da Bobina": [comprimento_bobina,'mm'],
                "Peso de cobre por Bobina": [peso_condutor_bobina, 'kg'],
                "Quantidade de Bobinas": [numero_bobinas, "unidades"],
                "Peso total de cobre": [peso_total_condutor,'kg'],
                "Peso total de cobre (com segurança)": [peso_com_seguranca,'kg'],
                "Largura da Ranhura": [largura_ranhura, 'mm'],
                "Espessura da Isolação": [espessura_iso, 'mm'],
                "Densidade de corrente": [densidade, 'A/mm²'],
                "Campo Elétrico": [campo_eletrico, 'kV/mm'],
                "Espaco para Calço": [espaco_calco, 'mm'],
            }

        else:
            return None

    def calcularisolacao(self, sobreposicao, coef, espessura_iso):
        sobrep = sobreposicao/100
        coefseg = coef      
        
        altura_bobina = self.bobinas.altura_bobina
        altura_bobina_iso = self.bobinas.altura_bobina_iso
        largura_bobina = self.bobinas.largura_bobina
        largura_bobina_iso = self.bobinas.altura_bobina_iso


        perimetro_ext = self.bobinas.perimetro_externo
        perimetro_int = self.bobinas.perimetro_interno
        perimetro = self.bobinas.perimetro_medio
        fita_param = self.iso_principal['parametros']
        if "Largura" in fita_param:
            largura_fita = fita_param['Largura']['valor']
            espessura_fita = fita_param['Espessura']['valor']
            comp_rolo = fita_param['Comprimento do rolo']['valor']

            camadas = espessura_iso / (espessura_fita / (1 - sobrep))

        print(f"perimetro médio: {perimetro}")

        
                



    def verificar_iso(self,iso):
        if iso != -1 and iso is not None:
            if 'Espessura' in iso['parametros']:
                iso_espessura = iso['parametros']['Espessura']['valor']
            else:
                iso_espessura = Decimal(0)
        else:
            iso_espessura = Decimal(0)

        return iso_espessura
    
        
        
        