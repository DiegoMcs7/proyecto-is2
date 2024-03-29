from cProfile import label
from email import message
from attr import fields
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from matplotlib import widgets
from .models import Estados, Miembro_Sprint, Profile, Proyectos, Miembros, Rol, Sprint, Tipo_User_Story, UserStory, \
    LogProyectos, LogSprint, TareaUserStory
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
            'estado_proyecto': forms.HiddenInput(attrs={'class': 'form-select', 'placeholder': 'Estado del Proyecto'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Fecha Inicio'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Fecha Fin'}),
            'scrum_master': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Scrum Master'}),
        }

    def __init__(self, *args, **kwargs):
        self._pwd = kwargs.pop('pwd', None)
        print(self._pwd)
        super().__init__(*args, **kwargs)
        self.fields['scrum_master'].queryset = User.objects.filter(is_superuser=self._pwd)

class CancelarProyecto(ModelForm):
    class Meta:
        model = Proyectos
        fields = ('cancelar',)
        labels = {
            'Motivo de cancelación': '',
        }
        widgets = {
            'cancelar': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Motivo de cancelación', 'style': 'height: 30%;'}),
        }

class LogProyectosForm(ModelForm):
    class Meta:
        model = LogProyectos
        fields = ('nombre_proyecto', 'desc_proyecto', 'estado_proyecto', 'fecha_inicio', 'fecha_fin', 'scrum_master', 'usuario_responsable','descripcion_action', )

        widgets = {
            'usuario_responsable': forms.HiddenInput(attrs={'class': 'form-control'}),
            'descripcion_action': forms.HiddenInput(attrs={'class': 'form-control'}),
            'nombre_proyecto': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Proyecto'}),
            'desc_proyecto': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Descripcion del Proyecto', 'style': 'height: 30%;'}),
            'estado_proyecto': forms.HiddenInput(attrs={'class': 'form-select', 'placeholder': 'Estado del Proyecto'}),
            'fecha_inicio': forms.HiddenInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Fecha Inicio'}),
            'fecha_fin': forms.HiddenInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Fecha Fin'}),
            'scrum_master': forms.HiddenInput(attrs={'class': 'form-select', 'placeholder': 'Scrum Master'}),
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
        self.fields['id_usuario'].queryset = User.objects.filter(is_superuser=False)


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
            'estado_sprint': forms.HiddenInput(attrs={'class': 'form-select', 'placeholder': 'Estado del sprint'}),
            'duracion_dias': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duración en días hábiles'}),
            'capacidad': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Duración en días hábiles'}),
            'id_proyecto': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Proyecto'}),
        }

class LogSprintForm(ModelForm):
    class Meta:
        model = LogSprint
        fields = ('nombre_sprint', 'desc_sprint', 'estado_sprint', 'duracion_dias','capacidad','id_proyecto','usuario_responsable','descripcion_action',)

        widgets = {
            'usuario_responsable': forms.HiddenInput(attrs={'class': 'form-control'}),
            'descripcion_action': forms.HiddenInput(attrs={'class': 'form-control'}),
            'nombre_sprint': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del sprint'}),
            'desc_sprint': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Descripcion del sprint', 'style': 'height: 30%;'}),
            'estado_sprint': forms.HiddenInput(attrs={'class': 'form-select', 'placeholder': 'Estado del sprint'}),
            'duracion_dias': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Duración en días hábiles'}),
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
            'horas_trabajo': 'Horas de trabajo por día',
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
        self.fields['usuario'].queryset = User.objects.filter(miembros__id_proyecto=self._pwd, is_superuser=False)

class ReasignarMiembroSprintForm(ModelForm):
    class Meta:
        model = Miembro_Sprint
        fields = ('usuario', 'sprint', 'horas_trabajo')
        labels = {
            'usuario': 'Usuario',
            'sprint': 'Sprint',
            'horas_trabajo': 'Horas de trabajo por día',
        }
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'sprint': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Sprint'}),
            'horas_trabajo': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Horas de trabajo por día'}),
        }

    def __init__(self, *args, **kwargs):
        self._pwd = kwargs.pop('pwd', None)
        print(self._pwd)
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = User.objects.filter(miembros__id_proyecto=self._pwd, is_superuser=False)


