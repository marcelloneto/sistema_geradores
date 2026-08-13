# ensaios/forms.py
from django import forms
from .models import RegistroEnsaio

# ensaios/forms.py
from django import forms
from .models import RegistroEnsaio, DadosTensaoAplicada, DadosSurgeTest, DadosBumpTest, DadosLoopTest

class RegistroEnsaioForm(forms.ModelForm):
    
    class Meta:
        model = RegistroEnsaio
        fields = ['maquina', 'ordem_servico', 'tipo_ensaio', 'data_realizacao', 'responsavel', 'resultado_geral', 'observacoes', 'laudo_anexo']
        widgets = {
            'maquina': forms.Select(attrs={'class': 'form-select'}),
            'ordem_servico': forms.Select(attrs={'class': 'form-select'}),
            'tipo_ensaio': forms.Select(attrs={'class': 'form-select'}),
            'responsavel': forms.Select(attrs={'class': 'form-select'}),
            'resultado_geral': forms.Select(attrs={'class': 'form-select'}),
            'data_realizacao': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'laudo_anexo': forms.FileInput(attrs={'class': 'form-control'}),
        }

# --- NOVOS FORMULÁRIOS ESPECÍFICOS ---

class DadosTensaoAplicadaForm(forms.ModelForm):
    class Meta:
        model = DadosTensaoAplicada
        exclude = ['registro']
        widgets = {
            'fase_testada': forms.TextInput(attrs={'class': 'form-control'}),
            'tensao_ensaio_volts': forms.NumberInput(attrs={'class': 'form-control'}),
            'tempo_aplicacao_segundos': forms.NumberInput(attrs={'class': 'form-control'}),
            'corrente_fuga_ma': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
        }

class DadosSurgeTestForm(forms.ModelForm):
    class Meta:
        model = DadosSurgeTest
        exclude = ['registro']
        widgets = {
            'tensao_pico_volts': forms.NumberInput(attrs={'class': 'form-control'}),
            'ear_porcentagem': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'analise_onda': forms.Select(attrs={'class': 'form-select'}),
        }

class DadosBumpTestForm(forms.ModelForm):
    class Meta:
        model = DadosBumpTest
        exclude = ['registro']
        widgets = {
            'local_impacto': forms.TextInput(attrs={'class': 'form-control'}),
            'frequencia_natural_hz': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'frequencia_natural_2_hz': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'amortecimento_porcentagem': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class DadosLoopTestForm(forms.ModelForm):
    class Meta:
        model = DadosLoopTest
        exclude = ['registro']
        widgets = {
            'numero_dutos_ar': forms.NumberInput(attrs={'class': 'form-control'}),
            'altura_duto_ar_mm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fator_empilhamento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'densidade_especifica_laminacao': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'diametro_furos_chapa_mm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'numero_furos_chapa': forms.NumberInput(attrs={'class': 'form-control'}),
            'densidade_fluxo_nominal_t': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'perdas_especificas_chapa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }