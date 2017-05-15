# -*- coding: utf-8 -*-
import base64
import json

from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import TemplateView

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.archivo.models import FotoBitacora
from apps.bitacora.models import Bitacora
from apps.bitacora.serializers import BitacoraSerializer, BitacoraClienteEventoSerializer
from apps.empleado.models import DatosUsuarioEmpleado
from apps.empleado.views import DatosActivos
from apps.instalacion.models import Instalacion
from apps.punto_control.models import PuntoControl


class BitacoraEmpleado(TemplateView):
    template_name = 'bitacora/bitacora_empleado.html'


class RegistroBitacoraAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        response_data = {'exito': False}
        tsp = transaction.savepoint()
        try:
            idinstalacion = request.data['instalacion']
            instalacion = Instalacion.objects.get(id=idinstalacion)
            idpuntocontrol = request.data['puntocontrol']
            puntocontrol = PuntoControl.objects.get(id=idpuntocontrol)
            numero_empleado = request.data['numero_empleado']
            empleado = DatosUsuarioEmpleado.objects.get(numero_empleado=numero_empleado)
            evento = request.data['evento']
            fecha = request.data['fecha']
            hora = request.data['hora']
            fotonombre = (request.data['foto'])[16:]
            fotob64 = request.data['foto64']
            foto = None
            if len(fotonombre) > 0 and len(fotob64) > 0:
                dfotob64 = base64.b64decode(fotob64)
                foto = FotoBitacora(foto=ContentFile(dfotob64, fotonombre))
                foto.save()
            registro = Bitacora(
                instalacion=instalacion,
                puntocontrol=puntocontrol,
                empleado=empleado,
                evento=evento,
                fecha=fecha,
                hora=hora
            )
            registro.save()
            if foto is not None:
                registro.foto = foto
                registro.save()
            if tsp:
                response_data['exito'] = True
                transaction.savepoint_commit(tsp)
        except Exception, e:
            response_data['exito'] = False
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class BitacoraAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        numero_empleado = request.GET.get('numero_empleado')
        fecha = request.GET.get('fecha')
        evento = request.GET.get('evento')
        eventos = bool(request.GET.get('eventos'))
        if numero_empleado is not None and fecha is not None and evento is not None:
            if evento == 'Evento':
                consulta = Bitacora.objects.filter(empleado__numero_empleado=numero_empleado).latest('id')
                serializer = BitacoraClienteEventoSerializer(consulta)
            elif str(evento).__contains__('Entrada'):
                consulta = Bitacora.objects.filter(
                    empleado__numero_empleado=numero_empleado, evento__contains=evento
                ).latest('id')
                serializer = BitacoraClienteEventoSerializer(consulta)
            elif str(evento).__contains__('Salida'):
                consulta = Bitacora.objects.filter(
                    empleado__numero_empleado=numero_empleado, evento__contains=evento
                ).exclude(evento__contains='a Comer').latest('id')
                serializer = BitacoraClienteEventoSerializer(consulta)
        elif eventos:
            consulta = Bitacora.objects.all().distinct('evento')
            serializer = BitacoraSerializer(consulta, many=True)
        return HttpResponse(json.dumps(serializer.data), content_type="application/json")


class BitacoraLista(DatosActivos):
    activo = 1
    modelo = Bitacora
    columnas = ['evento', 'puntocontrol__nombre', 'id']
    serializer = BitacoraSerializer

    def getfiltro(self, consulta, busqueda):
        if len(busqueda) == 21:
            fechas = busqueda.split('_', 1)
            return consulta.filter(fecha__range=[fechas[0], fechas[1]])
        else:
            return consulta.filter(
                Q(instalacion__nombre__icontains=busqueda) |
                Q(puntocontrol__nombre__icontains=busqueda) |
                Q(evento__icontains=busqueda) |
                Q(fecha__icontains=busqueda) |
                Q(hora__icontains=busqueda)
            )


class BitacoraReporte(BitacoraLista):
    activo = 0
    columnas = ['empleado__numero_empleado', 'evento', 'puntocontrol__nombre', 'id']

    def getfiltro(self, consulta, busqueda):
        filtros = busqueda.split('_', 6)
        if filtros[0] == u'0' and filtros[1] == u'0' and filtros[2] == u'0'\
                and filtros[3] == u'0' and filtros[4] == u'0' and filtros[5] == u'0':
            consulta = consulta
        else:
            if filtros[0] != u'0' and filtros[1] != u'0':
                consulta = consulta.filter(fecha__range=[filtros[0], filtros[1]])
            if filtros[2] != u'0':
                consulta = consulta.filter(instalacion__id__icontains=filtros[2])
            if filtros[3] != u'0':
                consulta = consulta.filter(puntocontrol__id__icontains=filtros[3])
            if filtros[4] != u'0':
                consulta = consulta.filter(empleado__id=filtros[4])
            if filtros[5] != u'0':
                consulta = consulta.filter(evento=filtros[5])
        return consulta
