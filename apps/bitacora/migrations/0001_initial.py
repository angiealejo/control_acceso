# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('instalacion', '0001_initial'),
        ('archivo', '0001_initial'),
        ('empleado', '0001_initial'),
        ('punto_control', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bitacora',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('evento', models.CharField(max_length=25, validators=[django.core.validators.RegexValidator(regex=b'^[[\\w]||[\xc3\xb1\xc3\x91\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\x81\xc3\x89\xc3\x8d\xc3\x93\xc3\x9a]]*$', message=b'Este campo solo debe contener caracteres alfabeticos')])),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('empleado', models.ForeignKey(to='empleado.DatosUsuarioEmpleado')),
                ('foto', models.OneToOneField(null=True, blank=True, to='archivo.FotoBitacora')),
                ('instalacion', models.ForeignKey(to='instalacion.Instalacion')),
                ('puntocontrol', models.ForeignKey(to='punto_control.PuntoControl')),
            ],
        ),
    ]
