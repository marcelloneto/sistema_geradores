from django.shortcuts import render
from cadastros.models import OrdemServico

def home(request):
    ordens = (
        OrdemServico.objects
        .select_related("cliente", "maquina")
        .order_by("numero")
    )

    tipos_servico = (
        OrdemServico.objects
        .values_list("tipo_servico", flat=True)
        .distinct()
        .order_by("tipo_servico")
    )

    clientes = (
        OrdemServico.objects
        .values_list("cliente__nome", flat=True)
        .distinct()
        .order_by("cliente__nome")
    )

    return render(request, "listagem/home.html", {
        "ordens": ordens,
        "tipos_servico": tipos_servico,
        "clientes": clientes,
    })