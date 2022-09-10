'''
     Vistas
     fecha: 20/8/2022

    Posteriormente en el modelo models.py se agregarán las clases que corresponden a tablas de la base de datos


    Para Importar desde la carpeta donde creamos las aplicaciones la clase a llamar.
        Dentro de la clase donde estamos modificando incluir el nombre de la clase que llamaremos.
        Creamos una nueva clase a la que se le aplicara la función de enlace.
        Incluimos dentro de la clase donde nos encontramos la nueva clase creada junto con la relación que deseamos que tenga.
'''

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# Create your models here.

# class Miembros(models.Model):
#    id = models.AutoField(primary_key=True)
#    id_usuario = models.ForeignKey("Usuarios",on_delete=models.CASCADE)
#    id_proyecto = models.ForeignKey("Proyectos",on_delete=models.CASCADE)
#    id_rol = models.ForeignKey("Roles",on_delete=models.CASCADE)
   

class Usuarios(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=15)
    contrasena_usuario = models.CharField(max_length=10)
    estado_usuario = models.CharField(max_length=30)

class Proyectos(models.Model):

    estados = [

        ('Pendiente','Pendiente'),
        ('Iniciado','Iniciado'),
        ('Cancelado','Cancelado'),
        ('Finalizado','Finalizado'),

    ]

    nombre_proyecto = models.CharField(max_length=30)
    desc_proyecto = models.TextField()
    estado_proyecto = models.CharField(max_length=11,choices=estados,default='Pendiente')
    miembro = models.ManyToManyField(settings.AUTH_USER_MODEL)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()



class Roles(models.Model):
    nombre_rol = models.CharField(max_length=30)
    desc_rol = models.TextField()
    #permisos_rol = models.ListField()

class UserStory(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_us = models.CharField(max_length=30)
    prioridad_us = models.CharField(max_length=30)
    tipo_us = models.CharField(max_length=30)
    desc_us = models.TextField()
    com_us = models.TextField()
    historial_us = models.CharField(max_length=30)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

class Reuniones(models.Model):
    nombre_reunion = models.CharField(max_length=30)
    desc_reunion = models.TextField()
    lugar_reunion = models.CharField(max_length=30)
    fecha_reunion = models.DateField()
    hora_reunion = models.DateTimeField()

#class Calendario(models.Model):
    #reuniones = models.ListField()

class Permisos(models.Model):
    nombre_permisos = models.CharField(max_length=30)
    desc_permisos = models.TextField()

class TipoUS(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_tipo_us = models.CharField(max_length=30)

class SprintBacklog(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_sprint_b = models.CharField(max_length=30)
    desc_sprint_b = models.TextField()
    #productos = models.ListField()

class Kanban(models.Model):
    colum = models.IntegerField()
    fila = models.IntegerField()
    #tag_colum = models.ListField()
    #tabla_kanban = models.ListField()

class Sprint(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_sprint = models.CharField(max_length=30)
    desc_sprint = models.TextField()
    estado_sprint = models.CharField(max_length=30)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

class Reportes(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_report = models.CharField(max_length=30)
    desc_report = models.TextField()

class Backlogs(models.Model):
    id_proyecto = models.ForeignKey("Proyectos",on_delete=models.CASCADE)
    #list_us = models.ListField()
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    telefono = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Perfil de usuario {self.user.username}'
