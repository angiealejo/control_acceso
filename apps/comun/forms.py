from django import forms

from apps.comun.models import Direccion, pais_default


class DireccionForm(forms.ModelForm):

    class Meta:
        model = Direccion
        fields = [
            'pais',
            'estado',
            'municipio',
            'ciudad',
            'calle',
            'asentamiento',
            'numero_interior',
            'numero_exterior',
            'codigo_postal',
            'datos_adicionales',
        ]
        labels = {
            'pais': 'Pais',
            'estado': 'Estado',
            'municipio': 'Municipio',
            'ciudad': 'Ciudad',
            'calle': 'Calle',
            'asentamiento': 'Asentamiento',
            'numero_interior': 'Num. Int',
            'numero_exterior': 'Num. Ext',
            'codigo_postal': 'Codigo Postal',
            'datos_adicionales': 'Datos adicionales',
        }
        widgets = {
            "pais": forms.TextInput(attrs={'class': 'col-md-4 form-control', 'value': pais_default}),
            "estado": forms.Select(attrs={'class': 'form-control'}),
            "municipio": forms.Select(attrs={'class': 'form-control'}),
            "ciudad": forms.TextInput(attrs={'placeholder': 'Ciudad', 'class': 'col-md-4 form-control'}),
            "asentamiento": forms.TextInput({'placeholder': 'Asentamiento', 'class': 'col-md-4 form-control'}),
            "calle": forms.TextInput(attrs={'placeholder': 'Calle', 'class': 'col-md-4 form-control'}),
            "numero_interior": forms.TextInput(attrs={'placeholder': 'Num. Int', 'class': 'col-md-4 form-control'}),
            "numero_exterior": forms.TextInput(attrs={'placeholder': 'Num. Ext', 'class': 'col-md-4 form-control'}),
            "codigo_postal": forms.TextInput(attrs={'placeholder': 'Codigo Postal', 'class': 'col-md-4 form-control'}),
            "datos_adicionales": forms.Textarea(attrs={'placeholder': 'Datos adicionales',
                                                       'class': 'col-md-4 form-control',
                                                       'style': 'width: 100%;', 'rows': '2'}),
        }
