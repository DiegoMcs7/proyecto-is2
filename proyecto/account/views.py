from datetime import datetime
from urllib.request import Request
from .models import Miembro_Sprint, Miembros, Profile, Proyectos, Rol, Sprint, UserStory
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import AddMembersForm, AddMembersSprintForm, ProyectosForm, RolForm, UserEditForm, UserRegistrationForm, detailsformuser, \
    SprintForm, UserStoryForm
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Permission
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
        user_form = UserRegistrationForm(request.POST,{'is_superuser':True})
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def update_us(request,id):

    User = get_user_model()
    users = User.objects.get(id=id)
    print(users)
    form = UserEditForm(request.POST or None, instance=users,initial={'id_usuario': id})

    if form.is_valid():
        form.save()
        return redirect('retrieve_user')

    return render(request, 'account/edit_us.html', {'users': users, 'form': form})


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
        form = ProyectosForm(request.POST, initial={'scrum_master': request.user.id})
        
        if form.is_valid():
            project = form.save(commit=False)
            project.manager = request.user
            project.save()
            #Creacion de los roles por defecto
            project_member = Proyectos.objects.filter(scrum_master=request.user.id).last()
            permisos= Permission.objects.all()
            permisos_prodOwner = permisos.filter(Q(content_type_id=1) | Q(content_type_id=9) | Q(content_type_id=11) | Q(codename__icontains="view"))
            permisos_miembros = permisos.filter(codename__icontains="view")
            permisos_prodOwner.union(permisos_miembros)
            rol_member1 = Rol.objects.create(rol="Scrum Master",desc_rol= "Scrum Master", proyecto=project_member)
            rol_member1.permisos.set(permisos)
            rol_member2 = Rol.objects.create(rol="Product Owner", desc_rol="Product Owner", proyecto=project_member)
            rol_member2.permisos.set(permisos_prodOwner)
            rol_member3 = Rol.objects.create(rol="Miembro", desc_rol="Miembro", proyecto=project_member)
            rol_member3.permisos.set(permisos_miembros)
            rol_member1.save()
            rol_member2.save()
            rol_member3.save()
            user_member = request.user
            miembro= Miembros.objects.create(id_usuario=user_member, id_proyecto=project_member)
            miembro.id_rol.add(rol_member1)
            miembro.save()
            return HttpResponseRedirect('/add_project?submitted=True')
    else:

        form = ProyectosForm(initial= {'scrum_master': request.user.id})

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
    members = Miembros.objects.all()
    user = request.user.id
    return render(request, 'project/project_list.html',
                  {'project_list': project_list,'members': members,'user': user})

def add_members(request, id):
    '''
        Agregar mimembro a un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden agregar miembros a diferentes proyectos.        
    '''
    project = Proyectos.objects.get(id=id)
    members = Miembros.objects.all()
    roles = Rol.objects.all()
    form = AddMembersForm(request.POST or None, pwd=project.id, initial={'id_proyecto': id})
    
    if form.is_valid():
        new_user = form.save()
        new_user.save()
        return redirect('/add_members/%d'%project.id)
    return render(request, 'project/add_members.html', {'project': project, 'form': form, 'members': members, 'roles': roles})

def update_members_project(request, id_proyecto, id_miembro):
    '''
        Editar un miembro del proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden editar miembros de un proyecto.
    '''
    project = Proyectos.objects.get(id=id_proyecto)
    members = Miembros.objects.get(id=id_miembro)
    roles = Rol.objects.all()
    form = AddMembersForm(request.POST or None, pwd=project.id, instance=members)
    if form.is_valid():
        form.save()
        return redirect('/add_members/%d'%id_proyecto)

    return render(request, 'project/update_members_project.html', {'project': project, 'members': members, 'form': form, 'roles': roles})

def all_roles(request, id_proyecto):
    '''
        Vista de todos los roles y permisos
        fecha: 25/9/2022

            Esta vista es la encargada de llamar al archivo roles_list.html con el fin de mostrar en pantalla la lista
            de todos los roles y permisos registrados en el sistema.       
    '''
    roles_list = Rol.objects.all()
    userid = request.user.id
    project = Proyectos.objects.get(id=id_proyecto)

    b = Miembros.objects.filter(id_usuario=userid,id_proyecto_id=id_proyecto).values_list('id')
    out = [item for t in b for item in t]
    a = Miembros.id_rol.through.objects.filter(miembros_id__in=out).values_list('rol_id')
    out = [item for t in a for item in t]
    a = Rol.permisos.through.objects.filter(rol_id__in=out).values_list('permission_id')
    out = [item for t in a for item in t]
    return render(request, 'roles_y_permisos/roles_list.html',{'roles_list': roles_list, 'out': out, 'project': project})


