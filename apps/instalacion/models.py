# coding=utf-8
from django.core.validators import RegexValidator
from django.db import models

from apps.comun.models import Direccion


class Instalacion(models.Model):
    activo = models.IntegerField(default=1)
    nombre = models.CharField(max_length=200, validators=[
        RegexValidator(
            regex='^[[\w]||[ñÑáéíóúÁÉÍÓÚ]]*$',
            message='Este campo solo debe contener caracteres alfabeticos'
        )
    ])
    direccion = models.OneToOneField(Direccion, null=True, blank=True)

    def __unicode__(self):
        return self.nombre
