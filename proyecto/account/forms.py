from django import forms
from django.contrib.auth.models import User
from .models import Profile, Proyectos
from django.conf import settings
from django.forms import ModelForm
class LoginForm(forms.Form):

    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ('username','first_name','email')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','is_active')

# class detailsform(forms.ModelForm):

#     class Meta:
#         model=Proyectos
#         fields="__all__"
class MyModelForm(forms.ModelForm):
    issue_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)

class detailsformuser(forms.ModelForm):
    class Meta:
        model=User
        fields = ('id','username','first_name','last_name','email','is_active')

class ProyectosForm(ModelForm):
	class Meta:
		model = Proyectos
		fields = ('nombre_proyecto', 'desc_proyecto', 'estado_proyecto', 'miembro', 'fecha_inicio','fecha_fin')
		labels = {
			'nombre_proyecto': '',
			'desc_proyecto': '',
			'estado_proyecto': '',
			'miembro': '',
			'fecha_inicio': 'Fecha Inicio',	
            'fecha_fin': 'Fecha Fin',		
		}
		widgets = {
			'nombre_proyecto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del Proyecto'}),
			'desc_proyecto': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripcion del Proyecto'}),
			'estado_proyecto': forms.Select(attrs={'class':'form-select', 'placeholder':'Estado del Proyecto'}),
			'miembro': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Miembros'}),
			'fecha_inicio': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Fecha Inicio'}),
            'fecha_fin': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Fecha Fin'}),
		}
