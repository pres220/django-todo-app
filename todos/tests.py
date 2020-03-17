from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse

from .models import Todo
from .views import *


class HomePageTest(SimpleTestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_view(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_content(self):
        self.assertContains(self.response, 'Home')

    def test_home_path_resolves_to_home_page_view(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)


class SignUpPageTest(SimpleTestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signup_template(self):
        self.assertTemplateUsed(self.response, 'signup.html')

    def test_signup_content(self):
        self.assertContains(self.response, 'Sign Up')

    def test_signup_path_resolves_to_sign_up_view(self):
        view = resolve('/accounts/signup/')
        self.assertEqual(view.func.__name__, SignUpView.as_view().__name__)


class TodoModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='username',
            password='supersecret123'
        )
        cls.todo = Todo.objects.create(
            author=cls.user,
            title='title',
            description='description',
        )
        cls.id = cls.todo.id

    def test_todo_model_fields(cls):
        todo = Todo.objects.get(id=cls.id)
        cls.assertEqual(todo.author.username, 'username')
        cls.assertEqual(todo.author.password, 'supersecret123')
        cls.assertEqual(todo.title, 'title')
        cls.assertEqual(todo.description, 'description')

    def test_todo_model_str(cls):
        todo = Todo.objects.get(id=cls.id)
        cls.assertEqual(str(todo), 'title')

    def test_todo_get_absolute_url(cls):
        todo = Todo.objects.get(id=cls.id)
        cls.assertEqual(todo.get_absolute_url(), f'/todos/{cls.id}/')


class TodoListViewTests(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            username='test_user',
            password='test_password123'
        )
        self.test_todo = Todo.objects.create(
            author=self.test_user,
            title='title',
            description='description',
        )
        self.test_id = self.test_todo.id

    def test_list_view_resolves(self):
        view = resolve('/todos/')
        self.assertEqual(view.func.__name__, TodoListView.as_view().__name__)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/todos/')

    def test_logged_in_user_one_todo(self):
        login = self.client.login(username='test_user', password='test_password123')
        self.assertTrue(login)

        # Confirm user is logged in and 1 todo exists in the template context
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'test_user')
        self.assertTemplateUsed(response, 'todo_list.html')
        self.assertEqual(len(response.context['todo_list']), 1)

        # Confirm page content is correct
        self.assertContains(response, 'You have 1 uncompleted todo.')
        self.assertContains(response, 'title')
        self.assertContains(response, 'description')

    def test_logged_in_user_multiple_todos(self):
        # Create three more todos
        for i in range(1, 4):
            Todo.objects.create(
                author=self.test_user,
                title=f'title{i}',
                description=f'description{i}',
            )
        login = self.client.login(username='test_user', password='test_password123')
        self.assertTrue(login)

        # Confirm user is logged in and 4 total todos exist in template context
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(str(response.context['user']), 'test_user')
        self.assertEqual(len(response.context['todo_list']), 4)

        # Confirm author of each todo in the todo_list is the creator of said todo
        for todo in response.context['todo_list']:
            self.assertEqual(response.context['user'], todo.author)

        # Confirm page content is correct
        self.assertContains(response, 'You have 4 uncompleted todos.')
        for i in range(1, 4):
            self.assertContains(response, f'title{i}')
            self.assertContains(response, f'description{i}')


class TodoDetailViewTests(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            username='test_user',
            password='test_password123'
        )
        self.test_todo = Todo.objects.create(
            author=self.test_user,
            title='title',
            description='description',
        )
        self.test_id = self.test_todo.id

    def test_detail_view_resolves(self):
        view = resolve(f'/todos/{self.test_id}/')
        self.assertEqual(view.func.__name__, TodoDetailView.as_view().__name__)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('todo_detail', kwargs={'pk': self.test_id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/todos/{self.test_id}/')

    def test_logged_in_user_template(self):
        login = self.client.login(username='test_user', password='test_password123')
        self.assertTrue(login)
        response = self.client.get(reverse('todo_detail', kwargs={'pk': self.test_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_detail.html')
        self.assertContains(response, 'title')
        self.assertContains(response, 'description')
        self.assertContains(response, 'Todo Detail')


class TodoUpdateViewTests(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            username='test_user',
            password='test_password123'
        )
        self.test_todo = Todo.objects.create(
            author=self.test_user,
            title='title',
            description='description',
        )
        self.test_id = self.test_todo.id

    def test_update_view_resolves(self):
        view = resolve(f'/todos/{self.test_id}/edit/')
        self.assertEqual(view.func.__name__, TodoUpdateView.as_view().__name__)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('todo_edit', kwargs={'pk': self.test_id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/todos/{self.test_id}/edit/')

    def test_logged_in_user_template(self):
        login = self.client.login(username='test_user', password='test_password123')
        self.assertTrue(login)
        response = self.client.get(reverse('todo_edit', kwargs={'pk': self.test_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_edit.html')
        self.assertContains(response, 'title')
        self.assertContains(response, 'description')
        self.assertContains(response, 'Edit Todo')

    def test_unauthorized_user_cannot_edit_todo(self):
        User.objects.create_user(username='unauthorized_user', password='test_password321')
        login = self.client.login(username='unauthorized_user', password='test_password321')
        self.assertTrue(login)
        response = self.client.get(reverse('todo_edit', kwargs={'pk': self.test_id}))
        self.assertEqual(response.status_code, 403)

    def test_post_to_update_view_updates_table(self):
        login = self.client.login(username='test_user', password='test_password123')
        self.assertTrue(login)
        response = self.client.post(
            reverse('todo_edit', kwargs={'pk': self.test_id}),
            {'title': 'new_title', 'description': 'new_description'}
        )

        # Confirm redirect to todo_detail following post
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_detail', kwargs={'pk': self.test_id}))

        # Confirm table has been updated
        updated_todo = Todo.objects.get(id=self.test_id)
        self.assertEqual(updated_todo.title, 'new_title')
        self.assertEqual(updated_todo.description, 'new_description')

        # Confirm detail page reflects update
        response = self.client.get(reverse('todo_detail', kwargs={'pk': self.test_id}))
        self.assertContains(response, 'new_title')
        self.assertContains(response, 'new_description')


class TodoDeleteViewTests(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            username='test_user',
            password='test_password123'
        )
        self.test_todo = Todo.objects.create(
            author=self.test_user,
            title='title',
            description='description',
        )
        self.test_id = self.test_todo.id

    def test_delete_view_resolves(self):
        view = resolve(f'/todos/{self.test_id}/delete/')
        self.assertEqual(view.func.__name__, TodoDeleteView.as_view().__name__)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('todo_delete', kwargs={'pk': self.test_id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/todos/{self.test_id}/delete/')

    def test_logged_in_user_template(self):
        login = self.client.login(username='test_user', password='test_password123')
        self.assertTrue(login)
        response = self.client.get(reverse('todo_delete', kwargs={'pk': self.test_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_delete.html')
        self.assertContains(response, 'title')
        self.assertContains(response, 'Delete Todo')

    def test_unauthorized_user_cannot_delete_todo(self):
        User.objects.create_user(username='unauthorized_user', password='test_password321')
        login = self.client.login(username='unauthorized_user', password='test_password321')
        self.assertTrue(login)
        response = self.client.get(reverse('todo_delete', kwargs={'pk': self.test_id}))
        self.assertEqual(response.status_code, 403)

    def test_post_to_delete_view_updates_table(self):
        login = self.client.login(username='test_user', password='test_password123')
        self.assertTrue(login)
        response = self.client.post(reverse('todo_delete', kwargs={'pk': self.test_id}))

        # Confirm redirect to todo_list following post
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))

        # Confirm entry has been removed from the table
        with self.assertRaises(Todo.DoesNotExist):
            Todo.objects.get(id=self.test_id)

        # Confirm table row count has been decremented
        self.assertEqual(Todo.objects.count(), 0)

        # Confirm list page reflects update
        response = self.client.get(reverse('todo_list'))
        self.assertNotContains(response, 'new_title')
        self.assertNotContains(response, 'new_description')
        self.assertContains(response, 'You have 0 uncompleted todos.')


class TodoCreateViewTests(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            username='test_user',
            password='test_password123'
        )

    def test_create_view_resolves(self):
        view = resolve(f'/todos/new/')
        self.assertEqual(view.func.__name__, TodoCreateView.as_view().__name__)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('todo_new'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/todos/new/')

    def test_logged_in_user_template(self):
        login = self.client.login(username='test_user', password='test_password123')
        self.assertTrue(login)
        response = self.client.get(reverse('todo_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_new.html')
        self.assertContains(response, 'New Todo')

    def test_post_to_create_view_updates_table(self):
        login = self.client.login(username='test_user', password='test_password123')
        self.assertTrue(login)
        response = self.client.post(
            reverse('todo_new'),
            {'title': 'new_title', 'description': 'new_description'}
        )

        # Confirm todo has been inserted into the table
        try:
            todo = Todo.objects.get(title='new_title')
        except Todo.DoesNotExist:
            self.fail('Todo not created following post to todo_new')

        # Confirm redirect to todo_detail following post
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, todo.get_absolute_url())

        # Confirm table row count has been incremented
        self.assertEqual(Todo.objects.count(), 1)

        # Confirm author of todo is logged-in user
        self.assertEqual(str(todo.author), 'test_user')

        # Confirm list page reflects update
        response = self.client.get(reverse('todo_list'))
        self.assertContains(response, 'new_title')
        self.assertContains(response, 'new_description')
        self.assertContains(response, 'You have 1 uncompleted todo.')
