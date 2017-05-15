# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_change_done, password_reset, password_reset_done, \
    password_reset_confirm, password_reset_complete

from apps.archivo.views import FotoEmpleadoFormView
from apps.comun.decoradores import no_logeado, group_required
from apps.usuario.views import UsuarioDireccion, PasswordAPI, RegistroView, RegistroCompletoView, ModificarEmailForm, \
    UsuarioAdminDatosForm, EmailAPI, restaurar_password, cambiar_password, LoginTokenAPI, GrupoAPI, \
    AsignarPuntoControlAPI, ResetearInformar

urlpatterns = [
    url(r'^direccion$', group_required('empleado')(login_required(UsuarioDireccion.as_view())),
        name='usuario_direccion'),
    url(r'^password_api$', group_required('empleado')(login_required(PasswordAPI.as_view())),
        name='password_api'),
    url(r'^email_api', group_required('empleado')(login_required(EmailAPI.as_view())),
        name='email_api'),
    url(r'^registro/$', login_required(RegistroView.as_view()),
        name='registro'),
    url(r'^registro/completo/$', no_logeado(RegistroCompletoView.as_view()),
        name='registro_completo'),
    url(r'^registro/completo/(?P<ne>\d+)$', no_logeado(RegistroCompletoView.as_view()),
        name='registro_completo'),
    url(r'^editar$', group_required('empleado')(login_required(UsuarioAdminDatosForm.as_view())),
        name='editar'),
    url(r'^grupo_api$', group_required('recursos_humanos', 'administrador')(login_required(GrupoAPI.as_view())),
        name='grupo_api'),
    url(r'^password_change/$', group_required('empleado')(login_required(cambiar_password)), name='password_change'),
    url(r'^password_change/done$', group_required('empleado')(login_required(password_change_done)),
        {'template_name': 'registration/password_change_done.html'}, name='password_change_done'),
    url(r'^password_reset/$', no_logeado(password_reset),
        {'subject_template_name': 'registration/password_reset_subject.txt',
         'template_name': 'registration/password_reset_form.html',
         'post_reset_redirect': 'usuario:password_reset_done',
         'email_template_name': 'registration/password_reset_email.html',
         'html_email_template_name': 'registration/password_reset_email.html'}, name='password_reset'),
    url(r'^password_reset/done$', no_logeado(password_reset_done),
        {'template_name': 'registration/password_reset_done.html'}, name='password_reset_done'),
    url(r'^password_reset/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', no_logeado(restaurar_password)
        , name='password_reset_confirm'),
    url(r'^password_reset/complete$', no_logeado(password_reset_complete),
        {'template_name': 'registration/password_reset_complete.html'}, name='password_reset_complete'),
    # Sección dedicada a subir y cambiar las fotos de empleado del usuario logueado
    url(r'^subir_foto$',
        group_required("empleado")(login_required(FotoEmpleadoFormView.as_view())),
        name='subir_foto_administrador'),
    url(r'^cambiar_foto$',
        group_required("empleado")(login_required(FotoEmpleadoFormView.as_view())),
        name='cambiar_foto_administrador'),
    # Url usada en el cliente para regresar token a un usuario que se logea desde este
    url(r'^login_token_api', LoginTokenAPI.as_view()),
    # Url usada en el cliente para regresar token a un usuario que se logea desde este
    url(r'^asignar_puntocontrol_api', AsignarPuntoControlAPI.as_view()),
    # Desechadas pero utiles en otros posiblemente
    # url(r'email_change$', group_required('empleado')(login_required(ModificarEmailForm.as_view())),
    # name='email_change'),
    url(r'^resetear_informar', ResetearInformar.as_view(), name='resetear_informar'),
]