class UserStoryForm(ModelForm):
    class Meta:
        model = UserStory
        fields = ('nombre_us', 'desc_us', 'horas_estimadas', 'encargado', 'prioridad_negocio', 'prioridad_tecnica', 'id_tipo_user_story', 'id_sprint', 'id_proyecto' )
        labels = {
            'nombre_us': 'Nombre',
            'desc_us': 'Descripción',
            'horas_estimadas': 'Horas estimadas',
            'encargado': 'Encargado',
            'prioridad_negocio' : 'Prioridad Negocio',
            'prioridad_tecnica' : 'Prioridad Técnica',
            'id_proyecto': 'Proyecto',
            'id_tipo_user_story': 'Tipo de user story',
            'id_sprint': 'Sprint',

        }
        widgets = {
            'nombre_us': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del user story'}),
            'desc_us': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion del user story', 'style': 'height: 20%;'}),
            'horas_estimadas': forms.HiddenInput(attrs={'class': 'form-control'}),
            'encargado': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Encargado'}),
            'prioridad_negocio': forms.NumberInput(attrs={'class':'form-control'}), 
            'prioridad_tecnica': forms.NumberInput(attrs={'class':'form-control'}),
            'id_tipo_user_story': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tipo de user story'}),
            'id_sprint': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Sprint'}),
            'id_proyecto': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Sprint'}),
        }

    def __init__(self, *args, **kwargs):
        self._pwd = kwargs.pop('pwd', None)
        print(self._pwd)
        super().__init__(*args, **kwargs)
        self.fields['encargado'].queryset = User.objects.filter(miembros__id_proyecto=self._pwd)
        self.fields['id_tipo_user_story'].queryset = Tipo_User_Story.objects.filter(id_proyecto_id=self._pwd)
        self.fields['id_sprint'].queryset = Sprint.objects.filter(id_proyecto_id=self._pwd)


class UserStorySprintForm(ModelForm):
    class Meta:
        model = UserStory
        fields = ('horas_estimadas', 'encargado', 'id_sprint')
        labels = {
            'horas_estimadas': 'Horas estimadas',
            'encargado': 'Encargado',
        }
        widgets = {
            'horas_estimadas': forms.NumberInput(attrs={'class': 'form-control'}),
            'encargado': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Encargado'}),
            'id_sprint': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Sprint'}),
        }
    def __init__(self, *args, **kwargs):
        self._pwd = kwargs.pop('pwd', None)
        print(self._pwd)
        super().__init__(*args, **kwargs)
        #self.fields['encargado'].queryset = Miembro_Sprint.objects.filter(sprint=self._pwd)
        self.fields['encargado'].queryset = User.objects.filter(miembro_sprint__sprint=self._pwd)
        #Miembro_Sprint.sprint.through.objects.filter(tipo_user_story_id=id_tipo_us).values_list('estados_id')



class TipoUsForm(ModelForm):
    class Meta:
        model = Tipo_User_Story
        fields = ('nombre_tipo_us', 'id_proyecto')
        labels = {
            'nombre_tipo_us': '',
            'id_proyecto': '',

        }

        widgets = {
            'nombre_tipo_us': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Tipo_US'}),
            'id_proyecto': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Proyecto'}),
        }


class EditarPosicionEstadoForm(ModelForm):
    class Meta:
        model = Estados
        fields = ('posicion',)

        widgets = {
            'posicion': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Posicion'}),
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
            'id_tipo_user_story': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Tipo User Story'}),
        }


class UsHorasForm(ModelForm):
    class Meta:
        model = UserStory
        fields = ('horas_trabajadas',)
        labels = {'horas_trabajadas': 'Horas a Trabajar'}
        widgets = {
            'horas_trabajadas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Horas a Trabajar'}),
        }


class ReasignarEncargadoForm(ModelForm):
    class Meta:
        model = UserStory
        fields = ('horas_estimadas', 'encargado', 'id_sprint')
        labels = {
            'horas_estimadas': 'Horas estimadas',
            'encargado': 'Encargado',
        }
        widgets = {
            'horas_estimadas': forms.HiddenInput(attrs={'class': 'form-control'}),
            'encargado': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Encargado'}),
            'id_sprint': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Sprint'}),
        }
    def __init__(self, *args, **kwargs):
        self._pwd = kwargs.pop('pwd', None)
        print(self._pwd)
        super().__init__(*args, **kwargs)
        #self.fields['encargado'].queryset = Miembro_Sprint.objects.filter(sprint=self._pwd)
        self.fields['encargado'].queryset = User.objects.filter(miembro_sprint__sprint=self._pwd)
        #Miembro_Sprint.sprint.through.objects.filter(tipo_user_story_id=id_tipo_us).values_list('estados_id')


class TareaUserStoryForm(ModelForm):
    class Meta:
        model = TareaUserStory
        fields = ('fecha', 'desc_tarea', 'duracion','id_user_story')
        labels = {'duracion': 'Duración',
                  'fecha': 'Fecha',
                  'desc_tarea': 'Descripción',
                  'id_user_story': 'User Story',
                  }
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'duracion': forms.NumberInput(attrs={'class': 'form-control',  'placeholder': 'Duración en horas'}),
            'desc_tarea': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 30%;'}),
            'id_user_story': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'User Story'}),

        }
