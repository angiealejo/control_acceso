from django.contrib import admin

from apps.comun.models import Direccion, Asentamiento, Municipio, Entidad


admin.site.register(Direccion)
admin.site.register(Asentamiento)
admin.site.register(Municipio)
admin.site.register(Entidad)
