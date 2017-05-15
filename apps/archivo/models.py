from django.db import models


class FotoEmpleado(models.Model):
    foto = models.ImageField(upload_to='usuarios')


class FotoBitacora(models.Model):
    foto = models.ImageField(upload_to='bitacora/%Y/%m/%d/')
