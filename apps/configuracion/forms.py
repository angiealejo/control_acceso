# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import MinValueValidator
from rest_framework.compat import MaxValueValidator

from apps.configuracion.models import Configuracion


class ConfiguracionForm(forms.ModelForm):

    class Meta:
        model = Configuracion
        fields = [
            'horas_ley',
            'horas_extras',
            'minutos_tolerancia',
            'lapso_entrada_salida',
            'empleado',
        ]
        labels = {
            'horas_ley': 'Horas Ley',
            'horas_extras': 'Horas Extras',
            'minutos_tolerancia': 'Minutos de Tolerancia',
            'lapso_entrada_salida': 'Lapso minimo entre entrada y salida',
        }
        widgets = {
            'horas_ley': forms.TextInput(
                attrs={'class': 'col-md-4 form-control', "type": "number", "min": "0", "max": "12", "value": "8"}),
            'horas_extras': forms.TextInput(
                attrs={'class': 'col-md-4 form-control', "type": "number", "min": "0", "max": "6", "value": "3"}),
            'minutos_tolerancia': forms.TextInput(
                attrs={'class': 'col-md-4 form-control', "type": "number", "min": "0", "max": "60", "value": "10"}),
            'lapso_entrada_salida': forms.TextInput(attrs={'class': 'col-md-4 form-control'}),
        }


class ConfiguracionEmpleadoForm(forms.Form):
    minutos_tolerancia = forms.IntegerField(label='Minutos de Tolerancia', required=True,
                                            validators=[MaxValueValidator(60), MinValueValidator(0)],
                                            widget=forms.TextInput(
                                                attrs={'class': 'col-md-4 form-control', "type": "number",
                                                       "min": "0", "max": "60", "value": "10"}))
    empleado = forms.Field(label="Empleado:", required=True,
                           widget=forms.Select(attrs={'class': 'col-md-4 form-control'}))
