# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from apps.comun.decoradores import group_required
from apps.reporte.views import Reporte

urlpatterns = [
    url(r'^$', group_required("recursos_humanos", "administrador")(login_required(Reporte.as_view())),
        name="reporte_recursos"),
]
