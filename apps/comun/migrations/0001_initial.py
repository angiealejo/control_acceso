# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asentamiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entidad', models.CharField(max_length=110, null=True, blank=True)),
                ('municipio', models.CharField(max_length=110, null=True, blank=True)),
                ('asentamiento', models.CharField(max_length=110, null=True, blank=True)),
                ('tipoasentamiento', models.CharField(max_length=110, null=True, blank=True)),
                ('tipozona', models.CharField(max_length=110, null=True, blank=True)),
                ('codigopostal', models.CharField(max_length=5, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pais', models.CharField(max_length=110, validators=[django.core.validators.RegexValidator(regex=b'^[[\\w]||[\xc3\xb1\xc3\x91\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\x81\xc3\x89\xc3\x8d\xc3\x93\xc3\x9a]]*$', message=b'Este campo solo debe contener caracteres alfabeticos')])),
                ('estado', models.CharField(max_length=110, validators=[django.core.validators.RegexValidator(regex=b'^[[\\w]||[\xc3\xb1\xc3\x91\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\x81\xc3\x89\xc3\x8d\xc3\x93\xc3\x9a]]*$', message=b'Este campo solo debe contener caracteres alfabeticos')])),
                ('municipio', models.CharField(max_length=110, validators=[django.core.validators.RegexValidator(regex=b'^[[\\w]||[\xc3\xb1\xc3\x91\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\x81\xc3\x89\xc3\x8d\xc3\x93\xc3\x9a]]*$', message=b'Este campo solo debe contener caracteres alfabeticos')])),
                ('ciudad', models.CharField(blank=True, max_length=110, null=True, validators=[django.core.validators.RegexValidator(regex=b'^[[\\w]||[\xc3\xb1\xc3\x91\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\x81\xc3\x89\xc3\x8d\xc3\x93\xc3\x9a]]*$', message=b'Este campo solo debe contener caracteres alfabeticos')])),
                ('calle', models.CharField(blank=True, max_length=110, null=True, validators=[django.core.validators.RegexValidator(regex=b'^[[\\w]||[\xc3\xb1\xc3\x91\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\x81\xc3\x89\xc3\x8d\xc3\x93\xc3\x9a\xc2\xb0]]*$', message=b'Este campo solo debe contener caracteres alfan\xc3\xbamericos')])),
                ('asentamiento', models.CharField(max_length=110, validators=[django.core.validators.RegexValidator(regex=b'^[[\\w]||[\xc3\xb1\xc3\x91\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\x81\xc3\x89\xc3\x8d\xc3\x93\xc3\x9a\xc2\xb0]]*$', message=b'Este campo solo debe contener caracteres alfan\xc3\xbamericos')])),
                ('numero_interior', models.CharField(blank=True, max_length=5, null=True, validators=[django.core.validators.RegexValidator(regex=b'^[[0-9a-zA-Z]||[\xc3\xb1\xc3\x91]]*$', message=b'Este campo solo debe contener caracteres alfan\xc3\xbamericos')])),
                ('numero_exterior', models.CharField(blank=True, max_length=5, null=True, validators=[django.core.validators.RegexValidator(regex=b'^[[0-9a-zA-Z]||[\xc3\xb1\xc3\x91]]*$', message=b'Este campo solo debe contener caracteres alfan\xc3\xbamericos')])),
                ('codigo_postal', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator(regex=b'^[0-9]*$', message=b'Este campo debe tener solo numeros y ademas no iniciar en un cero')])),
                ('datos_adicionales', models.CharField(blank=True, max_length=110, null=True, validators=[django.core.validators.RegexValidator(regex=b'^[\\w]||[\xc3\xb1\xc3\x91\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\x81\xc3\x89\xc3\x8d\xc3\x93\xc3\x9a\xc2\xb0]*$', message=b'Este campo solo debe contener caracteres alfan\xc3\xbamericos')])),
            ],
        ),
        migrations.CreateModel(
            name='Entidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entidad', models.CharField(max_length=110, null=True, blank=True)),
                ('capital', models.CharField(max_length=110, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entidad', models.CharField(max_length=110, null=True, blank=True)),
                ('municipio', models.CharField(max_length=110, null=True, blank=True)),
                ('cabecera', models.CharField(max_length=110, null=True, blank=True)),
            ],
        ),
    ]
