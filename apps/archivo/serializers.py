from rest_framework import serializers

from apps.archivo.models import FotoEmpleado, FotoBitacora


class FotoEmpleadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = FotoEmpleado
        fields = ('id', 'foto')


class FotoBitacoraSerializer(serializers.ModelSerializer):

    class Meta:
        model = FotoBitacora
        fields = ('id', 'foto')
