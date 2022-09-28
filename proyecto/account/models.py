'''
     Vistas
     fecha: 20/8/2022

    Posteriormente en el modelo models.py se agregarán las clases que corresponden a tablas de la base de datos


    Para Importar desde la carpeta donde creamos las aplicaciones la clase a llamar.
        Dentro de la clase donde estamos modificando incluir el nombre de la clase que llamaremos.
        Creamos una nueva clase a la que se le aplicara la función de enlace.
        Incluimos dentro de la clase donde nos encontramos la nueva clase creada junto con la relación que deseamos que tenga.
'''

from email.policy import default
from pyexpat import model
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Permission
# Create your models here.

class Miembros(models.Model):
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    id_proyecto = models.ForeignKey("Proyectos",on_delete=models.CASCADE)
    id_rol = models.ManyToManyField("Rol")
   
class Usuarios(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=15)
    contrasena_usuario = models.CharField(max_length=10)
    estado_usuario = models.CharField(max_length=30)

class Proyectos(models.Model):

    estados = [

        ('Planificado','Planificado'),
        ('Iniciado','Iniciado'),
        ('Cancelado','Cancelado'),
        ('Finalizado','Finalizado'),

    ]

    nombre_proyecto = models.CharField(max_length=30)
    desc_proyecto = models.TextField()
    estado_proyecto = models.CharField(max_length=11,choices=estados,default='Planificado')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    scrum_master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre_proyecto

class Rol(models.Model):

      rol = models.CharField(max_length=20,blank=True, null=True)
      desc_rol = models.TextField()
      permisos = models.ManyToManyField(Permission)

      def __str__(self):
        return self.rol


class UserStory(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_us = models.CharField(max_length=30)
    # tipo_us = models.CharField(max_length=30, default='si')
    # tipo_us = models.ForeignKey("TipoUS",on_delete=models.CASCADE)
    desc_us = models.TextField()
    #com_us = models.TextField()
    #historial_us = models.CharField(max_length=30)
    horas_estimadas = models.IntegerField(null=True)
    encargado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    prioridad = [

        ('Baja','Baja'),
        ('Media','Media'),
        ('Alta','Alta'),

    ]
    prioridad_us = models.CharField(choices=prioridad, max_length=10, default='Baja')
    id_proyecto = models.ForeignKey("Proyectos", on_delete=models.CASCADE, null=True)
    id_sprint = models.ForeignKey("Sprint", on_delete=models.CASCADE, null=True, blank=True)

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
    estado = [

        ('Planificado','Planificado'),
        ('Iniciado','Iniciado'),
        ('Cancelado','Cancelado'),
        ('Terminado','Terminado'),
        

    ]
    estado_sprint = models.CharField(choices=estado, default='Iniciado', max_length=12)
    fecha_inicio = models.DateField(auto_now=True,blank=True,null=True)
    duracion_dias = models.IntegerField(null=True) #Duracion en dias habiles
    capacidad = models.IntegerField(default=0) #Capacidad de produccion
    id_proyecto = models.ForeignKey("Proyectos",on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.nombre_sprint

class Miembro_Sprint (models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sprint = models.ForeignKey("Sprint", on_delete=models.CASCADE)
    horas_trabajo = models.IntegerField(null=True)

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

class Permission(Permission):
    def permission_string_method(self):
        if 'Can delete' in self.name:
            self.name = self.name.replace('Can delete', 'Puede eliminar')
        elif 'Can add' in self.name:
            self.name = self.name.replace('Can add', 'Puede crear')
        elif 'Can change' in self.name:
            self.name = self.name.replace('Can change', 'Puede modificar')
        elif 'Can view' in self.name:
            self.name = self.name.replace('Can view', 'Puede ver')
        return '%s' % (self.name)
    Permission.__str__ = permission_string_method