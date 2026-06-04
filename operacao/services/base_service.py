from operacao.forms import DadosEstatorForm
from operacao.services.session_service import SessionService


class BaseService:
    
    def __init__(self,secao):
        self.secao=secao
        self.SECOES  = {
        "estator":  DadosEstatorForm,
        }
        self.sessionservice = SessionService(self.secao)

    def obter_dados(self,ordem):
        if ordem and ordem.maquina:
            return getattr(
                ordem.maquina,
                f"dados_{self.secao}",
                None
            )

        return None

    
    def criar_form_get(self,request, dados):
        temp = self.sessionservice.obter_temp_secao(request)

        if temp:
            return self.SECOES[self.secao](
                temp,
                instance=dados
            )

        return DadosEstatorForm(
            instance=dados
        )

    @staticmethod
    def criar_form_post(request, dados):
        return DadosEstatorForm(
            request.POST,
            instance=dados
        )

    
    def processar_post(self,request, dados):
        if "restaurar" in request.POST:
            self.sessionservice.limpar_estator_(request)
            return DadosEstatorForm(instance=dados)

        if "aplicar_estator" in request.POST:
            form = BaseService.criar_form_post(
                request,
                dados
            )

            if form.is_valid():
                self.sessionservice.salvar_temp_secao(
                    request,
                    form.cleaned_data
                )

            return form

        return DadosEstatorForm(instance=dados)

    @staticmethod
    def montar_contexto_form(form):
        """utilizado apenas para a seção do estator"""
        return {
            "form": form,
            "campos_bobinado": form.obter_bobinado(),
            "campos_nucleo": form.obter_nucleo(),
        }