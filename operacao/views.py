from django.shortcuts import render

from operacao.services.ordem_service import OrdemService
from operacao.services.estator_service import EstatorService
from operacao.services.session_service import SessionService


def home(request):
    ordem_selecionada = OrdemService.obter_ordem_selecionada(
        request
    )

    ordens = OrdemService.listar_ordens()

    return render(request, "operacao/home.html", {
        "ordens": ordens,
        "ordem_selecionada": ordem_selecionada,
    })


def estator(request):
    ordem_selecionada = OrdemService.obter_ordem_selecionada(
        request
    )

    SessionService.atualizar_os_anterior(request)

    ordens = OrdemService.listar_ordens()

    dados_estator = EstatorService.obter_dados_estator(
        ordem_selecionada
    )

    if request.method == "POST":
        form = EstatorService.processar_post(
            request,
            dados_estator
        )
    else:
        form = EstatorService.criar_form_get(
            request,
            dados_estator
        )

    contexto_form = EstatorService.montar_contexto_form(
        form
    )

    return render(request, "operacao/estator.html", {
        "ordens": ordens,
        "ordem_selecionada": ordem_selecionada,
        "dados_estator": dados_estator,
        "estatortemp": SessionService.obter_estator_temp(request),
        **contexto_form,
    })