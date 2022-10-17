from datetime import datetime
from gc import get_objects
from urllib import response
from urllib.request import Request
from .permisos import permisos
from .models import Estados, Miembro_Sprint, Miembros, Profile, Proyectos, Rol, Sprint, Tipo_User_Story, UserStory
from django.shortcuts import render, redirect
from .forms import AddMembersForm, AddMembersSprintForm, EstadosForm, ProyectosForm, RolForm, TipoUsForm, \
    UsPrioridadForm, UserEditForm, \
    UserRegistrationForm, \
    SprintForm, UserStoryForm, AsignarEstadosTipoUsForm, UserStorySprintForm
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

@login_required
def tablero(request):
    '''
        Vistas
        fecha: 20/8/2022

        Una función de visualización es una función de Python que toma una solicitud web y devuelve una respuesta web .
               Esta vista es la encargada de llamar al archivo tablero.html con el fin de mostrar en pantalla el menu
               luego de la peticion correspondient
    '''

    return render(request, 'account/tablero.html', {'section': 'tablero'})

def kanban(request):

    return render(request, 'kanban/index.html')


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
            project_member = Proyectos.objects.filter(scrum_master=project.scrum_master.id).last()
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
            user_member = project.scrum_master
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

    # a = Sprint.objects.filter(Q(id_proyecto_id=id),
    #                           Q(estado_sprint="Iniciado") | Q(estado_sprint="Iniciado")).values_list('id')
    # out = [item for t in a for item in t]
    project_state = Proyectos.objects.get(id=id)
    if project_state.estado_proyecto == 'Cancelado':
        messages.error(request, 'No puedes realizar la acción ya que el proyecto ha sido cancelado')
    elif project_state.estado_proyecto == 'Finalizado':
        messages.error(request, 'No puedes realizar la acción ya que el proyecto ha sido finalizado')
    else:
        if form.is_valid():
            form.save()
            return redirect('list-projects')

    return render(request, 'project/update_project.html', {'project': project, 'form': form})


def action_project(request, id):
    '''
        Seleccionar accion por proyecto
        fecha: 16/10/2022

            Funcion en la cual se seleccionan las acciones por proyecto
    '''
    project = Proyectos.objects.get(id=id)

    return render(request, 'project/action_project.html', {'project': project})

def inicializar_proyecto(request, id):

    Proyectos.objects.filter(id=id).update(estado_proyecto='Iniciado')

    return redirect('list-projects')

def cancelar_proyecto(request, id):

    Proyectos.objects.filter(id=id).update(estado_proyecto='Cancelado')

    return redirect('list-projects')


def finalizar_proyecto(request, id):

    Proyectos.objects.filter(id=id).update(estado_proyecto='Finalizado')
    project_state = Proyectos.objects.get(id=id)
    if project_state.estado_proyecto == 'Cancelado':
        messages.error(request, 'No puedes realizar la acción ya que el proyecto ha sido cancelado')
    elif project_state.estado_proyecto == 'Finalizado':
        messages.error(request, 'No puedes realizar la acción ya que el proyecto ha sido finalizado')

    return redirect('list-projects')

@login_required
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

class proyecto_iterador:

    list_id = 0
    indice_permiso = 0

    def __init__(self, list_id, indice_permiso): 
        self.list_id = list_id 
        self.indice_permiso = indice_permiso
    
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

    out = permisos(request.user.id,id)
    
    if form.is_valid():
        new_user = form.save()
        new_user.save()
        return redirect('/add_members/%d'%project.id)
    return render(request, 'project/add_members.html', {'project': project, 'form': form, 'members': members, 'roles': roles, 'out': out})

def add_miembros(request, id):
    '''
        Agregar mimembro a un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden agregar miembros a diferentes proyectos.        
    '''
    project = Proyectos.objects.get(id=id)
    members = Miembros.objects.all()
    roles = Rol.objects.all()
    form = AddMembersForm(request.POST or None, pwd=project.id, initial={'id_proyecto': id})

    out = permisos(request.user.id,id)
    
    if form.is_valid():
        new_user = form.save()
        new_user.save()
        return redirect('/add_members/%d'%project.id)
    return render(request, 'project/add_miembro.html', {'project': project, 'form': form, 'members': members, 'roles': roles, 'out': out})

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

