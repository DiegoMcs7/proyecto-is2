from datetime import datetime
from urllib.request import Request
from .models import Miembro_Sprint, Miembros, Profile, Proyectos, Rol, Sprint
from django.shortcuts import render, redirect
from .forms import AddMembersForm, AddMembersSprintForm, ProyectosForm, RolForm, UserRegistrationForm,detailsformuser, SprintForm
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

@login_required()
def tablero(request):
    '''
        Vistas
        fecha: 20/8/2022

        Una función de visualización es una función de Python que toma una solicitud web y devuelve una respuesta web .
               Esta vista es la encargada de llamar al archivo tablero.html con el fin de mostrar en pantalla el menu
               luego de la peticion correspondiente
    '''
    return render(request, 'account/tablero.html', {'section': 'tablero'})


def register(request):
    '''
        Registrar usuario
        fecha: 25/9/2022

        Funcion en la cual se puede registrar un usuario al sistema para que pueda acceder a las diferentes opciones que
        ofrece el mismo.
    '''
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def edit_us(request, id):
    '''
        Editar usuario
        fecha: 25/9/2022

        Funcion en la cual se pueden editar los diferentes campos con los que cuenta un usuario. 
    '''
    User = get_user_model()
    object = User.objects.get(id=id)
    print(object)
    return render(request, 'account/edit.html', {'object': object})


def update_us(request, id):
    '''
        Editar usuario
        fecha: 25/9/2022

        Funcion en la cual se pueden editar los diferentes campos con los que cuenta un usuario. 
    '''
    if request.method == 'POST':
        User = get_user_model()
        object = User.objects.get(id=id)
        form = detailsformuser(request.POST, instance=object)
        if form.is_valid():
            form.save()
            object = User.objects.all()
            messages.success(request, 'Se han actualizado los datos!')
            return redirect('retrieve_user')
        else:
            messages.error(request, 'Error al actualizar datos.')
        return render(request, 'account/edit.html', {'object': object, 'form': form})


def retrieve_user(request):
    '''
        Vista de todos los usuarios
        fecha: 25/9/2022

            Esta vista es la encargada de llamar al archivo retrieve_user.html con el fin de mostrar en pantalla la lista
            de todos los usuarios registrados en el sistema.       
    '''
    User = get_user_model()
    users = User.objects.all()

    return render(request, 'account/retrieve_user.html', {'users': users})

# Nuevo crud para proyecto
def add_project(request):
    '''
        Agregar un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden agregar proyectos.        
    '''
    submitted = False
    if request.method == "POST":
        form = ProyectosForm(request.POST)
        
        if form.is_valid():
            project = form.save(commit=False)
            project.manager = request.user
            project.save()
            #############CORREGIR LAST############
            project_member = Proyectos.objects.last()
            user_member = User.objects.get(id=form['scrum_master'].value())
            rol_member = Rol.objects.get(id=1)
            Miembros.objects.create(id_usuario=user_member, id_proyecto=project_member)
            Miembros.objects.last().id_rol.add(rol_member)
            return HttpResponseRedirect('/add_project?submitted=True')
    else:

        form = ProyectosForm

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'project/add_project.html', {'form': form, 'submitted': submitted})


def update_project(request, id):
    '''
        Editar un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden editar proyectos.        
    '''
    project = Proyectos.objects.get(id=id)

    form = ProyectosForm(request.POST or None, instance=project)

    if form.is_valid():
        form.save()
        return redirect('list-projects')

    return render(request, 'project/update_project.html', {'project': project, 'form': form})


def all_projects(request):
    '''
        Vista de todos los proyectos
        fecha: 25/9/2022

            Esta vista es la encargada de llamar al archivo project_list.html con el fin de mostrar en pantalla la lista
            de todos los proyectos registrados en el sistema.       
    '''
    project_list = Proyectos.objects.all()
    return render(request, 'project/project_list.html',
                  {'project_list': project_list})

def add_members(request, id):
    '''
        Agregar mimembro a un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden agregar miembros a diferentes proyectos.        
    '''
    project = Proyectos.objects.get(id=id)
    members = Miembros.objects.all()
    roles = Rol.objects.all()
    form = AddMembersForm(request.POST or None, initial={'id_proyecto': id})
    
    if form.is_valid():
        new_user = form.save()
        new_user.save()
        return redirect('list-projects')
    return render(request, 'project/add_members.html', {'project': project, 'form': form, 'members': members, 'roles': roles})

