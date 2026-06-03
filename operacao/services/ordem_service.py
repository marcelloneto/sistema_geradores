from cadastros.models import OrdemServico
from operacao.services.session_service import SessionService


class OrdemService:

    @staticmethod
    def listar_ordens():
        return (
            OrdemServico.objects
            .select_related("cliente", "maquina")
            .all()
            .order_by("-data_registro")
        )

    @staticmethod
    def obter_ordem_selecionada(request):
        os_numero = request.GET.get("os")

        if os_numero:
            SessionService.limpar_temp_se_trocar_os(
                request,
                os_numero
            )
            SessionService.definir_os(
                request,
                os_numero
            )
        else:
            os_numero = SessionService.obter_os(request)

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