from rest_framework import serializers

from apps.usuario.models import PasswordCliente, HuellaDigital


class PasswordClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = PasswordCliente
        fields = ('id', 'password')


class HuellaDigitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = HuellaDigital
        fields = ('id', 'archivo')
