# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('empleado', '0004_auto_20160613_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='curp',
            field=models.CharField(blank=True, max_length=18, null=True, validators=[django.core.validators.RegexValidator(regex=b'[A-Z]{1}[AEIOUX]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}', message=b'La CURP no tiene el formato requerido')]),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='rfc',
            field=models.CharField(blank=True, max_length=14, null=True, validators=[django.core.validators.RegexValidator(regex=b'([A-Z,\xc3\x91,&]{3,4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[A-Z|0-9]{3,4})', message=b'El RFC no tiene el formato requerido')]),
        ),
    ]
