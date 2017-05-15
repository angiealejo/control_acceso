from rest_framework import serializers

from apps.archivo.serializers import FotoBitacoraSerializer
from apps.bitacora.models import Bitacora
from apps.empleado.serializers import DatosSerializer
from apps.instalacion.serializers import InstalacionSerializer
from apps.punto_control.serializers import PuntoControlSerializer


class BitacoraSerializer(serializers.ModelSerializer):
    instalacion = InstalacionSerializer()
    puntocontrol = PuntoControlSerializer()
    empleado = DatosSerializer()
    foto = FotoBitacoraSerializer()
    ubicacion = serializers.SerializerMethodField()
    nombre_numero_empleado = serializers.SerializerMethodField()
    fecha_hora = serializers.SerializerMethodField()

    @staticmethod
    def get_ubicacion(obj):
        return '%s , %s' % (obj.instalacion.nombre, obj.puntocontrol.nombre)

    @staticmethod
    def get_nombre_numero_empleado(obj):
        return '%s - %s %s %s' % (obj.empleado.numero_empleado,
                                  obj.empleado.empleado.nombre,
                                  obj.empleado.empleado.apellido_paterno,
                                  obj.empleado.empleado.apellido_materno)

    @staticmethod
    def get_fecha_hora(obj):
        return '%s %s' % (obj.fecha, obj.hora)

    class Meta:
        model = Bitacora
        fields = ('id', 'instalacion', 'puntocontrol', 'empleado', 'evento', 'fecha', 'hora', 'foto',
                  'ubicacion', 'nombre_numero_empleado', 'fecha_hora')


class BitacoraClienteEventoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bitacora
        fields = ('id', 'evento', 'fecha', 'hora')
