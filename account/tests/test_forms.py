from django.test import TestCase, override_settings

from account.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from account.models import User

# Create your tests here.
class AccountFormTest(TestCase):
    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.user =User.objects.create_user(
            email="test2@example.com",
            username="test",
            password="Test123Qaz",
            first_name="test",
            last_name="ing",
            phone='375291324567'
        )


    def test_user_login_form_not_valid(self):
        form_data = {'username': self.user.username, 'password': 'Test123Qaz'}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_login_form_username_field_label(self):
        form = UserLoginForm()
        self.assertTrue(
            form.fields['username'].label == None or form.fields['username'].label == 'Имя пользователя'
        )

    def test_user_login_form_password_field_label(self):
        form = UserLoginForm()
        self.assertTrue(
            form.fields['password'].label == None or form.fields['password'].label == 'Password'
        )

    def test_user_register_form_valid(self):
        form_data = {'first_name': 'Test', 'last_name': 'Test', 'username': 'ivan', 'email': 'ivan@test.by', 'phone': '37533',
                     'password1': 'Test123Qaz', 'password2': 'Test123Qaz'}
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_register_form_not_valid_email(self):
        form_data = {'first_name': 'Test', 'last_name': 'Test', 'username': 'ivan', 'email': 'ivantest.by', 'phone': '37533',
                     'password1': 'Test123Qaz', 'password2': 'Test123Qaz'}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_register_form_not_valid_password(self):
        form_data = {'first_name': 'Test', 'last_name': 'Test', 'username': 'ivan', 'email': 'ivan@test.by', 'phone': '37533',
                     'password1': 'Test123Qaz', 'password2': 'Test123Qaz1'}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_register_form_not_valid_phone(self):
        form_data = {'first_name': 'Test', 'last_name': 'Test', 'username': 'ivan', 'email': 'ivan@test.by', 'phone': '3'*16,
                     'password1': 'Test123Qaz', 'password2': 'Test123Qaz'}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_register_form_not_valid_username_empty(self):
        form_data = {'first_name': 'Test', 'last_name': 'Test', 'email': 'ivan@test.by', 'phone': '3'*16,
                     'password1': 'Test123Qaz', 'password2': 'Test123Qaz'}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_register_form_username_field_label(self):
        form = UserRegistrationForm()
        self.assertTrue(
            form.fields['username'].label == None or form.fields['username'].label == 'Username'
        )

    def test_user_register_form_email_field_label(self):
        form = UserRegistrationForm()
        self.assertTrue(
            form.fields['email'].label == None or form.fields['email'].label == 'Email'
        )

    def test_user_register_form_phone_field_label(self):
        form = UserRegistrationForm()
        self.assertTrue(
            form.fields['phone'].label == None or form.fields['phone'].label == 'Phone'
        )

    def test_user_register_form_first_name_field_label(self):
        form = UserRegistrationForm()
        self.assertTrue(
            form.fields['first_name'].label == None or form.fields['first_name'].label == 'First name'
        )

    def test_user_register_form_last_name_field_label(self):
        form = UserRegistrationForm()
        self.assertTrue(
            form.fields['last_name'].label == None or form.fields['last_name'].label == 'Last name'
        )