# forms.py
from django import forms
from .models import FeriadoPersonalizado

class FeriadoPersonalizadoForm(forms.ModelForm):
    class Meta:
        model = FeriadoPersonalizado
        fields = ['nome', 'data', 'tipo', 'estado', 'municipio']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'})
        }

