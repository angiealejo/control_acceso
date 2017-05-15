from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.comun.decoradores import group_required, staff_super_usuario_logeado
from apps.punto_control.views import PuntoControlList, PuntoControlAPI, DeletePuntoControlAPI, PuntoControlFormView, \
    PuntoControlRecycle, RestorePuntoControlAPI, PuntosActivos, PuntosInactivos, \
    ReleasePuntoControlAPI, BlockPuntoControlAPI

urlpatterns = [
    url(r'^$', group_required("configurador", "administrador")(login_required(PuntoControlList.as_view())),
        name='punto_control_list'),
    url(r'^eliminar$', group_required("configurador", "administrador")(login_required(DeletePuntoControlAPI.as_view())),
        name='punto_control_eliminar'),
    url(r'^bloquear$', group_required("configurador", "administrador")(login_required(BlockPuntoControlAPI.as_view())),
        name='punto_control_bloquear'),
    url(r'^liberar$', group_required("configurador", "administrador")(login_required(ReleasePuntoControlAPI.as_view())),
        name='punto_control_liberar'),
    url(r'^nuevo$', group_required("configurador", "administrador")(login_required(PuntoControlFormView.as_view())),
        name='punto_control_nuevo'),
    url(r'^agregar/instalacion/$',
        group_required("configurador", "administrador")(login_required(PuntoControlFormView.as_view())),
        name='punto_control_nuevo_instalacion'),
    url(r'^agregar/instalacion/(?P<fk>\d+)$',
        group_required("configurador", "administrador")(login_required(PuntoControlFormView.as_view())),
        name='punto_control_nuevo_instalacion'),
    url(r'^editar/$', group_required("configurador", "administrador")(login_required(PuntoControlFormView.as_view())),
        name='punto_control_editar'),
    # Url para las data tables de empleado list y recycle
    url(r'^punto_control_activos$',
        group_required("configurador", "administrador")(login_required(PuntosActivos.as_view())),
        name='puntos_control_activos'),
    url(r'^punto_control_inactivos$',
        group_required("configurador", "administrador")(login_required(PuntosInactivos.as_view())),
        name='puntos_control_inactivos'),
    url(r'^editar/(?P<pk>\d+)$',
        group_required("configurador", "administrador")(login_required(PuntoControlFormView.as_view())),
        name='punto_control_editar'),
    # Url usada en el servidor y el cliente y solo necesita autenticacion por token
    url(r'^api$', PuntoControlAPI.as_view(), name='punto_control_api'),
    # Urls disponibles solo para super usuarios super usuarios staff administradores
    url(r'^reciclaje$',
        group_required("configurador", "administrador")(staff_super_usuario_logeado()(PuntoControlRecycle.as_view())),
        name='punto_control_recycle'),
    url(r'^restaurar$',
        group_required("configurador", "administrador")(staff_super_usuario_logeado()(RestorePuntoControlAPI.as_view())),
        name='punto_control_restaurar'),
]
