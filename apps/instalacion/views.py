# encoding: utf-8
import json

from django.core.exceptions import SuspiciousOperation
from django.db import transaction
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic import FormView, TemplateView

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.comun.forms import DireccionForm
from apps.comun.models import Direccion, pais_default
from apps.instalacion.forms import InstalacionForm
from apps.instalacion.models import Instalacion
from apps.instalacion.serializers import InstalacionSerializer
from apps.empleado.views import DatosActivos


class InstalacionActivos(DatosActivos):
    modelo = Instalacion
    columnas = ['id', 'nombre']
    serializer = InstalacionSerializer

    def getfiltro(self, consulta, busqueda):
        return consulta.filter(nombre__icontains=busqueda)


class InstalacionInactivos(InstalacionActivos):
    activo = 0


class DeleteInstalacionAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    activo = 0

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        id_instalacion = request.POST['pk']
        print (id_instalacion)
        response_data = {'exito': True}
        tsp = transaction.savepoint()
        try:
            instalacion = Instalacion.objects.get(id=id_instalacion)
            if instalacion.activo == self.activo:
                response_data['exito'] = False
            else:
                instalacion.activo = self.activo
                instalacion.save()
            if tsp:
                transaction.savepoint_commit(tsp)
        except Instalacion.DoesNotExist:
            response_data['exito'] = False
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class RestoreInstalacionAPI(DeleteInstalacionAPI):
    activo = 1


class InstalacionFormView(FormView):
    model = Instalacion
    second_model = Direccion
    form_class = InstalacionForm
    second_form_class = DireccionForm
    success_url = reverse_lazy('instalacion:instalacion_list')
    template_name = "instalacion/instalacion_form.html"

    def get(self, request, *args, **kwargs):
        # Aqui se coloco el get de forma en que si se desea editar un registro inactivo redireccione a la lista
        id_instalacion = kwargs.get('pk')
        url = self.request.resolver_match.url_name
        form = self.get_form()
        form2 = self.second_form_class
        if id_instalacion is not None:
            try:
                # Busca si existe el dato
                instalacion = self.model.objects.get(id=id_instalacion)
                if instalacion.activo == 0:
                    # Redirecciona si es activo 0
                    raise Http404
                else:
                    # Renderiza si esta activo
                    return self.render_to_response(self.get_context_data(form=form, form2=form2))
            except self.model.DoesNotExist:
                # Redirecciona si con el pk enviado no existe un dato
                raise Http404
        else:
            # Redirecciona si con el pk enviado no existe un dato
            # Si intenta usar editar sin pk
            if url == 'instalacion_editar':
                raise SuspiciousOperation('400')
                # Si es crear
            elif url == 'instalacion_nuevo':
                # Renderiza porque si pk es none se trata de un nuevo registro
                return self.render_to_response(self.get_context_data(form=form, form2=form2))

    def get_context_data(self, **kwargs):
        context = super(InstalacionFormView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()
        context['id'] = pk
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        pais = pais_default
        id_instalacion = kwargs.get('pk', 0)
        tsp = transaction.savepoint()
        try:
            if id_instalacion == 0:
                form = self.form_class(request.POST)
                form2 = self.second_form_class(request.POST)
                if form.is_valid() and form2.is_valid():
                    # creando la instalacion
                    instalacion = form.save()
                    # creando la direccion
                    direccion = form2.save()
                    direccion.pais = pais
                    direccion.save()
                    # relacionando el instalacion con la direccion
                    instalacion.direccion = direccion
                    instalacion.save()
                    if tsp:
                        transaction.savepoint_commit(tsp)
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    return self.render_to_response(
                      self.get_context_data(form=form, form2=form2))
            else:
                    # obtener los datos
                    instalacion = self.model.objects.get(id=id_instalacion)
                    direccion = self.second_model.objects.get(id=instalacion.direccion.id)
                    form = self.form_class(request.POST, instance=instalacion)
                    form2 = self.second_form_class(request.POST, instance=direccion)
                    if form.is_valid() and form2.is_valid():
                        # guadando cambios en instalacion y direccion
                        instalacion = form.save()
                        direccion = form2.save()
                        direccion.pais = pais
                        direccion.save()
                        instalacion.direccion = direccion
                        instalacion.save()
                        # guardando cambios
                        tsp = transaction.savepoint()
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
        except Exception, e:
            raise e


class InstalacionAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        instalacion = request.GET.get('instalacion')
        lista_datos = request.GET.get('lista')
        activo = request.GET.get('activo')
        if lista_datos is not None and activo is not None:
            consulta = Instalacion.objects.filter(activo=activo).order_by('id')
            serializer = InstalacionSerializer(consulta, many=True)
        elif instalacion is not None:
            consulta = Instalacion.objects.get(id=instalacion)
            serializer = InstalacionSerializer(consulta)
        return HttpResponse(json.dumps(serializer.data), content_type="application/json")


class InstalacionList(TemplateView):
    template_name = "instalacion/instalacion_list.html"


class InstalacionRecycle(TemplateView):
    template_name = "instalacion/instalacion_recycle.html"
