# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('empleado', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('servidor', models.IntegerField(default=0)),
                ('horas_ley', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(12)])),
                ('horas_extras', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(6)])),
                ('horas_maximas', models.PositiveIntegerField(default=0)),
                ('minutos_tolerancia', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(60)])),
                ('lapso_entrada_salida', models.TimeField()),
                ('empleado', models.OneToOneField(null=True, blank=True, to='empleado.DatosUsuarioEmpleado')),
            ],
        ),
    ]
