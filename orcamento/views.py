from decimal import Decimal, InvalidOperation
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from cadastros.models import Cliente, Material
from .models import Orcamento, DadosGeometricosRoebel, MateriaisOrcamentoRoebel


CAMPOS_MATERIAIS_ROEBEL = [
    "isolacao_panqueca", "consolidacao_condutores",
    "massa_enchimento", "isolacao_condutores", "isolacao_principal",
    "fita_sacrificio", "verniz_condutivo", "fita_condutiva",
    "verniz_semicondutivo", "fita_semicondutiva", "cadarco_fibra_vidro",
    "fita_acabamento", "calcos_radiais", "calcos_tangenciais",
    "conexoes", "barramentos_ligacao", "pavio_central",
    "cunhagem", "sensor", "aros_amarracao",
]


def _to_decimal(value):
    if value is None or str(value).strip() == "":
        return None
    try:
        return Decimal(str(value).strip().replace(",", "."))
    except InvalidOperation:
        return None


def _to_int(value):
    if value is None or str(value).strip() == "":
        return None
    try:
        return int(str(value).strip())
    except ValueError:
        return None


def get_materiais_agrupados():
    materiais_ativos = (
        Material.objects.filter(ativo=True)
        .select_related("categoria", "fornecedor", "unidade_preco")
        .order_by("prioridade", "codigo_material", "nome")
    )
    por_categoria = {}
    for mat in materiais_ativos:
        cat_nome = (mat.categoria.nome or "").strip().lower()
        por_categoria.setdefault(cat_nome, []).append(mat)

    return {
        "condutores": por_categoria.get("condutor", []),
        "mat_isolacao": por_categoria.get("isolação", []),
        "mat_resina": por_categoria.get("resina", []),
        "mat_massa": por_categoria.get("massa", []),
        "mat_verniz": por_categoria.get("verniz", []),
        "mat_fita": por_categoria.get("fita", []),
        "mat_cadarco": por_categoria.get("cadarço", []),
        "mat_pavio": por_categoria.get("pavio", []),
        "mat_aro": por_categoria.get("aro", []),
        "mat_calco": por_categoria.get("calço", []),
        "mat_conexao": por_categoria.get("conexão", []),
        "mat_barramento": por_categoria.get("barramento", []),
        "mat_cunha": por_categoria.get("cunha", []),
        "mat_sensor": por_categoria.get("sensor", []),
    }


def lista_orcamentos(request):
    hoje = timezone.localdate()
    aba = request.GET.get("aba", "ativos")
    cliente_id = request.GET.get("cliente", "")
    data_filtro = request.GET.get("data", "")
    tipo_bobina = request.GET.get("tipo_bobina", "")
    tipo_bobinado = request.GET.get("tipo_bobinado", "")

    qs = Orcamento.objects.select_related("cliente")

    if aba == "vencidos":
        qs = qs.filter(
            Q(status=Orcamento.Status.VENCIDO) |
            Q(status=Orcamento.Status.ATIVO, data_validade__lt=hoje)
        )
    else:
        qs = qs.filter(
            status=Orcamento.Status.ATIVO,
            data_validade__gte=hoje
        )

    if cliente_id:
        qs = qs.filter(cliente_id=cliente_id)

    if data_filtro:
        qs = qs.filter(data_criacao__date=data_filtro)

    if tipo_bobina:
        qs = qs.filter(tipo_bobina=tipo_bobina)

    if tipo_bobinado:
        qs = qs.filter(tipo_bobinado=tipo_bobinado)

    context = {
        "orcamentos": qs,
        "clientes": Cliente.objects.all().order_by("nome"),
        "aba": aba,
        "filtros": {
            "cliente": cliente_id,
            "data": data_filtro,
            "tipo_bobina": tipo_bobina,
            "tipo_bobinado": tipo_bobinado,
        },
        "tipos_bobina": Orcamento.TipoBobina.choices,
        "tipos_bobinado": Orcamento.TipoBobinado.choices,
    }
    return render(request, "orcamento/lista.html", context)


