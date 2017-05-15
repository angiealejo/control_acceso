# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.comun.decoradores import group_required
from apps.bitacora.views import BitacoraEmpleado, RegistroBitacoraAPI, BitacoraAPI, BitacoraLista, BitacoraReporte

urlpatterns = [
    url(r'^$', group_required("empleado")(login_required(BitacoraEmpleado.as_view())),
        name="bitacora_empleado"),
    # Url para la data table
    url(r'^bitacora_lista', group_required("empleado")(login_required(BitacoraLista.as_view())), name="bitacora_lista"),
    url(r'^bitacora_reporte',
        group_required("recursos_humanos", "administrador")(login_required(BitacoraReporte.as_view())),
        name="bitacora_reporte"),
    # Urls para registrar y consultar registros
    url(r'^registro_api', RegistroBitacoraAPI.as_view(), name="registro_api"),
    url(r'^bitacora_api', BitacoraAPI.as_view(), name="bitacora_api"),
]
