"""control_accesos_v2_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url, handler500, handler404, handler400, handler403
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout_then_login
from django.views.static import serve

from control_accesos_v2_server import settings
from control_accesos_v2_server.views import Home, HomeRedirect  # , RegistrarUsuarios
from apps.comun.decoradores import no_logeado, staff_super_usuario_logeado, decorated_includes
from apps.comun.views import http400, http401, http403, http404, http500, http503

admin.autodiscover()

handler400 = 'control_accesos_v2_server.views.handler400'
handler403 = 'control_accesos_v2_server.views.handler403'
handler404 = 'control_accesos_v2_server.views.handler404'
handler500 = 'control_accesos_v2_server.views.handler500'

urlpatterns = [
    url(r'^admin/', decorated_includes(staff_super_usuario_logeado(), include(admin.site.urls)), name='admin'),
    url(r'^login/', no_logeado(login), {'template_name': 'index.html'}, name='login'),
    url(r'^logout/', logout_then_login, name='logout'),
    # url(r'^registrar/$', no_logeado(RegistrarUsuarios.as_view()), name='registrar'),
    url(r'^$', HomeRedirect.as_view(), name='home_redirect'),
    url(r'^inicio$', login_required(Home.as_view()), name='home'),
    url(r'^400$', http400, name='400'),
    url(r'^401$', http401, name='401'),
    url(r'^403$', http403, name='403'),
    url(r'^404$', http404, name='404'),
    url(r'^500$', http500, name='500'),
    url(r'^503$', http503, name='503'),
    url(r'^comun/', include('apps.comun.urls', namespace='comun'), name='comun'),
    url(r'^empleado/', include('apps.empleado.urls', namespace='empleado'), name='empleado'),
    url(r'^instalacion/', include('apps.instalacion.urls', namespace='instalacion'), name='instalacion'),
    url(r'^puntocontrol/', include('apps.punto_control.urls', namespace='punto_control'), name='punto_control'),
    url(r'^usuario/', include('apps.usuario.urls', namespace='usuario'), name='usuario'),
    url(r'^archivo/', include('apps.archivo.urls', namespace='archivo'), name='archivo'),
    url(r'^configuracion/', include('apps.configuracion.urls', namespace='configuracion'), name='configuracion'),
    url(r'^bitacora/', include('apps.bitacora.urls', namespace='bitacora'), name='bitacora'),
    url(r'^reportes/', include('apps.reporte.urls', namespace='reporte'), name='reporte'),
]  # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
        ]
else:
    urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
