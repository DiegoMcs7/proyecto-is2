'''model
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


class Miembros(models.Model):
    '''
        Miembros
        fecha: 30/9/2022

           El modelo es utilizado para la creación de los diferentes miembros por proyecto con sus respectivos roles

            Se define el modelo que cuenta con los campos que referencian a
    '''

    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    id_proyecto = models.ForeignKey("Proyectos",on_delete=models.CASCADE)
    id_rol = models.ManyToManyField("Rol")


class Usuarios(models.Model):
    '''
        Editar un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden editar proyectos.
    '''

    id = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=15)
    contrasena_usuario = models.CharField(max_length=10)
    estado_usuario = models.CharField(max_length=30)

class Proyectos(models.Model):
    '''
        Modelo Proyecto
        fecha: 30/9/2022

           El modelo es utilizado para la creación de los diferentes proyectos con sus respectivas configuraciones

             Se define el modelo que cuenta con los detalles de un proyecto, como estados que puede tener, nombre,
             descripción, fechas y el scrum master asignado para el proyecto
    '''

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

    @property
    def project_exist(self):
        return self.id_proyecto>0

class Rol(models.Model):
    '''
        Roles
        fecha: 30/9/2022


             Se define el modelo que cuenta con los detalles del rol, como su nombre, descripción, permisos que contendrá
             el permiso, y el rol al que pertenece el proyecto
    '''
    rol = models.CharField(max_length=20,blank=True, null=True)
    desc_rol = models.TextField()
    permisos = models.ManyToManyField(Permission)
    proyecto = models.ForeignKey("Proyectos", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.rol
    
    @property
    def rol_exist(self):
        return self.id_rol>0


class UserStory(models.Model):
    '''
        Modelo User Story
        fecha: 30/9/2022

            El modelo es utilizado para la creación de los diferentes user story por proyecto

             Se define el modelo que cuenta con los detalles del user story, como su nombre, descripción, las horas estimadas
             el encargado del user story, prioridad entre otros detalles
    '''

    id = models.AutoField(primary_key=True)
    nombre_us = models.CharField(max_length=30)
    # tipo_us = models.CharField(max_length=30, default='si')
    # tipo_us = models.ForeignKey("TipoUS",on_delete=models.CASCADE)
    desc_us = models.TextField()
    #com_us = models.TextField()
    #historial_us = models.CharField(max_length=30)
    horas_estimadas = models.IntegerField(default=0)
    horas_trabajadas = models.IntegerField(default=0)
    encargado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    prioridad = [

        ('Baja','Baja'),
        ('Media','Media'),
        ('Alta','Alta'),

    ]
    prioridad_us = models.CharField(choices=prioridad, max_length=10, default='Baja')
    id_proyecto = models.ForeignKey("Proyectos", on_delete=models.CASCADE, null=True)
    id_sprint = models.ForeignKey("Sprint", on_delete=models.CASCADE, null=True, blank=True)
    id_tipo_user_story = models.ForeignKey("Tipo_User_Story", on_delete=models.CASCADE, null=True, blank=True)
    estado = models.TextField(default="To Do")
    @property
    def us_exist(self):
        return self.id_user_story>0


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


class Tipo_User_Story(models.Model):
    '''
        Modelo Tipo de user story
        fecha: 30/9/2022

            El modelo es utilizado para la creación de los diferentes tipos de US por proyecto
             Se define el modelo que cuenta con los detalles del rol, como su nombre, descripción, permisos que contendrá
             el permiso, y el rol al que pertenece el proyecto
    '''

    nombre_tipo_us = models.CharField(max_length=30)
    # id_estado = models.ManyToManyField("Estados", blank=True, db_table='estados_tipo_us')
    id_proyecto = models.ForeignKey("Proyectos",on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre_tipo_us
    
    @property
    def tipo_us_exist(self):
        return self.id_tipo_user_story_id>0


class Estados(models.Model):
    '''
        Modelo Estados
        fecha: 30/9/2022


             Se define el modelo que cuenta con los detalles de un estado para tipo de us, como su nombre y el tipo al que pertenece
            Este modelo es utilizado para definir los diferentes estados que pertencen para cada tipo de user story
    '''

    nombre_estado = models.CharField(max_length=30)
    posicion = models.IntegerField(default=0)
    id_tipo_user_story = models.ForeignKey("Tipo_User_Story", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre_estado


# lista_default = {to do, doing, done}
# Estados.objects.filter(id_estado__in_lista_default | id_tipo_user_story=id_tipo_user_story)

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
    '''
        Modelo Sprint
        fecha: 30/9/2022

            Se define el modelo que cuenta con los detalles de un sprint, como su nombre, descripción, estado entre otros detalles
            Este modelo es utilizado para definir los diferentes sprints que pertencen para cada proyecto
    '''

    id = models.AutoField(primary_key=True)
    nombre_sprint = models.CharField(max_length=30)
    desc_sprint = models.TextField()
    estado = [

        ('Planificado','Planificado'),
        ('Iniciado','Iniciado'),
        ('Cancelado','Cancelado'),
        ('Terminado','Terminado'),
        

    ]
    estado_sprint = models.CharField(choices=estado, default='Planificado', max_length=12)
    fecha_inicio = models.DateField(auto_now=True,blank=True,null=True)
    duracion_dias = models.IntegerField(null=True) #Duracion en dias habiles
    capacidad = models.IntegerField(default=0) #Capacidad de produccion
    id_proyecto = models.ForeignKey("Proyectos",on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.nombre_sprint

    @property
    def sprint_exist(self):
        return self.id_sprint>0


class Miembro_Sprint(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sprint = models.ForeignKey("Sprint", on_delete=models.CASCADE)
    horas_trabajo = models.IntegerField(null=True)

    def __str__(self):
        return self.usuario


class Reportes(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_report = models.CharField(max_length=30)
    desc_report = models.TextField()


class Backlogs(models.Model):
    id_proyecto = models.ForeignKey("Proyectos", on_delete=models.CASCADE)
    # list_us = models.ListField()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
