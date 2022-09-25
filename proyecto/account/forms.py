from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Miembro_Sprint, Profile, Proyectos, Miembros, Rol, Sprint
from django.conf import settings
from django.forms import ModelForm
from django.contrib.auth.models import Permission




class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        labels = {
            'username': 'Username',
            'first_name': 'Nombre',
            'email': 'Email',
        }
        help_texts = {
            'username': '',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_active')


class MyModelForm(forms.ModelForm):
    issue_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)


class detailsformuser(forms.ModelForm):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_active')


class ProyectosForm(ModelForm):
    class Meta:
        model = Proyectos
        fields = ('nombre_proyecto', 'desc_proyecto', 'estado_proyecto', 'fecha_inicio', 'fecha_fin')
        labels = {
            'nombre_proyecto': '',
            'desc_proyecto': '',
            'estado_proyecto': '',
            'fecha_inicio': 'Fecha Inicio',
            'fecha_fin': 'Fecha Fin',
        }
        widgets = {
            'nombre_proyecto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Proyecto'}),
            'desc_proyecto': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion del Proyecto', 'style': 'height: 30%;'}),
            'estado_proyecto': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Estado del Proyecto'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Fecha Inicio'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Fecha Fin'}),
        }


class AddMembersForm(ModelForm):
    class Meta:
        model = Miembros
        fields = ('id_usuario', 'id_proyecto', 'id_rol')
        labels = {
            'id_usuario': 'Usuario',
            'id_proyecto': 'Proyecto',
            'id_rol': 'Rol',
        }
        widgets = {
            'id_usuario': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'id_proyecto': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Proyecto'}),
            'id_rol': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Rol'}),
        }


class RolForm(ModelForm):
    class Meta:
        model = Rol
        fields = ('rol','desc_rol', 'permisos')
        labels = {
            'rol': '',
            'desc_rol': '',
            'permisos': ''
        }
        widgets = {
            'rol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rol'}),
            'desc_rol': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Descripcion', 'style': 'height: 30%;'}),
            'permisos': forms.SelectMultiple(
                attrs={'class': 'form-control', 'placeholder': 'Permisos', 'style': 'height: 40%;'}),

        }

    def __init__(self, *args, **kwargs):
        super(RolForm, self).__init__(*args, **kwargs)
        self.fields["permisos"].queryset = Permission.objects.exclude(
            Q(name__icontains="association") | Q(name__icontains='code') | Q(name__icontains='nonce') | Q(
                name__icontains='user social auth') | Q(name__icontains='partial') | Q(name__icontains='permission') |
            Q(name__icontains='miembro_ sprint') | Q(name__icontains='kanban') | Q(name__icontains='reuniones') |
            Q(name__icontains='reportes') | Q(name__icontains='sprint backlog') | Q(name__icontains='tipo us') |
            Q(name__icontains='backlog') | Q(name__icontains='user story') | Q(name__icontains='group') | Q(
                name__icontains='log entry') | Q(name__icontains='user') | Q(name__icontains='content type')
                | Q(name__icontains='session')| Q(name__icontains='profile'))


class SprintForm(ModelForm):
    class Meta:
        model = Sprint
        fields = ('nombre_sprint', 'desc_sprint', 'estado_sprint', 'duracion_dias','id_proyecto')
        labels = {
            'nombre_sprint': '',
            'desc_sprint': '',
            'estado_sprint': '',
            'duracion_dias': '',
            'id_proyecto': '',
        }
        widgets = {
            'nombre_sprint': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del sprint'}),
            'desc_sprint': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion del sprint', 'style': 'height: 30%;'}),
            'estado_sprint': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Estado del sprint'}),
            'duracion_dias': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duración en días hábiles'}),
            'id_proyecto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Proyecto'}),
        }

class AddMembersSprintForm(ModelForm):
    class Meta:
        model = Miembro_Sprint
        fields = ('usuario', 'sprint', 'horas_trabajo')
        labels = {
            'usuario': 'Usuario',
            'sprint': 'Sprint',
            'horas_trabajo': '',
        }
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'sprint': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Sprint'}),
            'horas_trabajo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Horas de trabajo por día'}),
        }