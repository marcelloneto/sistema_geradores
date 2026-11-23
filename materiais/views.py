from decimal import Decimal
from django.contrib import messages
from django.db.models import Count, ProtectedError, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from cadastros.models import Fornecedor
from .forms import CONFIG_TIPOS_MATERIAL
from .models import (
    Calco,
    Condutor,
    CordaoPavio,
    Cunha,
    Fita,
    Isolacao,
    Material,
    MaterialAuxiliar,
    ResinaVerniz,
    SensorTemperatura,
)

CAMPOS_BASE_IGNORAR = {
    "id",
    "material_ptr",
    "codigo_material",
    "codigo_fornecedor",
    "nome",
    "tipo_material",
    "descricao",
    "fornecedor",
    "prioridade",
    "preco",
    "unidade_preco",
    "data_atualizacao_preco",
    "ativo",
    "data_registro",
    "data_atualizacao",
}


def _fmt_num(valor):
    if valor is None:
        return None
    return f"{valor:f}".rstrip("0").rstrip(".").replace(".", ",")


def gerar_resumo_tecnico(material_base):
    obj = material_base.instancia_especifica

    if isinstance(obj, Condutor):
        partes = []
        if obj.forma == Condutor.Forma.REDONDO and obj.diametro_mm:
            partes.append(f"Ø {_fmt_num(obj.diametro_mm)} mm")
        elif obj.forma == Condutor.Forma.QUADRADO and obj.lado_mm:
            partes.append(f"Lado {_fmt_num(obj.lado_mm)} mm")
        elif obj.largura_mm and obj.altura_mm:
            partes.append(f"{_fmt_num(obj.largura_mm)} × {_fmt_num(obj.altura_mm)} mm")
        if obj.tipo_isolacao:
            partes.append(obj.tipo_isolacao)
        if obj.classe_termica:
            partes.append(f"Classe {obj.classe_termica}")
        return " • ".join(partes) or obj.get_forma_display()

    if isinstance(obj, Isolacao):
        partes = [obj.get_aplicacao_display()]
        if obj.espessura_mm and obj.largura_mm:
            partes.append(f"{_fmt_num(obj.espessura_mm)} × {_fmt_num(obj.largura_mm)} mm")
        if obj.comprimento_rolo_m:
            partes.append(f"Rolo {_fmt_num(obj.comprimento_rolo_m)} m")
        return " • ".join(partes)

    if isinstance(obj, Fita):
        partes = [obj.get_finalidade_display()]
        if obj.espessura_mm and obj.largura_mm:
            partes.append(f"{_fmt_num(obj.espessura_mm)} × {_fmt_num(obj.largura_mm)} mm")
        if obj.comprimento_rolo_m:
            partes.append(f"Rolo {_fmt_num(obj.comprimento_rolo_m)} m")
        return " • ".join(partes)

    if isinstance(obj, ResinaVerniz):
        partes = [f"{obj.get_categoria_quimica_display()} ({obj.get_finalidade_display()})"]
        if obj.rendimento_kg_m:
            partes.append(f"{_fmt_num(obj.rendimento_kg_m)} kg/m")
        return " • ".join(partes)

    if isinstance(obj, CordaoPavio):
        partes = [obj.get_tipo_display()]
        if obj.diametro_mm:
            partes.append(f"Ø {_fmt_num(obj.diametro_mm)} mm")
        return " • ".join(partes)

    if isinstance(obj, (Calco, Cunha)):
        partes = [obj.material_base] if obj.material_base else []
        dims = [_fmt_num(d) for d in (obj.espessura_mm, obj.largura_mm, obj.comprimento_mm) if d]
        if dims:
            partes.append(" × ".join(dims) + " mm")
        return " • ".join(partes) or "-"

    if isinstance(obj, SensorTemperatura):
        return f"{obj.get_tipo_sensor_display()} • {obj.numero_fios} fios"

    if isinstance(obj, MaterialAuxiliar):
        return obj.especificacao_dimensional or obj.get_subtipo_display()

    return "-"


