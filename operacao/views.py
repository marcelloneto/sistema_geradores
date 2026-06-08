from django.shortcuts import render, redirect
from django.forms.models import model_to_dict

from operacao.services.ordem_service import OrdemService
from operacao.services.base_service import BaseService
from operacao.services.session_service import SessionService

class home:
    @staticmethod
    def home(request):
        secao = 'maquina'
        ordemservice = OrdemService('home')
        baseservice = BaseService(secao)
        sessionservice = SessionService(secao)
        
        ordem_selecionada = ordemservice.obter_ordem_selecionada(
            request
        )
        if ordem_selecionada is None:
            ordens = ordemservice.listar_ordens()

            return render(request, "operacao/home.html", {
                "ordens": ordens,
                "ordem_selecionada": None,
                "dados": None,
            })
        
        ordens = ordemservice.listar_ordens()
        dados = ordem_selecionada.maquina
        
        temp = model_to_dict(dados)
        
        if f"{secao}_temp" in request.session:
            pass
        else:
            
            sessionservice.salvar_temp_secao(request,temp)
        
        if request.method == "POST":
            form = baseservice.processar_post(
                request,
                dados=dados
            )
        else:
            
            form = baseservice.criar_form_get(
                request,
                dados
            )
        
        contexto_form = baseservice.montar_contexto_form(
            form
                )
        

        return render(request, "operacao/home.html", {
            "ordens": ordens,
            "ordem_selecionada": ordem_selecionada,
            "maquina": dados,
            **contexto_form,
        })

class EstatorView:
   
    @staticmethod
    def estator(request):
        secao = 'estator'
        sessionservice = SessionService(secao)
        ordemservice =  OrdemService(secao)
        ordem_selecionada = ordemservice.obter_ordem_selecionada(
            request
        )

        baseservice = BaseService(secao)

        sessionservice.atualizar_os_anterior(request)

        ordens = ordemservice.listar_ordens()

        dados = baseservice.obter_dados(
            ordem_selecionada,
        )

        temp = model_to_dict(dados)
        if f"{secao}_temp" in request.session:
            pass
        else:
            
            sessionservice.salvar_temp_secao(request,temp)
        
        if request.method == "POST":
            form = baseservice.processar_post(
                request,
                dados=dados
            )
        else:
            form = baseservice.criar_form_get(
                request,
                dados
            )

        contexto_form = baseservice.montar_contexto_form(
            form
        )

        return render(request, "operacao/estator.html", {
            "ordens": ordens,
            "ordem_selecionada": ordem_selecionada,
            "dados_estator": dados,
            "estatortemp": sessionservice.obter_temp_secao(request),
            **contexto_form,
        })
    
class GeometricosView:
    @staticmethod
    def geometricos(request):
        secao = 'geometricos'
        sessionservice = SessionService(secao)
        ordemservice =  OrdemService(secao)
        ordem_selecionada = ordemservice.obter_ordem_selecionada(
            request
        )

        baseservice = BaseService(secao)

        sessionservice.atualizar_os_anterior(request)

        ordens = ordemservice.listar_ordens()

        dados = baseservice.obter_dados(
            ordem_selecionada,
        )

        temp = model_to_dict(dados)
        if f"{secao}_temp" in request.session:
            pass
        else:
            print(False)
            sessionservice.salvar_temp_secao(request,temp)

        if request.method == "POST":
            form = baseservice.processar_post(
                request,
                dados=dados
            )
        else:
            form = baseservice.criar_form_get(
                request,
                dados
            )

        contexto_form = baseservice.montar_contexto_form(
            form
        )

        return render(request, "operacao/geometricos.html", {
            "ordens": ordens,
            "ordem_selecionada": ordem_selecionada,
            "dados_geometricos": dados,
            "geometricostemp": sessionservice.obter_temp_secao(request),
            **contexto_form,
        })

