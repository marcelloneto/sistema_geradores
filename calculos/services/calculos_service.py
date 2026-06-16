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
    def __init__(self, dados,condutor):
        self.dados = dados
        self.condutor_sel = condutor
        self.bobinas = ResultadosBobinas(dados['dados_bobina'])
        self.estator = ResultadosEstator(dados['dados_estator'])
        self.condutor = ResultadosCondutor(condutor,self.bobinas)
        self.eletrica = ResultadosEletrica(dados)

    def calcularcondutor(self, coef):

        area_condutor = self.condutor.area()
        n_condutores_espira = self.dados['dados_estator']['numero_condutores_por_espira']
        n_espiras_bobina = self.dados['dados_estator']['numero_espiras_por_bobina']
        area_espira = self.bobinas.area_espira(area_condutor,n_condutores_espira)
        area_total_espiras = self.bobinas.area_secao_cobre(area_espira,n_espiras_bobina)
        comprimento_bobina = self.bobinas.comprimento()
        volume_condutor_bobina = self.bobinas.volume_cobre(comprimento_bobina,area_total_espiras)
        peso_condutor_bobina = self.condutor.peso(volume_condutor_bobina)
        numero_bobinas = self.dados['dados_estator']['numero_bobinas']
        peso_total_condutor = peso_condutor_bobina * numero_bobinas
        peso_com_seguranca = peso_total_condutor * Decimal(float(str(coef).replace(",",".")))

        n_paralelos = self.dados['dados_estator']['numero_paralelos']
        corrente = self.dados['maquina']['corrente_a']

        densidade = self.eletrica.densidade_corrente(corrente,n_paralelos,area_espira)

        medidas_espira = self.bobinas.medidas_espira_iso(self.condutor_sel['parametros'],n_condutores_espira,n_paralelos)
        largura_ranhura = self.dados['dados_geometricos']['ranhura_b']
        espessura_iso = self.bobinas.parede_iso(medidas_espira['b_espira'],largura_ranhura)

        tensao = self.dados['maquina']['tensao_v']

        campo_eletrico = self.eletrica.campo_eletrico(tensao,espessura_iso)   

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
        }
        
        
        