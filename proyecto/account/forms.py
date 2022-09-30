from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Estados, Miembro_Sprint, Profile, Proyectos, Miembros, Rol, Sprint, Tipo_User_Story, UserStory
from django.conf import settings
from django.forms import ModelForm
from django.contrib.auth.models import Permission




class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'is_superuser')
        CHOICES = [(True, 'Si'), (False, 'No')]
        labels = {
            'username': 'Username',
            'first_name': 'Nombre',
            'email': 'Email',
            'is_superuser': "SuperUser"
        }
        help_texts = {
            'username': '',
            'is_superuser': '',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'is_superuser': forms.RadioSelect(choices=CHOICES),
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'is_superuser')
        CHOICES = [(True, 'Si'), (False, 'No')]
        labels = {
            'username': 'Username',
            'first_name': 'Nombre',
            'email': 'Email',
            'is_superuser': "SuperUser"
        }
        help_texts = {
            'username': '',
            'is_superuser': '',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'is_superuser': forms.RadioSelect(choices=CHOICES),
        }




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
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_active','is_superuser')


class ProyectosForm(ModelForm):
    class Meta:
        model = Proyectos
        fields = ('nombre_proyecto', 'desc_proyecto', 'estado_proyecto', 'fecha_inicio', 'fecha_fin', 'scrum_master')
        labels = {
            'nombre_proyecto': '',
            'desc_proyecto': '',
            'estado_proyecto': '',
            'fecha_inicio': 'Fecha Inicio',
            'fecha_fin': 'Fecha Fin',
            'scrum_master': 'Scrum Master'
        }
        widgets = {
            'nombre_proyecto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Proyecto'}),
            'desc_proyecto': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion del Proyecto', 'style': 'height: 30%;'}),
            'estado_proyecto': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Estado del Proyecto'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Fecha Inicio'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Fecha Fin'}),
            'scrum_master': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Scrum Master'}),
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
    def __init__(self, *args, **kwargs):
        self._pwd = kwargs.pop('pwd', None)
        print(self._pwd)
        super().__init__(*args, **kwargs)
        self.fields['id_rol'].queryset = Rol.objects.filter(proyecto_id=self._pwd)


class RolForm(ModelForm):
    class Meta:
        model = Rol
        fields = ('rol','desc_rol', 'permisos', 'proyecto')
        labels = {
            'rol': '',
            'desc_rol': '',
            'permisos': '',
            'proyecto': '',
        }
        widgets = {
            'rol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rol'}),
            'desc_rol': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Descripcion', 'style': 'height: 30%;'}),
            'permisos': forms.SelectMultiple(
                attrs={'class': 'form-control', 'placeholder': 'Permisos', 'style': 'height: 40%;'}),
            'proyecto': forms.HiddenInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(RolForm, self).__init__(*args, **kwargs)
        self.fields["permisos"].queryset = Permission.objects.exclude(
            Q(name__icontains="association") | Q(name__icontains='code') | Q(name__icontains='nonce') | Q(
                name__icontains='user social auth') | Q(name__icontains='partial') | Q(name__icontains='permission') |
            Q(name__icontains='miembro_ sprint') | Q(name__icontains='kanban') | Q(name__icontains='reuniones') |
            Q(name__icontains='reportes') | Q(name__icontains='sprint backlog') | Q(name__icontains='tipo us') |
            Q(name__icontains='backlog') | Q(name__icontains='group') | Q(
                name__icontains='log entry') | Q(name='user') | Q(name__icontains='content type')
                | Q(name__icontains='session')| Q(name__icontains='usuarios') | Q(name__icontains='profile'))


class SprintForm(ModelForm):
    class Meta:
        model = Sprint
        fields = ('nombre_sprint', 'desc_sprint', 'estado_sprint', 'duracion_dias','capacidad','id_proyecto')
        labels = {
            'nombre_sprint': '',
            'desc_sprint': '',
            'estado_sprint': '',
            'duracion_dias': '',
            'capacidad': '',
            'id_proyecto': '',
        }
        widgets = {
            'nombre_sprint': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del sprint'}),
            'desc_sprint': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion del sprint', 'style': 'height: 30%;'}),
            'estado_sprint': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Estado del sprint'}),
            'duracion_dias': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duración en días hábiles'}),
            'capacidad': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Duración en días hábiles'}),
            'id_proyecto': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Proyecto'}),
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

    def __init__(self, *args, **kwargs):
        self._pwd = kwargs.pop('pwd', None)
        print(self._pwd)
        super().__init__(*args, **kwargs)
        print(User.objects.filter(miembros__id_proyecto=self._pwd))
        self.fields['usuario'].queryset = User.objects.filter(miembros__id_proyecto=self._pwd)


class UserStoryForm(ModelForm):
    class Meta:
        model = UserStory
        fields = ('nombre_us', 'desc_us', 'horas_estimadas', 'encargado', 'prioridad_us', 'id_tipo_user_story', 'id_sprint', 'id_proyecto' )
        labels = {
            'nombre_us': 'Nombre',
            'desc_us': 'Descripción',
            'horas_estimadas': 'Horas estimadas',
            'encargado': 'Encargado',
            'prioridad_us': 'Prioridad',
            'id_proyecto': 'Proyecto',
            'id_tipo_user_story': 'Tipo de user story',
            'id_sprint': 'Sprint',

        }
        widgets = {
            'nombre_us': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del user story'}),
            'desc_us': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion del user story', 'style': 'height: 30%;'}),
            'horas_estimadas': forms.NumberInput(attrs={'class': 'form-control'}),
            'encargado': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Encargado'}),
            'prioridad_us': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Horas de trabajo por día'}),
            'id_tipo_user_story': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tipo de user story'}),
            'id_sprint': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sprint'}),
            'id_proyecto': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Sprint'}),
        }

    def __init__(self, *args, **kwargs):
        self._pwd = kwargs.pop('pwd', None)
        print(self._pwd)
        super().__init__(*args, **kwargs)
        self.fields['encargado'].queryset = User.objects.filter(miembros__id_proyecto=self._pwd)
        self.fields['id_tipo_user_story'].queryset = Tipo_User_Story.objects.filter(id_proyecto_id=self._pwd)
        self.fields['id_sprint'].queryset = Sprint.objects.filter(id_proyecto_id=self._pwd)

class TipoUsForm(ModelForm):
    class Meta:
        model = Tipo_User_Story
        fields = ('nombre_tipo_us', 'id_estado', 'id_proyecto')
        labels = {
            'nombre_tipo_us': '',
            'id_estado': '',
            'id_proyecto': '',

        }
        widgets = {
            'nombre_tipo_us': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Tipo_US'}),
            'id_estado': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Estado'}),
            'id_proyecto': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Proyecto'}),
        }


class EstadosForm(ModelForm):
    class Meta:
        model = Estados
        fields = ('nombre_estado', 'id_tipo_user_story')
        labels = {
            'nombre_estado': '',
            'id_tipo_user_story': '',

        }
        widgets = {
            'nombre_estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Estados'}),
            'id_tipo_user_story': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tipo User Story'}),
        }