@login_required
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
    a = Permission.objects.filter(id__in=out).values_list('name')
    out = [item for t in a for item in t]
    # En linea 60 de roles_list utilizar los nombres de los permisos Ejempo:'can view rol' en vez del id 45
    # en otras metodos no se utiliza out pero en los templates si se utiliza?

    return render(request, 'roles_y_permisos/roles_list.html',
                  {'roles_list': roles_list, 'out': out,'project': project})


def list_permisos(request, id_proyecto, id_rol):

    roles_list = Rol.objects.all()
    project = Proyectos.objects.get(id=id_proyecto)

    return render(request, 'roles_y_permisos/permisos_list.html',
                  {'roles_list': roles_list, 'project': project, 'id_rol': id_rol})


def add_rol(request,id_proyecto):
    '''
        Agregar rol a un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden agregar roles y permisos a diferentes proyectos.        
    '''
    submitted = False
    project = Proyectos.objects.get(id=id_proyecto)
    if request.method == "POST":

        form = RolForm(request.POST, initial={'proyecto': project})

        if form.is_valid():
            print('guardar')
            role = form.save()
            role.manager = request.user
            role.save()
            return HttpResponseRedirect('/roles/%d'%id_proyecto)
    else:
        form = RolForm(initial={'proyecto': project})
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'roles_y_permisos/add_rol.html', {'form': form, 'submitted': submitted,'project':project})


def update_rol(request, id,id_proyecto):
    '''
        Editar rol de un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden editar roles y permisos a diferentes proyectos.        
    '''
    project = Proyectos.objects.get(id=id_proyecto)
    role = Rol.objects.get(id=id)
    form = RolForm(request.POST or None, instance=role)
    project = Proyectos.objects.get(id=id_proyecto)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/roles/%d'%id_proyecto)

    return render(request, 'roles_y_permisos/update_rol.html', {'role': role, 'form': form, 'project': project})


def delete_proyecto(request, id):
    project = Proyectos.objects.get(id=id)
    project.delete()
    return HttpResponseRedirect('/projects')


def delete_rol(request, id, id_proyecto):
    role = Rol.objects.get(id=id)
    role.delete()
    return HttpResponseRedirect('/roles/%d' % id_proyecto)


def delete_miembro_proyecto(request, id, id_proyecto):
    m = Miembros.objects.get(id=id)
    m.delete()
    return HttpResponseRedirect('/add_members/%d' % id_proyecto)

def export_roles(request, id_proyecto):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        rol_resource = RolResource()
        dataset = rol_resource.export(queryset=Rol.objects.filter(proyecto_id=id_proyecto))
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response

    return render(request, 'import_export/export.html', {'proyecto': id_proyecto})

def import_roles(request,id_proyecto):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        rol_resource = RolResource()
        dataset = Dataset()
        new_roles = request.FILES['importData']
        if file_format == 'CSV':
            imported_data = dataset.load(new_roles.read().decode('utf-8'),format='csv')
            result = rol_resource.import_data(dataset, dry_run=True)
            print(imported_data)
            if not result.has_errors():
                # Import now
                for i in range(imported_data.height):
                    r = imported_data.pop()
                    rol_nuevo = Rol.objects.create(rol=r[1], desc_rol=r[2], proyecto=Proyectos.objects.get(id=id_proyecto))
                    perm = list(r[3].split(","))
                    perm1= []
                    for x in perm:
                        perm1.append(int(x))
                    perm_tuple= tuple(perm1)
                    p = Permission.objects.filter(id__in= perm_tuple)
                    rol_nuevo.permisos.set(p)
                    rol_nuevo.save()
        elif file_format == 'JSON':
            imported_data = dataset.load(new_roles.read().decode('utf-8'),format='json')
            # Testing data import
            result = rol_resource.import_data(dataset, dry_run=True)
            if not result.has_errors():
                # Import now
                for i in range(imported_data.height):
                    r = imported_data.pop()
                    rol_nuevo = Rol.objects.create(rol=r[1], desc_rol=r[2], proyecto=Proyectos.objects.get(id=id_proyecto))
                    perm = list(r[3].split(","))
                    perm1 = []
                    for x in perm:
                        perm1.append(int(x))
                    perm_tuple = tuple(perm1)
                    p = Permission.objects.filter(id__in=perm_tuple)
                    rol_nuevo.permisos.set(p)
                    rol_nuevo.save()
            print(result)

    return render(request, 'import_export/import.html', {'proyecto': id_proyecto})


