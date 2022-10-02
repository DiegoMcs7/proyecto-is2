from import_export import resources
from .models import Rol, Tipo_User_Story

class RolResource(resources.ModelResource):
    class Meta:
        model = Rol

class Tipo_USResource(resources.ModelResource):
    class Meta:
        model = Tipo_User_Story