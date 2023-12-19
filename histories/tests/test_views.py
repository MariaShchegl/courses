from django.test import TestCase

# Create your tests here.
from account.models import User
from django.urls import reverse
from histories.models import History

class HistoryViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email="beta2@example.com",
            username="Beta2",
            password="Test123Qaz",
            first_name="test",
            last_name="ing",
            phone='375291324567'
        )
        for i in range(7):
            History.objects.create(
                title=f'test_history_{i}',
                alias=f'test_history_{i}',
                user=User.objects.get(username='Beta2'),
                article=f'test{i}',
                meta_title=f'test{i}',
                meta_keywords=f'test{i}',
                meta_description=f'test{i}',
                is_show=True
            )

    def setUp(self):
        self.user = User.objects.create_user(
            username="test4",
            email="test4@example.com",
            password="Test123Qaz"
        )

        self.staff = User.objects.create_user(
            username="test5",
            email="test5@example.com",
            password="Test123Qaz",
            is_staff=True,
            is_superuser=True
        )

    def test_view_url_history_index_exists_at_desired_location(self):
        resp = self.client.get('/history/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['histories']), 5)
        self.assertEqual(len(resp.context['paginationList']), 2)
        self.assertTemplateUsed(resp, 'histories/history.html')

    def test_view_url_history_index_accessible_by_name(self):
        resp = self.client.get(reverse('histories:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['histories']), 5)
        self.assertEqual(len(resp.context['paginationList']), 2)
        self.assertTemplateUsed(resp, 'histories/history.html')

    def test_view_url_history_index_page_exists_at_desired_location(self):
        resp = self.client.get('/history/?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['histories']), 2)
        self.assertEqual(len(resp.context['paginationList']), 2)
        self.assertTemplateUsed(resp, 'histories/history.html')

    def test_view_url_history_show_exists_at_desired_location(self):
        resp = self.client.get('/history/test_history_1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'histories/note.html')

    def test_view_url_history_show_404_exists_at_desired_location(self):
        resp = self.client.get('/history/test_history_25/')
        self.assertEqual(resp.status_code, 404)

    def test_view_url_history_change_not_auth_exists_at_desired_location(self):
        history = History.objects.get(alias='test_history_1')
        resp = self.client.get(f'/admin/histories/history/{history.id}/change/')
        self.assertEqual(resp.status_code, 302)

    def test_view_url_history_change_auth_user_exists_at_desired_location(self):
        login = self.client.login(username='test4', password='Test123Qaz')
        history = History.objects.get(alias='test_history_1')
        resp = self.client.get(f'/admin/histories/history/{history.id}/change/')
        self.assertEqual(resp.status_code, 302)

    def test_view_url_history_change_auth_staff_exists_at_desired_location(self):
        login = self.client.login(username='test5', password='Test123Qaz')
        history = History.objects.get(alias='test_history_1')
        resp = self.client.get(f'/admin/histories/history/{history.id}/change/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_history_change_auth_staff_404_exists_at_desired_location(self):
        login = self.client.login(username='test5', password='Test123Qaz')
        history = History.objects.get(alias='test_history_1')
        resp = self.client.get(f'/admin/histories/history/25/change/')
        self.assertEqual(resp.status_code, 302)

    def test_view_url_history_delete_not_auth_exists_at_desired_location(self):
        history = History.objects.get(alias='test_history_1')
        resp = self.client.get(f'/admin/histories/history/{history.id}/delete/')
        self.assertEqual(resp.status_code, 302)

    def test_view_url_history_delete_auth_user_exists_at_desired_location(self):
        login = self.client.login(username='test4', password='Test123Qaz')
        history = History.objects.get(alias='test_history_1')
        resp = self.client.get(f'/admin/histories/history/{history.id}/delete/')
        self.assertEqual(resp.status_code, 302)

    def test_view_url_history_delete_auth_staff_exists_at_desired_location(self):
        login = self.client.login(username='test5', password='Test123Qaz')
        history = History.objects.get(alias='test_history_1')
        resp = self.client.get(f'/admin/histories/history/{history.id}/delete/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_history_delete_auth_staff_404_exists_at_desired_location(self):
        login = self.client.login(username='test5', password='Test123Qaz')
        history = History.objects.get(alias='test_history_1')
        resp = self.client.get(f'/admin/histories/history/25/delete/')
        self.assertEqual(resp.status_code, 302)