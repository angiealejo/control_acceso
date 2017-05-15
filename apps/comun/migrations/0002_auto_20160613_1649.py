# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('comun', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direccion',
            name='asentamiento',
            field=models.CharField(blank=True, max_length=110, null=True, validators=[django.core.validators.RegexValidator(regex=b'^[[\\w]||[\xc3\xb1\xc3\x91\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\x81\xc3\x89\xc3\x8d\xc3\x93\xc3\x9a\xc2\xb0]]*$', message=b'Este campo solo debe contener caracteres alfan\xc3\xbamericos')]),
        ),
        migrations.AlterField(
            model_name='direccion',
            name='codigo_postal',
            field=models.CharField(blank=True, max_length=5, null=True, validators=[django.core.validators.RegexValidator(regex=b'^[0-9]*$', message=b'Este campo debe tener solo numeros y ademas no iniciar en un cero')]),
        ),
        migrations.AlterField(
            model_name='direccion',
            name='estado',
            field=models.CharField(blank=True, max_length=110, null=True, validators=[django.core.validators.RegexValidator(regex=b'^[[\\w]||[\xc3\xb1\xc3\x91\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\x81\xc3\x89\xc3\x8d\xc3\x93\xc3\x9a]]*$', message=b'Este campo solo debe contener caracteres alfabeticos')]),
        ),
        migrations.AlterField(
            model_name='direccion',
            name='municipio',
            field=models.CharField(blank=True, max_length=110, null=True, validators=[django.core.validators.RegexValidator(regex=b'^[[\\w]||[\xc3\xb1\xc3\x91\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\x81\xc3\x89\xc3\x8d\xc3\x93\xc3\x9a]]*$', message=b'Este campo solo debe contener caracteres alfabeticos')]),
        ),
        migrations.AlterField(
            model_name='direccion',
            name='pais',
            field=models.CharField(blank=True, max_length=110, null=True, validators=[django.core.validators.RegexValidator(regex=b'^[[\\w]||[\xc3\xb1\xc3\x91\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\x81\xc3\x89\xc3\x8d\xc3\x93\xc3\x9a]]*$', message=b'Este campo solo debe contener caracteres alfabeticos')]),
        ),
    ]
