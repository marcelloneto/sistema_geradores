from cadastros.models import Material


class DadosMaterialService:

    CAMPOS = {
        "condutor": {
            "campo": "condutor",
            "categoria": "Condutor",
        },
        "isolamento_principal": {
            "campo": "isolacao_principal",
            "categoria": "Isolação Principal",
        },
        "isolacao_condutores": {
            "campo": "isolacao_condutores",
            "categoria": "Isolação Condutores",
        },
        "fita_condutiva": {
            "campo": "fita_condutiva",
            "categoria": "Fita Condutiva",
        },
        "verniz_condutivo": {
            "campo": "verniz_condutivo",
            "categoria": "Verniz Condutivo",
        },
        "fita_semicondutiva": {
            "campo": "fita_semicondutiva",
            "categoria": "Fita Semicondutiva",
        },
        "verniz_semicondutivo": {
            "campo": "verniz_semicondutivo",
            "categoria": "Verniz Semicondutivo",
        },
    }

    def __init__(self, secao):
        self.secao = secao
        self.config = self.CAMPOS[secao]

    def obter_dados(self, maquina):
        
        materiais_bobinagem = maquina.dados_bobinagem_roebel

        material_utilizado = getattr(
            materiais_bobinagem,
            self.config["campo"],
            None
        )

        return {
            "material_utilizado": self.material_para_dict(
                material_utilizado
            ),
            "materiais_disponiveis": [
                self.material_para_dict(material)
                for material in Material.objects.filter(
                    categoria__nome=self.config["categoria"],
                    ativo=True
                )
            ]
        }

    def material_para_dict(self, material):

        if not material:
            return None

        parametros = {}

        for parametro in material.parametros_tecnicos.all():

            valor = (
                parametro.valor_numero
                if parametro.valor_numero is not None
                else parametro.valor_texto
            )

            parametros[
                parametro.parametro.nome
            ] = {
                "valor": valor,
                "unidade": (
                    parametro.unidade.simbolo
                    if parametro.unidade
                    else None
                )
            }

        return {
            "id": material.id,
            "nome": material.nome,
            "codigo_material": material.codigo_material,
            "descricao": material.descricao,
            "parametros": parametros,
        }