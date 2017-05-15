import base64
import json

from django.core.exceptions import SuspiciousOperation
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.views.generic import FormView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.archivo.form import FotoEmpleadoForm
from apps.archivo.models import FotoEmpleado
from apps.archivo.serializers import FotoEmpleadoSerializer
from apps.comun.utilidades import borrarfotoempleadovieja, borrararchivo
from apps.empleado.models import DatosUsuarioEmpleado
from apps.punto_control.models import PuntoControl
from apps.usuario.models import HuellaDigital
from control_accesos_v2_server.settings import MEDIA_ROOT


class FotoEmpleadoClienteAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        idpcrecibida = request.GET.get('idpuntocontrol')
        response_data = []
        puntocontrol = PuntoControl.objects.get(id=idpcrecibida, asignado=1, activo=1)
        datos = DatosUsuarioEmpleado.objects.filter(activo=1, puntocontrol=puntocontrol).order_by('numero_empleado')
        for dato in datos:
            if dato.foto is not None:
                ruta = MEDIA_ROOT + "/" + str(dato.foto.foto)
                imagen = open(ruta, "rb")
                imagen64 = base64.b64encode(imagen.read())
                data = {"ruta": str(dato.foto.foto), "imgbase64": str(imagen64)}
                response_data.append(data)
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class FotoEmpleadoAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        fotoempleado = request.GET.get('fotoempleado')
        if fotoempleado is not None:
            consulta = DatosUsuarioEmpleado.objects.get(id=fotoempleado)
            serializer = FotoEmpleadoSerializer(consulta.foto)
        return HttpResponse(json.dumps(serializer.data), content_type="application/json")


class FotoEmpleadoFormView(FormView):
    model = FotoEmpleado
    second_model = DatosUsuarioEmpleado
    form_class = FotoEmpleadoForm
    success_url = reverse_lazy('empleado:empleado_list')
    template_name = 'archivo/fotoempleado_form.html'

    def get_context_data(self, **kwargs):
        context = super(FotoEmpleadoFormView, self).get_context_data(**kwargs)
        url = self.request.resolver_match.url_name
        numero_empleado_usuario = self.request.user.username
        try:
            if url == 'subir_foto_administrador' or url == 'cambiar_foto_administrador':
                self.success_url = reverse_lazy('home')
            datos = self.second_model.objects.get(usuario__username__exact=numero_empleado_usuario)
            if url == 'subir_foto_administrador' or url == 'subir_foto_empleado':
                context['id'] = 0
                if url == 'subir_foto_empleado':
                    fk = self.kwargs['fk']
                    empleado = self.second_model.objects.get(id=fk)
                    if empleado.activo == 0:
                        raise Http404('404')
            elif url == 'cambiar_foto_administrador':
                context['id'] = datos.id
            elif url == 'cambiar_foto_empleado':
                fk = self.kwargs['fk']
                empleado = self.second_model.objects.get(id=fk)
                if empleado.activo == 1:
                    context['id'] = fk
                elif empleado.activo == 0:
                    raise Http404('404')
        except self.model.DoesNotExist:
            raise Http404('404')
        except self.second_model.DoesNotExist:
            raise Http404('404')
        except Exception, e:
            raise e
        return context

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        url = request.resolver_match.url_name
        numero_empleado_usuario = self.request.user.username
        try:
            if url == 'subir_foto_administrador' or url == 'cambiar_foto_administrador':
                self.success_url = reverse_lazy('home')
                datos = self.second_model.objects.get(usuario__username__exact=numero_empleado_usuario)
                # Redirecciona si el administrador esta intentando entrar a subir y ya tiene foto
                if datos.foto is not None and url == 'subir_foto_administrador':
                    self.success_url = reverse_lazy('usuario:cambiar_foto_administrador')
                    raise Http404('404')
                # Redirecciona si el administrador esta intentando entrar a cambiar y no tiene foto
                elif datos.foto is None and url == 'cambiar_foto_administrador':
                    self.success_url = reverse_lazy('usuario:subir_foto_administrador')
                    raise Http404('404')
                # Renderiza si el administrador esta intentando subir o cambiar su foto correctamente
                elif (datos.foto is None and url == 'subir_foto_administrador') or \
                        (datos.foto is not None and url == 'cambiar_foto_administrador'):
                    return self.render_to_response(self.get_context_data(form=form))
            elif url == 'subir_foto_empleado' or url == 'cambiar_foto_empleado':
                fk = kwargs['fk']
                datos = self.second_model.objects.get(empleado_id__exact=fk)
                """
                datosuseradmin = self.second_model.objects.get(usuario__username__exact=numero_empleado_usuario)
                # Redirecciona si el administrador esta intentando subir su propia foto con subir foto empleado
                if url == 'subir_foto_empleado' and datosuseradmin.empleado.id == int(fk):
                    raise SuspiciousOperation('400')
                # Redirecciona si el administrador esta intentando cambiar su propia foto con cambiar foto empleado
                elif url == 'cambiar_foto_empleado' and \
                            datos.foto is not None and datos.foto.id == datosuseradmin.foto.id:
                    raise SuspiciousOperation('400')
                # Renderiza si el administrador esta intentando subir foto a un empleado correctamente y este no tiene
                # y si el empleado esta activo
                elif url == 'subir_foto_empleado' and (datos.foto is None and datos.activo == 1):
                """
                if url == 'subir_foto_empleado' and (datos.foto is None and datos.activo == 1):
                    return self.render_to_response(self.get_context_data(form=form))
                # Redirecciona si el administrador esta intentando subir foto a un empleado que ya tiene
                # o si el empleado esta inactivo
                elif url == 'subir_foto_empleado' and (datos.foto is not None or datos.activo == 0):
                    raise Http404('404')
                # Renderiza si el administrador esta intentando cambiar foto a un empleado correctamente y este si tiene
                # y si el empleado esta activo
                elif url == 'cambiar_foto_empleado' and (datos.foto is not None and datos.activo == 1):
                    return self.render_to_response(self.get_context_data(form=form))
                # Redirecciona si el administrador esta intentando cambiar foto a un empleado que no tiene
                # o si el empleado esta inactivo
                elif url == 'cambiar_foto_empleado' and (datos.foto is None or datos.activo == 0):
                    raise Http404('404')
        except self.second_model.DoesNotExist:
            raise Http404('404')
        except KeyError:
            raise SuspiciousOperation('400')
        except Exception, e:
            raise e

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        tsp = transaction.savepoint()
        url = request.resolver_match.url_name
        try:
            if url == 'subir_foto_administrador' or url == 'cambiar_foto_administrador':
                numero_empleado_usuario = request.user.username
                datos = self.second_model.objects.get(usuario__username__exact=numero_empleado_usuario)
                self.success_url = reverse_lazy('home')
                form = self.form_class(request.POST, request.FILES)
                if form.is_valid():
                    formatoimagen = request.FILES['foto'].image.format
                    cambiarnombreimagen = datos.numero_empleado + '.' + formatoimagen
                    request.FILES['foto'].name = cambiarnombreimagen
                    borrarfotoempleadovieja(datos.numero_empleado)
                    if datos.foto is None:
                        fotoempleado = self.model(foto=request.FILES['foto'])
                        fotoempleado.save()
                        datos.foto = fotoempleado
                        datos.save()
                    elif datos.foto is not None:
                        borrararchivo(str(datos.foto.foto))
                        datos.foto.foto = None
                        datos.foto.foto = request.FILES['foto']
                        datos.foto.save()
                        datos.save()
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    return self.render_to_response(self.get_context_data(form=form))
            elif url == 'subir_foto_empleado' or url == 'cambiar_foto_empleado':
                form = self.form_class(request.POST, request.FILES)
                fk = kwargs['fk']
                datos = self.second_model.objects.get(id__exact=fk)
                if form.is_valid():
                    formatoimagen = request.FILES['foto'].image.format
                    cambiarnombreimagen = datos.numero_empleado + '.' + formatoimagen
                    request.FILES['foto'].name = cambiarnombreimagen
                    borrarfotoempleadovieja(datos.numero_empleado)
                    if datos.foto is None:
                        fotoempleado = self.model(foto=request.FILES['foto'])
                        fotoempleado.save()
                        datos.foto = fotoempleado
                        datos.save()
                    elif datos.foto is not None:
                        borrararchivo(str(datos.foto.foto))
                        datos.foto.foto = None
                        datos.foto.save()
                        datos.foto.foto = request.FILES['foto']
                        datos.foto.save()
                        datos.save()
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    return self.render_to_response(self.get_context_data(form=form))
        except self.model.DoesNotExist:
            raise Exception('500')
        except self.second_model.DoesNotExist:
            raise Exception('500')
        except Exception, e:
            raise e


