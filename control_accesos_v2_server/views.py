# coding=utf-8
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, RedirectView

from control_accesos_v2_server.forms import RegistrarForm
from apps.empleado.models import DatosUsuarioEmpleado


# Estos son para sustituir cuando debug es false
def handler400(request):
    return render(request, '400.html', status=400)


def handler403(request):
    return render(request, '403.html', status=403)


def handler404(request):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


class Home(TemplateView):
    template_name = 'home.html'


class RegistrarUsuarios(CreateView):
    model = User
    form_class = RegistrarForm
    template_name = "registrar_usuario.html"
    success_url = reverse_lazy('login')


class HomeRedirect(RedirectView):
    permanent = False
    query_string = False

    @transaction.atomic
    def get_redirect_url(self):
        grupos = [u'pcin', u'empleado', u'administrador', u'configurador', u'recursos_humanos']
        for grupo in grupos:
            try:
                Group.objects.get(name__exact=grupo)
            except Group.DoesNotExist:
                crear = Group(name=grupo)
                crear.save()
        if self.request.user.is_anonymous():
            return reverse('login')
        else:
            username = self.request.user.username
            try:
                if int(username) >= 0:
                    datos = DatosUsuarioEmpleado.objects.get(usuario__username__exact=username)
                    usuario = User.objects.get(username__exact=username)
                    if usuario.check_password(datos.numero_empleado):
                        return reverse('usuario:password_change')
                    else:
                        return reverse('home')
            except Exception, e:
                try:
                    usuario = User.objects.get(username__exact=username)
                    grupos = usuario.groups.all()
                    logout = False
                    for grupo in grupos:
                        if grupo.name == 'pcin':
                            logout = True
                    # cerrar sesión si se trata de un usuario de punto de control
                    if logout:
                        return reverse('logout')
                    elif DatosUsuarioEmpleado.objects.get(usuario__exact=usuario.id):
                        return reverse('home')
                except DatosUsuarioEmpleado.DoesNotExist:
                    return reverse('usuario:registro')
            except User.DoesNotExist:
                return reverse('logout')
