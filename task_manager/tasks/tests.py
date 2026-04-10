import uuid
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model

from .models import Task
from task_manager.statuses.models import Status

User = get_user_model()


class TaskCRUDTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username=f'admin_{uuid.uuid4().hex[:8]}',
            email='admin@test.com',
            password='pass'
        )
        self.client.force_login(self.admin)

        self.status = Status.objects.create(
            name=f'status_{uuid.uuid4().hex[:8]}'
        )

        self.user = User.objects.create_user(
            username=f'user_{uuid.uuid4().hex[:8]}',
            password='pass'
        )

    def test_create_task_message(self):
        name = f'task_{uuid.uuid4().hex[:8]}'

        response = self.client.post(reverse('tasks:task_create'), {
            'name': name,
            'description': 'Описание тестовой задачи',
            'status': self.status.id,
            'executor': self.user.id,
        }, follow=True)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Задача успешно создана!" in str(m) for m in messages))
        self.assertTrue(Task.objects.filter(name=name).exists())

    def test_update_task_message(self):
        task = Task.objects.create(
            name=f'task_{uuid.uuid4().hex[:8]}',
            description='Описание',
            status=self.status,
            author=self.admin,
            executor=self.user
        )

        new_name = f'task_{uuid.uuid4().hex[:8]}'

        response = self.client.post(
            reverse('tasks:task_update', args=[task.id]),
            {
                'name': new_name,
                'description': 'Новое описание',
                'status': self.status.id,
                'executor': self.user.id,
            },
            follow=True
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Задача успешно изменена!" in str(m) for m in messages))

        task.refresh_from_db()
        self.assertEqual(task.name, new_name)

    def test_delete_task_message(self):
        task = Task.objects.create(
            name=f'task_{uuid.uuid4().hex[:8]}',
            description='Описание',
            status=self.status,
            author=self.admin,
            executor=self.user
        )

        response = self.client.post(
            reverse('tasks:task_delete', args=[task.id]),
            follow=True
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Задача успешно удалена!" in str(m) for m in messages))

        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_create_task(self):
        name = f'task_{uuid.uuid4().hex[:8]}'

        response = self.client.post(reverse('tasks:task_create'), {
            'name': name,
            'description': 'Описание',
            'status': self.status.id,
            'executor': self.user.id,
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name=name).exists())

    def test_update_task(self):
        task = Task.objects.create(
            name=f'task_{uuid.uuid4().hex[:8]}',
            description='Описание',
            status=self.status,
            author=self.admin,
            executor=self.user
        )

        new_name = f'task_{uuid.uuid4().hex[:8]}'

        response = self.client.post(
            reverse('tasks:task_update', args=[task.id]),
            {
                'name': new_name,
                'description': 'Новое описание',
                'status': self.status.id,
                'executor': self.user.id,
            }
        )

        self.assertEqual(response.status_code, 302)

        task.refresh_from_db()
        self.assertEqual(task.name, new_name)
        self.assertEqual(task.description, 'Новое описание')

    def test_delete_task(self):
        task = Task.objects.create(
            name=f'task_{uuid.uuid4().hex[:8]}',
            description='Описание',
            status=self.status,
            author=self.admin,
            executor=self.user
        )

        response = self.client.post(
            reverse('tasks:task_delete', args=[task.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_access_requires_login(self):
        self.client.logout()

        response = self.client.get(reverse('tasks:task_list'))

        self.assertRedirects(response, '/login/?next=/tasks/')