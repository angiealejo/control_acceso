from django.contrib import admin

from apps.usuario.models import PasswordCliente, HuellaDigital


admin.site.register(PasswordCliente)
admin.site.register(HuellaDigital)

