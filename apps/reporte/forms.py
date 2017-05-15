from django import forms


class ReporteForm(forms.Form):
    instalacion = forms.Field(label="Instalacion:",
                              widget=forms.Select(attrs={'class': 'col-md-4 form-control'}))
    puntocontrol = forms.Field(label="Punto de Control:",
                               widget=forms.Select(attrs={'class': 'col-md-4 form-control'}))
    empleado = forms.Field(label="Empleado:",
                           widget=forms.Select(attrs={'class': 'col-md-4 form-control'}))
    fecha_inicio = forms.Field(label="De",
                               widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'js-datepicker form-control',
                                                                                'data-date-format': 'yyyy-mm-dd',
                                                                                'placeholder': 'AAAA-MM-DD'}))
    fecha_fin = forms.Field(label="A",
                            widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'js-datepicker form-control',
                                                                             'data-date-format': 'yyyy-mm-dd',
                                                                             'placeholder': 'AAAA-MM-DD'}))
    evento = forms.Field(label="Evento:",
                         widget=forms.Select(attrs={'class': 'col-md-4 form-control'}))
