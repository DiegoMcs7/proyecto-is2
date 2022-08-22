from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

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