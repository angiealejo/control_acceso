from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.comun.decoradores import group_required, staff_super_usuario_logeado
from apps.instalacion.views import InstalacionFormView, InstalacionAPI, InstalacionList, DeleteInstalacionAPI,\
    RestoreInstalacionAPI, InstalacionRecycle, InstalacionActivos, InstalacionInactivos

urlpatterns = [
    url(r'^$', group_required("configurador", "administrador")(login_required(InstalacionList.as_view())),
        name='instalacion_list'),
    url(r'^eliminar$', group_required("configurador", "administrador")(login_required(DeleteInstalacionAPI.as_view())),
        name='instalacion_eliminar'),
    url(r'^nuevo$', group_required("configurador", "administrador")(login_required(InstalacionFormView.as_view())),
        name='instalacion_nuevo'),
    url(r'^editar/$', group_required("configurador", "administrador")(login_required(InstalacionFormView.as_view())),
        name='instalacion_editar'),
    # Url para las data tables de instalacion list y recycle
    url(r'^instalacion_activos$',
        group_required("configurador", "administrador")(login_required(InstalacionActivos.as_view())),
        name='instalacion_activos'),
    url(r'^instalacion_inactivos$',
        group_required("configurador", "administrador")(login_required(InstalacionInactivos.as_view())),
        name='instalacion_inactivos'),
    url(r'^editar/(?P<pk>\d+)$',
        group_required("configurador", "administrador")(login_required(InstalacionFormView.as_view())),
        name='instalacion_editar'),
    url(r'^api$', InstalacionAPI.as_view(), name='instalacion_api'),
    # Urls disponibles solo para super usuarios super usuarios staff
    url(r'^reciclaje$',
        group_required("configurador", "administrador")(staff_super_usuario_logeado()(InstalacionRecycle.as_view())),
        name='instalacion_recycle'),
    url(r'^restaurar$',
        group_required("configurador", "administrador")(staff_super_usuario_logeado()(RestoreInstalacionAPI.as_view())),
        name='instalacion_restaurar'),
]
