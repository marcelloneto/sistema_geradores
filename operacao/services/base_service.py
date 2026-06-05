from operacao.forms import DadosEstatorForm, DadosGeometricosForm, DadosPerifericosForm, DadosMaquinaForm, DadosBobinaForm
from operacao.services.session_service import SessionService


class BaseService:
    
    def __init__(self,secao):
        self.secao=secao
        self.SECOES  = {
        "estator":  DadosEstatorForm,
        "geometricos": DadosGeometricosForm,
        "perifericos": DadosPerifericosForm,
        "maquina": DadosMaquinaForm,
        "bobina": DadosBobinaForm,
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

        return self.SECOES[self.secao](
            instance=dados
        )

   
    def criar_form_post(self,request, dados):
        return self.SECOES[self.secao](
            request.POST,
            instance=dados
        )

    
    def processar_post(self,request, dados):
        if "restaurar" in request.POST:
            self.sessionservice.limpar_temp_(request)
            return self.SECOES[self.secao](instance=dados)

        if "aplicar" in request.POST:
            form = self.criar_form_post(
                request,
                dados
            )

            if form.is_valid():
                self.sessionservice.salvar_temp_secao(
                    request,
                    form.cleaned_data
                )                

            return form
        
        if "salvar" in request.POST:
            self.salvar_no_banco(
                request,
                dados
            )
            
            return self.SECOES[self.secao](instance=dados)

        return self.SECOES[self.secao](instance=dados)

    def salvar_no_banco(self,request, dados):
        temp = self.sessionservice.obter_temp_secao(request)
        print(temp)
        if not temp:
            return None

        form = self.SECOES[self.secao](
            temp,
            instance=dados
        )

        if form.is_valid():
            objeto = form.save()
            self.sessionservice.limpar_temp_secao(request)
            return objeto

        return None
   
    def montar_contexto_form(self,form):
        """utilizado apenas para a seção do estator"""
        if self.secao == "estator":
            return {
                "form": form,
                "campos_bobinado": form.obter_bobinado(),
                "campos_nucleo": form.obter_nucleo(),
            }
        elif self.secao == "geometricos":
            return {
                "form": form,
                "campos_ranhura": form.obter_ranhura(),
                "campos_bobina": form.obter_bobina(),
                "campos_condutor": form.obter_condutor,
                "campos_calco": form.obter_calco,
            }
        elif self.secao == "perifericos":
            return {
                "form": form,
                "campos_aro": form.obter_aro(),
                "campos_calco": form.obter_n_calco(),
                "campos_obs_calco": form.obter_obs_calco,
                "campos_inferior": form.obter_inferior,
            }
        elif self.secao == 'maquina' or self.secao == 'bobina':
            return {
                "form": form,
            }