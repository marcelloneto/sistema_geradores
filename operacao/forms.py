from django import forms
from cadastros.models import DadosEstator,DadosGeometricosMaquina, DadosPerifericos, Maquina, DadosConstrutivosBobina


class DadosEstatorForm(forms.ModelForm):

    BOBINADO = [
        "tipo_bobina",
        "tipo_bobinado",
        "cor_estator",
        "numero_bobinas",
        "numero_condutores_por_espira",
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
    ]

    NUCLEO = [
        "comprimento_nucleo_magnetico",
        "numero_canais_ventilacao",
        "diametro_interno_nucleo",
        "diametro_externo_nucleo",
        "diametro_rotor",
        "entreferro_gerador",
    ]

    class Meta:
        model = DadosEstator
        exclude = ["maquina"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({
                "class": "form-control"
            })

            if isinstance(field, forms.DecimalField):
                field.widget.attrs.update({
                    "step": "0.01"
                })

            elif isinstance(field, forms.IntegerField):
                field.widget.attrs.update({
                    "step": "1",
                    "min": "0"
                })

    def obter_grupo(self, grupo):
        return [
            self[campo]
            for campo in grupo
        ]

    def obter_bobinado(self):
        
        return self.obter_grupo(self.BOBINADO)

    def obter_nucleo(self):

        return self.obter_grupo(self.NUCLEO)


class DadosGeometricosForm(forms.ModelForm):

    RANHURA = [
        
        "ranhura_a",
        "ranhura_b",
        "ranhura_c",
        "ranhura_d",
        "ranhura_e",
        "ranhura_f",
    ]

    BOBINA = [
        "bobina_e",
        "bobina_f",
        "bobina_g",
        "bobina_h",
    ]

    CONDUTOR = [
        "condutor_e",
        "condutor_f",
        "condutor_E_iso",
        "condutor_F_iso",
    ]

    CALCO = [
        
        "calco_a",
        "calco_b",
        "calco_c",
        "calco_d",
    ]

    LABELS = {

        # Ranhura
        "ranhura_a": "a",
        "ranhura_b": "b",
        "ranhura_c": "c",
        "ranhura_d": "d",
        "ranhura_e": "e",
        "ranhura_f": "f",

        # Bobina
        "bobina_e": "e",
        "bobina_f": "f",
        "bobina_g": "g",
        "bobina_h": "h",

        # Condutor
        "condutor_e": "e",
        "condutor_f": "f",
        "condutor_E_iso": "E",
        "condutor_F_iso": "F",

        # Calço
        "calco_a": "a",
        "calco_b": "b",
        "calco_c": "c",
        "calco_d": "d",
    }

    class Meta:
        model = DadosGeometricosMaquina
        exclude = ["maquina"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })

            if isinstance(field, forms.DecimalField):
                field.widget.attrs.update({
                    "step": "0.01"
                })

            elif isinstance(field, forms.IntegerField):
                field.widget.attrs.update({
                    "step": "1",
                    "min": "0"
                })
        
        for campo, label in self.LABELS.items():

            if campo in self.fields:
                self.fields[campo].label = label

    def obter_grupo(self, grupo):
        return [
            self[campo]
            for campo in grupo
            if campo in self.fields
        ]

    def obter_ranhura(self):
        return self.obter_grupo(self.RANHURA)

    def obter_bobina(self):
        return self.obter_grupo(self.BOBINA)

    def obter_condutor(self):
        return self.obter_grupo(self.CONDUTOR)

    def obter_calco(self):
        return self.obter_grupo(self.CALCO)

class DadosPerifericosForm(forms.ModelForm):

    ARO = [
        
        "aro_amarracao_ll",
        "aro_amarracao_lol",
        "material_aro_ll",
        "material_aro_lol",
    ]

    N_CALCO = [
        "calco_amarracao_inferior_ll",
        "calco_amarracao_superior_ll",
        "calco_amarracao_inferior_lol",
        "calco_amarracao_superior_lol",
    ]

    OBS_CALCO = [
        "obs_calco_amarracao_inferior_ll",
        "obs_calco_amarracao_superior_ll",
        "obs_calco_amarracao_inferior_lol",
        "obs_calco_amarracao_superior_lol",
    ]

    INFERIOR = [
        
        "material_calcos",
        "campo_eletrico",
        "densidade_corrente",
        "tensao_cabo",
        "classe_termica_cabo",
        "comprimento_cabo_interno",
        "descricao_terminal",
        "comprimento_cabo_externo"
    ]

    LABELS = {

        # aro
        "aro_amarracao_ll": "LL",
        "aro_amarracao_lol": "LOL",
        "material_aro_ll": "LL",
        "material_aro_lol": "LOL",

        # calco
        "calco_amarracao_inferior_ll": "Inferior LL",
        "calco_amarracao_superior_ll": "Superior LL",
        "calco_amarracao_inferior_lol": "Inferior LOL",
        "calco_amarracao_superior_lol": "Superior LOL",

        # obs calco
        "obs_calco_amarracao_inferior_ll": "",
        "obs_calco_amarracao_superior_ll": "",
        "obs_calco_amarracao_inferior_lol": "",
        "obs_calco_amarracao_superior_lol": "",

        # Calço
        "material_calcos": "Material do calços",
        "campo_eletrico": "Campo Elétrico",
        "densidade_corrente": "Densidade de Corrente",
        "tensao_cabo": "Tensão do Cabo",
        "classe_termica_cabo": "Classe térmica do cabo",
        "comprimento_cabo_interno": "Comp. do cabo (barra à terminal)",
        "descricao_terminal": "Descrição do terminal",
        "comprimento_cabo_externo": "Comp. do cabo (fora da carcaça)"
    }

    class Meta:
        model = DadosPerifericos
        exclude = ["maquina"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })

            if isinstance(field, forms.DecimalField):
                field.widget.attrs.update({
                    "step": "0.01"
                })

            elif isinstance(field, forms.IntegerField):
                field.widget.attrs.update({
                    "step": "1",
                    "min": "0"
                })
        
        for campo, label in self.LABELS.items():

            if campo in self.fields:
                self.fields[campo].label = label

    def obter_grupo(self, grupo):
        return [
            self[campo]
            for campo in grupo
            if campo in self.fields
        ]

    def obter_aro(self):
        return self.obter_grupo(self.ARO)

    def obter_n_calco(self):
        return self.obter_grupo(self.N_CALCO)

    def obter_obs_calco(self):
        return self.obter_grupo(self.OBS_CALCO)

    def obter_inferior(self):
        return self.obter_grupo(self.INFERIOR)

class DadosMaquinaForm(forms.ModelForm):
    class Meta:
            model = Maquina
            exclude = [
            "id",
            "cliente",
            "numero_serie",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({
                "class": "form-control"
            })

            if isinstance(field, forms.DecimalField):
                field.widget.attrs.update({
                    "step": "0.01"
                })

            elif isinstance(field, forms.IntegerField):
                field.widget.attrs.update({
                    "step": "1",
                    "min": "0"
                })

class DadosBobinaForm(forms.ModelForm):
    class Meta:
            model = DadosConstrutivosBobina
            exclude = [
            "maquina",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({
                "class": "form-control"
            })

            if isinstance(field, forms.DecimalField):
                field.widget.attrs.update({
                    "step": "0.01"
                })

            elif isinstance(field, forms.IntegerField):
                field.widget.attrs.update({
                    "step": "1",
                    "min": "0"
                })