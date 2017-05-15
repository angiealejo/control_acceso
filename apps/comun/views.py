# coding=utf-8
# todas las importaciones deben hacerse en orden jerarquico
# importar paquetes arriba del nivel de django (python, etc)
import csv
import json

# importar paquetes django
# from django.db import transaction
from django.http import HttpResponse, \
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError
from django.template.loader import get_template
from django.views.generic import TemplateView

# importar paquetes que complementan a django
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# importar paquetes propios
from apps.comun.models import Asentamiento, Municipio, Entidad
from apps.comun.serializers import AsentamientoSerializer, MunicipioSerializer, EntidadSerializer


class AsentamientoAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        campo = request.GET.get('consulta')
        entidad = request.GET.get('estado')
        municipio = request.GET.get('municipio')
        asentamiento = request.GET.get('asentamiento')
        ciudad = request.GET.get('ciudad')
        if campo == 'estado':
            consulta = Entidad.objects.all().order_by('entidad')
            serializer = EntidadSerializer(consulta, many=True)
        elif campo == 'municipio':
            consulta = Municipio.objects.filter(entidad=entidad).order_by('municipio')
            serializer = MunicipioSerializer(consulta, many=True)
        elif campo == 'asentamiento':
            consulta = Asentamiento.objects\
                .filter(entidad=entidad, municipio=municipio)\
                .order_by('asentamiento')
            if asentamiento is not None and asentamiento != '':
                consulta = consulta.filter(asentamiento__icontains=asentamiento)
            serializer = AsentamientoSerializer(consulta, many=True)
        elif campo == 'ciudad':
            consulta = Municipio.objects.filter(entidad=entidad, municipio=municipio)
            serializer = MunicipioSerializer(consulta, many=True)
        elif campo == 'codigopostal':
            consulta = Asentamiento.objects.get(entidad=entidad, municipio=municipio, asentamiento=asentamiento)
            serializer = AsentamientoSerializer(consulta)
        return HttpResponse(json.dumps(serializer.data), content_type="application/json")


class CargarCSV(TemplateView):
    template_name = 'comun/cargar_archivo.html'

    # @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = {"success": True}
        archivo = request.FILES['file']
        reader = csv.reader(archivo)
        for row in reader:
            # if archivo.name == 'comun_entidad.csv':
                # Entidad.objects.create(entidad=row[1], capital=row[2])
            # if archivo.name == 'comun_municipio.csv':
                # Municipio.objects.create(entidad=row[1], municipio=row[2], cabecera=row[3])
            if archivo.name == 'comun_asentamiento.csv':
                print row
                if row[4] == u'Distrito Federal':
                    entidad = u'Ciudad de México'
                else:
                    entidad = row[4]
                Asentamiento.objects.create(codigopostal=row[0],
                                            asentamiento=row[1],
                                            tipoasentamiento=row[2],
                                            municipio=row[3],
                                            entidad=entidad,
                                            tipozona=row[5])
            """tsp = transaction.savepoint()
            if tsp:
                transaction.savepoint_commit(tsp)
            else:
                transaction.savepoint_rollback(tsp)"""
            continue
        return HttpResponse(json.dumps(data), content_type="application/json")


# Estos son para mandarlos desde las views, son template views extendidas a sus respectivas http response,
# a excepcion del 401 y el 503
def http400(request):
    template = get_template('400.html')
    return HttpResponseBadRequest(template.render())


def http401(request):
    template = get_template('401.html')
    return HttpResponse(template.render(), 'Unauthorized', status=401)


def http403(request):
    template = get_template('403.html')
    return HttpResponseForbidden(template.render())


def http404(request):
    template = get_template('404.html')
    return HttpResponseNotFound(template.render())


def http500(request):
    template = get_template('500.html')
    return HttpResponseServerError(template.render())


def http503(request):
    template = get_template('503.html')
    return HttpResponse(template.render(), 'Service Unavailable', status=503)
