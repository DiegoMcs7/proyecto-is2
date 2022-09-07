from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.tablero, name='tablero'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('edit/<int:id>',views.edit_us,name="edit"),
    path('retrieve_user/',views.retrieve_user,name="retrieve_user"),
    path('index/',views.index,name='index'),
    path('create/',views.create,name="create"), 
    path('retrieve/',views.retrieve,name="retrieve"),
    path('editp/<int:id>',views.edit,name="editp"),
    path('update/<int:id>',views.update,name="update"),
    path(r'^delete_proyecto/(?P<pk>[0-9]+)/$', views.delete,name="delete"), 
    path(r'^delete_user/(?P<pk>[0-9]+)/$', views.delete_us,name="delete"), 
    
]