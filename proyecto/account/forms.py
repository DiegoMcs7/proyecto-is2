from django import forms
from django.contrib.auth.models import User
from .models import Profile, Proyectos
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
        fields = ('telefono','is_active')

class detailsform(forms.ModelForm):
    class Meta:
        model=Proyectos
        fields="__all__"


