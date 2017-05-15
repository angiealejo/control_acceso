from django.core.validators import MaxValueValidator
from django.db import models

from apps.empleado.models import DatosUsuarioEmpleado


class Configuracion(models.Model):
    servidor = models.IntegerField(default=0)
    horas_ley = models.PositiveIntegerField(validators=[MaxValueValidator(12)])
    horas_extras = models.PositiveIntegerField(validators=[MaxValueValidator(6)])
    horas_maximas = models.PositiveIntegerField(default=0)
    minutos_tolerancia = models.PositiveIntegerField(validators=[MaxValueValidator(60)])
    lapso_entrada_salida = models.TimeField()
    empleado = models.OneToOneField(DatosUsuarioEmpleado, unique=True, null=True, blank=True)
