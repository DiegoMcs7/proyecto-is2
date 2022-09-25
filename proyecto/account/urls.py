from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.tablero, name='tablero'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('edit_us/<int:id>',views.edit_us,name="edit_us"),
    path('retrieve_user/',views.retrieve_user,name="retrieve_user"),
    path('add_members/<int:id>', views.add_members, name="add-members"),
    path('projects', views.all_projects, name="list-projects"),
    path('add_project', views.add_project, name='add-project'),
    path('update_project/<int:id>', views.update_project, name='update-project'),
    path('roles', views.all_roles, name="list-roles"),
    path('add_rol', views.add_rol, name='add-rol'),
    path('update_rol/<int:id>', views.update_rol, name='update-rol'),
    path('add_members_sprint/<int:id>', views.add_members_sprint, name="add-members-sprint"),
    path('sprint/<int:id>', views.all_sprints, name="sprint-list"),
    path('add_sprint/<int:id>', views.add_sprint, name='add-sprint'),
    path('update_sprint/<int:id>', views.update_sprint, name='update-sprint'),
]