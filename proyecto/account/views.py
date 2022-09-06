from .models import Profile, Proyectos
from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm, detailsform
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Autenticado'' Satisfactoriamente')
                else:
                    return HttpResponse('Cuenta desabilitada')
            else:
                return HttpResponse("Login Invalido")
    else:
        form=LoginForm()
    return render(request,'account/login.html',{'form':form})

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

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        print(profile_form)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Se han actualizado los datos!')
        else:
            messages.error(request, 'Error al actualizar datos.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'account/edit.html',{'user_form':user_form,'profile_form':profile_form})

def index(request):
    return render(request,'index.html')
#anda
def create(request):
    if request.method=="POST":
        obj = detailsform(request.POST)
        if obj.is_valid():
            obj.save()
        return render(request,'create_done.html',{'obj': obj})
#anda
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
        print(form)
        if form.is_valid():
            print("1")
            form.save()
            object=Proyectos.objects.all()
            messages.success(request,'Se han actualizado los datos!')
            return render(request,'retrieve.html',{'object':object})
        else:
            print("2")
            messages.error(request, 'Error al actualizar datos.')
    else:
        print("3")
        form.save()
        object=Proyectos.objects.get(id=id)
        form=detailsform(request.POST,instance=object)
    return render(request,'editp.html',{'object':object,'form':form})


def delete(request,pk):   
        Proyectos.objects.filter(id=pk).delete()
        return redirect('retrieve')