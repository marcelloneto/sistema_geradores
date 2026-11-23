from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from materiais.models import (
    Condutor,
    Fita,
    Isolacao,
    Material,
    ResinaVerniz,
    SensorTemperatura,
)
from .models import (
    Cliente,
    DadosConstrutivosBobina,
    DadosEstator,
    DadosGeometricosMaquina,
    DadosPerifericos,
    Fornecedor,
    Maquina,
    MateriaisBobinagemRoebel,
    OrdemServico,
    ResIsolamento,
    UnidadeGeradora,
    UnidadeMedida,
    Usinas,
)


class FornecedorResource(resources.ModelResource):
    class Meta:
        model = Fornecedor
        import_id_fields = ("nome",)
        fields = (
            "nome",
            "identificador",
            "razao_social",
            "cnpj",
            "email",
            "telefone",
            "site",
            "observacoes",
            "ativo",
        )


@admin.register(Fornecedor)
class FornecedorAdmin(ImportExportModelAdmin):
    resource_class = FornecedorResource

    list_display = (
        "id",
        "nome",
        "identificador",
        "razao_social",
        "cnpj",
        "email",
        "telefone",
        "ativo",
        "data_registro",
    )

    list_filter = (
        "ativo",
        "data_registro",
    )

    search_fields = (
        "nome",
        "razao_social",
        "cnpj",
        "email",
        "telefone",
    )

    readonly_fields = (
        "data_registro",
        "data_atualizacao",
    )

    fieldsets = (
        ("Identificação", {
            "fields": (
                "nome",
                "identificador",
                "razao_social",
                "cnpj",
                "ativo",
            )
        }),
        ("Contato", {
            "fields": (
                "email",
                "telefone",
                "site",
            )
        }),
        ("Observações", {
            "fields": (
                "observacoes",
            )
        }),
        ("Controle", {
            "fields": (
                "data_registro",
                "data_atualizacao",
            )
        }),
    )


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "localizacao", "contato_1", "data_registro")
    search_fields = ("nome", "localizacao")


class UnidadeGeradoraInline(admin.TabularInline):
    model = UnidadeGeradora
    extra = 1
    fields = (
        "nome",
        "potencia_kva",
        "tensao_kv",
        "fabricante",
        "tipo_turbina",
        "ano_operacao",
        "status",
    )


@admin.register(Usinas)
class UsinasAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome",
        "tipo",
        "estado",
        "localizacao",
        "operadora",
        "n_maquinas",
        "potencia_total",
        "data_registro",
    )
    list_filter = ("tipo", "estado", "operadora")
    search_fields = ("nome", "codigo_ceg", "localizacao", "estado", "operadora__nome")
    readonly_fields = ("data_registro",)
    inlines = [UnidadeGeradoraInline]

    fieldsets = (
        ("Identificação", {
            "fields": (
                ("nome", "tipo"),
                ("codigo_ceg", "operadora"),
                ("localizacao", "estado"),
            )
        }),
        ("Dados Técnicos Gerais", {
            "fields": (
                ("n_maquinas", "potencia_total"),
                "capacidade_ponte_rolante_t",
            )
        }),
        ("Observações e Controle", {
            "fields": (
                "observacoes",
                "data_registro",
            )
        }),
    )


@admin.register(UnidadeGeradora)
class UnidadeGeradoraAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usina",
        "nome",
        "potencia_kva",
        "tensao_kv",
        "fabricante",
        "tipo_turbina",
        "ano_operacao",
        "status",
    )
    list_filter = ("status", "tipo_turbina", "fabricante", "usina")
    search_fields = ("nome", "usina__nome", "fabricante")
    ordering = ("usina__nome", "nome")


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ("numero", "cliente", "maquina", "tipo_servico", "localizacao", "data_registro")
    list_filter = ("cliente", "maquina", "tipo_servico")
    search_fields = ("numero", "cliente__nome", "maquina__numero_serie")


