import pytest
import warnings
from django.contrib.auth.models import User
from account.models import Proyectos, Sprint, Miembros, Rol

@pytest.mark.django_db
def test_user_create():
    User.objects.create_user(username='diego', email='diegoespinola@hotmail.com', password='sasd')
    assert User.objects.filter(username="diego").exists(),"Usuario no existe"
    assert User.objects.filter(email="diegoespinola@hotmail.com").exists(),"Email no existe"

    warnings.warn(UserWarning("Crear Nuevo Usuario"))

@pytest.mark.django_db
def test_project_create():
    Proyectos.objects.create(nombre_proyecto='Proyecto 1',desc_proyecto='asd',estado_proyecto='Planificado',fecha_inicio='2022-11-02',fecha_fin='2022-11-04')
    assert Proyectos.objects.filter(nombre_proyecto="Proyecto 1").exists(),"No existe el proyecto"

    warnings.warn(UserWarning("Crear Nuevo Proyecto"))

@pytest.mark.django_db
def test_sprint_create():
    Sprint.objects.create(nombre_sprint='Sprint 1',desc_sprint='asd',estado_sprint='Cancelado',fecha_inicio='2022-11-02')
    assert Sprint.objects.filter(nombre_sprint="Sprint 1").exists(),"No existe el sprint"

    warnings.warn(UserWarning("Crear Nuevo Sprint"))

@pytest.mark.django_db
def test_miembros_create():
    x = Proyectos.objects.create(nombre_proyecto='Proyecto 2',desc_proyecto='asd',estado_proyecto='Planificado',fecha_inicio='2022-11-02',fecha_fin='2022-11-04')
    y = User.objects.create_user(username='diego', email='diegoespinola@hotmail.com', password='sasd')

    Miembros.objects.create( id_proyecto=x,id_usuario=y)
    assert Miembros.objects.filter(id_usuario=y).exists(),"No existe miembro en el proyecto"

    warnings.warn(UserWarning("Agregar Miembro al Proyecto"))

@pytest.mark.django_db
def test_rol_create():
    Rol.objects.create(rol= "Scrum Master",desc_rol="asdas")
    assert Rol.objects.filter(rol="Scrum Master").exists(),"No existe rol"

    warnings.warn(UserWarning("Agregar nuevo Rol"))