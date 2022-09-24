from django import forms
from django.contrib.auth.models import User
from .models import Profile, Proyectos, Miembros, Rol
from django.conf import settings
from django.forms import ModelForm



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')


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
            'desc_proyecto': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion del Proyecto'}),
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
        fields = ('rol','desc_rol','permisos')
        labels = {
            'rol': '',
            'desc_rol': '',
            'permisos': ''
        }
        widgets = {
            'rol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rol'}),
            'desc_rol': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
            'permisos': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Permisos'}),

        }