@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "numero_serie",
        "usina",
        "unidade_geradora",
        "cliente",
        "tipo",
        "potencia_kva",
        "tensao_v",
        "corrente_a",
        "numero_polos",
        "frequencia_hz",
    )

    list_filter = (
        "tipo",
        "usina",
        "cliente",
        "frequencia_hz",
        "numero_polos",
    )

    search_fields = (
        "numero_serie",
        "unidade_geradora__nome",
        "usina__nome",
        "cliente__nome",
        "excitatriz",
    )

    fieldsets = (
        ("Identificação", {
            "fields": (
                "numero_serie",
                "usina",
                "unidade_geradora",
                "cliente",
                "tipo",
            )
        }),
        ("Dados elétricos principais", {
            "fields": (
                "potencia_kva",
                "tensao_v",
                "corrente_a",
                "fator_potencia",
            )
        }),
        ("Dados mecânicos", {
            "fields": (
                "rotacao_rpm",
                "numero_polos",
                "frequencia_hz",
            )
        }),
        ("Excitatriz", {
            "fields": (
                "excitatriz",
                "tensao_excitatriz_v",
                "corrente_excitatriz_a",
            )
        }),
    )


@admin.register(UnidadeMedida)
class UnidadeMedidaAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "nome",
        "simbolo",
        "fator_base",
        "ativa",
    )

    list_filter = (
        "ativa",
    )

    search_fields = (
        "nome",
        "simbolo",
    )

    ordering = (
        "simbolo",
    )


class DadosEstatorResource(resources.ModelResource):
    maquina = fields.Field(
        column_name="maquina",
        attribute="maquina",
        widget=ForeignKeyWidget(Maquina, "numero_serie")
    )

    class Meta:
        model = DadosEstator
        import_id_fields = ("maquina",)
        fields = (
            "maquina",
            "numero_bobinas",
            "numero_condutores_por_espira",
            "cor_estator",
            "numero_espiras_por_bobina",
            "numero_series",
            "tipo_condutor",
            "numero_elementos",
            "numero_saidas",
            "numero_paralelos",
            "tipo_ligacao",
            "numero_sensores",
            "tipo_cunha",
            "passo",
            "tipo_sensor",
            "local_sensor",
            "peso_cobre_total",
            "peso_bobina",
            "area_espira",
            "comprimento_nucleo_magnetico",
            "numero_canais_ventilacao",
            "diametro_interno_nucleo",
            "diametro_externo_nucleo",
            "diametro_rotor",
            "entreferro_gerador",
        )


@admin.register(DadosEstator)
class DadosEstatorAdmin(ImportExportModelAdmin):
    resource_class = DadosEstatorResource
    list_display = (
        "id",
        "maquina",
        "tipo_bobina",
        "tipo_bobinado",
        "numero_bobinas",
        "tipo_ligacao",
        "tipo_condutor",
    )

    fieldsets = (
        ("Bobinagem / Enrolamento", {
            "fields": (
                "tipo_bobina",
                "tipo_bobinado",
                "numero_bobinas",
                "numero_condutores_por_espira",
                "numero_espiras_por_bobina",
                "numero_elementos",
                "passo",
                "tipo_condutor",
            )
        }),
        ("Configuração elétrica", {
            "fields": (
                "tipo_ligacao",
                "numero_series",
                "numero_saidas",
                "numero_paralelos",
            )
        }),
        ("Sensores", {
            "fields": (
                "numero_sensores",
                "tipo_sensor",
                "local_sensor",
            )
        }),
        ("Núcleo magnético", {
            "fields": (
                "comprimento_nucleo_magnetico",
                "numero_canais_ventilacao",
                "diametro_interno_nucleo",
                "diametro_externo_nucleo",
                "diametro_rotor",
                "entreferro_gerador",
            )
        }),
        ("Pesos, áreas e acabamento", {
            "fields": (
                "peso_cobre_total",
                "peso_bobina",
                "area_espira",
                "cor_estator",
                "tipo_cunha",
            )
        }),
    )


