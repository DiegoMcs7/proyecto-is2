from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User

print(User.objects.all())

urlpatterns = [

    path('', views.tablero, name='tablero'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

]