from decimal import Decimal
import math
from calculos.calculos.bobina import ResultadosBobinas
from calculos.calculos.condutor import ResultadosCondutor
from calculos.calculos.eletrica import ResultadosEletrica
from calculos.calculos.estator import ResultadosEstator


class Verificacao:
    @staticmethod
    def validar_valores(material):
        if not material or not isinstance(material, dict):
            return "Material não possui dados registrados"

        campos_obrigatorios = [
            "altura_mm",
            "largura_mm",
            "altura_isolacao_mm",
            "largura_isolacao_mm",
            "densidade_kg_m3",
        ]
        for campo in campos_obrigatorios:
            if material.get(campo) is None:
                return "Material não possui dados registrados"
        return None

    @staticmethod
    def chamar_calculos(request, escolhido):
        if escolhido is None:
            return "nenhum condutor registrado"
        ver = Verificacao.validar_valores(escolhido)
        if ver:
            return ver
        return True


class Filtros:
    def __init__(
        self,
        dados,
        iso_sel={},
        condutor={},
        iso_principal={},
        folga=0.4,
        sobreposicao=Decimal(0.5),
        fitas={},
    ):
        self.dados = dados
        self.condutor_sel = condutor
        self.iso_principal = iso_principal
        self.iso_sel = iso_sel
        self.fitas = fitas

        self.estator = ResultadosEstator(dados["dados_estator"])

        if self.validar_dados(self.condutor_sel):
            self.bobinas = ResultadosBobinas(
                self.dados,
                dados["dados_bobina"],
                condutor,
                iso_principal,
                iso_sel,
                folga,
                sobreposicao,
                fitas,
            )
            self.condutor = ResultadosCondutor(
                self.dados, condutor, self.bobinas.calcular_comprimento()
            )

        self.eletrica = ResultadosEletrica(dados)

    def validar_dados(self, secao):
        return Verificacao.validar_valores(secao) is None

    def calcular_condutor(self, coef):
        if self.validar_dados(self.condutor_sel):
            area_condutor = self.condutor.area
            n_condutores_espira = self.dados["dados_estator"]["numero_condutores_por_espira"]
            n_espiras_bobina = self.dados["dados_estator"]["numero_espiras_por_bobina"]
            area_espira = self.bobinas.area_espira
            area_total_espiras = self.bobinas.area_secao_cobre
            comprimento_bobina = self.bobinas.calcular_comprimento_condutor()
            volume_condutor_bobina = self.bobinas.volume_cobre
            peso_condutor_barra = self.condutor.peso(volume_condutor_bobina) / 2
            numero_barras = self.dados["dados_estator"]["numero_bobinas"] * 2
            peso_condutor_bobina = self.condutor.peso(volume_condutor_bobina)
            numero_bobinas = self.dados["dados_estator"]["numero_bobinas"]
            peso_total_condutor = peso_condutor_bobina * numero_bobinas
            peso_com_seguranca = peso_total_condutor * Decimal(float(str(coef).replace(",", ".")))

            n_paralelos = self.dados["dados_estator"]["numero_paralelos"]
            corrente = self.dados["maquina"]["corrente_a"]

            densidade = self.eletrica.densidade_corrente(corrente, n_paralelos, area_espira)
            largura_ranhura = self.dados["dados_geometricos"]["ranhura_b"]
            espessura_iso = self.bobinas.parede_iso
            tensao = self.dados["maquina"]["tensao_v"]
            campo_eletrico = self.eletrica.campo_eletrico(tensao, espessura_iso)
            espaco_calco = self.bobinas.espaco_para_calco

            return {
                "Área do Condutor": [area_condutor, "mm²"],
                "Quantidade de condutores por espira": [n_condutores_espira, ""],
                "Área da Espira": [area_espira, "mm²"],
                "Quantidade de espiras por bobina": [n_espiras_bobina, ""],
                "Área Total Espiras": [area_total_espiras, "mm²"],
                "Comprimento da Barra": [comprimento_bobina / 2, "mm"],
                "Peso de Cobre por Barra": [peso_condutor_barra, "kg"],
                "Quantidade de Barras": [numero_barras, "unidades"],
                "Comprimento da Bobina": [comprimento_bobina, "mm"],
                "Peso de cobre por Bobina": [peso_condutor_bobina, "kg"],
                "Quantidade de Bobinas": [numero_bobinas, "unidades"],
                "Peso total de cobre": [peso_total_condutor, "kg"],
                "Peso total de cobre (com segurança)": [peso_com_seguranca, "kg"],
                "Largura da Ranhura": [largura_ranhura, "mm"],
                "Espessura da Isolação": [espessura_iso, "mm"],
                "Densidade de corrente": [densidade, "A/mm²"],
                "Campo Elétrico": [campo_eletrico, "kV/mm"],
                "Espaco para Calço": [espaco_calco, "mm"],
            }
        return None

    def calcular_isolacao(self, coef):
        altura_bobina_iso = self.bobinas.altura_bobina_iso
        largura_bobina_iso = self.bobinas.largura_bobina_iso
        perimetro_ext = self.bobinas.perimetro_externo
        perimetro_int = self.bobinas.perimetro_interno
        perimetro = self.bobinas.perimetro_medio

        if self.iso_principal is not None:
            n_voltas = self.bobinas.voltas_isolacao
            l_fita_isolante_bobina = self.bobinas.comprimento_fita_isolante_bobina
            l_fita_isolante_total = self.bobinas.comprimento_fita_isolante_total
            rolos_fita_isolante_bobina = self.bobinas.rolo_fita_isolante_bobina
            rolos_fita_isolante = self.bobinas.rolo_fita_isolante_total
            n_camadas = self.bobinas.n_camadas_isolacao
            rolos_seguranca = rolos_fita_isolante * Decimal(coef)

            return {
                "Altura total da Bobina": [altura_bobina_iso, "mm"],
                "Largura total da Bobina": [largura_bobina_iso, "mm"],
                "Perímetro da Bobina (sem isolação)": [perimetro_int, "mm"],
                "Perímetro da Bobina Isolada": [perimetro_ext, "mm"],
                "Perímetro médio da Isolação da Bobina": [perimetro, "mm"],
                "Número de voltas": [n_voltas, ""],
                "Número de camadas": [math.ceil(n_camadas), ""],
                "Comprimento de fita por Bobina": [
                    math.ceil(l_fita_isolante_bobina / Decimal(1000)),
                    "metros",
                ],
                "Rolos de fita necessários por bobina": [
                    math.ceil(rolos_fita_isolante_bobina),
                    "rolos",
                ],
                "Comprimento de fita total": [
                    math.ceil(l_fita_isolante_total / Decimal(1000)),
                    "metros",
                ],
                "Rolos de Fita Isolante necessários": [math.ceil(rolos_fita_isolante), "rolos"],
                "Rolos de Fita Isolante Necessários (com segurança)": [
                    math.ceil(rolos_seguranca),
                    "rolos",
                ],
            }

    def calcular_fitas(self, coef):
        FITAS_LABEL = {
            "aplicacao_fita": "Comprimento de Aplicação",
            "camadas": "Número de camadas",
            "n_voltas": "Número de voltas",
            "rolos_bobina": "Rolos de Fita Necessários por Bobina",
            "comprimento_fita_bobina": "Comprimento de Fita por Bobina",
            "comprimento_fita_total": "Comprimento de Fita Total",
            "rolos_total": "Rolos de Fita Necessários",
            "rolos_seguranca": "Rolos de Fita Necessários (com segurança)",
        }
        FITAS_UNIDADES = {
            "aplicacao_fita": "mm",
            "camadas": "",
            "n_voltas": "",
            "rolos_bobina": "rolos",
            "comprimento_fita_bobina": "m",
            "comprimento_fita_total": "m",
            "rolos_total": "rolos",
            "rolos_seguranca": "rolos",
        }
        FITAS_MULTIPLICADOR = {
            "aplicacao_fita": 1,
            "camadas": 1,
            "n_voltas": 1,
            "rolos_bobina": 1,
            "comprimento_fita_bobina": 0.001,
            "comprimento_fita_total": 0.001,
            "rolos_total": 1,
            "rolos_seguranca": 1,
        }

        fitas = self.bobinas.resultados_fitas
        for fita in fitas:
            fitas[fita]["rolos_seguranca"] = math.ceil(
                fitas[fita]["rolos_total"] * Decimal(self.fitas[fita]["coeficiente_seguranca"])
            )

        if fitas != {}:
            return {
                "fita_condutiva": self.context_fitas(
                    fitas["fita_condutiva"], FITAS_LABEL, FITAS_UNIDADES, FITAS_MULTIPLICADOR
                ),
                "fita_semicondutiva": self.context_fitas(
                    fitas["fita_semicondutiva"], FITAS_LABEL, FITAS_UNIDADES, FITAS_MULTIPLICADOR
                ),
                "fita_acabamento": self.context_fitas(
                    fitas["fita_acabamento"], FITAS_LABEL, FITAS_UNIDADES, FITAS_MULTIPLICADOR
                ),
            }

    @staticmethod
    def context_fitas(fita, label, unidades, multiplicador):
        return {
            label[parametro]: [fita[parametro] * Decimal(multiplicador[parametro]), unidades[parametro]]
            for parametro in fita
        }

    def verificar_iso(self, iso):
        if iso != -1 and iso is not None and isinstance(iso, dict):
            return iso.get("espessura_mm") or Decimal(0)
        return Decimal(0)