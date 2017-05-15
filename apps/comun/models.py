# coding=utf-8
from django.core.validators import RegexValidator
from django.db import models

# Variable usada en partes donde se sobrescribe el país agregado.
pais_default = u'México'


class Direccion(models.Model):
    pais = models.CharField(max_length=110, null=True, blank=True, validators=[
        RegexValidator(
            regex='^[[\w]||[ñÑáéíóúÁÉÍÓÚ]]*$',
            message='Este campo solo debe contener caracteres alfabeticos'
        )
    ])
    estado = models.CharField(max_length=110, null=True, blank=True, validators=[
        RegexValidator(
            regex='^[[\w]||[ñÑáéíóúÁÉÍÓÚ]]*$',
            message='Este campo solo debe contener caracteres alfabeticos'
        )
    ])
    municipio = models.CharField(max_length=110, null=True, blank=True, validators=[
        RegexValidator(
            regex='^[[\w]||[ñÑáéíóúÁÉÍÓÚ]]*$',
            message='Este campo solo debe contener caracteres alfabeticos'
        )
    ])
    ciudad = models.CharField(max_length=110, null=True, blank=True, validators=[
        RegexValidator(
            regex='^[[\w]||[ñÑáéíóúÁÉÍÓÚ]]*$',
            message='Este campo solo debe contener caracteres alfabeticos'
        )
    ])
    calle = models.CharField(max_length=110, null=True, blank=True, validators=[
        RegexValidator(
            regex='^[[\w]||[ñÑáéíóúÁÉÍÓÚ°]]*$',
            message='Este campo solo debe contener caracteres alfanúmericos'
        )
    ])
    asentamiento = models.CharField(max_length=110, null=True, blank=True, validators=[
        RegexValidator(
            regex='^[[\w]||[ñÑáéíóúÁÉÍÓÚ°]]*$',
            message='Este campo solo debe contener caracteres alfanúmericos'
        )
    ])
    numero_interior = models.CharField(max_length=5, null=True, blank=True, validators=[
        RegexValidator(
            regex='^[[0-9a-zA-Z]||[ñÑ]]*$',
            message='Este campo solo debe contener caracteres alfanúmericos'
        )
    ])
    numero_exterior = models.CharField(max_length=5, null=True, blank=True, validators=[
        RegexValidator(
            regex='^[[0-9a-zA-Z]||[ñÑ]]*$',
            message='Este campo solo debe contener caracteres alfanúmericos'
        )
    ])
    codigo_postal = models.CharField(max_length=5, null=True, blank=True, validators=[
        RegexValidator(
            regex='^[0-9]*$',
            message='Este campo debe tener solo numeros y ademas no iniciar en un cero'
        )
    ])
    datos_adicionales = models.CharField(max_length=110, null=True, blank=True, validators=[
        RegexValidator(
            regex='^[\w]||[ñÑáéíóúÁÉÍÓÚ°]*$',
            message='Este campo solo debe contener caracteres alfanúmericos'
        )
    ])


# Rellenar este catalogo con los archivos en /sqls
class Entidad(models.Model):
    entidad = models.CharField(max_length=110, null=True, blank=True)
    capital = models.CharField(max_length=110, null=True, blank=True)


# Rellenar este catalogo con los archivos en /sqls
class Municipio(models.Model):
    entidad = models.CharField(max_length=110, null=True, blank=True)
    municipio = models.CharField(max_length=110, null=True, blank=True)
    cabecera = models.CharField(max_length=110, null=True, blank=True)


# Rellenar este catalogo con los archivos en /sqls
class Asentamiento(models.Model):
    entidad = models.CharField(max_length=110, null=True, blank=True)
    municipio = models.CharField(max_length=110, null=True, blank=True)
    asentamiento = models.CharField(max_length=110, null=True, blank=True)
    tipoasentamiento = models.CharField(max_length=110, null=True, blank=True)
    tipozona = models.CharField(max_length=110, null=True, blank=True)
    codigopostal = models.CharField(max_length=5, null=True, blank=True)
