from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from todo.models import Item


class SharedStaffTodoAccessTests(TestCase):
    def setUp(self):
        self.item = Item.objects.create(name='Confidential staff item')

    def test_guest_cannot_read_or_mutate(self):
        for path in ('/', '/add', f'/edit/{self.item.pk}', f'/delete/{self.item.pk}', f'/toggle/{self.item.pk}'):
            self.assertEqual(self.client.get(path).status_code, 302)
            self.assertEqual(self.client.post(path, {'name': 'changed'}).status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Confidential staff item')

    def test_nonstaff_cannot_read_or_mutate(self):
        user = get_user_model().objects.create_user(username='ordinary')
        self.client.force_login(user)
        self.assertEqual(self.client.get('/').status_code, 302)
        self.assertEqual(self.client.post(f'/delete/{self.item.pk}').status_code, 302)
        self.assertTrue(Item.objects.filter(pk=self.item.pk).exists())

    def test_staff_get_does_not_delete_or_toggle_and_csrf_required(self):
        user = get_user_model().objects.create_user(username='staff', is_staff=True)
        self.client.force_login(user)
        for action in ('delete', 'toggle'):
            self.assertEqual(self.client.get(f'/{action}/{self.item.pk}').status_code, 405)
        protected = Client(enforce_csrf_checks=True)
        protected.force_login(user)
        self.assertEqual(protected.post(f'/delete/{self.item.pk}').status_code, 403)
        self.item.refresh_from_db()
        self.assertFalse(self.item.done)

    def test_rendered_staff_form_permits_valid_csrf_post(self):
        user = get_user_model().objects.create_user(username='staff', is_staff=True)
        client = Client(enforce_csrf_checks=True)
        client.force_login(user)
        self.assertEqual(client.get('/').status_code, 200)
        token = client.cookies['csrftoken'].value
        self.assertEqual(client.post(f'/delete/{self.item.pk}', {'csrfmiddlewaretoken': token}).status_code, 302)
        self.assertFalse(Item.objects.filter(pk=self.item.pk).exists())
