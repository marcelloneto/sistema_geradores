from decimal import Decimal
from materiais.models import Condutor, Fita, Isolacao, Material, ResinaVerniz


class DadosMaterialService:

    CAMPOS = {
        "condutor": {
            "campo": "condutor",
            "model": Condutor,
        },
        "isolamento_principal": {
            "campo": "isolacao_principal",
            "model": Isolacao,
        },
        "isolacao_condutores": {
            "campo": "isolacao_condutores",
            "model": Isolacao,
        },
        "fita_condutiva": {
            "campo": "fita_condutiva",
            "model": Fita,
        },
        "verniz_condutivo": {
            "campo": "verniz_condutivo",
            "model": ResinaVerniz,
        },
        "fita_semicondutiva": {
            "campo": "fita_semicondutiva",
            "model": Fita,
        },
        "verniz_semicondutivo": {
            "campo": "verniz_semicondutivo",
            "model": ResinaVerniz,
        },
        "fita_acabamento": {
            "campo": "fita_acabamento",
            "model": Fita,
        },
    }

    def __init__(self, secao):
        self.secao = secao
        self.config = self.CAMPOS[secao]

    def _resolver_material_novo(self, material_legado):
        """
        Converte uma referência antiga (cadastros.Material) ou já migrada (materiais.Material)
        para a instância tipada correspondente em materiais.models.
        """
        if not material_legado:
            return None

        if isinstance(material_legado, Material):
            return material_legado.instancia_especifica

        model_cls = self.config["model"]
        codigo = (getattr(material_legado, "codigo_material", None) or "").strip().upper()
        if codigo:
            encontrado = model_cls.objects.filter(codigo_material=codigo).first()
            if encontrado:
                return encontrado

        return model_cls.objects.filter(nome__iexact=material_legado.nome.strip()).first()

    def obter_dados(self, maquina):
        materiais_bobinagem = getattr(maquina, "dados_bobinagem_roebel", None)
        material_bruto = (
            getattr(materiais_bobinagem, self.config["campo"], None)
            if materiais_bobinagem
            else None
        )
        material_utilizado = self._resolver_material_novo(material_bruto)

        model_cls = self.config["model"]
        materiais = model_cls.objects.filter(ativo=True).order_by("prioridade", "nome")

        materiais_disponiveis = {}
        for indice, material in enumerate(materiais):
            materiais_disponiveis[str(indice)] = self.material_para_dict(material)

        return {
            "material_utilizado": self.material_para_dict(material_utilizado),
            "materiais_disponiveis": materiais_disponiveis,
        }

    def material_para_dict(self, material):
        if not material:
            return None

        if isinstance(material, Material):
            material = material.instancia_especifica

        dados = {
            "id": material.id,
            "nome": material.nome,
            "codigo_material": material.codigo_material,
            "descricao": material.descricao,
            "tipo_material": material.tipo_material,
            "parametros": {},
        }

        if isinstance(material, Condutor):
            largura = material.lado_mm if material.forma == Condutor.Forma.QUADRADO else material.largura_mm
            altura = material.lado_mm if material.forma == Condutor.Forma.QUADRADO else material.altura_mm
            largura_iso = material.lado_isolacao_mm if material.forma == Condutor.Forma.QUADRADO else material.largura_isolacao_mm
            altura_iso = material.lado_isolacao_mm if material.forma == Condutor.Forma.QUADRADO else material.altura_isolacao_mm

            dados.update({
                "forma": material.forma,
                "largura_mm": largura,
                "altura_mm": altura,
                "lado_mm": material.lado_mm,
                "diametro_mm": material.diametro_mm,
                "largura_isolacao_mm": largura_iso,
                "altura_isolacao_mm": altura_iso,
                "densidade_kg_m3": material.densidade_kg_m3,
                "tipo_isolacao": material.tipo_isolacao,
                "classe_termica": material.classe_termica,
                "parametros": {
                    "Largura": {"valor": largura, "unidade": "mm"},
                    "Altura": {"valor": altura, "unidade": "mm"},
                    "Largura isolação": {"valor": largura_iso, "unidade": "mm"},
                    "Altura isolação": {"valor": altura_iso, "unidade": "mm"},
                    "Densidade": {"valor": material.densidade_kg_m3, "unidade": "kg/m³"},
                    "Tipo de condutor": {"valor": material.get_forma_display(), "unidade": None},
                },
            })

        elif isinstance(material, Isolacao):
            comprimento_mm = (
                material.comprimento_rolo_m * Decimal("1000")
                if material.comprimento_rolo_m is not None
                else Decimal("0")
            )
            dados.update({
                "aplicacao": material.aplicacao,
                "substrato": material.substrato,
                "espessura_mm": material.espessura_mm,
                "largura_mm": material.largura_mm,
                "comprimento_rolo_m": material.comprimento_rolo_m,
                "comprimento_rolo_mm": comprimento_mm,
                "parametros": {
                    "Espessura": {"valor": material.espessura_mm, "unidade": "mm"},
                    "Largura": {"valor": material.largura_mm, "unidade": "mm"},
                    "Comprimento do rolo": {"valor": material.comprimento_rolo_m, "unidade": "m"},
                },
            })

        elif isinstance(material, Fita):
            comprimento_mm = (
                material.comprimento_rolo_m * Decimal("1000")
                if material.comprimento_rolo_m is not None
                else Decimal("0")
            )
            dados.update({
                "finalidade": material.finalidade,
                "espessura_mm": material.espessura_mm,
                "largura_mm": material.largura_mm,
                "comprimento_rolo_m": material.comprimento_rolo_m,
                "comprimento_rolo_mm": comprimento_mm,
                "parametros": {
                    "Finalidade": {"valor": material.get_finalidade_display(), "unidade": None},
                    "Espessura": {"valor": material.espessura_mm, "unidade": "mm"},
                    "Largura": {"valor": material.largura_mm, "unidade": "mm"},
                    "Comprimento do rolo": {"valor": material.comprimento_rolo_m, "unidade": "m"},
                },
            })

        elif isinstance(material, ResinaVerniz):
            dados.update({
                "categoria_quimica": material.categoria_quimica,
                "finalidade": material.finalidade,
                "rendimento_kg_m": material.rendimento_kg_m,
                "rendimento_kg_m2": material.rendimento_kg_m2,
                "densidade_kg_m3": material.densidade_kg_m3,
                "parametros": {
                    "Finalidade": {"valor": material.get_finalidade_display(), "unidade": None},
                    "Rendimento": {"valor": material.rendimento_kg_m, "unidade": "kg/m"},
                },
            })

        return dados

    @staticmethod
    def separacao_verniz(opcoes):
        opcoes_disponiveis = opcoes["materiais_disponiveis"]
        opcoes_condutivo = {}
        opcoes_semicondutivo = {}
        opcoes_isolante = {}

        cond = 0
        semi = 0
        iso = 0
        for opcao in opcoes_disponiveis.values():
            finalidade = opcao.get("finalidade")
            if finalidade == ResinaVerniz.Finalidade.CONDUTIVO:
                opcoes_condutivo[str(cond)] = opcao
                cond += 1
            elif finalidade == ResinaVerniz.Finalidade.SEMICONDUTIVO:
                opcoes_semicondutivo[str(semi)] = opcao
                semi += 1
            elif finalidade == ResinaVerniz.Finalidade.ISOLANTE:
                opcoes_isolante[str(iso)] = opcao
                iso += 1

        return {
            "opcoes_condutivo": opcoes_condutivo,
            "opcoes_semicondutivo": opcoes_semicondutivo,
            "opcoes_isolante": opcoes_isolante,
        }