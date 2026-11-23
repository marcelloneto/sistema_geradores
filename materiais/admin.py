from django.contrib import admin
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


class BaseMaterialAdmin(admin.ModelAdmin):
    list_filter = ("ativo", "fornecedor")
    search_fields = ("codigo_material", "codigo_fornecedor", "nome", "descricao", "fornecedor__nome")
    list_editable = ("prioridade", "ativo")
    readonly_fields = ("tipo_material", "data_registro", "data_atualizacao")
    ordering = ("prioridade", "nome")

    fieldsets_comerciais = (
        "Dados Comerciais e Fornecedor",
        {
            "fields": (
                ("fornecedor", "codigo_fornecedor"),
                ("preco", "unidade_preco", "data_atualizacao_preco"),
                ("prioridade", "ativo"),
            )
        },
    )

    fieldsets_auditoria = (
        "Controle do Sistema",
        {
            "classes": ("collapse",),
            "fields": (("tipo_material", "data_registro", "data_atualizacao"),),
        },
    )


@admin.register(Material)
class MaterialGeralAdmin(admin.ModelAdmin):
    list_display = (
        "codigo_material",
        "nome",
        "tipo_material",
        "fornecedor",
        "preco",
        "unidade_preco",
        "prioridade",
        "ativo",
    )
    list_filter = ("tipo_material", "ativo", "fornecedor")
    search_fields = ("codigo_material", "codigo_fornecedor", "nome", "descricao")
    list_editable = ("prioridade", "ativo")
    readonly_fields = ("tipo_material", "data_registro", "data_atualizacao")


@admin.register(Condutor)
class CondutorAdmin(BaseMaterialAdmin):
    list_display = (
        "codigo_material",
        "nome",
        "forma",
        "largura_mm",
        "altura_mm",
        "largura_isolacao_mm",
        "altura_isolacao_mm",
        "tipo_isolacao",
        "fornecedor",
        "prioridade",
        "ativo",
    )
    list_filter = ("forma", "classe_termica", "ativo", "fornecedor")
    fieldsets = (
        ("Identificação", {"fields": (("codigo_material", "nome"), "descricao")}),
        (
            "Dimensões e Propriedades do Condutor",
            {
                "fields": (
                    ("forma", "tipo_isolacao", "classe_termica"),
                    ("largura_mm", "altura_mm", "diametro_mm"),
                    ("largura_isolacao_mm", "altura_isolacao_mm", "diametro_isolacao_mm"),
                    "densidade_kg_m3",
                )
            },
        ),
        BaseMaterialAdmin.fieldsets_comerciais,
        BaseMaterialAdmin.fieldsets_auditoria,
    )


@admin.register(Isolacao)
class IsolacaoAdmin(BaseMaterialAdmin):
    list_display = (
        "codigo_material",
        "nome",
        "aplicacao",
        "substrato",
        "espessura_mm",
        "largura_mm",
        "comprimento_rolo_m",
        "fornecedor",
        "prioridade",
        "ativo",
    )
    list_filter = ("aplicacao", "substrato", "classe_termica", "ativo", "fornecedor")
    fieldsets = (
        ("Identificação", {"fields": (("codigo_material", "nome"), "descricao")}),
        (
            "Especificações da Isolação",
            {
                "fields": (
                    ("aplicacao", "substrato", "classe_termica"),
                    ("espessura_mm", "largura_mm", "comprimento_rolo_m"),
                    "tensao_maxima_kv",
                )
            },
        ),
        BaseMaterialAdmin.fieldsets_comerciais,
        BaseMaterialAdmin.fieldsets_auditoria,
    )


@admin.register(Fita)
class FitaAdmin(BaseMaterialAdmin):
    list_display = (
        "codigo_material",
        "nome",
        "finalidade",
        "espessura_mm",
        "largura_mm",
        "comprimento_rolo_m",
        "fornecedor",
        "prioridade",
        "ativo",
    )
    list_filter = ("finalidade", "classe_termica", "ativo", "fornecedor")
    fieldsets = (
        ("Identificação", {"fields": (("codigo_material", "nome"), "descricao")}),
        (
            "Especificações da Fita / Cadarço",
            {
                "fields": (
                    ("finalidade", "material_base", "classe_termica"),
                    ("espessura_mm", "largura_mm", "comprimento_rolo_m"),
                )
            },
        ),
        BaseMaterialAdmin.fieldsets_comerciais,
        BaseMaterialAdmin.fieldsets_auditoria,
    )


