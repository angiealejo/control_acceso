# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_huelladigital'),
        ('empleado', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosusuarioempleado',
            name='huelladigital',
            field=models.OneToOneField(null=True, blank=True, to='usuario.HuellaDigital'),
        ),
    ]
