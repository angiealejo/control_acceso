from django.contrib.auth.models import User

from rest_framework import serializers

from apps.instalacion.serializers import InstalacionSerializer
from apps.punto_control.models import PuntoControl


class PuntoControlSerializer(serializers.ModelSerializer):
    instalacion = InstalacionSerializer()

    class Meta:
        model = PuntoControl
        fields = ('id', 'activo', 'asignado', 'nombre', 'instalacion',
                  'ip_publica', 'ip_privada', 'puerto_privado', 'puerto_publico')


class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class PuntoControlClienteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = PuntoControl
        fields = ('id', 'activo', 'asignado', 'usuario', 'nombre',
                  'ip_publica', 'ip_privada', 'puerto_privado', 'puerto_publico')