class DadosPerifericosResource(resources.ModelResource):
    maquina = fields.Field(
        column_name="maquina",
        attribute="maquina",
        widget=ForeignKeyWidget(Maquina, "numero_serie")
    )

    class Meta:
        model = DadosPerifericos
        import_id_fields = ("maquina",)
        fields = (
            "maquina",
            "aro_amarracao_ll",
            "aro_amarracao_lol",
            "material_aro_ll",
            "material_aro_lol",
            "calco_amarracao_inferior_ll",
            "obs_calco_amarracao_inferior_ll",
            "calco_amarracao_inferior_lol",
            "obs_calco_amarracao_inferior_lol",
            "calco_amarracao_superior_ll",
            "obs_calco_amarracao_superior_ll",
            "calco_amarracao_superior_lol",
            "obs_calco_amarracao_superior_lol",
            "material_calcos",
            "campo_eletrico",
            "densidade_corrente",
            "classe_termica_cabo",
            "tensao_cabo",
            "comprimento_cabo_interno",
            "comprimento_cabo_externo",
            "descricao_terminal",
        )


@admin.register(DadosPerifericos)
class DadosPerifericosAdmin(ImportExportModelAdmin):
    resource_class = DadosPerifericosResource

    list_display = (
        "id",
        "maquina",
        "material_aro_ll",
        "material_aro_lol",
        "material_calcos",
        "tensao_cabo",
    )

    search_fields = (
        "maquina__numero_serie",
        "material_aro_ll",
        "material_aro_lol",
        "material_calcos",
        "descricao_terminal",
    )

    fieldsets = (
        ("Máquina", {
            "fields": ("maquina",)
        }),
        ("Aro de amarração", {
            "fields": (
                ("aro_amarracao_ll", "aro_amarracao_lol"),
                ("material_aro_ll", "material_aro_lol"),
            )
        }),
        ("Calços de amarração por bobina", {
            "fields": (
                ("calco_amarracao_inferior_ll", "obs_calco_amarracao_inferior_ll", "calco_amarracao_inferior_lol", "obs_calco_amarracao_inferior_lol"),
                ("calco_amarracao_superior_ll", "obs_calco_amarracao_superior_ll", "calco_amarracao_superior_lol", "obs_calco_amarracao_superior_lol"),
                "material_calcos",
            )
        }),
        ("Cabo", {
            "fields": (
                "campo_eletrico",
                "densidade_corrente",
                "classe_termica_cabo",
                "tensao_cabo",
                "comprimento_cabo_interno",
                "comprimento_cabo_externo",
            )
        }),
        ("Terminal", {
            "fields": (
                "descricao_terminal",
            )
        }),
    )


class DadosGeometricosMaquinaResource(resources.ModelResource):
    maquina = fields.Field(
        column_name="maquina",
        attribute="maquina",
        widget=ForeignKeyWidget(Maquina, "numero_serie")
    )

    class Meta:
        model = DadosGeometricosMaquina
        import_id_fields = ("maquina",)
        fields = (
            "maquina",
            "tipo_ranhura",
            "ranhura_a",
            "ranhura_b",
            "ranhura_c",
            "ranhura_d",
            "ranhura_e",
            "ranhura_f",
            "folga_ranhura",
            "bobina_e",
            "bobina_f",
            "bobina_g",
            "bobina_h",
            "sobreposicao_isolante",
            "condutor_e",
            "condutor_f",
            "condutor_E_iso",
            "condutor_F_iso",
            "tipo_calco",
            "calco_a",
            "calco_b",
            "calco_c",
            "calco_d",
        )


@admin.register(DadosGeometricosMaquina)
class DadosGeometricosMaquinaAdmin(ImportExportModelAdmin):
    resource_class = DadosGeometricosMaquinaResource

    list_display = (
        "id",
        "maquina",
        "tipo_ranhura",
        "tipo_calco",
    )

    search_fields = (
        "maquina__numero_serie",
        "tipo_ranhura",
        "tipo_calco",
    )

    fieldsets = (
        ("Máquina", {
            "fields": ("maquina",)
        }),
        ("Ranhura", {
            "fields": (
                "tipo_ranhura",
                ("ranhura_a", "ranhura_b", "ranhura_c"),
                ("ranhura_d", "ranhura_e", "ranhura_f"),
                "folga_ranhura",
            )
        }),
        ("Seção da Bobina", {
            "fields": (
                ("bobina_e", "bobina_f"),
                ("bobina_g", "bobina_h"),
                "sobreposicao_isolante",
            )
        }),
        ("Seção do Condutor", {
            "fields": (
                ("condutor_e", "condutor_f"),
                ("condutor_E_iso", "condutor_F_iso"),
            )
        }),
        ("Seção do Calço", {
            "fields": (
                "tipo_calco",
                ("calco_a", "calco_b"),
                ("calco_c", "calco_d"),
            )
        }),
    )


