from operacao.forms import *
from operacao.services.session_service import SessionService
from cadastros.models import DadosEstator
from django.db import transaction

class BaseService:
    
    def __init__(self, secao):
        self.secao = secao
        self.SECOES = {
            "estator": DadosEstatorForm,
            "geometricos": DadosGeometricosForm,
            "perifericos": DadosPerifericosForm,
            "maquina": DadosMaquinaForm,
            "bobina": DadosBobinaForm,
            "ensaios": DadosEnsaiosForm,
            "registrar_os": RegistroOSForm,
            "registrar_cliente": RegistroClienteForm,
            "registrar_maquina": RegistroMaquinaForm,
            "bobinagem_roebel": MateriaisBobinagemRoebelForm,
        }
        self.sessionservice = SessionService(self.secao)

    def obter_dados(self, ordem):
        if ordem and ordem.maquina:
            return getattr(
                ordem.maquina,
                f"dados_{self.secao}",
                None
            )
        return None

    def criar_form_get(self, request, dados):
        # Como removemos o rascunho, sempre retorna os dados oficiais do banco
        return self.SECOES[self.secao](instance=dados)

    def criar_form_post(self, request, dados):
        return self.SECOES[self.secao](
            request.POST,
            instance=dados
        )

    def processar_post(self, request, dados=None):
        # Ação direta: Valida e salva no banco de dados
        if "salvar" in request.POST:
            form = self.criar_form_post(request, dados)
            if form.is_valid():
                form.save()
            return form # Retorna o form (com erros se for inválido, ou atualizado se for válido)

        elif "novo_projeto" in request.POST:
            form = self.SECOES['registrar_os'](request.POST)
            if form.is_valid():
                return form.save()

        elif "novo_cliente" in request.POST:
            form = self.SECOES['registrar_cliente'](request.POST)
            if form.is_valid():
                return form.save()

        elif "nova_maquina" in request.POST:
            form = self.SECOES['registrar_maquina'](request.POST)
            if form.is_valid():
                return self.criar_novo_projeto(form)

        # Retorno padrão caso não encontre nenhum dos botões esperados
        return self.SECOES[self.secao](instance=dados)
   
    def montar_contexto_form(self, form):
        """Utilizado para estruturar o envio de dados aos templates"""
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
                "campos_condutor": form.obter_condutor(),
                "campos_calco": form.obter_calco(),
            }
        elif self.secao == "perifericos":
            return {
                "form": form,
                "campos_aro": form.obter_aro(),
                "campos_calco": form.obter_n_calco(),
                "campos_obs_calco": form.obter_obs_calco(),
                "campos_inferior": form.obter_inferior(),
            }
        elif self.secao == 'maquina':          
            return {
                "form_maquina": form,
            }
         
    def montar_contexto_form_bobina(self, request, form, maquina):
        # Leitura direta e segura do banco de dados, ignorando sessões temporárias
        try:
            estator = DadosEstator.objects.get(maquina=maquina)
            tipo_bobina = estator.tipo_bobina
            tipo_bobinado = estator.tipo_bobinado
        except DadosEstator.DoesNotExist:
            tipo_bobina = None
            tipo_bobinado = None

        if not tipo_bobina:
            tipo_bobina = "barra_roebel"
        if not tipo_bobinado:
            tipo_bobinado = "imbricado"

        if tipo_bobina == "barra_roebel":
            if tipo_bobinado == "ondulado":
                croqui = {
                    "titulo": "Croqui",
                    "campos": form.obter_croqui(),
                    "caminho_imagem": "operacao/img/croqui_roebel_ondulado.png"
                }
                amarracao = {
                    "titulo": "Amarração",
                    "campos": form.obter_amarracao(),
                    "caminho_imagem": "operacao/img/amarracao_roebel_ondulado.png",
                }
            elif tipo_bobinado == "imbricado":
                croqui = {
                    "titulo": "Croqui",
                    "campos": form.obter_croqui(),
                    "caminho_imagem": "operacao/img/croqui_roebel_imbricado.png"
                }
                amarracao = {
                    "titulo": "Amarração",
                    "campos": form.obter_amarracao(),
                    "caminho_imagem": "operacao/img/amarracao_roebel_imbricado.png",
                }
            configuracao = {
                "titulo": "Configuração",
                "campos": form.obter_configuracao(),
                "caminho_imagem": "operacao/img/configuracao.png",
            }
            montada = {
                "titulo": "Bobina Montada",
                "campos": form.obter_montada(),
                "caminho_imagem": "operacao/img/montada.png",
            }
        elif tipo_bobina == "multiespiras":
            croqui = {
                "titulo": "Croqui",
                "campos": form.obter_croqui(),
                "caminho_imagem": "operacao/img/croqui_multiespiras.png"
            }
            amarracao = {
                "titulo": "Amarração",
                "campos": form.obter_amarracao(),
                "caminho_imagem": "operacao/img/amarracao_multiespiras.png",
            }
            configuracao = {
                "titulo": "Configuração",
                "campos": form.obter_configuracao(),
                "caminho_imagem": "operacao/img/configuracao.png",
            }
            montada = {
                "titulo": "Bobina Montada",
                "campos": form.obter_montada(),
                "caminho_imagem": "operacao/img/montada.png",
            }

        return {
            "form": form,
            "secoes": [croqui, amarracao, configuracao, montada],
        }

    def montar_contexto_form_ensaios(self, form):
        """Utilizado apenas para a seção de ensaios"""
        if self.secao == "ensaios":
            return {
                "form": form,
                "campos_parte1": form.obter_parte1(),
                "campos_parte2": form.obter_parte2(),
            }

    def montar_contexto_form_roebel(self, form):
        return {
            "form": form,
            "campos_condutor_isolamento": form.obter_condutor_isolamento(),
            "campos_resinas": form.obter_resinas(),
            "campos_condutivo": form.obter_condutivo(),
            "campos_semicondutivo": form.obter_semicondutivo(),
            "campos_acabamento": form.obter_acabamento(),
            "campos_componentes": form.obter_componentes(),
            "campos_parametros": form.obter_parametros(),
        }

    @transaction.atomic
    def criar_novo_projeto(self, form):
        os_obj = form.save(commit=False)
        maquina = os_obj
        maquina.save()

        DadosEstator.objects.get_or_create(maquina=maquina)
        DadosPerifericos.objects.get_or_create(maquina=maquina)
        DadosGeometricosMaquina.objects.get_or_create(maquina=maquina)
        DadosConstrutivosBobina.objects.get_or_create(maquina=maquina)
        ResIsolamento.objects.get_or_create(maquina=maquina)
        MateriaisBobinagemRoebel.objects.get_or_create(maquina=maquina)

        return os_obj