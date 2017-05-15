import json

from django.contrib.auth.models import User, Group
from django.core.exceptions import SuspiciousOperation
from django.db import transaction
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import TemplateView, FormView

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.instalacion.models import Instalacion
from apps.punto_control.forms import PuntoControlForm
from apps.punto_control.models import PuntoControl
from apps.punto_control.serializers import PuntoControlSerializer, PuntoControlClienteSerializer
from apps.empleado.views import DatosActivos


class PuntosActivos(DatosActivos):
    modelo = PuntoControl
    columnas = ['id', 'nombre', 'instalacion__nombre', 'asignado', 'ip_publica',
                'ip_privada', 'puerto_publico', 'puerto_privado']
    serializer = PuntoControlSerializer

    def getfiltro(self, consulta, busqueda):
        return consulta.filter(
            Q(nombre__icontains=busqueda) |
            Q(instalacion__nombre__icontains=busqueda) |
            Q(ip_publica__icontains=busqueda) |
            Q(ip_privada__icontains=busqueda) |
            Q(puerto_publico__icontains=busqueda) |
            Q(puerto_privado__icontains=busqueda)
        )


class PuntosInactivos(PuntosActivos):
    activo = 0


class DeletePuntoControlAPI(APIView):
    desactivar_activar_liberar_bloquear = True
    activo_asignado = 0
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        id_puntocontrol = request.POST['id']
        response_data = {'exito': True}
        tsp = transaction.savepoint()
        try:
            puntocontrol = PuntoControl.objects.get(id=id_puntocontrol)
            # usuario = puntocontrol.usuario
            if self.desactivar_activar_liberar_bloquear:
                if puntocontrol.activo == self.activo_asignado:  # and not usuario.is_active:
                    response_data['exito'] = False
                else:
                    puntocontrol.activo = self.activo_asignado
                    puntocontrol.save()
                    # usuario.is_active = False
                    # usuario.save()
            else:
                if puntocontrol.asignado == self.activo_asignado:
                    response_data['exito'] = False
                else:
                    puntocontrol.asignado = self.activo_asignado
                    puntocontrol.save()
            if tsp:
                transaction.savepoint_commit(tsp)
        except PuntoControl.DoesNotExist:
            response_data['exito'] = False
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class RestorePuntoControlAPI(DeletePuntoControlAPI):
    activo_asignado = 1


class BlockPuntoControlAPI(RestorePuntoControlAPI):
    desactivar_activar_liberar_bloquear = False


class ReleasePuntoControlAPI(BlockPuntoControlAPI):
    activo_asignado = 0


