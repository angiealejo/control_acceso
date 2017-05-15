# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('instalacion', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PuntoControl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activo', models.IntegerField(default=1)),
                ('asignado', models.IntegerField(default=0)),
                ('nombre', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(regex=b'^[[\\w]||[\xc3\xb1\xc3\x91\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\x81\xc3\x89\xc3\x8d\xc3\x93\xc3\x9a]]*$', message=b'Este campo solo debe contener caracteres alfabeticos')])),
                ('ip_publica', models.GenericIPAddressField(null=True, blank=True)),
                ('ip_privada', models.GenericIPAddressField(null=True, blank=True)),
                ('puerto_privado', models.PositiveIntegerField(null=True, blank=True)),
                ('puerto_publico', models.PositiveIntegerField(null=True, blank=True)),
                ('instalacion', models.ForeignKey(to='instalacion.Instalacion')),
                ('usuario', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
