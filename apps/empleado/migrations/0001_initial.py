# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('comun', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuario', '0001_initial'),
        ('archivo', '0001_initial'),
        ('punto_control', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatosUsuarioEmpleado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('activo', models.IntegerField(default=1)),
                ('numero_empleado', models.CharField(blank=True, max_length=4, unique=True, null=True, validators=[django.core.validators.RegexValidator(regex=b'^[0-9]*$', message=b'El n\xc3\xbamero de empleado solo debe tener n\xc3\xbameros.')])),
                ('hora_entrada', models.TimeField()),
                ('hora_salida', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(regex=b'^[[A-Za-z]||[\xc3\xb1\xc3\x91\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\x81\xc3\x89\xc3\x8d\xc3\x93\xc3\x9a ]]*$', message=b'El nombre solo debe contener caracteres alfabeticos')])),
                ('apellido_paterno', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(regex=b'^[[A-Za-z]||[\xc3\xb1\xc3\x91\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\x81\xc3\x89\xc3\x8d\xc3\x93\xc3\x9a ]]*$', message=b'El apellido paterno solo debe contener caracteres alfabeticos')])),
                ('apellido_materno', models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.RegexValidator(regex=b'^[[A-Za-z]||[\xc3\xb1\xc3\x91\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\x81\xc3\x89\xc3\x8d\xc3\x93\xc3\x9a ]]*$', message=b'El apellido materno solo debe contener caracteres alfabeticos')])),
                ('fecha_nacimiento', models.DateField()),
                ('curp', models.CharField(unique=True, max_length=18, validators=[django.core.validators.RegexValidator(regex=b'[A-Z]{1}[AEIOUX]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}', message=b'La CURP no tiene el formato requerido')])),
                ('rfc', models.CharField(unique=True, max_length=14, validators=[django.core.validators.RegexValidator(regex=b'([A-Z,\xc3\x91,&]{3,4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[A-Z|0-9]{3,4})', message=b'El RFC no tiene el formato requerido')])),
                ('direccion', models.OneToOneField(null=True, blank=True, to='comun.Direccion')),
            ],
        ),
        migrations.AddField(
            model_name='datosusuarioempleado',
            name='empleado',
            field=models.OneToOneField(null=True, blank=True, to='empleado.Empleado'),
        ),
        migrations.AddField(
            model_name='datosusuarioempleado',
            name='foto',
            field=models.OneToOneField(null=True, blank=True, to='archivo.FotoEmpleado'),
        ),
        migrations.AddField(
            model_name='datosusuarioempleado',
            name='password',
            field=models.OneToOneField(null=True, blank=True, to='usuario.PasswordCliente'),
        ),
        migrations.AddField(
            model_name='datosusuarioempleado',
            name='puntocontrol',
            field=models.ManyToManyField(to='punto_control.PuntoControl', blank=True),
        ),
        migrations.AddField(
            model_name='datosusuarioempleado',
            name='usuario',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
