from django import forms
from .models import FeriadoPersonalizado

class FeriadoPersonalizadoForm(forms.ModelForm):
    class Meta:
        model = FeriadoPersonalizado
        fields = '__all__'
