import warnings
from mixer.backend.django import mixer
import pytest


@pytest.mark.django_db
class TestModels:

    def test_project_exist(self):
        project = mixer.blend('account.Proyectos', id_proyecto=1)
        assert project.project_exist == True,"Modelo Proyecto no existe"

        warnings.warn(UserWarning("Testeando Modelo Proyecto"))

    def test_rol_exist(self):
        rol = mixer.blend('account.Rol', id_rol=2)
        assert rol.rol_exist == True,"Modelo Rol no existe"

        warnings.warn(UserWarning("Testeando Modelo Roles "))

    def test_user_story_exist(self):
        us = mixer.blend('account.UserStory', id_user_story=3)
        assert us.us_exist == True,"Modelo User Story no existe"

        warnings.warn(UserWarning("Testeando Modelo User Story "))

    def test_estados_exist(self):
        estados = mixer.blend('account.Estados', id_estados=1)
        assert estados.estados_exist == True,"Modelo Estados no existe"

        warnings.warn(UserWarning("Testeando Modelo Estados "))

    def test_sprint_exist(self):
        sprint = mixer.blend('account.Sprint', id_sprint=1)
        assert sprint.sprint_exist == True,"Modelo Sprint no existe"

        warnings.warn(UserWarning("Testeando Modelo Sprint "))

    def test_tipo_us_exist(self):
        tipous = mixer.blend('account.Tipo_User_Story', id_tipo_user_story_id=1)
        assert tipous.tipo_us_exist == True,"Modelo Tipos User Story no existe"

        warnings.warn(UserWarning("Testeando Modelo Tipo User Story "))