def obter_campos_tecnicos_exibicao(material_obj):
    """Extrai todos os campos específicos da subclasse com rótulo e valor formatado."""
    obj = material_obj.instancia_especifica
    itens = []

    campos_ocultar = set()
    if isinstance(obj, Condutor):
        if obj.forma == Condutor.Forma.REDONDO:
            campos_ocultar = {
                "largura_mm", "altura_mm", "largura_isolacao_mm", "altura_isolacao_mm",
                "lado_mm", "lado_isolacao_mm",
            }
        elif obj.forma == Condutor.Forma.QUADRADO:
            campos_ocultar = {
                "largura_mm", "altura_mm", "largura_isolacao_mm", "altura_isolacao_mm",
                "diametro_mm", "diametro_isolacao_mm",
            }
        else:
            campos_ocultar = {
                "diametro_mm", "diametro_isolacao_mm",
                "lado_mm", "lado_isolacao_mm",
            }

    for field in obj._meta.fields:
        if field.name in CAMPOS_BASE_IGNORAR or field.name in campos_ocultar:
            continue

        if field.choices:
            valor = getattr(obj, f"get_{field.name}_display")()
        else:
            valor = getattr(obj, field.name)

        if isinstance(valor, Decimal):
            valor_fmt = _fmt_num(valor)
        elif valor is None or str(valor).strip() == "":
            valor_fmt = "—"
        else:
            valor_fmt = str(valor)

        itens.append({
            "label": str(field.verbose_name),
            "valor": valor_fmt,
        })

    return itens


