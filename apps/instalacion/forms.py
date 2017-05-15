# encoding: utf-8
from django import forms

from apps.instalacion.models import Instalacion


class InstalacionForm(forms.ModelForm):

    class Meta:
        model = Instalacion
        fields = [
            'nombre',
            'direccion',
        ]
        labels = {
            'nombre': 'Nombre de Instalación',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'col-md-4 form-control'})

        }
