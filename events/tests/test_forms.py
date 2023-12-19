from django.test import TestCase

from events.forms import EventForm, CommentForm
from events.models import Age, Venue, Street, District, City, TypeCity, Area

# Create your tests here.
class EventFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Age.objects.create(
            age='16+'
        )
        Area.objects.create(
            area='test_area2'
        )
        TypeCity.objects.create(
            type='test_type_city',
            abbreviation='ts'
        )
        City.objects.create(
            city='test_city2',
            type_city=TypeCity.objects.get(abbreviation='ts'),
            area=Area.objects.get(area='test_area2')
        )
        District.objects.create(
            district='test_district2',
            city=City.objects.get(city='test_city2')
        )
        Street.objects.create(
            street='test_street2',
            district=District.objects.get(district='test_district2')
        )
        Venue.objects.create(
            street=Street.objects.get(street='test_street2'),
            house='10'
        )

    def test_event_form_not_valid_price(self):
        venue = Venue.objects.get(house=10)
        form_data = {'title': 'Test', 'description': 'Test',  'contacts': 'test', 'price': '1'*26, 'meta_title': 'test', 'meta_description': 'test', 'meta_keywords': 'test'}
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_event_form_not_valid_price_empty(self):
        venue = Venue.objects.get(house=10)
        form_data = {'title': 'Test', 'description': 'Test',  'contacts': 'test', 'meta_title': 'test', 'meta_description': 'test', 'meta_keywords': 'test'}
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_event_form_title_field_label(self):
        form = EventForm()
        self.assertTrue(
            form.fields['title'].label == None or form.fields['title'].label == 'Название'
        )

    def test_event_form_not_valid_title(self):
        venue = Venue.objects.get(house=10)
        form_data = {'title': 'T'*256, 'description': 'Test',  'contacts': 'test', 'price': '100', 'meta_title': 'test', 'meta_description': 'test', 'meta_keywords': 'test'}
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_event_form_not_valid_title_empty(self):
        venue = Venue.objects.get(house=10)
        form_data = {'description': 'Test',  'contacts': 'test', 'price': '100', 'meta_title': 'test', 'meta_description': 'test', 'meta_keywords': 'test'}
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_event_form_description_field_label(self):
        form = EventForm()
        self.assertTrue(
            form.fields['description'].label == None or form.fields['description'].label == 'Описание объявления*'
        )

    def test_event_form_not_valid_description_empty(self):
        venue = Venue.objects.get(house=10)
        form_data = {'title': 'Test', 'contacts': 't'*256, 'price': '100', 'meta_title': 'test', 'meta_description': 'test', 'meta_keywords': 'test'}
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_event_form_contacts_field_label(self):
        form = EventForm()
        self.assertTrue(
            form.fields['contacts'].label == None or form.fields['contacts'].label == 'Контакты* (+375 29 123-45-67, www.example.com)'
        )

    def test_event_form_not_valid_contacts(self):
        venue = Venue.objects.get(house=10)
        form_data = {'title': 'Test', 'description': 'Test',  'contacts': 't'*256, 'price': '100', 'meta_title': 'test', 'meta_description': 'test', 'meta_keywords': 'test'}
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_event_form_not_valid_contacts_empty(self):
        venue = Venue.objects.get(house=10)
        form_data = {'title': 'Test', 'description': 'Test',  'price': '100', 'meta_title': 'test', 'meta_description': 'test', 'meta_keywords': 'test'}
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_event_form_meta_keywords_field_label(self):
        form = EventForm()
        self.assertTrue(
            form.fields['meta_keywords'].label == None or form.fields['meta_keywords'].label == 'Мета ключевые слова'
        )

    def test_event_form_not_valid_meta_keywords(self):
        venue = Venue.objects.get(house=10)
        form_data = {'title': 'Test', 'description': 'Test',  'contacts': 'test', 'price': '100', 'meta_title': 'test', 'meta_description': 'test', 'meta_keywords': 't'*256}
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_event_form_not_valid_meta_keywords_empty(self):
        venue = Venue.objects.get(house=10)
        form_data = {'title': 'Test', 'description': 'Test',  'contacts': 'test', 'price': '100', 'meta_title': 'test', 'meta_description': 'test'}
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_event_form_meta_title_field_label(self):
        form = EventForm()
        self.assertTrue(
            form.fields['meta_title'].label == None or form.fields['meta_title'].label == 'Мета заголовок'
        )

    def test_event_form_not_valid_meta_title(self):
        venue = Venue.objects.get(house=10)
        form_data = {'title': 'Test', 'description': 'Test',  'contacts': 'test', 'price': '100', 'meta_title': 't'*256, 'meta_description': 'test', 'meta_keywords': 'test'}
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_event_form_not_valid_meta_title_empty(self):
        venue = Venue.objects.get(house=10)
        form_data = {'title': 'Test', 'description': 'Test',  'contacts': 'test', 'price': '100', 'meta_description': 'test', 'meta_keywords': 'test'}
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_event_form_meta_description_field_label(self):
        form = EventForm()
        self.assertTrue(
            form.fields['meta_description'].label == None or form.fields['meta_description'].label == 'Мета описание'
        )

    def test_event_form_not_valid_meta_description_empty(self):
        venue = Venue.objects.get(house=10)
        form_data = {'title': 'Test', 'description': 'Test',  'contacts': 'test', 'price': '100', 'meta_title': 'test', 'meta_keywords': 'test'}
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_event_form_not_valid_venue_empty(self):
        venue = Venue.objects.get(house=10)
        form_data = {'title': 'Test', 'description': 'Test',  'contacts': 'test', 'price': '100', 'meta_title': 'test', 'meta_description': 'test', 'meta_keywords': 'test'}
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_comment_form_field_label(self):
        form = CommentForm()
        self.assertTrue(
            form.fields['comment'].label == None or form.fields['comment'].label == 'Сообщение'
        )

    def test_comment_form_valid(self):
        form_data = {'comment': 'Comment'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_not_valid_empty(self):
        form_data = {}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())