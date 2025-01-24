from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Todo, User
from rest_framework.authtoken.models import Token


class RegisterAPIViewTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')

        #Quite a lot of a boilerplate code but I'm a person who thinks it's the best to have static test variables where possible.
        self.valid_data = {
            "email": "testuser@example.com",
            "password": "password123"
        }

        self.invalid_email = {
            "email": "testuser@examplecom",
            "password": "password123"
        }

        self.no_email = {
            "password": "password123"
        }

        self.no_password = {
            "email": "testuser@example.com"
        }

        self.blank_email = {
            "email": "",
            "password": "password123"
        }

        self.blank_password = {
            "email": "testuser@example.com",
            "password": ""
        }

    def test_register_valid_user(self):
        response = self.client.post(self.register_url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "User registered successfully")
        self.assertTrue(User.objects.filter(email=self.valid_data['email']).exists())

    def test_register_with_existing_email(self):
        User.objects.create_user(email=self.valid_data['email'], password=self.valid_data['password'])
        response = self.client.post(self.register_url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], "user with this email already exists.")

    def test_register_with_invalid_email(self):
        response = self.client.post(self.register_url, self.invalid_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], "Enter a valid email address.")

    def test_register_with_blank_email(self):
        response = self.client.post(self.register_url, self.blank_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], "This field may not be blank.")

    def test_register_with_blank_password(self):
        response = self.client.post(self.register_url, self.blank_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'][0], "This field may not be blank.")

    def test_register_with_no_email(self):
        response = self.client.post(self.register_url, self.no_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], "This field is required.")

    def test_register_with_no_password(self):
        response = self.client.post(self.register_url, self.no_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'][0], "This field is required.")


class GenerateTokenViewTest(APITestCase):
    def setUp(self):
        self.token_url = reverse('token')
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')

    def test_token_generation(self):
        data = {
            'username': 'testuser@example.com',
            'password': 'password123',
        }

        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        token_value = response.data['token']
        token = Token.objects.get(key=token_value)
        self.assertEqual(token.user, self.user)

    def test_token_generation_failure_username(self):
        data = {
            'username': 'wronguser',
            'password': 'password123',
        }

        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_token_generation_invalid_password(self):
        data = {
            'username': 'testuser@example.com',
            'password': 'wrongpassword',
        }

        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)


class TodoCRUDTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.todo = Todo.objects.create(
            title="Test Todo",
            description="This is a test todo",
            is_completed=False,
            user=self.user
        )
        self.todo_list_url = reverse('todo_list')
        self.todo_detail_url = reverse('todo_detail', args=[self.todo.id])

    def test_create_todo(self):
        data = {
            "title": "New Todo",
            "description": "A new todo description",
            "is_completed": False,
        }
        
        response = self.client.post(self.todo_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 2)
        self.assertEqual(Todo.objects.first().title, "New Todo")
        self.assertEqual(Todo.objects.first().user, self.user)

    def test_get_todo_list(self):
        response = self.client.get(self.todo_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], self.todo.title)

    def test_get_todo_detail(self):
        response = self.client.get(self.todo_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.todo.title)
        self.assertEqual(response.data['description'], self.todo.description)

    def test_update_todo(self):
        data = {
            "title": "Updated Todo Title",
            "description": "Updated description",
            "is_completed": True,
        }

        response = self.client.put(self.todo_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, "Updated Todo Title")
        self.assertEqual(self.todo.description, "Updated description")
        self.assertTrue(self.todo.is_completed)

    def test_delete_todo(self):
        response = self.client.delete(self.todo_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)


class TodoPermissionsTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@example.com', password='password123')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password123')

        self.todo_user1 = Todo.objects.create(
            title="User 1 Todo",
            description="This is User 1's Todo",
            user=self.user1
        )
        self.todo_user2 = Todo.objects.create(
            title="User 2 Todo",
            description="This is User 2's Todo",
            user=self.user2
        )

        self.token_user1 = Token.objects.create(user=self.user1)
        self.token_user2 = Token.objects.create(user=self.user2)

        self.todo_list_url = reverse('todo_list')
        self.todo_detail_url_user1 = reverse('todo_detail', kwargs={'pk': self.todo_user1.pk})
        self.todo_detail_url_user2 = reverse('todo_detail', kwargs={'pk': self.todo_user2.pk})

    def test_user_can_access_own_todos(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_user1.key}')
        response = self.client.get(self.todo_detail_url_user1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_access_other_users_todos(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_user1.key}')
        response = self.client.get(self.todo_detail_url_user2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_gets_only_own_todos(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_user1.key}')
        response = self.client.get(self.todo_list_url)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'User 1 Todo')
