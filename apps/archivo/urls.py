from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.archivo.views import FotoEmpleadoAPI, FotoEmpleadoClienteAPI, SubirFotoEmpleadoClienteApi, \
    RegistroHuellaDigital, BorrarHuellaDigital
from apps.comun.decoradores import group_required

urlpatterns = [
    url(r'^foto_empleado_api$', group_required("empleado")(login_required(FotoEmpleadoAPI.as_view())),
        name='foto_empleado_api'),
    url(r'^foto_empleado_cliente_api$', FotoEmpleadoClienteAPI.as_view(), name='foto_empleado_cliente_api'),
    url(r'^subir_foto_empleado_cliente_api$', SubirFotoEmpleadoClienteApi.as_view(),
        name='subir_foto_empleado_cliente_api'),
    url(r'^registro_huella_digital$', RegistroHuellaDigital.as_view(), name='registro_huella_digital'),
    url(r'^borrar_huella_digital$', group_required("empleado")(login_required(BorrarHuellaDigital.as_view())),
        name='borrar_huella_digital'),
]
