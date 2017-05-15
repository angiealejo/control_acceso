# coding=utf-8
import json
import hashlib

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, TemplateView

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from apps.comun.forms import DireccionForm
from apps.comun.models import Direccion, pais_default
from apps.comun.utilidades import traergrupos, convertirnumeroempleadoentero, enviar_email_template
from apps.empleado.forms import EmpleadoForm, DatosUsuarioEmpleadoForm, RegistrarEditarForm
from apps.empleado.models import DatosUsuarioEmpleado, Empleado
from apps.empleado.serializers import GrupoSerializer
from apps.punto_control.models import PuntoControl
from apps.usuario.forms import ModificarEmail, ModificarPasswordForm, AsignarPasswordForm
from apps.usuario.models import PasswordCliente


class UsuarioDireccion(FormView):
    model = Direccion
    second_model = DatosUsuarioEmpleado
    form_class = DireccionForm
    template_name = 'usuario/usuario_direccion_form.html'
    success_url = reverse_lazy('home')

    # Redireccion si el usuario que solicita la operacion no tiene relacion con los datosusuarioempleado
    def get(self, request, *args, **kwargs):
        form = self.get_form()
        usuario = self.request.user.username
        try:
            datos = self.second_model.objects.get(usuario__username__exact=usuario)
            if datos:
                return self.render_to_response(self.get_context_data(form=form))
        except self.second_model.DoesNotExist:
            raise Http404
        except Exception, e:
            raise e

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        numero_empleado_usuario = request.user.username
        pais = pais_default
        tsp = transaction.savepoint()
        try:
            datos = self.second_model.objects.get(usuario__username__exact=numero_empleado_usuario)
            direccion = self.model.objects.get(id=datos.empleado.direccion.id)
            form = self.form_class(request.POST, instance=direccion)
            if form.is_valid():
                direccion = form.save()
                direccion.pais = pais
                direccion.save()
                if tsp:
                    transaction.savepoint_commit(tsp)
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.render_to_response(
                  self.get_context_data(form=form))
        except self.model.DoesNotExist:
            raise Exception('500')
        except self.second_model.DoesNotExist:
            raise Exception('500')


class PasswordAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        numero_empleado_usuario = request.GET.get('numero_empleado_usuario')
        response_data = {'exito': True, 'password': numero_empleado_usuario}
        try:
            datos = DatosUsuarioEmpleado.objects.get(usuario__username__exact=numero_empleado_usuario)
            if datos.usuario.check_password(datos.numero_empleado):
                response_data['password'] = datos.numero_empleado
                response_data['exito'] = True
            else:
                response_data['exito'] = False
        except DatosUsuarioEmpleado.DoesNotExist:
            response_data['exito'] = False
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class RegistroCompletoView(TemplateView):
    template_name = 'usuario/registro_completo.html'

    def get_context_data(self, **kwargs):
        context = super(RegistroCompletoView, self).get_context_data(**kwargs)
        numero_empleado = self.kwargs.get('ne', None)
        if numero_empleado is None:
            raise Http404('404')
        else:
            try:
                datos = DatosUsuarioEmpleado.objects.get(numero_empleado__iexact=numero_empleado)
                usuario = User.objects.get(username__iexact=datos.usuario.username)
                if usuario.check_password(datos.numero_empleado):
                    if 'registroCompleto' not in context:
                        context['registroCompleto'] = True
                    if 'numero_empleado' not in context:
                        context['numero_empleado'] = datos.numero_empleado
                    if 'usuario_empleado' not in context:
                        context['usuario_empleado'] = usuario.username
                else:
                    raise Http404('404')
            except Exception:
                raise Http404('404')
        return context


