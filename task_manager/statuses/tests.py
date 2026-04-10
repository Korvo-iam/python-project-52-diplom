import uuid
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model

from .models import Status

User = get_user_model()


class StatusCRUDTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username=f'admin_{uuid.uuid4().hex[:8]}',
            email='admin@test.com',
            password='pass'
        )
        self.client.force_login(self.admin)

    def test_create_status_message(self):
        name = f'status_{uuid.uuid4().hex[:8]}'

        response = self.client.post(
            reverse('statuses:create'),
            {'name': name},
            follow=True
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно создан" in str(m) for m in messages))
        self.assertTrue(Status.objects.filter(name=name).exists())

    def test_update_status_message(self):
        status = Status.objects.create(
            name=f'status_{uuid.uuid4().hex[:8]}'
        )

        new_name = f'status_{uuid.uuid4().hex[:8]}'

        response = self.client.post(
            reverse('statuses:update', args=[status.id]),
            {'name': new_name},
            follow=True
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно изменен" in str(m) for m in messages))

        status.refresh_from_db()
        self.assertEqual(status.name, new_name)

    def test_delete_status_message(self):
        status = Status.objects.create(
            name=f'status_{uuid.uuid4().hex[:8]}'
        )

        response = self.client.post(
            reverse('statuses:delete', args=[status.id]),
            follow=True
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно удален" in str(m) for m in messages))

        self.assertFalse(Status.objects.filter(id=status.id).exists())

    def test_list_statuses(self):
        s1 = Status.objects.create(name=f's1_{uuid.uuid4().hex[:8]}')
        s2 = Status.objects.create(name=f's2_{uuid.uuid4().hex[:8]}')

        response = self.client.get(reverse('statuses:list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, s1.name)
        self.assertContains(response, s2.name)

    def test_create_status(self):
        name = f'status_{uuid.uuid4().hex[:8]}'

        response = self.client.post(
            reverse('statuses:create'),
            {'name': name}
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name=name).exists())

    def test_update_status(self):
        status = Status.objects.create(
            name=f'status_{uuid.uuid4().hex[:8]}'
        )

        new_name = f'status_{uuid.uuid4().hex[:8]}'

        response = self.client.post(
            reverse('statuses:update', args=[status.id]),
            {'name': new_name}
        )

        self.assertEqual(response.status_code, 302)

        status.refresh_from_db()
        self.assertEqual(status.name, new_name)

    def test_delete_status(self):
        status = Status.objects.create(
            name=f'status_{uuid.uuid4().hex[:8]}'
        )

        response = self.client.post(
            reverse('statuses:delete', args=[status.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=status.id).exists())

    def test_access_requires_login(self):
        self.client.logout()

        response = self.client.get(reverse('statuses:list'))

        self.assertRedirects(
            response,
            '/login/?next=/statuses/'
        )
