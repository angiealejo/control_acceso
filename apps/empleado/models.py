# coding=utf-8
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

from apps.archivo.models import FotoEmpleado
from apps.comun.models import Direccion
from apps.punto_control.models import PuntoControl
from apps.usuario.models import PasswordCliente, HuellaDigital
from control_accesos_v2_server import settings


class Empleado(models.Model):
    nombre = models.CharField(max_length=100, validators=[
        RegexValidator(
            regex='^[[A-Za-z]||[ñÑáéíóúÁÉÍÓÚ ]]*$',
            message='El nombre solo debe contener caracteres alfabeticos',
        )
    ])
    apellido_paterno = models.CharField(max_length=50, validators=[
        RegexValidator(
            regex='^[[A-Za-z]||[ñÑáéíóúÁÉÍÓÚ ]]*$',
            message='El apellido paterno solo debe contener caracteres alfabeticos'
        )
    ])
    apellido_materno = models.CharField(max_length=50, null=True, blank=True, validators=[
        RegexValidator(
            regex='^[[A-Za-z]||[ñÑáéíóúÁÉÍÓÚ ]]*$',
            message='El apellido materno solo debe contener caracteres alfabeticos'
        )
    ])
    fecha_nacimiento = models.DateField(null=True, blank=True)
    curp = models.CharField(max_length=18, null=True, blank=True, validators=[
        RegexValidator(
            regex='[A-Z]{1}[AEIOUX]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}',
            message='La CURP no tiene el formato requerido'
        )
    ])
    rfc = models.CharField(max_length=14, null=True, blank=True, validators=[
        RegexValidator(
            regex='([A-Z,Ñ,&]{3,4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[A-Z|0-9]{3,4})',
            message='El RFC no tiene el formato requerido'
        )
    ])
    direccion = models.OneToOneField(Direccion, null=True, blank=True)

    def get_estatus_display(self):
        if self.activo == 1:
            return "Activo"
        else:
            return "Inactivo"


class DatosUsuarioEmpleado(models.Model):
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.IntegerField(default=1)
    usuario = models.OneToOneField(User, unique=True, null=True, blank=True)
    empleado = models.OneToOneField(Empleado, unique=True, null=True, blank=True)
    puntocontrol = models.ManyToManyField(PuntoControl, blank=True)
    numero_empleado = models.CharField(max_length=4, unique=True, validators=[
        RegexValidator(
            regex='^[0-9]*$',
            message='El número de empleado solo debe tener 4 números.'
        )
    ])
    password = models.OneToOneField(PasswordCliente, unique=True, null=True, blank=True)
    huelladigital = models.OneToOneField(HuellaDigital, unique=True, null=True, blank=True)
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()
    foto = models.OneToOneField(FotoEmpleado, unique=True, null=True, blank=True)

    def get_estatus_display(self):
        if self.activo == 1:
            return "Activo"
        else:
            return "Inactivo"