class SubirFotoEmpleadoClienteApi(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        response_data = {'exito': False}
        tsp = transaction.savepoint()
        try:
            numero_empleado = request.data['ruta']
            empleado = DatosUsuarioEmpleado.objects.get(numero_empleado=numero_empleado)
            fotonombre = numero_empleado + '.JPEG'
            fotob64 = request.data['imgbase64']
            if empleado.foto is None and len(fotob64) > 0:
                borrarfotoempleadovieja(empleado.numero_empleado)
                dfotob64 = base64.b64decode(fotob64)
                foto = FotoEmpleado(foto=ContentFile(dfotob64, fotonombre))
                foto.save()
                empleado.foto = foto
                empleado.save()
                if tsp:
                    response_data['exito'] = True
                    transaction.savepoint_commit(tsp)
        except Exception, e:
            response_data['exito'] = False
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class RegistroHuellaDigital(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        response_data = {'exito': False}
        tsp = transaction.savepoint()
        try:
            numero_empleado = request.data['numero_empleado']
            archivo_huella = request.data['archivo']
            empleado = DatosUsuarioEmpleado.objects.get(numero_empleado=numero_empleado)
            if empleado.huelladigital is None and archivo_huella is not None:
                borrararchivo("huellas/"+empleado.numero_empleado+".fpt")
                borrararchivo("huellas/" + empleado.numero_empleado + ".FPT")
                huella_digital = HuellaDigital(archivo=archivo_huella)
                huella_digital.save()
                empleado.huelladigital = huella_digital
                empleado.save()
                if tsp:
                    response_data['exito'] = True
                    transaction.savepoint_commit(tsp)
        except Exception, e:
            response_data['exito'] = False
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class BorrarHuellaDigital(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def delete(self, request):
        num_empleado_usuario = self.request.user.username
        response_data = {'exito': False}
        tsp = transaction.savepoint()
        try:
            datos = DatosUsuarioEmpleado.objects.get(usuario__username__exact=num_empleado_usuario)
            if datos.huelladigital is not None:
                huella_digital = datos.huelladigital
                datos.huelladigital = None
                datos.save()
                ruta = str(huella_digital.archivo)
                huella_digital.delete()
                borrararchivo(ruta)
                if tsp:
                    transaction.savepoint_commit(tsp)
                    response_data['exito'] = True
        except Exception:
            response_data['exito'] = False
        return HttpResponse(json.dumps(response_data), content_type="application/json")
