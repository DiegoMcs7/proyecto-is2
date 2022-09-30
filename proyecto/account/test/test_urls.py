from django.urls import reverse, resolve

class TestUrls:

    def test_register_url(self):

        path = reverse('register')
        assert resolve(path).view_name == 'register'
    
    def test_retrieve_user_url(self):

        path = reverse('retrieve_user')
        assert resolve(path).view_name == 'retrieve_user'

    def test_edit_us_url(self):

        path = reverse('update-us',kwargs={'id': 3})
        assert resolve(path).view_name == 'update-us'

    def test_add_members_url(self):

        path = reverse('add-members',kwargs={'id': 1})
        assert resolve(path).view_name == 'add-members'

    def test_add_project_url(self):

        path = reverse('add-project')
        assert resolve(path).view_name == 'add-project'

    def test_delete_project_url(self):

        path = reverse('delete-project',kwargs={'id': 1})
        assert resolve(path).view_name == 'delete-project'

    def test_project_url(self):

        path = reverse('list-projects')
        assert resolve(path).view_name == 'list-projects'

    def test_update_project_url(self):

        path = reverse('update-project',kwargs={'id': 1})
        assert resolve(path).view_name == 'update-project'

    def test_update_members_project_url(self):

        path = reverse('update-members_project',kwargs={'id_proyecto': 1,'id_miembro': 2})
        assert resolve(path).view_name == 'update-members_project'
    

    