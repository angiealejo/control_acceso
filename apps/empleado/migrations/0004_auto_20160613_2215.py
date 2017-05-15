# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('empleado', '0003_auto_20160613_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datosusuarioempleado',
            name='numero_empleado',
            field=models.CharField(unique=True, max_length=4, validators=[django.core.validators.RegexValidator(regex=b'^[0-9]*$', message=b'El n\xc3\xbamero de empleado solo debe tener 4 n\xc3\xbameros.')]),
        ),
    ]