# CRUD para sprint

@login_required
def all_sprints(request,id):
    '''
        Vista de todos los sprints creados para cada proyecto
        fecha: 25/9/2022

            Esta vista es la encargada de llamar al archivo sprint_list.html con el fin de mostrar en pantalla la lista
            de todos los sprints creados para cada proyecto.       
    '''
    sprint_list = Sprint.objects.all()
    project = Proyectos.objects.get(id=id)

    out = permisos(request.user.id,id)
                                                             
    return render(request, 'sprint/sprint_list.html',
                  {'sprint_list': sprint_list,'id_project': id, 'project': project, 'out': out})


def add_sprint(request,id):
    '''
        Agregar sprint a un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden agregar sprint para diferentes proyectos.        
    '''
    submitted = False
    project = Proyectos.objects.get(id=id)
    x = project.id
    if request.method == "POST":
        form = SprintForm(request.POST, initial={'id_proyecto':x})
        a = Sprint.objects.filter(Q(id_proyecto_id=id), Q(estado_sprint="Iniciado")).values_list('id')
        out = [item for t in a for item in t]

        if form.is_valid() and len(out)==0:
            sprint = form.save()
            sprint.manager = request.user
            sprint.save()

            return HttpResponseRedirect('/sprint/%d'%id)
        else:
            messages.error(request, 'Sprints no finalizados.')
            
    else:

        form = SprintForm(initial={'id_proyecto':x})
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'sprint/add_sprint.html', {'form': form, 'submitted': submitted, 'id_proyecto': id, 'project': project})


def update_sprint(request, id_proyecto, id_sprint):
    '''
        Editar sprint de un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden editar sprint a diferentes proyectos.        
    '''
    sprint = Sprint.objects.get(id=id_sprint)
    project = Proyectos.objects.get(id=id_proyecto)


    form = SprintForm(request.POST or None, instance=sprint, initial={'id_proyecto': id_proyecto})
    if form.is_valid():
        form.save()
        return redirect('/sprint/%d' %id_proyecto)

    return render(request, 'sprint/update_sprint.html', {'sprint': sprint, 'form': form, 'id_proyecto': id_proyecto, 'project': project})


def add_members_sprint(request, id_proyecto, id_sprint):
    '''
        Agregar mimembro a un sprint
        fecha: 25/9/2022

            Funcion en la cual se pueden agregar miembros a diferentes sprints.        
    '''
    sprint = Sprint.objects.get(id=id_sprint)
    project = Proyectos.objects.get(id=id_proyecto)
    members_sprint = Miembro_Sprint.objects.all()
    form = AddMembersSprintForm(request.POST or None, pwd=id_proyecto, initial={'id': id_sprint,'sprint':id_sprint})
    x = id_proyecto
    y = id_sprint

    if form.is_valid():
        sprint.capacidad = sprint.capacidad + int(form['horas_trabajo'].value())
        new_user = form.save()
        new_user.save()
        return redirect('/add_members_sprint/'+str(x)+'/'+str(y))
    return render(request, 'sprint/add_members_sprint.html',{'sprint': sprint, 'form': form, 'id_sprint': id_sprint, 'members_sprint': members_sprint, 'id_proyecto': id_proyecto, 'project': project})


