# -*- coding: utf-8 -*-
from django import forms

from apps.punto_control.models import PuntoControl


class PuntoControlForm(forms.ModelForm):

    class Meta:
        model = PuntoControl
        fields = [
            'nombre',
            'instalacion',
            'ip_publica',
            'ip_privada',
            'puerto_publico',
            'puerto_privado',
        ]
        labels = {
            'nombre': 'Nombre del Punto de Control',
            'instalacion': 'Instalación',
            'ip_publica': 'Ip. Pública',
            'ip_privada': 'Ip. Privada',
            'puerto_publico': 'Puerto Público',
            'puerto_privado': 'Puerto Privado',

        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'col-md-4 form-control'}),
            'instalacion': forms.Select(attrs={'class': 'col-md-4 form-control'}),
            'ip_publica': forms.TextInput(attrs={'class': 'col-md-4 form-control', 'value': '0.0.0.0'}),
            'ip_privada': forms.TextInput(attrs={'class': 'col-md-4 form-control', 'value': '0.0.0.0'}),
            'puerto_publico': forms.TextInput(attrs={'class': 'col-md-4 form-control', 'value': '0'}),
            'puerto_privado': forms.TextInput(attrs={'class': 'col-md-4 form-control', 'value': '0'}),

        }
