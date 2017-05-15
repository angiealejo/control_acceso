# coding=utf-8
import hashlib
from collections import OrderedDict

from django import forms

from apps.empleado.models import DatosUsuarioEmpleado


class ModificarEmail(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']

        return email


class AsignarPasswordForm(forms.Form):
    """
    Form que permite al usuario modificar su password sin ingresar el password anterior
    """
    error_messages = {
        'password_mismatch': "Las dos contraseñas no coindicen.",
    }
    new_password1 = forms.CharField(label="Nueva contraseña",
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirmar contraseña",
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AsignarPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        datos = DatosUsuarioEmpleado.objects.get(usuario_id__exact=self.user.id)
        password = datos.password
        password.password = hashlib.md5(self.cleaned_data['new_password1']).hexdigest()
        password.save()
        if commit:
            self.user.save()
        return self.user


class ModificarPasswordForm(AsignarPasswordForm):
    """
    Form que permite modificar la contraseña ingresando la contraseña anterior
    """
    error_messages = dict(AsignarPasswordForm.error_messages, **{
        'password_incorrect': "La contraseña anterior es incorrecta. " "Por favor ingresala de nuevo.",
    })
    old_password = forms.CharField(label="Old password",
                                   widget=forms.PasswordInput)

    def clean_old_password(self):
        """
        valida que el campo de la contraseña anterior sea correcto.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

ModificarPasswordForm.base_fields = OrderedDict(
    (k, ModificarPasswordForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
)