class DadosConstrutivosBobinaResource(resources.ModelResource):
    maquina = fields.Field(
        column_name="maquina",
        attribute="maquina",
        widget=ForeignKeyWidget(Maquina, "numero_serie")
    )

    class Meta:
        model = DadosConstrutivosBobina
        import_id_fields = ("maquina",)
        fields = (
            "maquina",
            "croqui_g",
            "croqui_h",
            "croqui_i",
            "croqui_j",
            "croqui_k",
            "croqui_l",
            "amarracao_a1",
            "amarracao_a2",
            "amarracao_b1",
            "amarracao_b2",
            "amarracao_c1",
            "amarracao_c2",
            "amarracao_d1",
            "amarracao_d2",
            "configuracao_a1",
            "configuracao_a2",
            "configuracao_b1",
            "configuracao_b2",
            "configuracao_c1",
            "configuracao_c2",
            "configuracao_d1",
            "configuracao_d2",
            "montada_a",
            "montada_b",
            "montada_c",
            "montada_d",
            "montada_e1",
            "montada_e2",
            "montada_f",
            "montada_f_sem_isolacao",
        )


@admin.register(DadosConstrutivosBobina)
class DadosConstrutivosBobinaAdmin(ImportExportModelAdmin):
    resource_class = DadosConstrutivosBobinaResource

    list_display = (
        "id",
        "maquina",
        "croqui_g",
        "croqui_h",
        "montada_f",
    )

    search_fields = (
        "maquina__numero_serie",
    )

    fieldsets = (
        ("Máquina", {
            "fields": ("maquina",)
        }),
        ("Croqui das Bobinas", {
            "fields": (
                ("croqui_g", "croqui_h"),
                ("croqui_i", "croqui_j"),
                ("croqui_k", "croqui_l"),
            )
        }),
        ("Amarração das Bobinas", {
            "fields": (
                ("amarracao_a1", "amarracao_a2"),
                ("amarracao_b1", "amarracao_b2"),
                ("amarracao_c1", "amarracao_c2"),
                ("amarracao_d1", "amarracao_d2"),
            )
        }),
        ("Configuração das Bobinas", {
            "fields": (
                ("configuracao_a1", "configuracao_a2"),
                ("configuracao_b1", "configuracao_b2"),
                ("configuracao_c1", "configuracao_c2"),
                ("configuracao_d1", "configuracao_d2"),
            )
        }),
        ("Bobina Montada", {
            "fields": (
                ("montada_a", "montada_b"),
                ("montada_c", "montada_d"),
                ("montada_e1", "montada_e2"),
                ("montada_f", "montada_f_sem_isolacao"),
            )
        }),
    )


