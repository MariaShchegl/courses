from django.test import TestCase

# Create your tests here.
from account.models import User

class AccountModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        User.objects.create(
            email="test@example.com",
            username="Delta",
            password="Test123Qaz",
            first_name="test",
            last_name="ing",
            phone='375291324567'
        )

    def test_phone_label(self):
        user = User.objects.get(username="Delta")
        field_label = user._meta.get_field('phone').verbose_name
        self.assertEquals(field_label,'phone')

    def test_photo_max_length(self):
        user = User.objects.get(username="Delta")
        max_length = user._meta.get_field('phone').max_length
        self.assertEquals(max_length,15)
