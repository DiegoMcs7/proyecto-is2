import warnings
from django.urls import reverse, resolve

class TestUrls:

    def test_register_url(self):

        path = reverse('register')
        assert resolve(path).view_name == 'register', "Error en el url register"

        warnings.warn(UserWarning("Testeando Url Registro Usuario"))
    
    def test_retrieve_user_url(self):

        path = reverse('retrieve_user')
        assert resolve(path).view_name == 'retrieve_user', "Error en el url retrieve_user"

        warnings.warn(UserWarning("Testeando Url Mostrar Usuarios"))

    def test_edit_us_url(self):

        path = reverse('update-us',kwargs={'id': 3})
        assert resolve(path).view_name == 'update-us', "Error en el url update-us"

        warnings.warn(UserWarning("Testeando Url Editar Usuario"))

    def test_add_members_url(self):

        path = reverse('add-members',kwargs={'id': 1})
        assert resolve(path).view_name == 'add-members', "Error en el url add-members"

        warnings.warn(UserWarning("Testeando Url Agregar Miembros"))

    def test_add_project_url(self):

        path = reverse('add-project')
        assert resolve(path).view_name == 'add-project', "Error en el url add-project"

        warnings.warn(UserWarning("Testeando Url Agregar Proyectos"))

    def test_delete_project_url(self):

        path = reverse('delete-project',kwargs={'id': 1})
        assert resolve(path).view_name == 'delete-project', "Error en el url delete-project"

        warnings.warn(UserWarning("Testeando Url Eliminar Proyectos"))

    def test_project_url(self):

        path = reverse('list-projects')
        assert resolve(path).view_name == 'list-projects', "Error en el url list-projects"

        warnings.warn(UserWarning("Testeando Url Lista Proyectos"))

    def test_update_project_url(self):

        path = reverse('update-project',kwargs={'id': 1})
        assert resolve(path).view_name == 'update-project', "Error en el url update-projects"

        warnings.warn(UserWarning("Testeando Url Editar Proyecto"))

    def test_update_members_project_url(self):

        path = reverse('update-members_project',kwargs={'id_proyecto': 1,'id_miembro': 2})
        assert resolve(path).view_name == 'update-members_project', "Error en el url update-members_project"

        warnings.warn(UserWarning("Testeando Url Editar Miembros Proyecto"))
    

    