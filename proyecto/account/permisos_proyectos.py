from datetime import datetime
from gc import get_objects
from urllib import response
from urllib import request
from urllib.request import Request
from .models import Estados, Miembro_Sprint, Miembros, Profile, Proyectos, Rol, Sprint, Tipo_User_Story, UserStory
from django.shortcuts import render, redirect
from .forms import AddMembersForm, AddMembersSprintForm, EstadosForm, ProyectosForm, RolForm, TipoUsForm, UserEditForm, \
    UserRegistrationForm, \
    SprintForm, UserStoryForm
from django.contrib.auth.decorators import login_required
from tablib import Dataset
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Permission
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from .sources import *
from django.http import HttpResponseForbidden


def permisos_proyectos(user_id):
        # retorna un diccionario que contiene todos los permisos que posee el usuario en los distintos proyectos
        proyectos = Proyectos.objects.all().values_list('id')
        id_proyectos = [item for t in proyectos for item in t]
        permisos = {}
        for id_proyecto in id_proyectos:
                b = Miembros.objects.filter(id_usuario=user_id, id_proyecto_id=id_proyecto).values_list('id')
                out = [item for t in b for item in t]
                a = Miembros.id_rol.through.objects.filter(miembros_id__in=out).values_list('rol_id')
                out = [item for t in a for item in t]
                a = Rol.permisos.through.objects.filter(rol_id__in=out).values_list('permission_id')
                out = [item for t in a for item in t]
                a = Permission.objects.filter(id__in=out).values_list('name')
                out = [item for t in a for item in t]
                permisos[id_proyecto] = out

        return permisos