class MateriaisBobinagemRoebelResource(resources.ModelResource):
    maquina = fields.Field(
        column_name="maquina",
        attribute="maquina",
        widget=ForeignKeyWidget(Maquina, "numero_serie")
    )

    MODELS_POR_CAMPO = {
        "condutor": Condutor,
        "isolacao_panqueca": Isolacao,
        "consolidacao_condutores": ResinaVerniz,
        "massa_enchimento": ResinaVerniz,
        "isolacao_condutores": Isolacao,
        "isolacao_principal": Isolacao,
        "fita_sacrificio": Fita,
        "verniz_condutivo": ResinaVerniz,
        "fita_condutiva": Fita,
        "verniz_semicondutivo": ResinaVerniz,
        "fita_semicondutiva": Fita,
        "cadarco_fibra_vidro": Fita,
        "fita_acabamento": Fita,
        "calcos_radiais": Material,
        "calcos_tangenciais": Material,
        "conexoes": Material,
        "barramentos_ligacao": Material,
        "pavio_central": Material,
        "cunhagem": Material,
        "sensor": SensorTemperatura,
        "aros_amarracao": Material,
    }

    for campo, model_cls in MODELS_POR_CAMPO.items():
        locals()[campo] = fields.Field(
            column_name=campo,
            attribute=campo,
            widget=ForeignKeyWidget(model_cls, "codigo_material")
        )

    class Meta:
        model = MateriaisBobinagemRoebel
        import_id_fields = ("maquina",)
        fields = (
            "maquina",
            "condutor",
            "isolacao_panqueca",
            "consolidacao_condutores",
            "massa_enchimento",
            "isolacao_condutores",
            "isolacao_principal",
            "fita_sacrificio",
            "verniz_condutivo",
            "fita_condutiva",
            "verniz_semicondutivo",
            "fita_semicondutiva",
            "cadarco_fibra_vidro",
            "fita_acabamento",
            "calcos_radiais",
            "calcos_tangenciais",
            "conexoes",
            "barramentos_ligacao",
            "pavio_central",
            "cunhagem",
            "sensor",
            "aros_amarracao",
            "sobressalente_bobinas",
            "coeficiente_seguranca_bobinas",
        )


@admin.register(MateriaisBobinagemRoebel)
class MateriaisBobinagemRoebelAdmin(ImportExportModelAdmin):
    resource_class = MateriaisBobinagemRoebelResource

    list_display = (
        "id",
        "maquina",
        "condutor",
        "isolacao_principal",
        "verniz_condutivo",
        "fita_condutiva",
    )

    search_fields = (
        "maquina__numero_serie",
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in MateriaisBobinagemRoebelResource.MODELS_POR_CAMPO:
            kwargs["queryset"] = db_field.related_model.objects.filter(
                ativo=True
            ).order_by("prioridade", "codigo_material")

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fieldsets = (
        ("Máquina", {
            "fields": ("maquina",)
        }),
        ("Condutor e isolamento", {
            "fields": (
                "condutor",
                "isolacao_panqueca",
                "isolacao_condutores",
                "isolacao_principal",
            )
        }),
        ("Consolidação e enchimento", {
            "fields": (
                "consolidacao_condutores",
                "massa_enchimento",
            )
        }),
        ("Sistema condutivo", {
            "fields": (
                "verniz_condutivo",
                "fita_condutiva",
            )
        }),
        ("Sistema semicondutivo", {
            "fields": (
                "verniz_semicondutivo",
                "fita_semicondutiva",
            )
        }),
        ("Acabamento e amarração", {
            "fields": (
                "fita_sacrificio",
                "cadarco_fibra_vidro",
                "fita_acabamento",
                "pavio_central",
                "aros_amarracao",
            )
        }),
        ("Componentes mecânicos/elétricos", {
            "fields": (
                "calcos_radiais",
                "calcos_tangenciais",
                "conexoes",
                "barramentos_ligacao",
                "cunhagem",
                "sensor",
            )
        }),
        ("Parâmetros de cálculo", {
            "fields": (
                "sobressalente_bobinas",
                "coeficiente_seguranca_bobinas",
            )
        }),
    )


@admin.register(ResIsolamento)
class ResIsolamentoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "maquina",
        "tensao",
        "temperatura",
        "umidade",
        "tempo",
        "res_ohmica_t",
    )

    search_fields = (
        "maquina__numero_serie",
    )

    fieldsets = (
        ("Máquina", {
            "fields": (
                "maquina",
            )
        }),
        ("Condições do ensaio", {
            "fields": (
                "tensao",
                "temperatura",
                "umidade",
                "tempo",
            )
        }),
        ("Medições fase x massa", {
            "fields": (
                "Ø01xm",
                "Ø02xm",
                "Ø03xm",
                "Ø04xm",
            )
        }),
        ("Resistência ôhmica", {
            "fields": (
                "res_ohmica_t",
                "Ø01",
                "Ø02",
                "Ø03",
            )
        }),
    )