def add_miembros_sprint(request, id_proyecto, id_sprint):
    '''
        Agregar mimembro a un sprint
        fecha: 25/9/2022

            Funcion en la cual se pueden agregar miembros a diferentes sprints.        
    '''
    sprint = Sprint.objects.get(id=id_sprint)
    project = Proyectos.objects.get(id=id_proyecto)
    members_sprint = Miembro_Sprint.objects.all()
    form = AddMembersSprintForm(request.POST or None, pwd=id_proyecto, initial={'id': id_sprint,'sprint':id_sprint})
    x = id_proyecto
    y = id_sprint
    if form.is_valid():
        new_user = form.save()
        sprint.capacidad = sprint.capacidad + new_user.horas_trabajo * sprint.duracion_dias
        sprint.save()
        print(sprint.capacidad)
        new_user.save()
        return redirect('/add_members_sprint/'+str(x)+'/'+str(y))
    return render(request, 'sprint/add_miembros_sprint.html',{'sprint': sprint, 'form': form, 'id_sprint': id_sprint, 'members_sprint': members_sprint, 'id_proyecto': id_proyecto, 'project': project})


def all_user_story(request, id):

    user_story = UserStory.objects.all()
    project = Proyectos.objects.get(id=id)

    return render(request, 'user_story/user_story_list.html',
                  {'user_story_list': user_story, 'id_project': id, 'project': project})


def all_user_story_sprint_backlog(request, id):

    user_story = UserStory.objects.all()
    s= Sprint.objects.get(id=id)
    project = Proyectos.objects.get(id=s.id_proyecto_id)
    out = permisos(request.user.id,id)

    return render(request, 'user_story/user_story_list_sprint_backlog.html',
                  {'user_story_list': user_story, 'id_sprint': id, 'id_proyecto': s.id_proyecto_id, 'project': project, 'out': out})


def product_backlog_sprint(request, id_proyecto, id_sprint):

    user_story = UserStory.objects.all()
    sprint = Sprint.objects.get(id=id_sprint)
    project = Proyectos.objects.get(id=id_proyecto)

    return render(request, 'user_story/all_user_story_sprint_backlog.html',
                  {'user_story_list': user_story, 'sprint': sprint, 'id_project': id_proyecto})


def add_user_story(request, id_proyecto):
    user_story = UserStory.objects.all()
    project = Proyectos.objects.get(id=id_proyecto)
    form = UserStoryForm(request.POST or None, pwd=id_proyecto, initial={'id_proyecto': id_proyecto})
    if form.is_valid():

        new_user_story = form.save()
        new_user_story.save()
        return HttpResponseRedirect('/user_story/%d'%id_proyecto)

    return render(request, 'user_story/add_user_story.html',
                  {'user_story': user_story, 'form': form, 'id_proyecto': id_proyecto, 'project': project})


def update_user_story(request, id_proyecto, id_user_story):

    user_story = UserStory.objects.get(id=id_user_story)
    project = Proyectos.objects.get(id=id_proyecto)
    form = UserStoryForm(request.POST or None, instance=user_story, pwd=id_proyecto, initial={'id_proyecto_id': id_proyecto})
    if form.is_valid():
        form.save()
        return redirect('/product-backlog-sprint/%d'%id_proyecto)

    return render(request, 'user_story/update_user_story.html', {'user_story': user_story, 'form': form, 'id_proyecto': id_proyecto, 'project': project})


def update_sprint_user_story(request, id_proyecto, id_user_story, id_sprint):

    user_story = UserStory.objects.get(id=id_user_story)
    sprint = Sprint.objects.get(id=id_sprint)
    project = Proyectos.objects.get(id=id_proyecto)
    form = UserStorySprintForm(request.POST or None, instance=user_story,initial={'id_sprint': id_sprint})
    print('Entra')
    if form.is_valid():
        new_user = form.save()
        aux = sprint.capacidad - new_user.horas_estimadas
        print(aux)
        print()
        if aux >= 0:
            new_user.save()
            sprint.capacidad = sprint.capacidad - new_user.horas_estimadas
            sprint.save()
        else:
            user_story.id_sprint = None
            user_story.save()
            messages.error(request, 'La capacidad del sprint ya ha sido rebasada')

        return redirect('/product_backlog_sprint/'+str(id_proyecto)+'/'+str(id_sprint))

    return render(request, 'user_story/update_user_story.html', {'user_story': user_story, 'form': form, 'id_proyecto': id_proyecto, 'project': project})




