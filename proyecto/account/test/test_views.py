from urllib import request
from django.test import RequestFactory
import warnings
from django.urls import reverse
from django.contrib.auth.models import User
from account.models import  Proyectos
from account.views import all_projects,all_roles,all_sprints,all_estados,all_user_story
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
        warnings.warn(UserWarning("Test Proyecto autenticado"))

    def test_sprint_authenticated(self):

        mixer.blend('account.Sprint')
        path = reverse('sprint-list',kwargs={'id':4})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = all_sprints(request,id=4)
        assert response.status_code == 200
        warnings.warn(UserWarning("Test Sprint autenticado"))

    def test_estados_authenticated(self):

        mixer.blend('account.Estados')
        path = reverse('estados-list',kwargs={'id_proyecto':4,'id_tipo_us':53})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = all_estados(request,id_proyecto=4,id_tipo_us=53)
        assert response.status_code == 200
        warnings.warn(UserWarning("Test Estado autenticado"))
    
    def test_us_authenticated(self):

        mixer.blend('account.UserStory')
        path = reverse('user_story-list',kwargs={'id':4})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = all_user_story(request,id=4)
        assert response.status_code == 200
        warnings.warn(UserWarning("Test user story autenticado"))

