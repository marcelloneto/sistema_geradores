from django.shortcuts import render
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

        
        ordens = ordemservice.listar_ordens()
        dados = ordem_selecionada.maquina
        print(dados)
        temp = model_to_dict(dados)
        if f"{secao}_temp" in request.session:
                    pass
        else:
            
            sessionservice.salvar_temp_secao(request,temp)
        
        if request.method == "POST":
            form = baseservice.processar_post(
                request,
                dados
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
                dados
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
                dados
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
                dados
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
                dados
            )
        else:
            form = baseservice.criar_form_get(
                request,
                dados
            )

        contexto_form = baseservice.montar_contexto_form(
            form
        )

        return render(request, "operacao/construtivos.html", {
            "ordens": ordens,
            "ordem_selecionada": ordem_selecionada,
            "dados_construtivos": dados,
            "construtivostemp": sessionservice.obter_temp_secao(request),
            **contexto_form,
        })