def add_rol(request, id_proyecto):

    '''
        Agregar rol a un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden agregar roles y permisos a diferentes proyectos.        
    '''
    submitted = False
    project = Proyectos.objects.get(id=id_proyecto)
    if request.method == "POST":
        form = RolForm(request.POST, initial={'proyecto': project})
        print(project.id)
        if form.is_valid():
            role = form.save()
            role.manager = request.user
            role.save()
            return HttpResponseRedirect('/roles/%d'%project.id)
    else:
        form = RolForm(initial={'proyecto': project})
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'roles_y_permisos/add_rol.html', {'form': form, 'submitted': submitted, 'project': project})

def update_rol(request, id, id_proyecto):
    '''
        Editar rol de un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden editar roles y permisos a diferentes proyectos.        
    '''
    role = Rol.objects.get(id=id)
    form = RolForm(request.POST or None, instance=role)
    project = Proyectos.objects.get(id=id_proyecto)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/roles/%d'%id_proyecto)
    return render(request, 'roles_y_permisos/update_rol.html', {'role': role, 'form': form}, {'project': project})

def delete_proyecto(request, id):
	project = Proyectos.objects.get(id=id)
	project.delete()
	return HttpResponseRedirect('/projects')
def delete_rol(request, id,id_proyecto):
	role = Rol.objects.get(id=id)
	role.delete()
	return HttpResponseRedirect('/roles/%d'%id_proyecto)

def delete_miembro_proyecto(request, id,id_proyecto):
	m = Miembros.objects.get(id=id)
	m.delete()
	return HttpResponseRedirect('/add_members/%d'%id_proyecto)

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

    form = SprintForm(request.POST or None, instance=sprint, initial={'id_proyecto': id_proyecto})
    if form.is_valid():
        form.save()
        return redirect('/sprint/%d' %id_proyecto)

    return render(request, 'sprint/update_sprint.html', {'sprint': sprint, 'form': form})


def add_members_sprint(request, id_proyecto, id_sprint):
    '''
        Agregar mimembro a un sprint
        fecha: 25/9/2022

            Funcion en la cual se pueden agregar miembros a diferentes sprints.        
    '''
    sprint = Sprint.objects.get(id=id_sprint)
    members_sprint = Miembro_Sprint.objects.all()
    form = AddMembersSprintForm(request.POST or None, pwd=id_proyecto, initial={'id': id_sprint,'sprint':id_sprint})
    x = id_proyecto
    y = id_sprint
    print(form['horas_trabajo'].value())
    if form.is_valid():
        sprint.capacidad = sprint.capacidad + form['horas_trabajo'].value()
        new_user = form.save()
        new_user.save()
        return redirect('/add_members_sprint/'+str(x)+'/'+str(y))
    return render(request, 'sprint/add_members_sprint.html',{'sprint': sprint, 'form': form, 'id_sprint': id_sprint, 'members_sprint': members_sprint})


def all_user_story(request, id):
    print('user_story')
    user_story = UserStory.objects.all()
    print(user_story)
    return render(request, 'user_story/user_story_list.html',
                  {'user_story_list': user_story, 'id_project': id})


def all_user_story_sprint_backlog(request, id):
    print('user_story')
    user_story = UserStory.objects.all()
    print(user_story)
    return render(request, 'user_story/user_story_list_sprint_backlog.html',
                  {'user_story_list': user_story, 'id_sprint': id})

def add_user_story(request, id_proyecto):
    user_story = UserStory.objects.all()
    form = UserStoryForm(request.POST or None, pwd=id_proyecto, initial={'id_proyecto': id_proyecto})

    if form.is_valid():
        print(form)
        new_user_story = form.save()
        new_user_story.save()
        return HttpResponseRedirect('/user_story/%d'%id_proyecto)
    return render(request, 'user_story/add_user_story.html',
                  {'user_story': user_story, 'form': form})


def update_user_story(request, id_proyecto, id_user_story):
    print('hola', id_user_story)
    user_story = UserStory.objects.get(id=id_user_story)
    form = UserStoryForm(request.POST or None, instance=user_story, pwd=id_proyecto, initial={'id_proyecto': id_proyecto})
    if form.is_valid():
        form.save()
        return redirect('/user_story/%d'%id_proyecto)

    return render(request, 'user_story/update_user_story.html', {'user_story': user_story, 'form': form})

#Edit de miembros del Equipo Proyecto y Sprint



def update_members_sprint(request, id_proyecto, id_sprint,id_usuario):
    '''
        Editar un miembro del sprint
        fecha: 25/9/2022

            Funcion en la cual se pueden editar miembros de un sprint.        
    '''
    members = Miembro_Sprint.objects.get(id=id_usuario)
    form = AddMembersSprintForm(request.POST or None, instance=members, initial={'usuario':id_usuario,'id_proyecto': id_proyecto,'sprint': id_sprint,})
    x = id_proyecto
    y = id_sprint
    if form.is_valid():
        form.save()
        return redirect('/add_members_sprint/'+str(x)+'/'+str(y))

    return render(request, 'project/update_members_sprint.html', {'id_proyecto': id_proyecto,'members': members, 'form': form})

