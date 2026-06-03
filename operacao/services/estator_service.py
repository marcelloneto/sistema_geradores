from operacao.forms import DadosEstatorForm
from operacao.services.session_service import SessionService


class EstatorService:

    @staticmethod
    def obter_dados_estator(ordem):
        if ordem and ordem.maquina:
            return getattr(
                ordem.maquina,
                "dados_estator",
                None
            )

        return None

    @staticmethod
    def criar_form_get(request, dados_estator):
        estator_temp = SessionService.obter_estator_temp(request)

        if estator_temp:
            return DadosEstatorForm(
                estator_temp,
                instance=dados_estator
            )

        return DadosEstatorForm(
            instance=dados_estator
        )

    @staticmethod
    def criar_form_post(request, dados_estator):
        return DadosEstatorForm(
            request.POST,
            instance=dados_estator
        )

    @staticmethod
    def processar_post(request, dados_estator):
        if "restaurar" in request.POST:
            SessionService.limpar_estator_(request,'estator_temp')
            return DadosEstatorForm(instance=dados_estator)

        if "aplicar_estator" in request.POST:
            form = EstatorService.criar_form_post(
                request,
                dados_estator
            )

            if form.is_valid():
                SessionService.salvar_estator_temp(
                    request,
                    form.cleaned_data
                )

            return form

        return DadosEstatorForm(instance=dados_estator)

    @staticmethod
    def montar_contexto_form(form):
        return {
            "form": form,
            "campos_bobinado": form.obter_bobinado(),
            "campos_nucleo": form.obter_nucleo(),
        }