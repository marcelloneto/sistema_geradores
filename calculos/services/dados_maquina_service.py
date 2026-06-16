from django.forms.models import model_to_dict


class DadosMaquinaService:
    """
    Serviço responsável por buscar e organizar os dados técnicos
    da máquina conforme a seção de cálculo solicitada.
    """

    SECOES = {
        "maquina": [
            "maquina",
        ],
        "bobinas": [
            "maquina",
            "dados_estator",
            "dados_bobina",
            "dados_construtivos_bobina",
            "dados_bobinagem_roebel",
        ],
        "isolamento": [
            "maquina",
            "dados_estator",
            "dados_bobina",
            "dados_bobinagem_roebel",
        ],
        "condutor": [
            "maquina",
            "dados_estator",
            "dados_geometricos",
            "dados_bobina",
            "dados_bobinagem_roebel",
        ],
        "pintura": [
            "maquina",
            "dados_estator",
            "dados_bobina",
            "dados_bobinagem_roebel",
        ],
        "geometria": [
            "maquina",
            "dados_bobina",
            "dados_construtivos_bobina",
        ],
    }

    def __init__(self, secao):
        self.secao = secao

    def obter_dados(self, ordem_servico):
        """
        Recebe uma OS e retorna apenas os dados necessários
        para a seção solicitada.
        """

        if not ordem_servico:
            return {}

        maquina = ordem_servico.maquina
        
        if not maquina:
            return {}

        dados = {}

        campos = self.SECOES.get(self.secao, [])

        for campo in campos:
            dados[campo] = self._obter_bloco(maquina, campo)

        return dados

    def _obter_bloco(self, maquina, campo):
        """
        Busca um bloco de dados relacionado à máquina.
        """

        if campo == "maquina":
            return model_to_dict(maquina)

        try:
            objeto = getattr(maquina, campo)
        except AttributeError:
            return {}

        if objeto is None:
            return {}

        return model_to_dict(objeto)