@admin.register(ResinaVerniz)
class ResinaVernizAdmin(BaseMaterialAdmin):
    list_display = (
        "codigo_material",
        "nome",
        "categoria_quimica",
        "finalidade",
        "rendimento_kg_m",
        "densidade_kg_m3",
        "fornecedor",
        "prioridade",
        "ativo",
    )
    list_filter = ("categoria_quimica", "finalidade", "classe_termica", "ativo", "fornecedor")
    fieldsets = (
        ("Identificação", {"fields": (("codigo_material", "nome"), "descricao")}),
        (
            "Propriedades Químicas e Aplicação",
            {
                "fields": (
                    ("categoria_quimica", "finalidade", "classe_termica"),
                    ("rendimento_kg_m", "rendimento_kg_m2", "densidade_kg_m3"),
                    ("proporcao_mistura", "temperatura_cura_c"),
                )
            },
        ),
        BaseMaterialAdmin.fieldsets_comerciais,
        BaseMaterialAdmin.fieldsets_auditoria,
    )


@admin.register(CordaoPavio)
class CordaoPavioAdmin(BaseMaterialAdmin):
    list_display = (
        "codigo_material",
        "nome",
        "tipo",
        "material_base",
        "diametro_mm",
        "comprimento_rolo_m",
        "fornecedor",
        "prioridade",
        "ativo",
    )
    list_filter = ("tipo", "ativo", "fornecedor")
    fieldsets = (
        ("Identificação", {"fields": (("codigo_material", "nome"), "descricao")}),
        (
            "Especificações",
            {"fields": (("tipo", "material_base"), ("diametro_mm", "comprimento_rolo_m"))},
        ),
        BaseMaterialAdmin.fieldsets_comerciais,
        BaseMaterialAdmin.fieldsets_auditoria,
    )


@admin.register(Calco)
class CalcoAdmin(BaseMaterialAdmin):
    list_display = (
        "codigo_material",
        "nome",
        "tipo_calco",
        "material_base",
        "espessura_mm",
        "largura_mm",
        "comprimento_mm",
        "fornecedor",
        "prioridade",
        "ativo",
    )
    list_filter = ("tipo_calco", "ativo", "fornecedor")
    fieldsets = (
        ("Identificação", {"fields": (("codigo_material", "nome"), "descricao")}),
        (
            "Especificações do Calço",
            {
                "fields": (
                    ("tipo_calco", "material_base"),
                    ("espessura_mm", "largura_mm", "comprimento_mm"),
                )
            },
        ),
        BaseMaterialAdmin.fieldsets_comerciais,
        BaseMaterialAdmin.fieldsets_auditoria,
    )


@admin.register(Cunha)
class CunhaAdmin(BaseMaterialAdmin):
    list_display = (
        "codigo_material",
        "nome",
        "tipo_cunha",
        "desenho_referencia",
        "espessura_mm",
        "largura_mm",
        "comprimento_mm",
        "fornecedor",
        "prioridade",
        "ativo",
    )
    list_filter = ("tipo_cunha", "ativo", "fornecedor")
    fieldsets = (
        ("Identificação", {"fields": (("codigo_material", "nome"), "descricao")}),
        (
            "Especificações da Cunha",
            {
                "fields": (
                    ("tipo_cunha", "material_base", "desenho_referencia"),
                    ("espessura_mm", "largura_mm", "comprimento_mm"),
                )
            },
        ),
        BaseMaterialAdmin.fieldsets_comerciais,
        BaseMaterialAdmin.fieldsets_auditoria,
    )


@admin.register(SensorTemperatura)
class SensorTemperaturaAdmin(BaseMaterialAdmin):
    list_display = (
        "codigo_material",
        "nome",
        "tipo_sensor",
        "numero_fios",
        "espessura_mm",
        "largura_mm",
        "comprimento_mm",
        "fornecedor",
        "prioridade",
        "ativo",
    )
    list_filter = ("tipo_sensor", "numero_fios", "ativo", "fornecedor")
    fieldsets = (
        ("Identificação", {"fields": (("codigo_material", "nome"), "descricao")}),
        (
            "Especificações do Sensor",
            {
                "fields": (
                    ("tipo_sensor", "numero_fios"),
                    ("espessura_mm", "largura_mm", "comprimento_mm", "comprimento_cabo_m"),
                )
            },
        ),
        BaseMaterialAdmin.fieldsets_comerciais,
        BaseMaterialAdmin.fieldsets_auditoria,
    )


@admin.register(MaterialAuxiliar)
class MaterialAuxiliarAdmin(BaseMaterialAdmin):
    list_display = (
        "codigo_material",
        "nome",
        "subtipo",
        "especificacao_dimensional",
        "fornecedor",
        "prioridade",
        "ativo",
    )
    list_filter = ("subtipo", "ativo", "fornecedor")
    fieldsets = (
        ("Identificação", {"fields": (("codigo_material", "nome"), "descricao")}),
        ("Classificação", {"fields": (("subtipo", "especificacao_dimensional"),)}),
        BaseMaterialAdmin.fieldsets_comerciais,
        BaseMaterialAdmin.fieldsets_auditoria,
    )