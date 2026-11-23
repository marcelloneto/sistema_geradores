from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView

from cadastros.models import Cliente, UnidadeGeradora, Usinas
from .forms import UnidadeGeradoraForm, UsinaForm


def _contexto_visualizar_usina(usina, ug_form=None, abrir_form_ug=False, mensagem_sucesso=None):
    usina = (
        Usinas.objects.select_related("operadora")
        .prefetch_related("unidades_geradoras__maquina", "maquinas__unidade_geradora")
        .get(pk=usina.pk)
    )
    return {
        "usina": usina,
        "modo": "visualizar",
        "unidades": usina.unidades_geradoras.all(),
        "maquinas": usina.maquinas.all(),
        "ug_form": ug_form or UnidadeGeradoraForm(),
        "abrir_form_ug": abrir_form_ug,
        "salvo_sucesso": mensagem_sucesso,
    }


class UsinaListView(ListView):
    model = Usinas
    template_name = "usinas/lista.html"
    context_object_name = "usinas"

    def get_queryset(self):
        queryset = (
            Usinas.objects.select_related("operadora")
            .annotate(
                total_ugs_cadastradas=Count("unidades_geradoras", distinct=True),
                total_maquinas_cadastradas=Count("maquinas", distinct=True),
            )
            .order_by("nome")
        )

        tipo = self.request.GET.get("tipo", "").strip()
        if tipo:
            queryset = queryset.filter(tipo=tipo)

        estado = self.request.GET.get("estado", "").strip()
        if estado:
            queryset = queryset.filter(estado__iexact=estado)

        operadora_id = self.request.GET.get("operadora", "").strip()
        if operadora_id:
            queryset = queryset.filter(operadora_id=operadora_id)

        busca = self.request.GET.get("q", "").strip()
        if busca:
            queryset = queryset.filter(
                Q(nome__icontains=busca)
                | Q(codigo_ceg__icontains=busca)
                | Q(localizacao__icontains=busca)
                | Q(operadora__nome__icontains=busca)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        totais = Usinas.objects.aggregate(
            potencia_geral=Sum("potencia_total"),
            maquinas_informadas=Sum("n_maquinas"),
        )

        contagens_tipo_raw = Usinas.objects.values("tipo").annotate(total=Count("id"))
        mapa_tipos = {row["tipo"]: row["total"] for row in contagens_tipo_raw}
        tipos_menu = [
            {
                "codigo": codigo,
                "label": label,
                "total": mapa_tipos.get(codigo, 0),
            }
            for codigo, label in Usinas.TipoUsina.choices
        ]

        estados_disponiveis = (
            Usinas.objects.exclude(estado="")
            .values_list("estado", flat=True)
            .distinct()
            .order_by("estado")
        )

        context["tipos_menu"] = tipos_menu
        context["total_geral"] = Usinas.objects.count()
        context["potencia_geral_kva"] = totais["potencia_geral"] or 0
        context["total_ugs_geral"] = totais["maquinas_informadas"] or 0
        context["estados_disponiveis"] = estados_disponiveis
        context["operadoras"] = (
            Cliente.objects.filter(usinas__isnull=False).distinct().order_by("nome")
        )
        context["tipo_atual"] = self.request.GET.get("tipo", "")
        context["estado_atual"] = self.request.GET.get("estado", "")
        context["operadora_atual"] = self.request.GET.get("operadora", "")
        context["busca_atual"] = self.request.GET.get("q", "")
        return context


class UsinaPainelView(View):
    template_name = "usinas/partials/detalhe_usina.html"

    def get(self, request, pk):
        usina = get_object_or_404(Usinas, pk=pk)
        modo = request.GET.get("modo", "visualizar")

        if modo == "editar":
            return render(
                request,
                self.template_name,
                {
                    "usina": usina,
                    "modo": "editar",
                    "form": UsinaForm(instance=usina),
                },
            )

        return render(request, self.template_name, _contexto_visualizar_usina(usina))

    def post(self, request, pk):
        usina = get_object_or_404(Usinas, pk=pk)
        form = UsinaForm(request.POST, instance=usina)

        if form.is_valid():
            usina = form.save()
            response = render(
                request,
                self.template_name,
                _contexto_visualizar_usina(
                    usina, mensagem_sucesso="Dados da usina atualizados com sucesso."
                ),
            )
            response["X-Usina-Salva"] = "1"
            return response

        return render(
            request,
            self.template_name,
            {
                "usina": usina,
                "modo": "editar",
                "form": form,
            },
        )


class UsinaNovoPainelView(View):
    template_name = "usinas/partials/detalhe_usina.html"

    def get(self, request):
        initial = {}
        tipo = request.GET.get("tipo", "").strip()
        if tipo:
            initial["tipo"] = tipo

        return render(
            request,
            self.template_name,
            {
                "usina": None,
                "modo": "criar",
                "form": UsinaForm(initial=initial),
            },
        )

    def post(self, request):
        form = UsinaForm(request.POST)
        if form.is_valid():
            usina = form.save()
            response = render(
                request,
                self.template_name,
                _contexto_visualizar_usina(
                    usina, mensagem_sucesso=f"Usina '{usina.nome}' cadastrada com sucesso."
                ),
            )
            response["X-Usina-Salva"] = "1"
            return response

        return render(
            request,
            self.template_name,
            {
                "usina": None,
                "modo": "criar",
                "form": form,
            },
        )


class UnidadeGeradoraPainelCreateView(View):
    template_name = "usinas/partials/detalhe_usina.html"

    def post(self, request, pk):
        usina = get_object_or_404(Usinas, pk=pk)
        ug_form = UnidadeGeradoraForm(request.POST)

        if ug_form.is_valid():
            ug = ug_form.save(commit=False)
            ug.usina = usina
            ug.save()
            response = render(
                request,
                self.template_name,
                _contexto_visualizar_usina(
                    usina, mensagem_sucesso=f"Unidade '{ug.nome}' adicionada."
                ),
            )
            response["X-Usina-Salva"] = "1"
            return response

        return render(
            request,
            self.template_name,
            _contexto_visualizar_usina(usina, ug_form=ug_form, abrir_form_ug=True),
        )


class UnidadeGeradoraPainelDeleteView(View):
    template_name = "usinas/partials/detalhe_usina.html"

    def post(self, request, pk, ug_pk):
        usina = get_object_or_404(Usinas, pk=pk)
        ug = get_object_or_404(UnidadeGeradora, pk=ug_pk, usina=usina)
        nome_ug = ug.nome
        ug.delete()

        response = render(
            request,
            self.template_name,
            _contexto_visualizar_usina(
                usina, mensagem_sucesso=f"Unidade '{nome_ug}' removida."
            ),
        )
        response["X-Usina-Salva"] = "1"
        return response