class RegistroView(FormView):
    # creacion de la relacion de usuario en cuestion con empleados y datos usuario y asignacion de un numero de empleado
    model = Empleado
    second_model = Direccion
    third_model = DatosUsuarioEmpleado
    fourth_model = User
    fifth_model = PasswordCliente
    form_class = EmpleadoForm
    second_form_class = DireccionForm
    third_form_class = RegistrarEditarForm
    success_url = reverse_lazy('usuario:registro_completo')
    template_name = "usuario/usuario_datos_empleado_form.html"

    # Redireccion si el usuario que solicita la operacion ya tiene relacion con los datosusuarioempleado
    def get(self, request, *args, **kwargs):
        form = self.get_form()
        form2 = self.second_form_class
        form3 = self.third_form_class
        usuario = self.request.user.username
        try:
            datos = self.third_model.objects.get(numero_empleado__exact=usuario)
            if datos:
                return Http404
        except self.third_model.DoesNotExist:
            return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3))

    def get_context_data(self, **kwargs):
        context = super(RegistroView, self).get_context_data(**kwargs)
        context['usuario_email'] = self.request.user.email
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()
        if 'form3' not in context:
            context['form3'] = self.third_form_class()
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        pais = pais_default
        nombre_usuario = self.request.user.username
        tsp = transaction.savepoint()
        try:
            request.POST._mutable = True
            numero_empleado = convertirnumeroempleadoentero(int(request.POST[u'numero_empleado_entero']))
            request.POST[u'numero_empleado'] = numero_empleado
            request.POST._mutable = False
            usuario = self.fourth_model.objects.get(username=nombre_usuario)
            form = self.form_class(request.POST)
            form2 = self.second_form_class(request.POST)
            form3 = self.third_form_class(request.POST)
            if form.is_valid() and form2.is_valid() and form3.is_valid():
                # asignando grupos de permisos
                grupo = 0
                if usuario.is_superuser:
                    grupo = 3
                grupos = traergrupos(grupo)
                usuario.groups.clear()
                for grupo in grupos:
                    usuario.groups.add(grupo)
                # creando el empleado
                empleado = form.save()
                # creando la direccion
                direccion = form2.save()
                direccion.pais = pais
                direccion.save()
                # relacionando el empleado con la direccion
                empleado.direccion = direccion
                empleado.save()
                # creando el datosusuarioempleado
                datos = form3.save()
                # creando el usuario
                email = self.request.POST.get('email')
                usuario.email = email
                usuario.first_name = empleado.nombre
                if empleado.apellido_materno == '':
                    usuario.last_name = empleado.apellido_paterno
                else:
                    usuario.last_name = empleado.apellido_paterno + ' ' + empleado.apellido_materno
                usuario.username = str(int(datos.numero_empleado))
                usuario.set_password(datos.numero_empleado)
                usuario.is_superuser = False
                usuario.is_staff = False
                usuario.save()
                # encriptar password
                passwordhasheada = hashlib.md5(datos.numero_empleado).hexdigest()
                password = self.fifth_model(password=passwordhasheada)
                password.save()
                # relacionando el usuario y el empleado con los datos
                datos.password = password
                datos.usuario = usuario
                datos.empleado = empleado
                datos.save()
                if tsp:
                    transaction.savepoint_commit(tsp)
                    """try:
                        mensaje = 'Bienvenid@ a Control de Acceso, ' \
                                  'su nombre de usuario, y numero de empleado, y contraseña ahora son: %s' \
                                  % (numero_empleado,)
                        correo = EmailMessage('Registro Completo en Control de Acceso',
                                              mensaje,
                                              to=[email])
                        correo.send()
                    except Exception, e:
                        print e"""
                return HttpResponseRedirect(self.get_success_url()+datos.numero_empleado)
            else:
                return self.render_to_response(
                  self.get_context_data(form=form, form2=form2, form3=form3))
        except self.model.DoesNotExist:
            raise Exception('500')
        except self.second_model.DoesNotExist:
            raise Exception('500')
        except self.third_model.DoesNotExist:
            raise Exception('500')
        except self.fourth_model.DoesNotExist:
            raise Exception('500')
        except self.fifth_model.DoesNotExist:
            raise Exception('500')
        except Exception, e:
            raise e


class ModificarEmailForm(FormView):
    model = User
    second_model = DatosUsuarioEmpleado
    form_class = ModificarEmail
    success_url = reverse_lazy('home')
    template_name = 'usuario/usuario_modificar_email.html'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        tsp = transaction.savepoint()
        try:
            form = self.form_class(request.POST)
            if form.is_valid():
                request.user.email = form.cleaned_data['email']
                request.user.save()
                if tsp:
                    transaction.savepoint_commit(tsp)
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.render_to_response(self.get_context_data(form=form))
        except self.model.DoesNotExist:
            raise Http404


