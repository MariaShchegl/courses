from django.test import TestCase
from histories.models import History
from account.models import User

# Create your tests here.
class HistoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email="beta@example.com",
            username="Beta",
            password="Test123Qaz",
            first_name="test",
            last_name="ing",
            phone='375291324567'
        )
        History.objects.create(
            title='test_history',
            alias='test_history',
            user=User.objects.get(username='Beta'),
            article='test',
            meta_title='test',
            meta_keywords='test',
            meta_description='test'
        )

    def test_history_max_length(self):
        history = History.objects.get(alias='test_history')
        max_length_meta_title = history._meta.get_field('meta_title').max_length
        max_length_meta_keywords = history._meta.get_field('meta_keywords').max_length
        max_length_title = history._meta.get_field('title').max_length
        max_length_alias = history._meta.get_field('alias').max_length
        self.assertEquals(max_length_alias, 255)
        self.assertEquals(max_length_title, 255)
        self.assertEquals(max_length_meta_keywords, 255)
        self.assertEquals(max_length_meta_title, 255)