from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.comun.views import AsentamientoAPI, CargarCSV
from apps.comun.decoradores import staff_super_usuario_logeado

urlpatterns = [
    url(r'^asentamientos_api$', login_required(AsentamientoAPI.as_view()), name='asentamientos_api'),
    # url(r'^cargar_cvs$', staff_super_usuario_logeado()(CargarCSV.as_view()), name='cargar_cvs'),
]
