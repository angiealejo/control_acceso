# -*- encoding:utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrarForm(UserCreationForm):
    password1 = forms.CharField(label="Contraseña",
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirmar Contraseña",
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="Correo", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']

        labels = {
            'username': 'Nombre de Usuario',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        required = {
            'username': True,
        }
