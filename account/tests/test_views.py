from django.test import TestCase

# Create your tests here.

from account.models import User
from django.urls import reverse
from events.models import TypeEvent, Area, TypeCity, City, District, Street, Age, Venue, Event, Comment

class AccountViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TypeEvent.objects.create(
            type='test_type3'
        )
        Area.objects.create(
            area='test_area3'
        )
        TypeCity.objects.create(
            type='test_type3',
            abbreviation='test3'
        )
        City.objects.create(
            city='test_city3',
            area=Area.objects.get(area="test_area3"),
            type_city=TypeCity.objects.get(abbreviation="test3")
        )
        District.objects.create(
            district='test_district3',
            city=City.objects.get(city="test_city3"),
        )
        Street.objects.create(
            street='test_street3',
            district=District.objects.get(district="test_district3")
        )
        Age.objects.create(
            age='10+'
        )
        Venue.objects.create(
            title='test_title3',
            house='house',
            office='office3',
            description='test_description',
            street=Street.objects.get(street='test_street3')
        )
        User.objects.create(
            email="alpha3@example.com",
            username="Alpha3",
            password="Test123Qaz",
            first_name="test",
            last_name="ing",
            phone='375291324567'
        )
        Event.objects.create(
            title='test_event3',
            description='test_description',
            contacts='test',
            alias='test_alias3',
            value="{'test':'test'}",
            price='12',
            meta_title='test',
            meta_keywords='test',
            meta_description='test',
            type_event=TypeEvent.objects.get(type="test_type3"),
            age=Age.objects.get(age="10+"),
            user=User.objects.get(username='Alpha3')
        )
        Event.objects.get(alias='test_alias3').venue.add(Venue.objects.get(office="office3"))
        Comment.objects.create(
            comment='test_comment3',
            user=User.objects.get(username='Alpha3'),
            event=Event.objects.get(alias="test_alias3")
        )

    def setUp(self):
        self.user = User.objects.create_user(
            username="test3",
            email="test3@example.com",
            password="Test123Qaz"
        )

    def test_view_url_login_exists_at_desired_location(self):
        resp = self.client.get('/account/login/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'account/login.html')

    def test_view_url_login_accessible_by_name(self):
        resp = self.client.get(reverse('account:login'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'account/login.html')

    def test_view_url_register_exists_at_desired_location(self):
        resp = self.client.get('/account/register/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'account/register.html')

    def test_view_url_register_accessible_by_name(self):
        resp = self.client.get(reverse('account:register'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'account/register.html')

    def test_view_url_index_not_auth_exists_at_desired_location(self):
        resp = self.client.get('/account/')
        self.assertEqual(resp.status_code, 403)

    def test_view_url_index_not_auth_accessible_by_name(self):
        resp = self.client.get(reverse('account:index'))
        self.assertEqual(resp.status_code, 403)

    def test_view_url_confirm_not_auth_exists_at_desired_location(self):
        resp = self.client.get('/account/confirm-page/')
        self.assertEqual(resp.status_code, 403)

    def test_view_url_confirm_not_auth_accessible_by_name(self):
        resp = self.client.get(reverse('account:confirm'))
        self.assertEqual(resp.status_code, 403)

    def test_view_url_index_auth_exists_at_desired_location(self):
        login = self.client.login(username='test3', password='Test123Qaz')
        resp = self.client.get('/account/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'account/account.html')

    def test_view_url_index_auth_accessible_by_name(self):
        login = self.client.login(username='test3', password='Test123Qaz')
        resp = self.client.get(reverse('account:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'account/account.html')

    def test_view_url_logout_not_auth_exists_at_desired_location(self):
        resp = self.client.get('/account/logout/')
        self.assertEqual(resp.status_code, 302)

    def test_view_url_logout_not_auth_accessible_by_name(self):
        resp = self.client.get(reverse('account:logout'))
        self.assertEqual(resp.status_code, 302)

    def test_view_url_logout_auth_exists_at_desired_location(self):
        login = self.client.login(username='test3', password='Test123Qaz')
        resp = self.client.get('/account/logout/')
        self.assertEqual(resp.status_code, 302)

    def test_view_url_logout_auth_accessible_by_name(self):
        login = self.client.login(username='test3', password='Test123Qaz')
        resp = self.client.get(reverse('account:logout'))
        self.assertEqual(resp.status_code, 302)

    def test_view_url_confirm_auth_exists_at_desired_location(self):
        login = self.client.login(username='test3', password='Test123Qaz')
        resp = self.client.get('/account/confirm-page/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'account/confirm-page.html')

    def test_view_url_confirm_auth_accessible_by_name(self):
        login = self.client.login(username='test3', password='Test123Qaz')
        resp = self.client.get(reverse('account:confirm'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'account/confirm-page.html')

    def test_view_url_confirm_method_not_auth_exists_at_desired_location(self):
        resp = self.client.get('/account/confirm-page/test_alias3/addEvent')
        self.assertEqual(resp.status_code, 403)

    def test_view_url_confirm_method_auth_exists_at_desired_location(self):
        login = self.client.login(username='test3', password='Test123Qaz')
        resp = self.client.get('/account/confirm-page/test_alias3/addEvent')
        self.assertEqual(resp.status_code, 302)

    def test_view_url_confirm_method_auth_accessible_by_name(self):
        login = self.client.login(username='test3', password='Test123Qaz')
        resp = self.client.get(reverse('account:confirm_method', kwargs={'alias': 'test_alias3', 'method': 'addEvent'}))
        self.assertEqual(resp.status_code, 302)

    def test_view_url_confirm_method_not_auth_accessible_by_name(self):
        resp = self.client.get(reverse('account:confirm_method', kwargs={'alias': 'test_alias3', 'method': 'addEvent'}))
        self.assertEqual(resp.status_code, 403)