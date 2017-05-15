# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.comun.decoradores import group_required
from apps.configuracion.views import ConfiguracionServidorFormView, ConfiguracionAPI, ConfiguracionEmpleadoFormView, \
    ConfiguracionList, DeleteConfiguracionAPI, ConfiguracionEmpleados

urlpatterns = [
    url(r'^servidor$',
        group_required("configurador", "administrador")(login_required(ConfiguracionServidorFormView.as_view())),
        name="configuracion_servidor"),
    url(r'^empleado$',
        group_required("configurador", "administrador", "recursos_humanos")
        (login_required(ConfiguracionEmpleadoFormView.as_view())),
        name="configuracion_empleado"),
    url(r'^listar$',
        group_required("configurador", "administrador", "recursos_humanos")
        (login_required(ConfiguracionList.as_view())),
        name="configuracion_lista"),
    url(r'^eliminar$',
        group_required("configurador", "administrador", "recursos_humanos")
        (login_required(DeleteConfiguracionAPI.as_view())),
        name='configuracion_eliminar'),
    url(r'^editar/$',
        group_required("configurador", "administrador", "recursos_humanos")
        (login_required(ConfiguracionEmpleadoFormView.as_view())),
        name='configuracion_editar'),
    url(r'^editar/(?P<pk>\d+)$',
        group_required("configurador", "administrador", "recursos_humanos")
        (login_required(ConfiguracionEmpleadoFormView.as_view())),
        name='configuracion_editar'),
    # Url usada en el servidor y el cliente y solo necesita autenticacion por token
    url(r'^api$', ConfiguracionAPI.as_view(), name="configuracion_api"),
    # Url para las data tables
    url(r'^datos_empleados$',
        group_required("configurador", "administrador", "recursos_humanos")
        (login_required(ConfiguracionEmpleados.as_view())),
        name='configuracion_empleados'),
]
