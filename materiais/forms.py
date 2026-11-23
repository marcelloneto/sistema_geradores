from django import forms
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

CAMPOS_IDENTIFICACAO = ["codigo_material", "nome", "descricao"]
CAMPOS_COMERCIAIS = [
    "fornecedor",
    "codigo_fornecedor",
    "preco",
    "unidade_preco",
    "data_atualizacao_preco",
    "prioridade",
    "ativo",
]


class BaseMaterialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = "form-check-input"
            elif isinstance(widget, forms.Select):
                widget.attrs["class"] = "form-select"
            elif isinstance(widget, forms.Textarea):
                widget.attrs["class"] = "form-control"
                widget.attrs.setdefault("rows", 2)
            else:
                widget.attrs["class"] = "form-control"
                if isinstance(widget, forms.DateInput):
                    widget.input_type = "date"

    def campos_identificacao(self):
        return [self[name] for name in CAMPOS_IDENTIFICACAO if name in self.fields]

    def campos_tecnicos(self):
        excluir = set(CAMPOS_IDENTIFICACAO + CAMPOS_COMERCIAIS)
        return [self[name] for name in self.fields if name not in excluir]

    def campos_comerciais(self):
        return [self[name] for name in CAMPOS_COMERCIAIS if name in self.fields]


class CondutorForm(BaseMaterialForm):
    class Meta:
        model = Condutor
        fields = CAMPOS_IDENTIFICACAO + [
            "forma",
            "tipo_isolacao",
            "classe_termica",
            "largura_mm",
            "altura_mm",
            "lado_mm",
            "diametro_mm",
            "largura_isolacao_mm",
            "altura_isolacao_mm",
            "lado_isolacao_mm",
            "diametro_isolacao_mm",
            "densidade_kg_m3",
        ] + CAMPOS_COMERCIAIS


class IsolacaoForm(BaseMaterialForm):
    class Meta:
        model = Isolacao
        fields = CAMPOS_IDENTIFICACAO + [
            "aplicacao",
            "substrato",
            "classe_termica",
            "espessura_mm",
            "largura_mm",
            "comprimento_rolo_m",
            "tensao_maxima_kv",
        ] + CAMPOS_COMERCIAIS


class FitaForm(BaseMaterialForm):
    class Meta:
        model = Fita
        fields = CAMPOS_IDENTIFICACAO + [
            "finalidade",
            "material_base",
            "classe_termica",
            "espessura_mm",
            "largura_mm",
            "comprimento_rolo_m",
        ] + CAMPOS_COMERCIAIS


class ResinaVernizForm(BaseMaterialForm):
    class Meta:
        model = ResinaVerniz
        fields = CAMPOS_IDENTIFICACAO + [
            "categoria_quimica",
            "finalidade",
            "classe_termica",
            "rendimento_kg_m",
            "rendimento_kg_m2",
            "densidade_kg_m3",
            "proporcao_mistura",
            "temperatura_cura_c",
        ] + CAMPOS_COMERCIAIS


class CordaoPavioForm(BaseMaterialForm):
    class Meta:
        model = CordaoPavio
        fields = CAMPOS_IDENTIFICACAO + [
            "tipo",
            "material_base",
            "diametro_mm",
            "comprimento_rolo_m",
        ] + CAMPOS_COMERCIAIS


class CalcoForm(BaseMaterialForm):
    class Meta:
        model = Calco
        fields = CAMPOS_IDENTIFICACAO + [
            "tipo_calco",
            "material_base",
            "espessura_mm",
            "largura_mm",
            "comprimento_mm",
        ] + CAMPOS_COMERCIAIS


class CunhaForm(BaseMaterialForm):
    class Meta:
        model = Cunha
        fields = CAMPOS_IDENTIFICACAO + [
            "tipo_cunha",
            "material_base",
            "desenho_referencia",
            "espessura_mm",
            "largura_mm",
            "comprimento_mm",
        ] + CAMPOS_COMERCIAIS


class SensorTemperaturaForm(BaseMaterialForm):
    class Meta:
        model = SensorTemperatura
        fields = CAMPOS_IDENTIFICACAO + [
            "tipo_sensor",
            "numero_fios",
            "espessura_mm",
            "largura_mm",
            "comprimento_mm",
            "comprimento_cabo_m",
        ] + CAMPOS_COMERCIAIS


class MaterialAuxiliarForm(BaseMaterialForm):
    class Meta:
        model = MaterialAuxiliar
        fields = CAMPOS_IDENTIFICACAO + [
            "subtipo",
            "especificacao_dimensional",
        ] + CAMPOS_COMERCIAIS


CONFIG_TIPOS_MATERIAL = {
    Material.TipoMaterial.CONDUTOR: {
        "model": Condutor,
        "form": CondutorForm,
        "label": "Condutor",
    },
    Material.TipoMaterial.ISOLACAO: {
        "model": Isolacao,
        "form": IsolacaoForm,
        "label": "Isolação",
    },
    Material.TipoMaterial.FITA: {
        "model": Fita,
        "form": FitaForm,
        "label": "Fita / Cadarço",
    },
    Material.TipoMaterial.RESINA_VERNIZ: {
        "model": ResinaVerniz,
        "form": ResinaVernizForm,
        "label": "Resina / Verniz / Massa",
    },
    Material.TipoMaterial.CORDAO_PAVIO: {
        "model": CordaoPavio,
        "form": CordaoPavioForm,
        "label": "Pavio / Camisa / Aro",
    },
    Material.TipoMaterial.CALCO: {
        "model": Calco,
        "form": CalcoForm,
        "label": "Calço",
    },
    Material.TipoMaterial.CUNHA: {
        "model": Cunha,
        "form": CunhaForm,
        "label": "Cunha",
    },
    Material.TipoMaterial.SENSOR: {
        "model": SensorTemperatura,
        "form": SensorTemperaturaForm,
        "label": "Sensor de Temperatura",
    },
    Material.TipoMaterial.AUXILIAR: {
        "model": MaterialAuxiliar,
        "form": MaterialAuxiliarForm,
        "label": "Material Auxiliar / Conexão",
    },
}