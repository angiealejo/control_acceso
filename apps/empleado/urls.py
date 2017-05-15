# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.empleado.views import EmpleadoFormView, EmpleadoList, EmpleadoRecycle, DeleteAPI, RestoreAPI, DatosAPI, \
    DatosActivos, DatosInactivos, ImportarExcel, ExportarEmpleados
from apps.comun.decoradores import group_required, staff_super_usuario_logeado
from apps.archivo.views import FotoEmpleadoFormView

urlpatterns = [
    url(r'^$', group_required("recursos_humanos", "administrador")(login_required(EmpleadoList.as_view())),
        name='empleado_list'),
    url(r'^nuevos$',
        group_required("recursos_humanos", "administrador")(login_required(ImportarExcel.as_view())),
        name='importar_excel'),
    url(r'^eliminar$', group_required("recursos_humanos", "administrador")(login_required(DeleteAPI.as_view())),
        name='empleado_eliminar'),
    url(r'^nuevo$', group_required("recursos_humanos", "administrador")(login_required(EmpleadoFormView.as_view())),
        name='empleado_nuevo'),
    url(r'^editar/$', group_required("recursos_humanos", "administrador")(login_required(EmpleadoFormView.as_view())),
        name='empleado_editar'),
    url(r'^editar/(?P<pk>\d+)$',
        group_required("recursos_humanos", "administrador")(login_required(EmpleadoFormView.as_view())),
        name='empleado_editar'),
    # Url usada en el servidor y el cliente y solo necesita autenticacion por token
    url(r'^datos_api$', DatosAPI.as_view(), name='datos_api'),
    # Url para las data tables de empleado list y recycle
    url(r'^datos_activos$',
        group_required("recursos_humanos", "administrador")(login_required(DatosActivos.as_view())),
        name='datos_activos'),
    url(r'^datos_inactivos$',
        group_required("recursos_humanos", "administrador")(login_required(DatosInactivos.as_view())),
        name='datos_inactivos'),
    # Sección dedicada a subir y cambiar las fotos de empleado,
    # se colocaron aqui para no hacer otra sección en el sidebar y este en la misma sección de empleado,
    # para que en lugar de archivo/ sea empleado/ en la barra de direcciones.
    url(r'^subir_foto_empleado/$',
        group_required("recursos_humanos", "administrador")(login_required(FotoEmpleadoFormView.as_view())),
        name='subir_foto_empleado'),
    url(r'^subir_foto_empleado/(?P<fk>\d+)$',
        group_required("recursos_humanos", "administrador")(login_required(FotoEmpleadoFormView.as_view())),
        name='subir_foto_empleado'),
    url(r'^cambiar_foto_empleado/$',
        group_required("recursos_humanos", "administrador")(login_required(FotoEmpleadoFormView.as_view())),
        name='cambiar_foto_empleado'),
    url(r'^cambiar_foto_empleado/(?P<fk>\d+)$',
        group_required("recursos_humanos", "administrador")(login_required(FotoEmpleadoFormView.as_view())),
        name='cambiar_foto_empleado'),
    # Urls disponibles solo para super usuarios super usuarios staff
    url(r'^reciclaje$',
        group_required("recursos_humanos", "administrador")(staff_super_usuario_logeado()(EmpleadoRecycle.as_view())),
        name='empleado_recycle'),
    url(r'^restaurar$',
        group_required("recursos_humanos", "administrador")(staff_super_usuario_logeado()(RestoreAPI.as_view())),
        name='empleado_restaurar'),
    url(r'^exportar$',
        group_required("recursos_humanos", "administrador")(staff_super_usuario_logeado()(ExportarEmpleados.as_view())),
        name='exportar_empleados'),
]
