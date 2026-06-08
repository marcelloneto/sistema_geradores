from cadastros.models import OrdemServico
from operacao.services.session_service import SessionService
from operacao.services.base_service import BaseService


class OrdemService:
    def __init__(self, secao):
        self.secao = secao
        self.sessionservice = SessionService(self.secao)
    @staticmethod
    def listar_ordens():
        return (
            OrdemServico.objects
            .select_related("cliente", "maquina")
            .all()
            .order_by("-data_registro")
        )

    
    def obter_ordem_selecionada(self,request):
        os_numero = request.GET.get("os")
        print(f"obter_ordem_selecionada: {os_numero}")
        secoes = list(BaseService(self.secao).SECOES.keys())
        if os_numero:
            self.sessionservice.limpar_temp_se_trocar_os(
                request,
                os_numero,
                secoes
            )
            self.sessionservice.definir_os(
                request,
                os_numero
            )
        else:
            
            os_numero = self.sessionservice.obter_os(request)
            print(f"obter_ordem_selecionada 2: {os_numero}")

        if not os_numero:
            return None

        try:
            return (
                OrdemServico.objects
                .select_related("cliente", "maquina")
                .get(numero=os_numero)
            )
        except OrdemServico.DoesNotExist:
            return None