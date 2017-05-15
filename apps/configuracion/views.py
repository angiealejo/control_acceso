# -*- coding: utf-8 -*-
import json

from django.core.exceptions import SuspiciousOperation, ImproperlyConfigured
from django.db import transaction
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.encoding import force_text
from django.views.generic import FormView, TemplateView

from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.configuracion.models import Configuracion
from apps.configuracion.forms import ConfiguracionForm, ConfiguracionEmpleadoForm
from apps.configuracion.serializers import ConfiguracionSerializer

from apps.empleado.models import DatosUsuarioEmpleado
from apps.punto_control.models import PuntoControl
from apps.empleado.views import DatosActivos


class ConfiguracionEmpleados(DatosActivos):
    activo = 0  # En realidad es servidor para este modelo
    modelo = Configuracion
    columnas = ['id', 'empleado__numero_empleado', 'minutos_tolerancia']
    serializer = ConfiguracionSerializer

    def getfiltro(self, consulta, busqueda):
        return consulta.filter(
            Q(empleado__numero_empleado__icontains=busqueda) |
            Q(minutos_tolerancia__icontains=busqueda) |
            Q(empleado__empleado__nombre__icontains=busqueda) |
            Q(empleado__empleado__apellido_paterno__icontains=busqueda) |
            Q(empleado__empleado__apellido_materno__icontains=busqueda)
        )


class ConfiguracionList(TemplateView):
    template_name = "configuracion/configuracion_list.html"
    success_url = reverse_lazy('configuracion:configuracion_servidor')
    model = Configuracion

    def get_success_url(self):
        if self.success_url:
            url = force_text(self.success_url)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            # Busca si existe la configuracion de servidor sino redirige a la pagina para configurarlo
            servidor_configuracion = self.model.objects.get(servidor=1)
            if servidor_configuracion.servidor is 1:
                return self.render_to_response(context)
            else:
                return HttpResponseRedirect(self.get_success_url())
        except self.model.DoesNotExist:
            # Redirecciona sino existe la configuracion de servidor
            return HttpResponseRedirect(self.get_success_url())


class ConfiguracionAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        id_configuracion = request.GET.get('id')
        lista = request.GET.get('lista')
        # Cuando se usa desde el cliente
        servidor = request.GET.get('servidor')
        idpcrecibida = request.GET.get('idpuntocontrol')
        if idpcrecibida is not None:
            puntocontrol = PuntoControl.objects.get(id=idpcrecibida, asignado=1, activo=1)
            consulta = Configuracion.objects.filter(empleado__activo=1, empleado__puntocontrol=puntocontrol)\
                .exclude(servidor=1).order_by('empleado__numero_empleado')
            serializer = ConfiguracionSerializer(consulta, many=True)
        elif id_configuracion is not None:
            consulta = Configuracion.objects.get(id=id_configuracion)
            serializer = ConfiguracionSerializer(consulta)
        elif lista is not None:
            consulta = Configuracion.objects.all().exclude(servidor=1).order_by('empleado__numero_empleado')
            serializer = ConfiguracionSerializer(consulta, many=True)
        elif servidor is not None:
            consulta = Configuracion.objects.get(servidor=1)
            serializer = ConfiguracionSerializer(consulta)
        return HttpResponse(json.dumps(serializer.data), content_type="application/json")