def all_roles(request):
    '''
        Vista de todos los roles y permisos
        fecha: 25/9/2022

            Esta vista es la encargada de llamar al archivo roles_list.html con el fin de mostrar en pantalla la lista
            de todos los roles y permisos registrados en el sistema.       
    '''
    roles_list = Rol.objects.all()
    userid = request.user.id

    b = Miembros.objects.filter(id_usuario=userid).values_list('id')
    out = [item for t in b for item in t]
    a = Miembros.id_rol.through.objects.filter(miembros_id__in=out).values_list('rol_id')
    out = [item for t in a for item in t]
    a = Rol.permisos.through.objects.filter(rol_id__in=out).values_list('permission_id')
    out = [item for t in a for item in t]

    return render(request, 'roles_y_permisos/roles_list.html',
                  {'roles_list': roles_list,'out':out})

def add_rol(request):
    '''
        Agregar rol a un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden agregar roles y permisos a diferentes proyectos.        
    '''
    submitted = False
    if request.method == "POST":
        form = RolForm(request.POST)
        if form.is_valid():
            role = form.save()
            role.manager = request.user
            role.save()
            return HttpResponseRedirect('/add_rol?submitted=True')
    else:

        form = RolForm

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'roles_y_permisos/add_rol.html', {'form': form, 'submitted': submitted})

def update_rol(request, id):
    '''
        Editar rol de un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden editar roles y permisos a diferentes proyectos.        
    '''
    role = Rol.objects.get(id=id)
    form = RolForm(request.POST or None, instance=role)

    if form.is_valid():
        form.save()
        return redirect('list-roles')

    return render(request, 'roles_y_permisos/update_rol.html', {'role': role, 'form': form})

# CRUD para sprint

def all_sprints(request,id):
    '''
        Vista de todos los sprints creados para cada proyecto
        fecha: 25/9/2022

            Esta vista es la encargada de llamar al archivo sprint_list.html con el fin de mostrar en pantalla la lista
            de todos los sprints creados para cada proyecto.       
    '''
    sprint_list = Sprint.objects.all()
                                                             
    return render(request, 'sprint/sprint_list.html',
                  {'sprint_list': sprint_list,'id_project': id})

def add_sprint(request,id):
    '''
        Agregar sprint a un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden agregar sprint para diferentes proyectos.        
    '''
    submitted = False
    project = Proyectos.objects.get(id=id)
    x = project.id
    print(x)
    if request.method == "POST":
        form = SprintForm(request.POST, initial={'id_proyecto':x})
        if form.is_valid():
            sprint = form.save()
            sprint.manager = request.user
            sprint.save()
            return HttpResponseRedirect('/sprint/%d'%id)
    else:

        form = SprintForm(initial={'id_proyecto':x})
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'sprint/add_sprint.html', {'form': form, 'submitted': submitted})


def update_sprint(request, id_proyecto, id_sprint):
    '''
        Editar sprint de un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden editar sprint a diferentes proyectos.        
    '''
    sprint = Sprint.objects.get(id=id_sprint)

    form = SprintForm(request.POST or None, instance=sprint)
    if form.is_valid():
        form.save()
        return redirect('/sprint/%d'%id_proyecto)

    return render(request, 'sprint/update_sprint.html', {'sprint': sprint, 'form': form})


def add_members_sprint(request, id_proyecto, id_sprint):
    '''
        Agregar mimembro a un sprint
        fecha: 25/9/2022

            Funcion en la cual se pueden agregar miembros a diferentes sprints.        
    '''
    sprint = Sprint.objects.get(id=id_sprint)
    members_sprint = Miembro_Sprint.objects.all()
    form = AddMembersSprintForm(request.POST or None, pwd=id_proyecto, initial={'id': id_sprint})
    
    if form.is_valid():
        new_user = form.save()
        new_user.save()
        return redirect('/sprint/%d'%id_sprint)
    return render(request, 'sprint/add_members_sprint.html',{'sprint': sprint, 'form': form, 'members_sprint': members_sprint})
