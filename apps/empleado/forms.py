# coding=utf-8
import re

from django import forms

from datetime import date, timedelta

from apps.comun.utilidades import convertirnumeroempleadoentero
from apps.empleado.models import Empleado, DatosUsuarioEmpleado


class EmpleadoForm(forms.ModelForm):
    grupo = forms.Field(label="Grupo:", required=False, widget=forms.Select(attrs={'class': 'form-control'}),)

    class Meta:
        model = Empleado
        fields = [
            'nombre',
            'apellido_paterno',
            'apellido_materno',
            'fecha_nacimiento',
            'curp',
            'rfc',
        ]
        labels = {
            'apellido_paterno': 'Apellido Paterno',
            'apellido_materno': 'Apellido Materno',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'curp': 'CURP',
            'rfc': 'RFC',
        }
        widgets = {
            "nombre": forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'col-md-4 form-control'}),
            "apellido_paterno": forms.TextInput(attrs={'placeholder': 'Apellido Paterno',
                                                       'class': 'col-md-4 form-control'}),
            "apellido_materno": forms.TextInput(attrs={'placeholder': 'Apellido Materno',
                                                       'class': 'col-md-4 form-control'}),
            "fecha_nacimiento": forms.DateInput(format='%Y-%m-%d', attrs={'class': 'js-datepicker form-control',
                                                                          'data-date-format': 'yyyy-mm-dd',
                                                                          'placeholder': 'AAAA-MM-DD'}),
            "curp": forms.TextInput(attrs={'placeholder': 'CURP', 'class': 'col-md-4 form-control'}),
            "rfc": forms.TextInput(attrs={'placeholder': 'RFC', 'class': 'col-md-4 form-control'}),
        }

    def clean_fecha_nacimiento(self):
        diccionario_limpio = self.cleaned_data
        fecha_nacimiento = diccionario_limpio.get('fecha_nacimiento')
        # Obtenemos la fecha actual y le restamos 18 años
        # fecha_actual = date.today() - timedelta(days=6570)
        patron = re.compile('[\d]{4}[-][\d]{2}[-][\d]{2}')
        if fecha_nacimiento is not None and fecha_nacimiento != u'' and not patron.match(str(fecha_nacimiento)):
            raise forms.ValidationError("La fecha no coincide con el formato requerido")
        # elif fecha_actual < fecha_nacimiento:
        #    raise forms.ValidationError("El fecha no debe ser mayor al dia de hoy y debe ser de al menos hace 18 años")
        else:
            return fecha_nacimiento


class DatosUsuarioEmpleadoForm(forms.ModelForm):

    class Meta:
        model = DatosUsuarioEmpleado
        fields = [
            'puntocontrol',
            'hora_entrada',
            'hora_salida',
        ]
        labels = {
            'puntocontrol': 'Puntos de control',
            'hora_entrada': 'Hora de entrada',
            'hora_salida': 'Hora de salida',
        }
        widgets = {
            'puntocontrol': forms.SelectMultiple(),
            'hora_entrada': forms.TimeInput(attrs={'placeholder': '24:00',
                                                   'class': 'form-control'}),
            'hora_salida': forms.TimeInput(attrs={'placeholder': '24:00',
                                                  'class': 'form-control'}),
        }

    def clean_hora_salida(self):
        diccionario_limpio = self.cleaned_data
        hora_entrada = diccionario_limpio.get('hora_entrada')
        hora_salida = diccionario_limpio.get('hora_salida')
        if hora_salida < hora_entrada:
            raise forms.ValidationError("La hora de entrada debe ser menor a la de salida.")
        else:
            return hora_salida


class RegistrarEditarVariosForm(DatosUsuarioEmpleadoForm):
    email = forms.EmailField(label="Correo", widget=forms.TextInput(attrs={'placeholder': 'correo@dominio.com',
                                                                           'class': 'form-control'}))

    class Meta:
        model = DatosUsuarioEmpleado
        fields = [
            'puntocontrol',
            'hora_entrada',
            'hora_salida',
            'numero_empleado'
        ]
        labels = {
            'puntocontrol': 'Puntos de control',
            'hora_entrada': 'Hora de entrada',
            'hora_salida': 'Hora de salida',
            'numero_empleado': "Número de Empleado"
        }
        widgets = {
            'puntocontrol': forms.SelectMultiple(),
            'hora_entrada': forms.TimeInput(attrs={'placeholder': '24:00',
                                                   'class': 'form-control'}),
            'hora_salida': forms.TimeInput(attrs={'placeholder': '24:00',
                                                  'class': 'form-control'}),
            'numero_empleado': forms.HiddenInput()
        }


class RegistrarEditarForm(RegistrarEditarVariosForm):
    numero_empleado_entero = forms.IntegerField(label="Número de Empleado",
                                                widget=forms.NumberInput(attrs={'placeholder': 'Número de Empleado',
                                                                                'class': 'form-control',
                                                                                'max': '9999', 'min': '0'}))

    def clean_numero_empleado(self):
        numero_empleado_entero = int(self.data['numero_empleado_entero'])
        if 0 <= numero_empleado_entero <= 9999:
            numero_empleado = convertirnumeroempleadoentero(numero_empleado_entero)
            try:
                instancia = DatosUsuarioEmpleado.objects.get(numero_empleado__iexact=numero_empleado)
                if instancia != self.instance:
                    raise forms.ValidationError("Ya existe un empleado con este número de empleado.")
                else:
                    return numero_empleado
            except DatosUsuarioEmpleado.DoesNotExist:
                return numero_empleado
        else:
            raise forms.ValidationError("El número de empleado debe estar entre 0 y 9999")


class ImportarExcelForm(forms.Form):
    archivo = forms.FileField(label='Subir archivo Excel (.xlsx)')
    puntocontrol = forms.Field(label='Puntos de Control', widget=forms.SelectMultiple())