def novo_orcamento(request):
    if request.method == "POST":
        with transaction.atomic():
            cliente_id = request.POST.get("cliente")
            quantidade_barras = _to_int(request.POST.get("quantidade_barras")) or 1
            tipo_bobina = request.POST.get("tipo_bobina")
            tipo_bobinado = request.POST.get("tipo_bobinado", "")
            data_validade = request.POST.get("data_validade")
            observacoes = request.POST.get("observacoes", "")

            orcamento = Orcamento.objects.create(
                cliente_id=cliente_id,
                quantidade_barras=quantidade_barras,
                tipo_bobina=tipo_bobina,
                tipo_bobinado=tipo_bobinado if tipo_bobina == "barra_roebel" else "",
                data_validade=data_validade or None,
                observacoes=observacoes,
            )

            if tipo_bobina == "barra_roebel":
                tipo_param_ranhura = request.POST.get("tipo_parametro_ranhura", "folga")

                DadosGeometricosRoebel.objects.create(
                    orcamento=orcamento,
                    # Barra de Fundo
                    fundo_a=_to_decimal(request.POST.get("fundo_a")),
                    fundo_b=_to_decimal(request.POST.get("fundo_b")),
                    fundo_c=_to_decimal(request.POST.get("fundo_c")),
                    fundo_d=_to_decimal(request.POST.get("fundo_d")),
                    fundo_l=_to_decimal(request.POST.get("fundo_l")),
                    fundo_num_condutores=_to_int(request.POST.get("fundo_num_condutores")),
                    fundo_num_espiras=_to_int(request.POST.get("fundo_num_espiras")),
                    fundo_condutores_por_espira=_to_int(request.POST.get("fundo_condutores_por_espira")),
                    fundo_condutor_id=_to_int(request.POST.get("fundo_condutor")),
                    # Barra de Topo
                    topo_a=_to_decimal(request.POST.get("topo_a")),
                    topo_b=_to_decimal(request.POST.get("topo_b")),
                    topo_c=_to_decimal(request.POST.get("topo_c")),
                    topo_d=_to_decimal(request.POST.get("topo_d")),
                    topo_l=_to_decimal(request.POST.get("topo_l")),
                    topo_num_condutores=_to_int(request.POST.get("topo_num_condutores")),
                    topo_num_espiras=_to_int(request.POST.get("topo_num_espiras")),
                    topo_condutores_por_espira=_to_int(request.POST.get("topo_condutores_por_espira")),
                    topo_condutor_id=_to_int(request.POST.get("topo_condutor")),
                    # Ranhura
                    ranhura_a=_to_decimal(request.POST.get("ranhura_a")),
                    ranhura_b=_to_decimal(request.POST.get("ranhura_b")),
                    ranhura_c=_to_decimal(request.POST.get("ranhura_c")),
                    ranhura_d=_to_decimal(request.POST.get("ranhura_d")),
                    tipo_parametro_ranhura=tipo_param_ranhura,
                    folga_ranhura=_to_decimal(request.POST.get("folga_ranhura")) if tipo_param_ranhura == "folga" else None,
                    espessura_isolacao=_to_decimal(request.POST.get("espessura_isolacao")) if tipo_param_ranhura == "isolacao" else None,
                )

                materiais_id_kwargs = {
                    f"{campo}_id": _to_int(request.POST.get(f"mat_{campo}"))
                    for campo in CAMPOS_MATERIAIS_ROEBEL
                }

                sobressalente = _to_decimal(request.POST.get("sobressalente_bobinas"))
                coeficiente = _to_decimal(request.POST.get("coeficiente_seguranca_bobinas"))

                MateriaisOrcamentoRoebel.objects.create(
                    orcamento=orcamento,
                    sobressalente_bobinas=sobressalente if sobressalente is not None else Decimal("0"),
                    coeficiente_seguranca_bobinas=coeficiente if coeficiente is not None else Decimal("1"),
                    **materiais_id_kwargs,
                )

        return redirect("orcamento:lista")

    context = {
        "clientes": Cliente.objects.all().order_by("nome"),
        "validade_padrao": (timezone.localdate() + timezone.timedelta(days=30)).isoformat(),
        **get_materiais_agrupados(),
    }
    return render(request, "orcamento/novo.html", context)


def detalhe_orcamento(request, pk):
    related_materiais = [f"materiais_roebel__{campo}" for campo in CAMPOS_MATERIAIS_ROEBEL]
    orcamento = get_object_or_404(
        Orcamento.objects.select_related(
            "cliente",
            "dados_roebel",
            "dados_roebel__fundo_condutor",
            "dados_roebel__fundo_condutor__fornecedor",
            "dados_roebel__topo_condutor",
            "dados_roebel__topo_condutor__fornecedor",
            "materiais_roebel",
            *related_materiais,
        ),
        pk=pk
    )
    context = {
        "orcamento": orcamento,
        "roebel": getattr(orcamento, "dados_roebel", None),
        "materiais": getattr(orcamento, "materiais_roebel", None),
    }
    return render(request, "orcamento/partials/detalhe_orcamento.html", context)