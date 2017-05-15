# coding=utf-8
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

from apps.instalacion.models import Instalacion


class PuntoControl(models.Model):
    activo = models.IntegerField(default=1)
    asignado = models.IntegerField(default=0)
    instalacion = models.ForeignKey(Instalacion)
    usuario = models.OneToOneField(User, unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=100, validators=[
        RegexValidator(
            regex='^[[\w]||[ñÑáéíóúÁÉÍÓÚ]]*$',
            message='Este campo solo debe contener caracteres alfabeticos'
        )
    ])
    ip_publica = models.GenericIPAddressField(null=True, blank=True)
    ip_privada = models.GenericIPAddressField(null=True, blank=True)
    puerto_privado = models.PositiveIntegerField(null=True, blank=True)
    puerto_publico = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.nombre
