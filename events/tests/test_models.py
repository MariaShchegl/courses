from django.test import TestCase
from events.models import Photo, Category, TypeEvent, Area, TypeCity, City, District, Street, Age, Venue, Event, Comment
from account.models import User
from datetime import datetime

# Create your tests here.
class EventModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Photo.objects.create(
            path="/test/test.jpg"
        )
        Category.objects.create(
            category='test_category',
            alias='test_cat',
        )
        TypeEvent.objects.create(
            type='test_type'
        )
        Area.objects.create(
            area='test_area'
        )
        TypeCity.objects.create(
            type='test_type',
            abbreviation='test'
        )
        City.objects.create(
            city='test_city',
            area=Area.objects.get(area="test_area"),
            type_city=TypeCity.objects.get(abbreviation="test")
        )
        District.objects.create(
            district='test_district',
            city=City.objects.get(city="test_city"),
        )
        Street.objects.create(
            street='test_street',
            district=District.objects.get(district="test_district")
        )
        Age.objects.create(
            age='10+'
        )
        Venue.objects.create(
            title='test_title',
            house='house',
            office='office',
            description='test_description',
            street=Street.objects.get(street='test_street')
        )
        User.objects.create(
            email="alpha@example.com",
            username="Alpha",
            password="Test123Qaz",
            first_name="test",
            last_name="ing",
            phone='375291324567'
        )
        Event.objects.create(
            title='test_event',
            description='test_description',
            contacts='test',
            alias='test_alias',
            value="{'test':'test'}",
            price='12',
            meta_title='test',
            meta_keywords='test',
            meta_description='test',
            type_event=TypeEvent.objects.get(type="test_type"),
            age=Age.objects.get(age="10+"),
            user=User.objects.get(username='Alpha')
        )
        Event.objects.get(alias='test_alias').venue.add(Venue.objects.get(office="office"))
        Comment.objects.create(
            comment='test_comment',
            user=User.objects.get(username='Alpha'),
            event=Event.objects.get(alias="test_alias")
        )

    def test_photo_max_length(self):
        photo = Photo.objects.get(path="/test/test.jpg")
        max_length = photo._meta.get_field('path').max_length
        self.assertEquals(max_length, 100)

    def test_category_max_length(self):
        category = Category.objects.get(alias="test_cat")
        max_length_cat = category._meta.get_field('category').max_length
        max_length_alias = category._meta.get_field('alias').max_length
        self.assertEquals(max_length_alias, 255)
        self.assertEquals(max_length_cat, 255)

    def test_type_event_max_length(self):
        type_event = TypeEvent.objects.get(type="test_type")
        max_length = type_event._meta.get_field('type').max_length
        self.assertEquals(max_length, 30)

    def test_area_max_length(self):
        area = Area.objects.get(area="test_area")
        max_length = area._meta.get_field('area').max_length
        self.assertEquals(max_length, 50)

    def test_type_city_max_length(self):
        type_city = TypeCity.objects.get(abbreviation="test")
        max_length_type = type_city._meta.get_field('type').max_length
        max_length_abbreviation = type_city._meta.get_field('abbreviation').max_length
        self.assertEquals(max_length_abbreviation, 10)
        self.assertEquals(max_length_type, 30)

    def test_city_max_length(self):
        city = City.objects.get(city="test_city")
        max_length = city._meta.get_field('city').max_length
        self.assertEquals(max_length, 50)

    def test_district_max_length(self):
        district = District.objects.get(district="test_district")
        max_length = district._meta.get_field('district').max_length
        self.assertEquals(max_length, 50)

    def test_street_max_length(self):
        street = Street.objects.get(street="test_street")
        max_length = street._meta.get_field('street').max_length
        self.assertEquals(max_length, 50)

    def test_age_max_length(self):
        age = Age.objects.get(age="10+")
        max_length = age._meta.get_field('age').max_length
        self.assertEquals(max_length, 10)

    def test_venue_max_length(self):
        venue = Venue.objects.get(office="office")
        max_length_office = venue._meta.get_field('office').max_length
        max_length_house = venue._meta.get_field('house').max_length
        max_length_title = venue._meta.get_field('title').max_length
        max_length_description = venue._meta.get_field('description').max_length
        self.assertEquals(max_length_description, 255)
        self.assertEquals(max_length_house, 10)
        self.assertEquals(max_length_title, 30)
        self.assertEquals(max_length_office, 10)

    def test_event_max_length(self):
        event = Event.objects.get(alias="test_alias")
        max_length_title = event._meta.get_field('title').max_length
        max_length_contacts = event._meta.get_field('contacts').max_length
        max_length_alias = event._meta.get_field('alias').max_length
        max_length_price = event._meta.get_field('price').max_length
        max_length_meta_title = event._meta.get_field('meta_title').max_length
        max_length_meta_keywords = event._meta.get_field('meta_keywords').max_length
        self.assertEquals(max_length_meta_keywords, 255)
        self.assertEquals(max_length_meta_title, 255)
        self.assertEquals(max_length_price, 20)
        self.assertEquals(max_length_title, 255)
        self.assertEquals(max_length_alias, 255)
        self.assertEquals(max_length_contacts, 255)

    def test_comment_max_length(self):
        comment = Comment.objects.get(comment="test_comment")
        test_str = comment.event.title + '|' + comment.user.username
        self.assertEquals(str(comment), test_str)