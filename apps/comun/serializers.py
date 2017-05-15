from rest_framework import serializers

from apps.comun.models import Direccion, Asentamiento, Municipio, Entidad, pais_default


class EntidadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entidad
        fields = ('entidad',)


class MunicipioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Municipio
        fields = ('municipio', 'cabecera')


class AsentamientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asentamiento
        fields = ('asentamiento', 'tipoasentamiento', 'tipozona', 'codigopostal')


class DireccionSerializer(serializers.ModelSerializer):
    completa = serializers.SerializerMethodField()

    @staticmethod
    def get_completa(obj):
        completa = u""
        contador = 0
        nombres = [u'Calle: ', u'No. Ext.: ', u'No. Int.: ', u'Asentamiento: ', u'C.P.: ', u'Ciudad: ',
                   u'', u'', u'', u'Datos Adicionales: ']
        campos = [obj.calle, obj.numero_exterior, obj.numero_interior, obj.asentamiento, obj.codigo_postal, obj.ciudad,
                  obj.municipio, obj.estado, obj.pais, obj.datos_adicionales]
        while contador < len(campos):
            if completa is not u'' and campos[contador] is not None and campos[contador] is not u'':
                completa += u', '
            if campos[contador] is not None and campos[contador] is not u'':
                completa += nombres[contador] + campos[contador]
            contador += 1
        return completa

    class Meta:
        model = Direccion
        fields = ('id', 'pais', 'estado', 'municipio', 'ciudad', 'calle', 'asentamiento',
                  'numero_interior', 'numero_exterior', 'codigo_postal', 'datos_adicionales',
                  'completa')
