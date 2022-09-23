from .models import Profile, Proyectos, Rol
from django.shortcuts import render, redirect
from .forms import AddMembersForm, ProyectosForm, RolForm, UserRegistrationForm,detailsformuser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


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
    User = get_user_model()
    object = User.objects.get(id=id)
    print(object)
    return render(request, 'account/edit.html', {'object': object})


def update_us(request, id):
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
    User = get_user_model()
    users = User.objects.all()

    return render(request, 'account/retrieve_user.html', {'users': users})


# CRUD PROYECTO
def edit(request, id):
    object = Proyectos.objects.get(id=id)
    return render(request, 'project/edit_project.html', {'object': object})


# Nuevo crud para proyecto
def add_project(request):
    submitted = False
    if request.method == "POST":
        form = ProyectosForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.manager = request.user
            project.save()
            return HttpResponseRedirect('/add_project?submitted=True')
    else:

        form = ProyectosForm

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'project/add_project.html', {'form': form, 'submitted': submitted})


def update_project(request, id):
    project = Proyectos.objects.get(id=id)

    form = ProyectosForm(request.POST or None, instance=project)

    if form.is_valid():
        form.save()
        return redirect('list-projects')

    return render(request, 'project/update_project.html', {'project': project, 'form': form})


def all_projects(request):
    project_list = Proyectos.objects.all()
    return render(request, 'project/project_list.html',
                  {'project_list': project_list})


def add_members(request, id):
    project = Proyectos.objects.get(id=id)
    form = AddMembersForm(request.POST or None, instance=project, initial={'id_proyecto': id})


    if form.is_valid():
        form.save()
        return redirect('list-projects')

    return render(request, 'project/add_members.html', {'project': project, 'form': form})

def all_roles(request):
    roles_list = Rol.objects.all()

    return render(request, 'roles_y_permisos/roles_list.html',
                  {'roles_list': roles_list})

def add_rol(request):
    submitted = False
    if request.method == "POST":
        form = RolForm(request.POST)
        if form.is_valid():
            role = form.save(commit=False)
            role.manager = request.user
            role.save()
            return HttpResponseRedirect('/add_rol?submitted=True')
    else:

        form = RolForm

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'roles_y_permisos/add_rol.html', {'form': form, 'submitted': submitted})

def update_rol(request, id):
    role = Rol.objects.get(id=id)
    form = RolForm(request.POST or None, instance=role)

    if form.is_valid():
        form.save()
        return redirect('list-roles')

    return render(request, 'roles_y_permisos/update_rol.html', {'role': role, 'form': form})