class ConfiguracionServidorFormView(FormView):
    model = Configuracion
    form_class = ConfiguracionForm
    success_url = reverse_lazy('home')
    template_name = "configuracion/configuracion_form.html"

    def get_context_data(self, **kwargs):
        context = super(ConfiguracionServidorFormView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        try:
            configuracion = self.model.objects.get(servidor=1)
            context['id'] = configuracion.id
        except self.model.DoesNotExist:
            context['id'] = 0
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        tsp = transaction.savepoint()
        try:
            configuracion = self.model.objects.get(servidor=1)
            form = self.form_class(request.POST, instance=configuracion)
            if form.is_valid():
                configuracion = form.save()
                horas_max = configuracion.horas_ley + configuracion.horas_extras
                configuracion.horas_maximas = horas_max
                configuracion.save()
                if tsp:
                    transaction.savepoint_commit(tsp)
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.render_to_response(self.get_context_data(form=form))

        except self.model.DoesNotExist:
            form = self.form_class(request.POST)
            if form.is_valid():
                configuracion = form.save()
                configuracion.servidor = 1
                configuracion.save()
                horas_max = configuracion.horas_ley + configuracion.horas_extras
                configuracion.horas_maximas = horas_max
                configuracion.save()
                if tsp:
                    transaction.savepoint_commit(tsp)
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.render_to_response(self.get_context_data(form=form))
        except Exception, e:
            raise e


class ConfiguracionEmpleadoFormView(FormView):
    model = Configuracion
    form_class = ConfiguracionEmpleadoForm
    second_model = DatosUsuarioEmpleado
    success_url = reverse_lazy('configuracion:configuracion_lista')
    template_name = "configuracion/configuracion_empleado.html"

    def get(self, request, *args, **kwargs):
        # Aqui se coloco el get de forma en que si se desea editar un registro inactivo redireccione a la lista
        id_empleado_configuracion = kwargs.get('pk')
        url = self.request.resolver_match.url_name
        form = self.get_form()
        try:
            # Busca si existe la configuracion de servidor sino redirige a la pagina para configurarlo
            servidor_configuracion = self.model.objects.get(servidor=1)
            if servidor_configuracion.servidor is 1:
                id_empleado_configuracion = kwargs.get('pk')
            else:
                self.success_url = reverse_lazy('configuracion:configuracion_servidor')
                return HttpResponseRedirect(self.get_success_url())
        except self.model.DoesNotExist:
            # Redirecciona si con el pk enviado no existe un dato
            self.success_url = reverse_lazy('configuracion:configuracion_servidor')
            return HttpResponseRedirect(self.get_success_url())
        if id_empleado_configuracion is not None:
            try:
                # Busca si existe el dato
                empleado_configuracion = self.model.objects.get(id=id_empleado_configuracion)
                if empleado_configuracion.servidor is 0:
                    return self.render_to_response(self.get_context_data(form=form))
                else:
                    raise Http404
            except self.model.DoesNotExist:
                # Redirecciona si con el pk enviado no existe un dato
                raise Http404
        else:
            # Redirecciona si con el pk enviado no existe un dato
            # Si intenta usar editar sin pk
            if url == 'configuracion_editar':
                raise SuspiciousOperation('400')
                # Si es crear
            elif url == 'configuracion_empleado':
                # Renderiza porque si pk es none se trata de un nuevo registro
                return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ConfiguracionEmpleadoFormView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        if 'form' not in context:
            context['form'] = self.form_class()
        context['id'] = pk
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        id_configuracion = kwargs.get('pk', 0)
        tsp = transaction.savepoint()
        form = self.form_class(request.POST)
        try:
            if id_configuracion == 0:
                configuraciongeneral = self.model.objects.get(servidor=1)
                if form.is_valid():
                    configuracion = self.model(
                        horas_ley=configuraciongeneral.horas_ley,
                        horas_extras=configuraciongeneral.horas_extras,
                        horas_maximas=configuraciongeneral.horas_maximas,
                        lapso_entrada_salida=configuraciongeneral.lapso_entrada_salida,
                        minutos_tolerancia=int(form.data['minutos_tolerancia']),
                        empleado=self.second_model.objects.get(id=int(form.data['empleado']))
                    )
                    configuracion.save()
                    if tsp:
                        transaction.savepoint_commit(tsp)
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    return self.render_to_response(self.get_context_data(form=form))
            else:
                configuracion = self.model.objects.get(id=id_configuracion)
                if form.is_valid():
                    configuracion.minutos_tolerancia = int(form.data['minutos_tolerancia'])
                    configuracion.save()
                    if tsp:
                        transaction.savepoint_commit(tsp)
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    return self.render_to_response(self.get_context_data(form=form))
        except self.model.DoesNotExist:
            raise Exception('500')
        except self.second_model.DoesNotExist:
            raise Exception('500')
        except Exception, e:
            raise e


class DeleteConfiguracionAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def delete(self, request):
        id_configuracion = request.POST['id']
        response_data = {'exito': True}
        tsp = transaction.savepoint()
        try:
            configuracion = Configuracion.objects.get(id=id_configuracion)
            configuracion.delete()
            if tsp:
                transaction.savepoint_commit(tsp)
        except Configuracion.DoesNotExist:
            response_data['exito'] = False
        return HttpResponse(json.dumps(response_data), content_type="application/json")
