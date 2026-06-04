from django.shortcuts import render

from operacao.services.ordem_service import OrdemService
from operacao.services.base_service import BaseService
from operacao.services.session_service import SessionService


def home(request):
    ordemservice = OrdemService('estator')
    
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
        sessionservice = SessionService('estator')
        ordemservice =  OrdemService('estator')
        ordem_selecionada = ordemservice.obter_ordem_selecionada(
            request
        )

        service = BaseService('estator')

        sessionservice.atualizar_os_anterior(request)

        ordens = ordemservice.listar_ordens()

        dados_estator = service.obter_dados(
            ordem_selecionada,
        )

        if request.method == "POST":
            form = service.processar_post(
                request,
                dados_estator
            )
        else:
            form = service.criar_form_get(
                request,
                dados_estator
            )

        contexto_form = service.montar_contexto_form(
            form
        )

        return render(request, "operacao/estator.html", {
            "ordens": ordens,
            "ordem_selecionada": ordem_selecionada,
            "dados_estator": dados_estator,
            "estatortemp": sessionservice.obter_temp_secao(request),
            **contexto_form,
        })