def update_prioridad_user_story(request, id_proyecto, id_user_story):

    user_story = UserStory.objects.get(id=id_user_story)
    project = Proyectos.objects.get(id=id_proyecto)
    form = UsPrioridadForm(request.POST or None, instance=user_story, initial={'id_proyecto_id': id_proyecto})
    if form.is_valid():
        form.save()
        return redirect('/user_story/%d'%id_proyecto)

    return render(request, 'user_story/update_prioridad_us.html', {'user_story': user_story, 'form': form, 'id_proyecto': id_proyecto, 'project': project})


#Edit de miembros del Equipo Proyecto y Sprint


def update_members_sprint(request, id_proyecto, id_sprint,id_usuario):
    '''
        Editar un miembro del sprint
        fecha: 25/9/2022

            Funcion en la cual se pueden editar miembros de un sprint.        
    '''
    members = Miembro_Sprint.objects.get(id=id_usuario)
    project = Proyectos.objects.get(id=id_proyecto)
    form = AddMembersSprintForm(request.POST or None, instance=members, initial={'usuario':id_usuario,'id_proyecto': id_proyecto,'sprint': id_sprint})
    x = id_proyecto
    y = id_sprint
    if form.is_valid():
        form.save()
        return redirect('/add_members_sprint/'+str(x)+'/'+str(y))

    return render(request, 'project/update_members_sprint.html', {'id_proyecto': id_proyecto, 'members': members, 'form': form, 'project': project})

#CRUD ESTADOS

def all_estados(request,id_proyecto,id_tipo_us):
    '''
        Vista de todos los estados creados para cada proyecto
        fecha: 25/9/2022

            Esta vista es la encargada de llamar al archivo sprint_list.html con el fin de mostrar en pantalla la lista
            de todos los sprints creados para cada proyecto.       
    '''
    estados_list = Estados.objects.filter(id_tipo_user_story=id_tipo_us)
    project = Proyectos.objects.get(id=id_proyecto)
    all_estados = Estados.objects.all()
    estados = Tipo_User_Story.id_estado.through.objects.filter(tipo_user_story_id=id_tipo_us).values_list('estados_id')
    out = [item for t in estados for item in t]

    pout = permisos(request.user.id,id_proyecto)
                                                       
    return render(request, 'estados/estados_list.html',
                  {'estados_list': estados_list,'id_proyecto': id_proyecto,'id_tipo_us': id_tipo_us, 'project': project, 'all_estados': all_estados, 'out': out, 'pout': pout})

def add_estados(request,id_proyecto,id_tipo_us):
    '''
        Agregar estados a un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden agregar estados para diferentes proyectos.
    '''
    submitted = False
    project = Proyectos.objects.get(id=id_proyecto)
    x = project.id
    y = id_tipo_us

    if request.method == "POST":
        form = EstadosForm(request.POST, initial={'id_tipo_user_story':y})
        if form.is_valid():
            sprint = form.save()
            sprint.manager = request.user
            sprint.save()
            return redirect('/estados/'+str(x)+'/'+str(y))
    else:

        form = EstadosForm(initial={'id_tipo_user_story':y})
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'estados/add_estados.html', {'form': form,'id_proyecto': id_proyecto,'id_tipo_us': id_tipo_us, 'submitted': submitted, 'project': project})


