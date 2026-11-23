from django import forms
from cadastros.models import UnidadeGeradora, Usinas


class BootstrapFormMixin:
    def _aplicar_estilo_bootstrap(self):
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.Select):
                widget.attrs["class"] = "form-select form-select-sm"
            elif isinstance(widget, forms.Textarea):
                widget.attrs["class"] = "form-control form-control-sm"
                widget.attrs.setdefault("rows", 2)
            else:
                widget.attrs["class"] = "form-control form-control-sm"


class UsinaForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Usinas
        fields = [
            "nome",
            "codigo_ceg",
            "tipo",
            "operadora",
            "localizacao",
            "estado",
            "n_maquinas",
            "potencia_total",
            "capacidade_ponte_rolante_t",
            "observacoes",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._aplicar_estilo_bootstrap()
        if "estado" in self.fields:
            self.fields["estado"].widget.attrs["maxlength"] = 2
            self.fields["estado"].widget.attrs["placeholder"] = "Ex.: PR"

    def clean_estado(self):
        estado = self.cleaned_data.get("estado", "")
        return estado.strip().upper()


class UnidadeGeradoraForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = UnidadeGeradora
        fields = [
            "nome",
            "potencia_kva",
            "tensao_kv",
            "fabricante",
            "tipo_turbina",
            "ano_operacao",
            "status",
            "observacoes",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._aplicar_estilo_bootstrap()