class MaterialListView(ListView):
    model = Material
    template_name = "materiais/lista.html"
    context_object_name = "materiais"

    def get_queryset(self):
        queryset = (
            Material.objects.select_related(
                "fornecedor",
                "unidade_preco",
                "condutor",
                "isolacao",
                "fita",
                "resinaverniz",
                "cordaopavio",
                "calco",
                "cunha",
                "sensortemperatura",
                "materialauxiliar",
            )
            .all()
            .order_by("-ativo", "tipo_material", "prioridade", "nome")
        )

        tipo = self.request.GET.get("tipo", "").strip()
        if tipo:
            queryset = queryset.filter(tipo_material=tipo)

        fornecedor_id = self.request.GET.get("fornecedor", "").strip()
        if fornecedor_id:
            queryset = queryset.filter(fornecedor_id=fornecedor_id)

        status = self.request.GET.get("status", "").strip()
        if status == "ativos":
            queryset = queryset.filter(ativo=True)
        elif status == "inativos":
            queryset = queryset.filter(ativo=False)

        busca = self.request.GET.get("q", "").strip()
        if busca:
            queryset = queryset.filter(
                Q(codigo_material__icontains=busca)
                | Q(codigo_fornecedor__icontains=busca)
                | Q(nome__icontains=busca)
                | Q(descricao__icontains=busca)
                | Q(fornecedor__nome__icontains=busca)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for item in context["materiais"]:
            item.resumo_tecnico = gerar_resumo_tecnico(item)

        contagens_raw = (
            Material.objects.values("tipo_material")
            .annotate(total=Count("id"))
        )
        mapa_contagens = {row["tipo_material"]: row["total"] for row in contagens_raw}

        tipos_menu = [
            {
                "codigo": codigo,
                "label": label,
                "total": mapa_contagens.get(codigo, 0),
            }
            for codigo, label in Material.TipoMaterial.choices
        ]

        context["tipos_menu"] = tipos_menu
        context["total_geral"] = Material.objects.count()
        context["total_ativos"] = Material.objects.filter(ativo=True).count()
        context["fornecedores"] = Fornecedor.objects.filter(ativo=True).order_by("nome")
        context["tipo_atual"] = self.request.GET.get("tipo", "")
        context["fornecedor_atual"] = self.request.GET.get("fornecedor", "")
        context["status_atual"] = self.request.GET.get("status", "")
        context["busca_atual"] = self.request.GET.get("q", "")
        return context


class MaterialPainelView(View):
    """Renderiza e processa o parcial lateral para visualização e edição de um material."""

    template_name = "materiais/partials/detalhe_material.html"

    def _obter_material_e_form_cls(self, pk):
        base_obj = get_object_or_404(
            Material.objects.select_related("fornecedor", "unidade_preco"),
            pk=pk,
        )
        obj = base_obj.instancia_especifica
        config = CONFIG_TIPOS_MATERIAL.get(
            obj.tipo_material,
            CONFIG_TIPOS_MATERIAL[Material.TipoMaterial.AUXILIAR],
        )
        return obj, config["form"]

    def get(self, request, pk):
        obj, form_cls = self._obter_material_e_form_cls(pk)
        modo = request.GET.get("modo", "visualizar")

        context = {
            "material": obj,
            "modo": modo,
            "tipo_label": obj.get_tipo_material_display(),
        }

        if modo == "editar":
            context["form"] = form_cls(instance=obj)
        else:
            context["especificacoes"] = obter_campos_tecnicos_exibicao(obj)

        return render(request, self.template_name, context)

    def post(self, request, pk):
        obj, form_cls = self._obter_material_e_form_cls(pk)
        form = form_cls(request.POST, instance=obj)

        if form.is_valid():
            obj = form.save()
            response = render(
                request,
                self.template_name,
                {
                    "material": obj,
                    "modo": "visualizar",
                    "tipo_label": obj.get_tipo_material_display(),
                    "especificacoes": obter_campos_tecnicos_exibicao(obj),
                    "salvo_sucesso": "Alterações salvas com sucesso.",
                },
            )
            response["X-Material-Salvo"] = "1"
            return response

        return render(
            request,
            self.template_name,
            {
                "material": obj,
                "modo": "editar",
                "tipo_label": obj.get_tipo_material_display(),
                "form": form,
            },
        )


class MaterialNovoPainelView(View):
    """Renderiza e processa o parcial lateral para cadastro de um novo material."""

    template_name = "materiais/partials/detalhe_material.html"

    def _obter_tipo(self, request):
        tipo = (
            request.POST.get("tipo_material_escolhido")
            or request.GET.get("tipo")
            or Material.TipoMaterial.CONDUTOR
        )
        if tipo not in CONFIG_TIPOS_MATERIAL:
            tipo = Material.TipoMaterial.CONDUTOR
        return tipo

    def _tipos_disponiveis(self):
        return [
            {"codigo": k, "label": v["label"]}
            for k, v in CONFIG_TIPOS_MATERIAL.items()
        ]

    def get(self, request):
        tipo = self._obter_tipo(request)
        config = CONFIG_TIPOS_MATERIAL[tipo]
        return render(
            request,
            self.template_name,
            {
                "material": None,
                "modo": "criar",
                "tipo_selecionado": tipo,
                "tipo_label": config["label"],
                "tipos_disponiveis": self._tipos_disponiveis(),
                "form": config["form"](),
            },
        )

    def post(self, request):
        tipo = self._obter_tipo(request)
        config = CONFIG_TIPOS_MATERIAL[tipo]
        form = config["form"](request.POST)

        if form.is_valid():
            obj = form.save()
            response = render(
                request,
                self.template_name,
                {
                    "material": obj,
                    "modo": "visualizar",
                    "tipo_label": obj.get_tipo_material_display(),
                    "especificacoes": obter_campos_tecnicos_exibicao(obj),
                    "salvo_sucesso": f"Material '{obj.nome}' cadastrado com sucesso.",
                },
            )
            response["X-Material-Salvo"] = "1"
            return response

        return render(
            request,
            self.template_name,
            {
                "material": None,
                "modo": "criar",
                "tipo_selecionado": tipo,
                "tipo_label": config["label"],
                "tipos_disponiveis": self._tipos_disponiveis(),
                "form": form,
            },
        )


class MaterialCreateView(CreateView):
    template_name = "materiais/material_form.html"

    def _obter_tipo_selecionado(self):
        tipo = (
            self.request.POST.get("tipo_material_escolhido")
            or self.request.GET.get("tipo")
            or Material.TipoMaterial.CONDUTOR
        )
        if tipo not in CONFIG_TIPOS_MATERIAL:
            tipo = Material.TipoMaterial.CONDUTOR
        return tipo

    def get_form_class(self):
        tipo = self._obter_tipo_selecionado()
        return CONFIG_TIPOS_MATERIAL[tipo]["form"]

    def get_queryset(self):
        tipo = self._obter_tipo_selecionado()
        return CONFIG_TIPOS_MATERIAL[tipo]["model"].objects.all()

    def get_success_url(self):
        return reverse("materiais:lista_materiais")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Material '{self.object.nome}' cadastrado com sucesso.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo_atual = self._obter_tipo_selecionado()
        context["tipo_selecionado"] = tipo_atual
        context["tipo_label"] = CONFIG_TIPOS_MATERIAL[tipo_atual]["label"]
        context["tipos_disponiveis"] = [
            {"codigo": k, "label": v["label"]}
            for k, v in CONFIG_TIPOS_MATERIAL.items()
        ]
        return context


class MaterialUpdateView(UpdateView):
    template_name = "materiais/material_form.html"

    def get_object(self, queryset=None):
        base_obj = get_object_or_404(Material, pk=self.kwargs["pk"])
        return base_obj.instancia_especifica

    def get_form_class(self):
        tipo = self.object.tipo_material
        config = CONFIG_TIPOS_MATERIAL.get(tipo)
        return config["form"] if config else CONFIG_TIPOS_MATERIAL[Material.TipoMaterial.AUXILIAR]["form"]

    def get_success_url(self):
        return reverse("materiais:material_editar", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Alterações salvas com sucesso.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tipo_selecionado"] = self.object.tipo_material
        context["tipo_label"] = self.object.get_tipo_material_display()
        context["tipos_disponiveis"] = []
        return context


class MaterialDeleteView(DeleteView):
    model = Material
    template_name = "materiais/material_confirm_delete.html"
    success_url = reverse_lazy("materiais:lista_materiais")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        nome = self.object.nome
        try:
            self.object.delete()
            messages.success(request, f"Material '{nome}' removido com sucesso.")
            return HttpResponseRedirect(self.success_url)
        except ProtectedError:
            messages.error(
                request,
                f"Não é possível excluir '{nome}' porque ele está vinculado a uma máquina ou orçamento. "
                "Edite o material e desmarque a opção 'Ativo' para inativá-lo.",
            )
            return HttpResponseRedirect(reverse("materiais:lista_materiais"))


class MaterialBulkDeleteView(View):
    def post(self, request, *args, **kwargs):
        ids_selecionados = request.POST.getlist("material_ids")
        acao = request.POST.get("acao", "excluir")

        if not ids_selecionados:
            return HttpResponseRedirect(reverse("materiais:lista_materiais"))

        qs = Material.objects.filter(id__in=ids_selecionados)

        if acao == "inativar":
            atualizados = qs.update(ativo=False)
            messages.success(request, f"{atualizados} material(is) marcado(s) como inativo(s).")
            return HttpResponseRedirect(reverse("materiais:lista_materiais"))

        excluidos = 0
        bloqueados = 0
        for mat in qs:
            try:
                mat.delete()
                excluidos += 1
            except ProtectedError:
                bloqueados += 1

        if excluidos:
            messages.success(request, f"{excluidos} material(is) excluído(s) com sucesso.")
        if bloqueados:
            messages.warning(
                request,
                f"{bloqueados} material(is) não puderam ser excluídos por possuírem vínculo com máquinas ou orçamentos. "
                "Use a opção 'Inativar Selecionados'.",
            )

        return HttpResponseRedirect(reverse("materiais:lista_materiais"))