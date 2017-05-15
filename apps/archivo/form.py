from django import forms

from apps.archivo.models import FotoEmpleado


class FotoEmpleadoForm(forms.Form):
    foto = forms.ImageField(label='Subir Foto:')

    class Meta:
        model = FotoEmpleado
        fields = ['foto']
