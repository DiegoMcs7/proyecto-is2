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

    def test_tablero_url(self):

        path = reverse('tablero')
        assert resolve(path).view_name == 'tablero', "Error al abrir tablero"

        warnings.warn(UserWarning("Testeando Url Tablero"))

    def test_login_url(self):

        path = reverse('login')
        assert resolve(path).view_name == 'login', "Error al loggear"

        warnings.warn(UserWarning("Testeando Url Login"))
    
    def test_logout_url(self):

        path = reverse('logout')
        assert resolve(path).view_name == 'logout', "Error al salir"

        warnings.warn(UserWarning("Testeando Url Logout"))

    def test_add_miembros_url(self):

        path = reverse('add-miembros',kwargs={'id': 1})
        assert resolve(path).view_name == 'add-miembros', "Error en el url add-miembros"

        warnings.warn(UserWarning("Testeando Url Agregar Miembros al sprint"))

    def test_log_project_url(self):

        path = reverse('log-project',kwargs={'id_proyecto': 1})
        assert resolve(path).view_name == 'log-project', "Error en el url log-project"

        warnings.warn(UserWarning("Testeando Url Log de Proyectos"))
    
    def test_action_project_url(self):

        path = reverse('action-project',kwargs={'id': 1})
        assert resolve(path).view_name == 'action-project', "Error en el url action-project"

        warnings.warn(UserWarning("Testeando Url Acciones Proyecto"))

    def test_action_sprint_url(self):

        path = reverse('action-sprint',kwargs={'id_proyecto': 1,'id_sprint': 2})
        assert resolve(path).view_name == 'action-sprint', "Error en el url action-sprint"

        warnings.warn(UserWarning("Testeando Url Acciones Sprint"))

    def test_inicializar_project_url(self):

        path = reverse('inicializar_proyecto',kwargs={'id': 1})
        assert resolve(path).view_name == 'inicializar_proyecto', "Error en el url inicializar_proyecto"

        warnings.warn(UserWarning("Testeando Url Inicializar Proyecto"))

    def test_cancelar_project_url(self):

        path = reverse('cancelar_proyecto',kwargs={'id': 1})
        assert resolve(path).view_name == 'cancelar_proyecto', "Error en el url cancelar_proyecto"

        warnings.warn(UserWarning("Testeando Url Cancelar Proyecto"))

    def test_finalizar_project_url(self):

        path = reverse('finalizar_proyecto',kwargs={'id': 1})
        assert resolve(path).view_name == 'finalizar_proyecto', "Error en el url finalizar_proyecto"

        warnings.warn(UserWarning("Testeando Url Finalizar Proyecto"))

    def test_inicializar_sprint_url(self):

        path = reverse('inicializar_sprint',kwargs={'id_proyecto': 1,'id_sprint': 2})
        assert resolve(path).view_name == 'inicializar_sprint', "Error en el url inicializar_sprint"

        warnings.warn(UserWarning("Testeando Url Inicializar Sprint"))

    def test_cancelar_sprint_url(self):

        path = reverse('cancelar_sprint',kwargs={'id_proyecto': 1,'id_sprint': 2})
        assert resolve(path).view_name == 'cancelar_sprint', "Error en el url cancelar_sprint"

        warnings.warn(UserWarning("Testeando Url Cancelar Sprint"))

    def test_finalizar_sprint_url(self):

        path = reverse('finalizar_sprint',kwargs={'id_proyecto': 1,'id_sprint': 2})
        assert resolve(path).view_name == 'finalizar_sprint', "Error en el url finalizar_sprint"

        warnings.warn(UserWarning("Testeando Url Finalizar Sprint"))

    def test_update_members_sprint_url(self):

        path = reverse('update-members_sprint',kwargs={'id_proyecto': 1,'id_sprint': 2,'id_miembro': 2})
        assert resolve(path).view_name == 'update-members_sprint', "Error en el url update-members_sprint"

        warnings.warn(UserWarning("Testeando Url Editar Miembros Sprint"))

    def test_roles_url(self):

        path = reverse('list-roles',kwargs={'id_proyecto': 1})
        assert resolve(path).view_name == 'list-roles', "Error en el url list-roles"

        warnings.warn(UserWarning("Testeando Url Mostrar Roles"))

    def test_permisos_url(self):

        path = reverse('list_permisos',kwargs={'id_proyecto': 1,'id_rol': 1})
        assert resolve(path).view_name == 'list_permisos', "Error en el url list_permisos"

        warnings.warn(UserWarning("Testeando Url Mostrar Permisos"))

    def test_exportar_roles_url(self):

        path = reverse('exportar-roles',kwargs={'id_proyecto': 1})
        assert resolve(path).view_name == 'exportar-roles', "Error en el url exportar-roles"

        warnings.warn(UserWarning("Testeando Url Exportar Roles"))

    def test_importar_roles_url(self):

        path = reverse('importar-roles',kwargs={'id_proyecto': 1})
        assert resolve(path).view_name == 'importar-roles', "Error en el url importar-roles"

        warnings.warn(UserWarning("Testeando Url Importar Roles"))

    def test_add_rol_url(self):

        path = reverse('add-rol',kwargs={'id_proyecto': 1})
        assert resolve(path).view_name == 'add-rol', "Error en el url add-rol"

        warnings.warn(UserWarning("Testeando Url Agregar roles"))

    def test_update_rol_url(self):

        path = reverse('update-rol',kwargs={'id': 1,'id_proyecto': 1})
        assert resolve(path).view_name == 'update-rol', "Error en el url update-rol"

        warnings.warn(UserWarning("Testeando Url Editar roles"))

    def test_delete_rol_url(self):

        path = reverse('delete-rol',kwargs={'id': 1,'id_proyecto': 1})
        assert resolve(path).view_name == 'delete-rol', "Error en el url delete-rol"

        warnings.warn(UserWarning("Testeando Url Eliminar roles"))

    def test_delete_member_project_url(self):

        path = reverse('delete-members_project',kwargs={'id': 1,'id_proyecto': 1})
        assert resolve(path).view_name == 'delete-members_project', "Error en el url delete-members_project"

        warnings.warn(UserWarning("Testeando Url Eliminar miembros del proyecto"))

    def test_add_member_project_url(self):

        path = reverse('add-members-sprint',kwargs={'id_proyecto': 1,'id_sprint': 1})
        assert resolve(path).view_name == 'add-members-sprint', "Error en el url add-members-sprint"

        warnings.warn(UserWarning("Testeando Url Agregar miembros al proyecto"))

    def test_add_miembros_project_url(self):

        path = reverse('add-miembros-sprint',kwargs={'id_proyecto': 1,'id_sprint': 1})
        assert resolve(path).view_name == 'add-miembros-sprint', "Error en el url add-miembros-sprint"

        warnings.warn(UserWarning("Testeando Url Agregar miembros al Sprint"))

    def test_sprint_url(self):

        path = reverse('sprint-list',kwargs={'id': 1})
        assert resolve(path).view_name == 'sprint-list', "Error en el url sprint-list"

        warnings.warn(UserWarning("Testeando Url Mostrar Sprints"))

    def test_log_sprint_url(self):

        path = reverse('log-sprint',kwargs={'id_proyecto': 1,'id_sprint': 1})
        assert resolve(path).view_name == 'log-sprint', "Error en el url log-sprint"

        warnings.warn(UserWarning("Testeando Url Mostrar Log Sprints"))

    def test_product_backlog_sprint_url(self):

        path = reverse('product-backlog-sprint',kwargs={'id_proyecto': 1,'id_sprint': 1})
        assert resolve(path).view_name == 'product-backlog-sprint', "Error en el url product-backlog-sprint"

        warnings.warn(UserWarning("Testeando Url Mostrar Product Backlog"))

    def test_all_user_story_url(self):

        path = reverse('user_story_sprint_backlog-list',kwargs={'id': 1})
        assert resolve(path).view_name == 'user_story_sprint_backlog-list', "Error en el url user_story_sprint_backlog-list"

        warnings.warn(UserWarning("Testeando Url Mostrar User Story"))

    def test_add_sprint_url(self):

        path = reverse('add-sprint',kwargs={'id': 1})
        assert resolve(path).view_name == 'add-sprint', "Error en el url add-sprint"

        warnings.warn(UserWarning("Testeando Url Agregar Sprint"))

    def test_update_sprint_url(self):

        path = reverse('update-sprint',kwargs={'id_proyecto': 1,'id_sprint': 1})
        assert resolve(path).view_name == 'update-sprint', "Error en el url update-sprint"

        warnings.warn(UserWarning("Testeando Url Editar Sprint"))

    def test_user_story_url(self):

        path = reverse('user_story-list',kwargs={'id': 1})
        assert resolve(path).view_name == 'user_story-list', "Error en el url user_story-list"

        warnings.warn(UserWarning("Testeando Url User Story"))

    def test_add_user_story_url(self):

        path = reverse('add-user_story',kwargs={'id_proyecto': 1})
        assert resolve(path).view_name == 'add-user_story', "Error en el url add-user_story"

        warnings.warn(UserWarning("Testeando Url Agregar User Story"))

    def test_tipos_user_story_url(self):

        path = reverse('tipos_us-list',kwargs={'id_proyecto': 1})
        assert resolve(path).view_name == 'tipos_us-list', "Error en el url tipos_us-list"

        warnings.warn(UserWarning("Testeando Url Tipos User Story"))

    def test_tipos_us_list_kbn_url(self):

        path = reverse('tipos_us-list-kbn',kwargs={'id_proyecto': 1,'id_sprint': 1})
        assert resolve(path).view_name == 'tipos_us-list-kbn', "Error en el url tipos_us-list-kbn"

        warnings.warn(UserWarning("Testeando Url Tipos User Story Kanban"))

    def test_exportar_tipos_us_url(self):

        path = reverse('tipos_us-export',kwargs={'id_proyecto': 1})
        assert resolve(path).view_name == 'tipos_us-export', "Error en el url tipos_us-export"

        warnings.warn(UserWarning("Testeando Url Exportar Tipo US"))

    def test_importar_tipos_us_url(self):

        path = reverse('tipos_us-import',kwargs={'id_proyecto': 1})
        assert resolve(path).view_name == 'tipos_us-import', "Error en el url tipos_us-import"

        warnings.warn(UserWarning("Testeando Url Importar Tipo US"))

    def test_add_tipos_user_story_url(self):

        path = reverse('add-tipos_us',kwargs={'id': 1})
        assert resolve(path).view_name == 'add-tipos_us', "Error en el url add-tipos_us"

        warnings.warn(UserWarning("Testeando Url Agregar Tipos de User Story"))

    
    

    

    