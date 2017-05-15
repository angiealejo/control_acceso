# coding=utf-8
from django.core.validators import RegexValidator
from django.db import models

from apps.archivo.models import FotoBitacora
from apps.empleado.models import DatosUsuarioEmpleado
from apps.instalacion.models import Instalacion
from apps.punto_control.models import PuntoControl


class Bitacora(models.Model):
    instalacion = models.ForeignKey(Instalacion)
    puntocontrol = models.ForeignKey(PuntoControl)
    empleado = models.ForeignKey(DatosUsuarioEmpleado)
    evento = models.CharField(max_length=25, validators=[
        RegexValidator(
            regex='^[[\w]||[ñÑáéíóúÁÉÍÓÚ]]*$',
            message='Este campo solo debe contener caracteres alfabeticos'
        )
    ])
    fecha = models.DateField()
    hora = models.TimeField()
    foto = models.OneToOneField(FotoBitacora, unique=True, null=True, blank=True)
