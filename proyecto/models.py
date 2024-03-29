# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class AccountBacklogs(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_proyecto = models.ForeignKey('AccountProyectos', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_backlogs'


class AccountKanban(models.Model):
    id = models.BigAutoField(primary_key=True)
    colum = models.IntegerField()
    fila = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'account_kanban'


class AccountMiembros(models.Model):
    id_proyecto = models.ForeignKey('AccountProyectos', models.DO_NOTHING)
    id_usuario = models.ForeignKey('AccountUsuarios', models.DO_NOTHING)
    id_rol = models.ForeignKey('AccountRoles', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_miembros'


class AccountPermisos(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre_permisos = models.CharField(max_length=30)
    desc_permisos = models.TextField()

    class Meta:
        managed = False
        db_table = 'account_permisos'


class AccountProyectos(models.Model):
    nombre_proyecto = models.CharField(max_length=30)
    desc_proyecto = models.TextField()
    estado_proyecto = models.CharField(max_length=30)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
         verbose_name = 'Proyecto'
         verbose_name_plural = 'Proyectos'
    
    def __str__(self):
        return self.title


class AccountReportes(models.Model):
    nombre_report = models.CharField(max_length=30)
    desc_report = models.TextField()

    class Meta:
        managed = False
        db_table = 'account_reportes'


class AccountReuniones(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre_reunion = models.CharField(max_length=30)
    desc_reunion = models.TextField()
    lugar_reunion = models.CharField(max_length=30)
    fecha_reunion = models.DateField()
    hora_reunion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'account_reuniones'


class AccountRoles(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=30)
    desc_rol = models.TextField()

    class Meta:
        managed = False
        db_table = 'account_roles'


class AccountSprint(models.Model):
    nombre_sprint = models.CharField(max_length=30)
    desc_sprint = models.TextField()
    estado_sprint = models.CharField(max_length=30)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        managed = False
        db_table = 'account_sprint'


class AccountSprintbacklog(models.Model):
    nombre_sprint_b = models.CharField(max_length=30)
    desc_sprint_b = models.TextField()

    class Meta:
        managed = False
        db_table = 'account_sprintbacklog'


class AccountTipous(models.Model):
    nombre_tipo_us = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'account_tipous'


class AccountUserstory(models.Model):
    nombre_us = models.CharField(max_length=30)
    prioridad_us = models.CharField(max_length=30)
    tipo_us = models.CharField(max_length=30)
    desc_us = models.TextField()
    com_us = models.TextField()
    historial_us = models.CharField(max_length=30)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        managed = False
        db_table = 'account_userstory'


class AccountUsuarios(models.Model):
    nombre_usuario = models.CharField(max_length=15)
    contrasena_usuario = models.CharField(max_length=10)
    estado_usuario = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'account_usuarios'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class SocialAuthAssociation(models.Model):
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'social_auth_association'
        unique_together = (('server_url', 'handle'),)


class SocialAuthCode(models.Model):
    email = models.CharField(max_length=254)
    code = models.CharField(max_length=32)
    verified = models.BooleanField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_auth_code'
        unique_together = (('email', 'code'),)


class SocialAuthNonce(models.Model):
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=65)

    class Meta:
        managed = False
        db_table = 'social_auth_nonce'
        unique_together = (('server_url', 'timestamp', 'salt'),)


class SocialAuthPartial(models.Model):
    token = models.CharField(max_length=32)
    next_step = models.SmallIntegerField()
    backend = models.CharField(max_length=32)
    data = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_auth_partial'


class SocialAuthUsersocialauth(models.Model):
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    extra_data = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_auth_usersocialauth'
        unique_together = (('provider', 'uid'),)
