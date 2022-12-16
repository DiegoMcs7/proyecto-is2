from urllib import request
from django.test import RequestFactory
import warnings
from django.urls import reverse
from django.contrib.auth.models import User,AnonymousUser
from account.models import  Proyectos
from account.views import all_projects,all_sprints,all_estados,all_user_story
from mixer.backend.django import mixer
import pytest

@pytest.mark.django_db
class TestViews:
    
    def test_proyecto_authenticated(self):

        mixer.blend('account.Proyectos')
        path = reverse('list-projects')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = all_projects(request)
        assert response.status_code == 200
        warnings.warn(UserWarning("Testeando Proyecto autenticado"))
    
    def test_proyecto_unauthenticated(self):

        mixer.blend('account.Proyectos')
        path = reverse('list-projects')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = all_projects(request)
        assert 'account/projects' in response.url
    
    @pytest.mark.django_db
    def test_register_success(self):
        superuser = User.objects.create_superuser(
            username="admin",
            email="admin@admin.com",
            password="admin"
        )
        superuser.save()
        assert User.objects.count() > 0
    