class UsuarioAdminDatosForm(FormView):
    model = Empleado
    second_model = DatosUsuarioEmpleado
    third_model = User
    form_class = EmpleadoForm
    second_form_class = DatosUsuarioEmpleadoForm
    success_url = reverse_lazy('home')
    template_name = 'usuario/usuario_datos_admin_form.html'

    # Redireccion si el usuario que solicita la operacion no tiene relacion con los datosusuarioempleado
    def get(self, request, *args, **kwargs):
        form = self.get_form()
        form2 = self.second_form_class
        usuario = self.request.user.username
        try:
            datos = self.second_model.objects.get(usuario__username__exact=usuario)
            if datos:
                return self.render_to_response(self.get_context_data(form=form, form2=form2))
        except self.second_model.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(UsuarioAdminDatosForm, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        nombre_usuario = self.request.user.username
        tsp = transaction.savepoint()
        try:
            datos = self.second_model.objects.get(usuario__username__exact=nombre_usuario)
            password = datos.password
            direccion = datos.empleado.direccion
            empleado = self.model.objects.get(id=datos.empleado.id)
            user = self.third_model.objects.get(username=nombre_usuario)
            form_horas = True
            if bool(user.groups.filter(name__in=(u'administrador', u'recursos_humanos'))):
                form_horas = False
            hora_entrada = datos.hora_entrada
            hora_salida = datos.hora_salida
            form = self.form_class(request.POST, instance=empleado)
            form2 = self.second_form_class(request.POST, instance=datos)
            if form.is_valid() and form2.is_valid():
                empleado = form.save()
                empleado.direccion = direccion
                empleado.save()
                datos = form2.save()
                if form_horas:
                    datos.hora_entrada = hora_entrada
                    datos.hora_salida = hora_salida
                    datos.save()
                user.first_name = empleado.nombre
                if empleado.apellido_materno == '':
                    user.last_name = empleado.apellido_paterno
                else:
                    user.last_name = empleado.apellido_paterno + ' ' + empleado.apellido_materno
                user.save()
                datos.password = password
                datos.usuario = user
                datos.empleado = empleado
                datos.save()
                if tsp:
                    transaction.savepoint_commit(tsp)
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.render_to_response(
                  self.get_context_data(form=form, form2=form2))
        except self.model.DoesNotExist:
            raise Exception('500')
        except self.second_model.DoesNotExist:
            raise Exception('500')
        except self.third_model.DoesNotExist:
            raise Exception('500')
        except Exception, e:
            raise e


class EmailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        email = request.POST.get('email')
        response_data = {'exito': True, 'email': email}
        num_empleado_usuario = self.request.user.username
        tsp = transaction.savepoint()
        usuario = User.objects.get(username__exact=num_empleado_usuario)
        try:
            usuario.email = email
            usuario.save()
            if tsp:
                transaction.savepoint_commit(tsp)
        except Exception, e:
            response_data = {'exito': False, 'email': usuario.email}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class LoginTokenAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        nombreusuario = request.POST.get('usuario')
        password = request.POST.get('password')
        response_data = {'exito': False, 'token': "False"}
        try:
            if nombreusuario is not None:
                usuario = User.objects.get(username__exact=nombreusuario.strip())
                grupos = usuario.groups.all()
                gruporequerido = False
                for grupo in grupos:
                    if grupo.name == 'administrador'\
                        or grupo.name == 'configurador' \
                            or grupo.name == 'pcin':
                        gruporequerido = True
                if usuario.is_active and gruporequerido and usuario.check_password(password.strip()):
                    token = Token.objects.get_or_create(user=usuario)
                    response_data = {'exito': True, 'token': 'Token '+token[0].key}
        except Exception, e:
            response_data = {'exito': False, 'token': "False"}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class AsignarPuntoControlAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        tsp = transaction.savepoint()
        usuario = request.POST.get('usuario')
        asignado = request.POST.get('asignado')
        response_data = {'exito': False}
        try:
            if usuario is not None:
                puntocontrol = PuntoControl.objects.get(usuario__username__exact=usuario.strip())
                puntocontrol.asignado = asignado
                puntocontrol.save()
                if tsp:
                    response_data['exito'] = True
                    transaction.savepoint_commit(tsp)
        except PuntoControl.DoesNotExist:
            response_data['exito'] = False
            raise Exception('500')
        except Exception, e:
            response_data['exito'] = False
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@sensitive_post_parameters()
@csrf_protect
def cambiar_password(request,
                     template_name='registration/password_change_form.html',
                     post_change_redirect=None,
                     password_change_form=ModificarPasswordForm,
                     current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('usuario:password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': 'Password change',
    }
    if extra_context is not None:
        context.update(extra_context)
    if current_app is not None:
        request.current_app = current_app
    return TemplateResponse(request, template_name, context)


@sensitive_post_parameters()
@never_cache
def restaurar_password(request, uidb64=None, token=None,
                       template_name='registration/password_reset_confirm.html',
                       token_generator=default_token_generator,
                       set_password_form=AsignarPasswordForm,
                       post_reset_redirect='usuario:password_reset_complete',
                       current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = 'Enter new password'
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = 'Password reset unsuccessful'
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


class GrupoAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        lista = request.GET.get('lista')
        serializer = None
        dataJson = None
        if lista is not None:
            grupos = [u'administrador', u'configurador', u'recursos_humanos']
            for grupo in grupos:
                consulta = Group.objects.filter(name=grupo).distinct('name')
                serializer = GrupoSerializer(consulta, many=True)
                if dataJson is None:
                    dataJson = serializer.data
                else:
                    dataJson += serializer.data
        else:
            consulta = Group.objects.all()
            serializer = GrupoSerializer(consulta, many=True)
            dataJson = serializer.data
        return HttpResponse(json.dumps(dataJson), content_type="application/json")


class ResetearInformar(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request, use_https=None):
        tsp = transaction.savepoint()
        id_empleado = request.POST.get('id')
        restaurar = request.POST.get('restaurar')
        informar = request.POST.get('informar')
        mensaje_email = request.POST.get('mensaje_email')
        response_data = {'exito': False}
        try:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
            if restaurar and int(id_empleado) > 0:
                empleado = DatosUsuarioEmpleado.objects.get(id=id_empleado, activo=1)
                asunto = u'Restauración de Contraseña'
                plantilla = 'usuario/restaurar_email.html'
                contexto = {
                    'usuario': empleado.usuario.username,
                    'password': empleado.numero_empleado,
                    'domain': domain,
                    'site_name': site_name,
                    'protocol': 'https' if use_https else 'http'
                }
                destinatario = empleado.usuario.email
                if destinatario is not None and destinatario != u'':
                    enviar_email_template(subject=asunto, email_template_name=plantilla, email_context=contexto,
                                          recipients=destinatario)
                    password_cliente = empleado.password
                    password_cliente.password = hashlib.md5(empleado.numero_empleado).hexdigest()
                    password_cliente.save()
                    usuario = empleado.usuario
                    usuario.set_password(empleado.numero_empleado)
                    usuario.save()
                    response_data = {'exito': True}
            elif informar:
                response_data = {'exito': True}
                if mensaje_email == u'' or mensaje_email is None:
                    mensaje_email = u'Su registro en el Control de Acceso ha sido un exito, a continuación le ' \
                                    u'proveemos de su nombre de usuario y su contraseña inicial. Le sugerimos' \
                                    u' iniciar sesión y cambiarla por otra para mayor seguridad.'
                empleados = DatosUsuarioEmpleado.objects.all().filter(activo=1)
                if int(id_empleado) != 0:
                    empleados = empleados.filter(id=id_empleado)
                asunto = u'Registro Exitoso'
                plantilla = 'usuario/informar_email.html'
                for empleado in empleados:
                    contexto = {
                        'usuario': empleado.usuario.username,
                        'password': empleado.numero_empleado,
                        'mensaje': mensaje_email,
                        'domain': domain,
                        'site_name': site_name,
                        'protocol': 'https' if use_https else 'http'
                    }
                    destinatario = empleado.usuario.email
                    if destinatario is not None and destinatario != u'' \
                            and empleado.usuario.check_password(empleado.numero_empleado):
                        enviar_email_template(subject=asunto, email_template_name=plantilla, email_context=contexto,
                                              recipients=destinatario)
        except Exception:
            response_data = {'exito': False}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
