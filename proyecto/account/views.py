from .models import Profile
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm,UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

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

def get(self, request, **kwargs):
        # verificamos permisos
        if not self.request.user.has_perm('account.view_proyectos') :
            return HttpResponseForbidden()
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


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
