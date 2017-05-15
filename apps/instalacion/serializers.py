from rest_framework import serializers

from apps.comun.serializers import DireccionSerializer
from apps.instalacion.models import Instalacion


class InstalacionSerializer(serializers.ModelSerializer):
    direccion = DireccionSerializer()

    class Meta:
        model = Instalacion
        fields = ('id', 'activo', 'nombre', 'direccion')
