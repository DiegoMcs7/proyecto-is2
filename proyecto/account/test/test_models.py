import warnings
from mixer.backend.django import mixer
import pytest


@pytest.mark.django_db
class TestModels:

    def test_project_exist(self):
        project = mixer.blend('account.Proyectos', id_proyecto=0)
        assert project.project_exist == True

        warnings.warn(UserWarning("Test Proyecto "))

    def test_rol_exist(self):
        rol = mixer.blend('account.Rol', id_rol=2)
        assert rol.rol_exist == True

        warnings.warn(UserWarning("Test Roles "))

    def test_user_story_exist(self):
        us = mixer.blend('account.UserStory', id_user_story=3)
        assert us.us_exist == True

        warnings.warn(UserWarning("Test User Story "))

    def test_estados_exist(self):
        estados = mixer.blend('account.Estados', id_estados=1)
        assert estados.estados_exist == True

        warnings.warn(UserWarning("Test Estados "))

    def test_sprint_exist(self):
        sprint = mixer.blend('account.Sprint', id_sprint=1)
        assert sprint.sprint_exist == True

        warnings.warn(UserWarning("Test Sprint "))

    def test_tipo_us_exist(self):
        tipous = mixer.blend('account.Tipo_User_Story', id_tipo_user_story_id=1)
        assert tipous.tipo_us_exist == True

        warnings.warn(UserWarning("Test Tipo User Story "))