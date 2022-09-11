from .models import Profile, Proyectos
from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm, ProfileForm, ProyectosForm,UserRegistrationForm,UserEditForm,ProfileEditForm, detailsformuser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect

@login_required()
def tablero(request):
    '''
        Vistas
        fecha: 20/8/2022

        Una función de visualización es una función de Python que toma una solicitud web y devuelve una respuesta web .
               Esta vista es la encargada de llamar al archivo tablero.html con el fin de mostrar en pantalla el menu
               luego de la peticion correspondiente
    '''
    return render(request,'account/tablero.html', {'section':'tablero'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,'account/register_done.html',{'new_user': new_user})
    else:
        user_form=UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})

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

#CRUD PROYECTO
def index(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request,'index.html',{'users': users})
    
def create(request):
    if request.method=="POST":
        data = request.POST.getlist('miembro_id')
        obj = detailsform(request.POST)
        print(data)
        if obj.is_valid():
            obj.save()
        return render(request,'create_done.html',{'obj': obj})

def retrieve(request):
    details=Proyectos.objects.all()
    return render(request,'retrieve.html',{'details':details})

def edit(request,id):
    object=Proyectos.objects.get(id=id)
    return render(request,'editp.html',{'object':object})
    
def update(request,id):
    if request.method == 'POST':
        object=Proyectos.objects.get(id=id)
        form=detailsform(request.POST,instance=object)
        if form.is_valid():
            form.save()
            object=Proyectos.objects.all()
            messages.success(request,'Se han actualizado los datos!')
            return redirect('retrieve')
        else:
            messages.error(request, 'Error al actualizar datos.')
    else:
        form.save()
        object=Proyectos.objects.get(id=id)
        form=detailsform(request.POST,instance=object)
    return render(request,'editp.html',{'object':object,'form':form})


def delete(request,pk):   
        Proyectos.objects.filter(id=pk).delete()
        return redirect('retrieve')

def delete_us(request,pk):
        User = get_user_model()
        User.objects.filter(id=pk).delete()
        return redirect('retrieve_user')


#Nuevo crud para proyecto
def add_project(request):
	submitted = False
	if request.method == "POST":
			form = ProyectosForm(request.POST)
			if form.is_valid():
				project = form.save(commit=False)
				project.manager = request.user 
				project.save()
				return 	HttpResponseRedirect('/add_project?submitted=True')	
	else:
	
		form = ProyectosForm

		if 'submitted' in request.GET:
			submitted = True

	return render(request, 'add_project.html', {'form':form, 'submitted':submitted})


def update_project(request, id):
	project = Proyectos.objects.get(id=id)

	form = ProyectosForm(request.POST or None, instance=project)
	
	if form.is_valid():
		form.save()
		return redirect('list-projects')

	return render(request, 'update_project.html',{'project': project,'form':form})

def all_projects(request):
	project_list = Proyectos.objects.all()
	return render(request, 'project_list.html', 
		{'project_list': project_list})