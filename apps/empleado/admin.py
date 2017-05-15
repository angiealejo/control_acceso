from django.contrib import admin

from apps.empleado.models import Empleado, DatosUsuarioEmpleado


admin.site.register(Empleado)
admin.site.register(DatosUsuarioEmpleado)