class PuntoControlFormView(FormView):
    model = PuntoControl
    second_model = Instalacion
    third_model = User
    form_class = PuntoControlForm
    success_url = reverse_lazy('punto_control:punto_control_list')
    template_name = "punto_control/punto_control_form.html"

    def get(self, request, *args, **kwargs):
        # Aqui se coloco el get de forma en que si se desea editar un registro inactivo redireccione a la lista
        id_punto_control = kwargs.get('pk')
        id_instalacion = kwargs.get('fk')
        url = self.request.resolver_match.url_name
        form = self.get_form()
        if id_punto_control is not None:
            try:
                # Busca si existe el dato
                puntocontrol = self.model.objects.get(id=id_punto_control)
                if puntocontrol.activo == 0:
                    # Redirecciona si es activo 0
                    raise Http404
                else:
                    # Renderiza si esta activo
                    return self.render_to_response(self.get_context_data(form=form))
            except self.model.DoesNotExist:
                # Redirecciona si con el pk enviado no existe un dato
                raise Http404
        elif id_instalacion is not None:
            try:
                # Busca si existe el dato
                self.success_url = reverse_lazy('instalacion:instalacion_list')
                instalacion = self.second_model.objects.get(id=id_instalacion)
                if instalacion.activo == 0:
                    # Redirecciona si es activo 0
                    raise Http404
                else:
                    # Renderiza si esta activo
                    return self.render_to_response(self.get_context_data(form=form))
            except self.second_model.DoesNotExist:
                # Redirecciona si con el pk enviado no existe un dato
                raise Http404
        else:
            # Redirecciona si con el pk enviado no existe un dato
            # Si intenta usar nuevo-instalacion sin fk
            if url == 'punto_control_nuevo_instalacion':
                self.success_url = reverse_lazy('instalacion:instalacion_list')
                raise SuspiciousOperation('400')
            # Si intenta usar editar sin pk
            if url == 'punto_control_editar':
                raise SuspiciousOperation('400')
                # Si es crear
            elif url == 'punto_control_nuevo':
                # Renderiza porque si pk es none se trata de un nuevo registro
                return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(PuntoControlFormView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        fk = self.kwargs.get('fk', 0)
        if 'form' not in context:
            context['form'] = self.form_class()
        context['id'] = pk
        context['idf'] = fk
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        id_punto_control = kwargs.get('pk', 0)
        id_instalacion = kwargs.get('fk', 0)
        tsp = transaction.savepoint()
        try:
            if id_punto_control == 0:
                if id_instalacion != 0:
                    self.success_url = reverse_lazy('instalacion:instalacion_list')
                form = self.form_class(request.POST)
                if form.is_valid():
                    # creando el punto de control
                    puntocontrol = form.save()
                    # creando el usuario para este punto control y crear su auth token
                    nombre = str(puntocontrol.id)+"pc"+str(puntocontrol.instalacion.id)+"in"
                    usuario = self.third_model(username=nombre)
                    usuario.set_password(nombre)
                    usuario.save()
                    grupo = Group.objects.get(name='pcin')
                    usuario.groups.add(grupo)
                    usuario.save()
                    # creando el token para el punto de control
                    Token.objects.get_or_create(user=usuario)
                    # creando la direccion
                    puntocontrol.usuario = usuario
                    puntocontrol.save()
                    if tsp:
                        transaction.savepoint_commit(tsp)
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    return self.render_to_response(
                      self.get_context_data(form=form))
            else:
                # obtener los datos
                puntocontrol = self.model.objects.get(id=id_punto_control)
                asignado = puntocontrol.asignado
                usuario = puntocontrol.usuario
                form = self.form_class(request.POST, instance=puntocontrol)
                if form.is_valid():
                    # guadando cambios en punto de control
                    puntocontrol = form.save()
                    puntocontrol.usuario = usuario
                    puntocontrol.asignado = asignado
                    puntocontrol.save()
                    # guardando cambios
                    if tsp:
                        transaction.savepoint_commit(tsp)
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    return self.render_to_response(
                        self.get_context_data(form=form))
        except self.model.DoesNotExist:
            raise Exception('500')
        except self.third_model.DoesNotExist:
            raise Exception('500')
        except Exception, e:
            raise e


class PuntoControlAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        puntocontrol = request.GET.get('punto_control')
        lista_datos = request.GET.get('lista')
        activo = request.GET.get('activo')
        idinstalacion = request.GET.get('id_instalacion')
        # Cuando se usa desde el cliente
        instalacion = request.GET.get('instalacion')
        if instalacion is not None:
            consulta = PuntoControl.objects.filter(activo=1, asignado=0,
                                                   instalacion_id__exact=instalacion, instalacion__activo=1
                                                   ).order_by('id')
            serializer = PuntoControlClienteSerializer(consulta, many=True)
        elif idinstalacion is not None:
            consulta = PuntoControl.objects.filter(activo=1, instalacion_id__exact=idinstalacion, instalacion__activo=1
                                                   ).order_by('id')
            serializer = PuntoControlClienteSerializer(consulta, many=True)
        elif lista_datos is not None and activo is not None:
            consulta = PuntoControl.objects.filter(activo=activo, instalacion__activo=1).order_by('id')
            serializer = PuntoControlSerializer(consulta, many=True)
        elif puntocontrol is not None:
            consulta = PuntoControl.objects.get(id=puntocontrol)
            serializer = PuntoControlSerializer(consulta)
        return HttpResponse(json.dumps(serializer.data), content_type="application/json")


class PuntoControlList(TemplateView):
    template_name = "punto_control/punto_control_list.html"


class PuntoControlRecycle(TemplateView):
    template_name = "punto_control/punto_control_recycle.html"
