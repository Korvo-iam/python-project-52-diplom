import uuid
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCRUDTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username=f'admin_{uuid.uuid4().hex[:8]}',
            password='pass'
        )
        self.client.force_login(self.admin)

    def test_create_user_message(self):
        username = f'user_{uuid.uuid4().hex[:8]}'

        response = self.client.post(reverse('users:user_create'), {
            'username': username,
            'first_name': 'flash',
            'last_name': 'user',
            'password1': '12345',
            'password2': '12345'
        }, follow=True)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно зарегистрирован" in str(m) for m in messages))

        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username=username).exists())

    def test_update_user_message(self):
        user = User.objects.create_user(
            username=f'u_{uuid.uuid4().hex[:8]}',
            password='12345'
        )

        new_username = f'updated_{uuid.uuid4().hex[:8]}'

        response = self.client.post(
            reverse('users:user_update', args=[user.id]),
            {
                'username': new_username,
                'first_name': 'updated',
                'last_name': 'user',
                'password1': '12345',
                'password2': '12345'
            },
            follow=True
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно изменен" in str(m) for m in messages))

        user.refresh_from_db()
        self.assertEqual(user.username, new_username)

    def test_delete_user_message(self):
        user = User.objects.create_user(
            username=f'del_{uuid.uuid4().hex[:8]}',
            password='12345'
        )

        response = self.client.post(
            reverse('users:user_delete', args=[user.id]),
            follow=True
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно удален" in str(m) for m in messages))

        self.assertFalse(User.objects.filter(id=user.id).exists())

    def test_create_user(self):
        username = f'test_{uuid.uuid4().hex[:8]}'

        response = self.client.post(reverse('users:user_create'), {
            'username': username,
            'first_name': 'test',
            'last_name': 'user',
            'password1': '12345',
            'password2': '12345'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username=username).exists())

    def test_update_user(self):
        user = User.objects.create_user(
            username=f'u_{uuid.uuid4().hex[:8]}',
            password='12345'
        )

        new_username = f'updated_{uuid.uuid4().hex[:8]}'

        response = self.client.post(
            reverse('users:user_update', args=[user.id]),
            {
                'username': new_username,
                'first_name': 'updated',
                'last_name': 'user',
                'password1': '123456',
                'password2': '123456'
            }
        )

        self.assertEqual(response.status_code, 302)

        user.refresh_from_db()
        self.assertEqual(user.username, new_username)

    def test_delete_user(self):
        user = User.objects.create_user(
            username=f'del_{uuid.uuid4().hex[:8]}',
            password='12345'
        )

        response = self.client.post(
            reverse('users:user_delete', args=[user.id]),
            follow=True
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно удален" in str(m) for m in messages))

        self.assertFalse(User.objects.filter(id=user.id).exists())