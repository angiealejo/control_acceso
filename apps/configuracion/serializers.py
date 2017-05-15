from rest_framework import serializers

from apps.configuracion.models import Configuracion
from apps.empleado.serializers import DatosClienteSerializer


class ConfiguracionSerializer(serializers.ModelSerializer):
    empleado = DatosClienteSerializer()
    nombre_numero_empleado = serializers.SerializerMethodField()

    @staticmethod
    def get_nombre_numero_empleado(obj):
        nombre_numero_empleado = ''
        if obj.empleado is not None:
            nombre_numero_empleado = '%s - %s %s %s' % (obj.empleado.numero_empleado, obj.empleado.empleado.nombre,
                                                        obj.empleado.empleado.apellido_paterno,
                                                        obj.empleado.empleado.apellido_materno)
        return nombre_numero_empleado

    class Meta:
        model = Configuracion
        fields = ('id', 'servidor', 'horas_ley', 'horas_extras',
                  'horas_maximas', 'minutos_tolerancia', 'lapso_entrada_salida',
                  'empleado', 'nombre_numero_empleado')
