from django import forms
from django.forms import inlineformset_factory
from cadastros.models import Material, MaterialParametroValor

class MaterialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control rounded-custom'

    class Meta:
        model = Material
        fields = '__all__'

# forms.py dentro do inlineformset_factory
ParametroFormSet = inlineformset_factory(
    Material, 
    MaterialParametroValor, 
    fields=('parametro', 'valor_texto', 'valor_numero', 'valor_booleano', 'unidade', 'observacoes'),
    extra=0,
    can_delete=False,
    widgets={
        'valor_texto': forms.TextInput(attrs={'class': 'form-control'}),
        'valor_numero': forms.NumberInput(attrs={'class': 'form-control'}),
        'observacoes': forms.TextInput(attrs={'class': 'form-control'}),
        'unidade': forms.Select(attrs={'class': 'form-select'}),
    }
)