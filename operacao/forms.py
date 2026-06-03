from django import forms
from cadastros.models import DadosEstator


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

    def obter_dados_grupo(self, grupo):
        return {
            campo: self.cleaned_data.get(campo)
            for campo in grupo
        }

    def obter_dados_bobinado(self):
        return self.obter_dados_grupo(self.BOBINADO)

    def obter_dados_nucleo(self):
        return self.obter_dados_grupo(self.NUCLEO)