class PerifericosView:
    @staticmethod
    def perifericos(request):
        secao = 'perifericos'
        sessionservice = SessionService(secao)
        ordemservice =  OrdemService(secao)
        ordem_selecionada = ordemservice.obter_ordem_selecionada(
            request
        )

        baseservice = BaseService(secao)

        sessionservice.atualizar_os_anterior(request)

        ordens = ordemservice.listar_ordens()

        dados = baseservice.obter_dados(
            ordem_selecionada,
        )

        temp = model_to_dict(dados)
        if f"{secao}_temp" in request.session:
            pass
        else:
            print(False)
            sessionservice.salvar_temp_secao(request,temp)

        if request.method == "POST":
            form = baseservice.processar_post(
                request,
                dados=dados
            )
        else:
            form = baseservice.criar_form_get(
                request,
                dados
            )

        contexto_form = baseservice.montar_contexto_form(
            form
        )

        return render(request, "operacao/perifericos.html", {
            "ordens": ordens,
            "ordem_selecionada": ordem_selecionada,
            "dados_perifericos": dados,
            "perifericostemp": sessionservice.obter_temp_secao(request),
            **contexto_form,
        })

class ConstrutivosView:

    @staticmethod
    def construtivos(request):
        secao = 'bobina'
        sessionservice = SessionService(secao)
        ordemservice =  OrdemService(secao)
        ordem_selecionada = ordemservice.obter_ordem_selecionada(
            request
        )

        baseservice = BaseService(secao)

        sessionservice.atualizar_os_anterior(request)

        ordens = ordemservice.listar_ordens()

        dados = baseservice.obter_dados(
            ordem_selecionada,
        )

        temp = model_to_dict(dados)
        
        if f"{secao}_temp" in request.session:
            pass
        else:
            print(False)
            sessionservice.salvar_temp_secao(request,temp)

        if request.method == "POST":
            form = baseservice.processar_post(
                request,
                dados=dados
            )
        else:
            form = baseservice.criar_form_get(
                request,
                dados
            )
        
        contexto_form = baseservice.montar_contexto_form_bobina(
            request,
            form,
            ordem_selecionada.maquina
        )

        return render(request, "operacao/construtivos.html", {
            "ordens": ordens,
            "ordem_selecionada": ordem_selecionada,
            "dados_bobina": dados,
            "construtivostemp": sessionservice.obter_temp_secao(request),
            **contexto_form,
        })

class EnsaioIsolamentoView:
    @staticmethod
    def ensaios(request):
        secao = 'ensaios'
        sessionservice = SessionService(secao)
        ordemservice =  OrdemService(secao)
        ordem_selecionada = ordemservice.obter_ordem_selecionada(
            request
        )

        baseservice = BaseService(secao)

        sessionservice.atualizar_os_anterior(request)

        ordens = ordemservice.listar_ordens()

        dados = baseservice.obter_dados(
            ordem_selecionada,
        )
        
        temp = model_to_dict(dados)
        if f"{secao}_temp" in request.session:
            pass
        else:
            print(False)
            sessionservice.salvar_temp_secao(request,temp)

        if request.method == "POST":
            form = baseservice.processar_post(
                request,
                dados=dados
            )
        else:
            form = baseservice.criar_form_get(
                request,
                dados
            )

        contexto_form = baseservice.montar_contexto_form_ensaios(
            form,
        )

        return render(request, "operacao/ensaios.html", {
            "ordens": ordens,
            "ordem_selecionada": ordem_selecionada,
            "dados_ensaios": dados,
            "ensaiostemp": sessionservice.obter_temp_secao(request),
            **contexto_form,
        })

class Registro:
    @staticmethod
    def registrar_os(request):
        secao = 'registrar_os'
        baseservice = BaseService(secao)
        
        if request.method == "POST":
            form = baseservice.processar_post(
                request,
                )


        return redirect(request.META.get("HTTP_REFERER", "admin:index"))

    @staticmethod
    def registrar_cliente(request):
        secao = 'registrar_cliente'
        baseservice = BaseService(secao)
        print("registrar_cliente")
        if request.method == "POST":
            form = baseservice.processar_post(
                request,
                )
        return redirect(request.META.get("HTTP_REFERER", "operacao:home") + "?abrir_modal_os=1")

    @staticmethod
    def registrar_maquina(request):
        secao = 'registrar_maquina'
        baseservice = BaseService(secao)
        print("registrar_maquina")
        if request.method == "POST":
            form = baseservice.processar_post(
                request,
                )
        return redirect(request.META.get("HTTP_REFERER", "operacao:home") + "?abrir_modal_os=1")