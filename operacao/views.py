from django.shortcuts import render

from operacao.services.ordem_service import OrdemService
from operacao.services.base_service import BaseService
from operacao.services.session_service import SessionService


def home(request):
    ordemservice = OrdemService('home')
    
    ordem_selecionada = ordemservice.obter_ordem_selecionada(
        request
    )

    ordens = ordemservice.listar_ordens()

    return render(request, "operacao/home.html", {
        "ordens": ordens,
        "ordem_selecionada": ordem_selecionada,
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

        print(list(request.session.keys()))

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