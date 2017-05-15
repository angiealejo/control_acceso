# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archivo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fotobitacora',
            name='foto',
            field=models.ImageField(upload_to=b'bitacora/%Y/%m/%d/'),
        ),
    ]
