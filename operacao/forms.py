from django import forms
from cadastros.models import OrdemServico, Cliente, Maquina

class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = [
            'numero',
            'cliente',
            'maquina',
            'localizacao',
            'tipo_servico',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        if 'cliente' in self.fields:
            self.fields['cliente'].widget.attrs.update({'class': 'form-select'})
        if 'maquina' in self.fields:
            self.fields['maquina'].widget.attrs.update({'class': 'form-select'})

# Alias para compatibilidade com o context_processors
RegistroOSForm = OrdemServicoForm

class RegistroClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome']

class RegistroMaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = ['numero_serie', 'cliente']