def update_estados(request,id_proyecto,id_tipo_us,id_estado):
    '''
        Editar estados de un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden editar estados a diferentes proyectos.
    '''
    project = Proyectos.objects.get(id=id_proyecto)
    tipous = Tipo_User_Story.objects.get(id=id_tipo_us)
    nombre_estado = Estados.objects.get(id=id_estado)
    x = project.id
    y = id_tipo_us
    form = EstadosForm(request.POST or None, instance=tipous, initial={'id_tipo_user_story': id_tipo_us, 'nombre_estado': nombre_estado.nombre_estado})
    if form.is_valid():
        print(form)
        form.save()
        return redirect('/estados/'+str(x)+'/'+str(y))

    return render(request, 'estados/update_estados.html', {'id_proyecto': id_proyecto,'tipous': tipous, 'form': form, 'project': project})

#CRUD TIPOS_US

def all_tipos_us(request,id_proyecto):
    '''
        Vista de todos los tipo de user story para cada proyecto
        fecha: 25/9/2022

            Esta vista es la encargada de llamar al archivo tipos_us_list.html con el fin de mostrar en pantalla la lista
            de todos los tipos de user story creados para cada proyecto.
    '''
    tipos_us_list = Tipo_User_Story.objects.all()
    project = Proyectos.objects.get(id=id_proyecto)

    out = permisos(request.user.id,id_proyecto)    

    return render(request, 'tipos_us/tipos_us_list.html',
                  {'tipos_us_list': tipos_us_list,'id_proyecto': id_proyecto, 'project': project, 'out': out})

def add_tipos_us(request,id):
    '''
        Agregar tipo de user story a un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden agregar tipo de user story para diferentes proyectos.
    '''
    submitted = False
    project = Proyectos.objects.get(id=id)
    x = project.id
    out = permisos(request.user.id,id)
    if request.method == "POST":
        form = TipoUsForm(request.POST, initial={'id_proyecto':x})
        if form.is_valid():
            sprint = form.save()
            sprint.manager = request.user
            sprint.save()
            estado1 = Estados.objects.create(nombre_estado="To Do", id_tipo_user_story=Tipo_User_Story.objects.last())
            estado2 = Estados.objects.create(nombre_estado="Doing", id_tipo_user_story=Tipo_User_Story.objects.last())
            estado3 = Estados.objects.create(nombre_estado="Done", id_tipo_user_story=Tipo_User_Story.objects.last())
            estado1.save()
            estado2.save()
            estado3.save()

            return HttpResponseRedirect('/tipos_us/%d'%id)
    else:

        form = TipoUsForm(initial={'id_proyecto':x})
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'tipos_us/add_tipos_us.html', {'form': form, 'submitted': submitted, 'id_proyecto': id, 'project': project,'out': out,})


def update_tipos_us(request,id_proyecto,id_tipo_us):
    '''
        Editar tipo de user de un proyecto
        fecha: 25/9/2022

            Funcion en la cual se pueden editar tipo de user a diferentes proyectos.
    '''
    tipous = Tipo_User_Story.objects.get(id=id_tipo_us)
    project = Proyectos.objects.get(id=id_proyecto)

    form = TipoUsForm(request.POST or None, instance=tipous, initial={'id_proyecto': id_proyecto})
    if form.is_valid():
        form.save()
        return redirect('/tipos_us/%d' %id_proyecto)

    return render(request, 'tipos_us/update_tipos_us.html', {'tipous': tipous, 'form': form,'id_proyecto': id_proyecto, 'project': project})


def asignar_estados_tipos_us(request,id_proyecto,id_tipo_us):
    '''
        Asignar estados a cada tipo de user story
        fecha: 12/9/2022

            vista que permite asignar los estados a cada tipo de user story
    '''
    tipous = Tipo_User_Story.objects.get(id=id_tipo_us)
    project = Proyectos.objects.get(id=id_proyecto)
    x = id_proyecto
    y = id_tipo_us

    form = AsignarEstadosTipoUsForm(request.POST or None, instance=tipous, pwd=id_tipo_us, initial={'id_proyecto': id_proyecto})
    if form.is_valid():
        form.save()
        return redirect('/estados/'+str(x)+'/'+str(y))

    return render(request, 'tipos_us/asignar_estados_tipo_us.html', {'tipous': tipous, 'form': form,'id_proyecto': id_proyecto, 'project': project})

