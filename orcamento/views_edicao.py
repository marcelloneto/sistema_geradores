from decimal import Decimal
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from cadastros.models import Cliente
from .models import Orcamento, DadosGeometricosRoebel, MateriaisOrcamentoRoebel
from .views import CAMPOS_MATERIAIS_ROEBEL, _to_decimal, _to_int, get_materiais_agrupados


def editar_orcamento(request, pk):
    orcamento = get_object_or_404(
        Orcamento.objects.select_related("cliente"),
        pk=pk
    )

    roebel = getattr(orcamento, "dados_roebel", None)
    materiais = getattr(orcamento, "materiais_roebel", None)

    if request.method == "POST":
        with transaction.atomic():
            orcamento.cliente_id = request.POST.get("cliente")
            orcamento.quantidade_barras = _to_int(request.POST.get("quantidade_barras")) or 1
            orcamento.tipo_bobina = request.POST.get("tipo_bobina")
            tipo_bobinado = request.POST.get("tipo_bobinado", "")
            orcamento.tipo_bobinado = tipo_bobinado if orcamento.tipo_bobina == "barra_roebel" else ""
            orcamento.status = request.POST.get("status", orcamento.status)
            orcamento.data_validade = request.POST.get("data_validade") or orcamento.data_validade
            orcamento.observacoes = request.POST.get("observacoes", "")
            orcamento.save()

            if orcamento.tipo_bobina == "barra_roebel":
                tipo_param_ranhura = request.POST.get("tipo_parametro_ranhura", "folga")

                roebel_obj, _ = DadosGeometricosRoebel.objects.get_or_create(orcamento=orcamento)
                # Barra de Fundo
                roebel_obj.fundo_a = _to_decimal(request.POST.get("fundo_a"))
                roebel_obj.fundo_b = _to_decimal(request.POST.get("fundo_b"))
                roebel_obj.fundo_c = _to_decimal(request.POST.get("fundo_c"))
                roebel_obj.fundo_d = _to_decimal(request.POST.get("fundo_d"))
                roebel_obj.fundo_l = _to_decimal(request.POST.get("fundo_l"))
                roebel_obj.fundo_num_condutores = _to_int(request.POST.get("fundo_num_condutores"))
                roebel_obj.fundo_num_espiras = _to_int(request.POST.get("fundo_num_espiras"))
                roebel_obj.fundo_condutores_por_espira = _to_int(request.POST.get("fundo_condutores_por_espira"))
                roebel_obj.fundo_condutor_id = _to_int(request.POST.get("fundo_condutor"))

                # Barra de Topo
                roebel_obj.topo_a = _to_decimal(request.POST.get("topo_a"))
                roebel_obj.topo_b = _to_decimal(request.POST.get("topo_b"))
                roebel_obj.topo_c = _to_decimal(request.POST.get("topo_c"))
                roebel_obj.topo_d = _to_decimal(request.POST.get("topo_d"))
                roebel_obj.topo_l = _to_decimal(request.POST.get("topo_l"))
                roebel_obj.topo_num_condutores = _to_int(request.POST.get("topo_num_condutores"))
                roebel_obj.topo_num_espiras = _to_int(request.POST.get("topo_num_espiras"))
                roebel_obj.topo_condutores_por_espira = _to_int(request.POST.get("topo_condutores_por_espira"))
                roebel_obj.topo_condutor_id = _to_int(request.POST.get("topo_condutor"))

                # Ranhura
                roebel_obj.ranhura_a = _to_decimal(request.POST.get("ranhura_a"))
                roebel_obj.ranhura_b = _to_decimal(request.POST.get("ranhura_b"))
                roebel_obj.ranhura_c = _to_decimal(request.POST.get("ranhura_c"))
                roebel_obj.ranhura_d = _to_decimal(request.POST.get("ranhura_d"))
                roebel_obj.tipo_parametro_ranhura = tipo_param_ranhura
                roebel_obj.folga_ranhura = (
                    _to_decimal(request.POST.get("folga_ranhura"))
                    if tipo_param_ranhura == "folga" else None
                )
                roebel_obj.espessura_isolacao = (
                    _to_decimal(request.POST.get("espessura_isolacao"))
                    if tipo_param_ranhura == "isolacao" else None
                )
                roebel_obj.save()

                # Materiais
                mat_obj, _ = MateriaisOrcamentoRoebel.objects.get_or_create(orcamento=orcamento)
                for campo in CAMPOS_MATERIAIS_ROEBEL:
                    setattr(mat_obj, f"{campo}_id", _to_int(request.POST.get(f"mat_{campo}")))

                sobressalente = _to_decimal(request.POST.get("sobressalente_bobinas"))
                coeficiente = _to_decimal(request.POST.get("coeficiente_seguranca_bobinas"))
                mat_obj.sobressalente_bobinas = sobressalente if sobressalente is not None else Decimal("0")
                mat_obj.coeficiente_seguranca_bobinas = coeficiente if coeficiente is not None else Decimal("1")
                mat_obj.save()

        return redirect("orcamento:lista")

    context = {
        "orcamento": orcamento,
        "roebel": roebel,
        "materiais": materiais,
        "clientes": Cliente.objects.all().order_by("nome"),
        "status_choices": Orcamento.Status.choices,
        **get_materiais_agrupados(),
    }
    return render(request, "orcamento/editar.html", context)