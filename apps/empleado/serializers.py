from django.contrib.auth.models import User, Group

from rest_framework import serializers

from apps.archivo.serializers import FotoEmpleadoSerializer
from apps.comun.serializers import DireccionSerializer
from apps.empleado.models import Empleado, DatosUsuarioEmpleado
from apps.punto_control.serializers import PuntoControlSerializer
from apps.usuario.serializers import HuellaDigitalSerializer, PasswordClienteSerializer


class EmpleadoSerializer(serializers.ModelSerializer):
    direccion = DireccionSerializer()

    class Meta:
        model = Empleado
        fields = ('id', 'nombre', 'apellido_paterno', 'apellido_materno',
                  'fecha_nacimiento', 'curp', 'rfc', 'direccion')


class GrupoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name')


class UsuarioSerializer(serializers.ModelSerializer):
    groups = GrupoSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')


class DatosSerializer(serializers.ModelSerializer):
    empleado = EmpleadoSerializer()
    usuario = UsuarioSerializer()
    puntocontrol = PuntoControlSerializer(many=True)
    foto = FotoEmpleadoSerializer()
    huelladigital = HuellaDigitalSerializer()
    password_default = serializers.SerializerMethodField()

    @staticmethod
    def get_password_default(obj):
        if obj.usuario.check_password(obj.numero_empleado):
            return True
        else:
            return False

    class Meta:
        model = DatosUsuarioEmpleado
        fields = ('id', 'activo', 'usuario', 'empleado', 'puntocontrol',
                  'numero_empleado', 'hora_entrada', 'hora_salida', 'foto', 'huelladigital',
                  'password_default')


class DatosClienteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    empleado = EmpleadoSerializer()
    password = PasswordClienteSerializer()
    foto = FotoEmpleadoSerializer()
    huelladigital = HuellaDigitalSerializer()

    class Meta:
        model = DatosUsuarioEmpleado
        fields = ('id', 'usuario', 'empleado', 'numero_empleado',
                  'password', 'hora_entrada', 'hora_salida', 'foto', 'huelladigital')
