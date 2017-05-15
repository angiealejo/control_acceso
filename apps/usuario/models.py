from django.db import models

# Create your models here.


class PasswordCliente(models.Model):
    # atributo de la clase AbstractBaseUser
    password = models.CharField(max_length=128)


class HuellaDigital(models.Model):
    archivo = models.FileField(upload_to='huellas')
