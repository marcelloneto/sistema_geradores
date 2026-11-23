from django.shortcuts import render
from django.utils import timezone
from cadastros.models import Maquina, OrdemServico, Usinas
from materiais.models import Material

try:
    from orcamento.models import Orcamento
except Exception:
    Orcamento = None


def home(request):
    stats = {
        "maquinas": Maquina.objects.count(),
        "usinas": Usinas.objects.count(),
        "materiais": Material.objects.filter(ativo=True).count(),
        "ordens_servico": OrdemServico.objects.count(),
        "orcamentos_ativos": (
            Orcamento.objects.filter(status="ativo").count()
            if Orcamento is not None else 0
        ),
    }

    context = {
        "stats": stats,
        "hoje": timezone.localdate(),
    }
    return render(request, "portal/home.html", context)