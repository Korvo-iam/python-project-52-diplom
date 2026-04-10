import uuid
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model

from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from .models import Label

User = get_user_model()


class LabelCRUDTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username=f'admin_{uuid.uuid4().hex[:8]}',
            password='pass'
        )
        self.client.force_login(self.admin)

    def test_create_label_message(self):
        name = f'label_{uuid.uuid4().hex[:8]}'

        response = self.client.post(
            reverse('labels:create'),
            {'name': name},
            follow=True
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно создана" in str(m) for m in messages))
        self.assertTrue(Label.objects.filter(name=name).exists())

    def test_update_label_message(self):
        label = Label.objects.create(
            name=f'old_{uuid.uuid4().hex[:8]}'
        )

        new_name = f'new_{uuid.uuid4().hex[:8]}'

        response = self.client.post(
            reverse('labels:update', args=[label.id]),
            {'name': new_name},
            follow=True
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно изменена" in str(m) for m in messages))

        label.refresh_from_db()
        self.assertEqual(label.name, new_name)

    def test_delete_label_message(self):
        label = Label.objects.create(
            name=f'del_{uuid.uuid4().hex[:8]}'
        )

        response = self.client.post(
            reverse('labels:delete', args=[label.id]),
            follow=True
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно удалена" in str(m) for m in messages))

        self.assertFalse(Label.objects.filter(id=label.id).exists())

    def test_list_labels(self):
        l1 = Label.objects.create(name=f'l1_{uuid.uuid4().hex[:8]}')
        l2 = Label.objects.create(name=f'l2_{uuid.uuid4().hex[:8]}')

        response = self.client.get(reverse('labels:list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, l1.name)
        self.assertContains(response, l2.name)

    def test_create_label(self):
        name = f'label_{uuid.uuid4().hex[:8]}'

        response = self.client.post(
            reverse('labels:create'),
            {'name': name}
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name=name).exists())

    def test_update_label(self):
        label = Label.objects.create(
            name=f'old_{uuid.uuid4().hex[:8]}'
        )

        new_name = f'new_{uuid.uuid4().hex[:8]}'

        response = self.client.post(
            reverse('labels:update', args=[label.id]),
            {'name': new_name}
        )

        self.assertEqual(response.status_code, 302)

        label.refresh_from_db()
        self.assertEqual(label.name, new_name)

    def test_delete_label(self):
        label = Label.objects.create(
            name=f'del_{uuid.uuid4().hex[:8]}'
        )

        response = self.client.post(
            reverse('labels:delete', args=[label.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(id=label.id).exists())

    def test_cannot_delete_label_linked_to_task(self):
        label = Label.objects.create(
            name=f'linked_{uuid.uuid4().hex[:8]}'
        )

        status = Status.objects.create(
            name=f'status_{uuid.uuid4().hex[:8]}'
        )

        user = User.objects.create_user(
            username=f'user_{uuid.uuid4().hex[:8]}',
            password='pass'
        )

        task = Task.objects.create(
            name='Task',
            description='Description',
            status=status,
            author=user
        )

        task.labels.add(label)

        response = self.client.post(
            reverse('labels:delete', args=[label.id]),
            follow=True
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("Невозможно удалить метку" in str(m) for m in messages)
        )

        self.assertTrue(Label.objects.filter(id=label.id).exists())

    def test_access_requires_login(self):
        self.client.logout()

        response = self.client.get(reverse('labels:list'))

        self.assertRedirects(response, '/login/?next=/labels/')