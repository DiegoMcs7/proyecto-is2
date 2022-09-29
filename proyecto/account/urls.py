from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.tablero, name='tablero'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('update_us/<int:id>',views.update_us,name="update-us"),
    path('retrieve_user/',views.retrieve_user,name="retrieve_user"),
    path('add_members/<int:id>', views.add_members, name="add-members"),
    path('projects', views.all_projects, name="list-projects"),
    path('add_project', views.add_project, name='add-project'),
    path('delete_rol/<int:id>', views.delete_proyecto, name='delete-project'),
    path('update_project/<int:id>', views.update_project, name='update-project'),
    path('update_members_project/<int:id_proyecto>/<int:id_miembro>', views.update_members_project, name='update-members_project'),
    path('update_members_sprint/<int:id_proyecto>/<int:id_sprint>/<int:id_usuario>', views.update_members_sprint, name='update-members_sprint'),
    path('roles/<int:id_proyecto>', views.all_roles, name="list-roles"),
    path('add_rol/<int:id_proyecto>', views.add_rol, name='add-rol'),
    path('update_rol/<int:id>/<int:id_proyecto>', views.update_rol, name='update-rol'),
    path('delete_rol/<int:id>/<int:id_proyecto>', views.delete_rol, name='delete-rol'),
    path('delete_miembro/<int:id>/<int:id_proyecto>', views.delete_miembro_proyecto, name='delete-members_project'),
    path('add_members_sprint/<int:id_proyecto>/<int:id_sprint>', views.add_members_sprint, name="add-members-sprint"),
    path('sprint/<int:id>', views.all_sprints, name="sprint-list"),
    path('add_sprint/<int:id>', views.add_sprint, name='add-sprint'),
    path('update_sprint/<int:id_proyecto>/<int:id_sprint>', views.update_sprint, name='update-sprint'),
    path('user_story/<int:id>', views.all_user_story, name="user_story-list"),
    path('user_story_list_sprint_backlog/<int:id>', views.all_user_story_sprint_backlog, name="user_story_sprint_backlog-list"),
    path('add_user_story/<int:id_proyecto>', views.add_user_story, name='add-user_story'),
    path('update_user_story/<int:id_proyecto>/<int:id_user_story>', views.update_user_story, name='update-user_story'),
]