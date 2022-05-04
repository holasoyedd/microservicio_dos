from django.db import models

class Usuarios(models.Model):
    usuarioId = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField()
    nombreUsuario = models.CharField(max_length=100)
    contrasenia = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
