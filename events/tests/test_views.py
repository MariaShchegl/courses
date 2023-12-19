from django.test import TestCase

# Create your tests here.
from account.models import User
from django.urls import reverse
from events.models import Photo, Category, TypeEvent, Area, TypeCity, City, District, Street, Age, Venue, Event, Comment

class EventViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Photo.objects.create(
            path="/test1/test1.jpg"
        )
        Category.objects.create(
            category='test_category1',
            alias='test_cat1',
            is_publish=True,
            is_show=True
        )
        TypeEvent.objects.create(
            id=1,
            type='test_type1'
        )
        TypeEvent.objects.create(
            id=2,
            type='test_type2'
        )
        Area.objects.create(
            area='test_area1',
            is_publish=True
        )
        TypeCity.objects.create(
            type='test_type1',
            abbreviation='test1'
        )
        City.objects.create(
            city='test_city1',
            area=Area.objects.get(area="test_area1"),
            type_city=TypeCity.objects.get(abbreviation="test1"),
            is_publish=True
        )
        District.objects.create(
            district='test_district1',
            city=City.objects.get(city="test_city1"),
            is_publish=True
        )
        Street.objects.create(
            street='test_street1',
            district=District.objects.get(district="test_district1"),
            is_publish=True
        )
        Age.objects.create(
            age='8+',
            is_publish=True
        )
        Venue.objects.create(
            title='test_title1',
            house='house1',
            office='office1',
            description='test_description1',
            street=Street.objects.get(street='test_street1'),
        )
        User.objects.create_user(
            email="beta4@example.com",
            username="Beta4",
            password="Test123Qaz",
            first_name="test",
            last_name="ing",
            phone='375291324567',
            is_active=True
        )
        for i in range(7):
            Event.objects.create(
                title=f'test_event_{i}',
                description=f'test_description_{i}',
                contacts='test',
                alias=f'test_alias_event_{i}',
                value={'social_links':[]},
                price='12',
                meta_title='test',
                meta_keywords='test',
                meta_description='test',
                type_event=TypeEvent.objects.get(type='test_type2'),
                age=Age.objects.get(age="8+"),
                user=User.objects.get(username='Beta4'),
                is_show=True,
                is_publish=True
            ).venue.add(Venue.objects.get(office="office1"))

        for i in range(7):
            Event.objects.create(
                title=f'test_event_{i}_1',
                description=f'test_description_{i}_1',
                contacts='test',
                alias=f'test_alias_event_{i}_1',
                value={'social_links':[]},
                price='12',
                meta_title='test',
                meta_keywords='test',
                meta_description='test',
                type_event=TypeEvent.objects.get(type='test_type1'),
                age=Age.objects.get(age="8+"),
                user=User.objects.get(username='Beta4'),
                is_show=True,
                is_publish=True,
                start_event='2024-01-10 00:00:00'
            ).venue.add(Venue.objects.get(office="office1"))
        Comment.objects.create(
            comment='test_comment_1',
            user=User.objects.get(username='Beta4'),
            event=Event.objects.get(alias='test_alias_event_1_1'),
            is_publish=True
        )
        Comment.objects.create(
            comment='test_comment_1',
            user=User.objects.get(username='Beta4'),
            event=Event.objects.get(alias='test_alias_event_1'),
            is_publish=True
        )

    def setUp(self):
        self.user = User.objects.create_user(
            username="test8",
            email="test8@example.com",
            password="Test123Qaz"
        )

        self.staff = User.objects.create_user(
            username="test9",
            email="test9@example.com",
            password="Test123Qaz",
            is_staff=True,
            is_superuser=True
        )

    def test_view_url_events_index_exists_at_desired_location(self):
        resp = self.client.get('/events')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['events']), 5)
        self.assertEqual(len(resp.context['paginationList']), 2)
        self.assertTemplateUsed(resp, 'events/event.html')

    def test_view_url_events_index_accessible_by_name(self):
        resp = self.client.get(reverse('events:index_event'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['events']), 5)
        self.assertEqual(len(resp.context['paginationList']), 2)
        self.assertTemplateUsed(resp, 'events/event.html')

    def test_view_url_events_index_page_exists_at_desired_location(self):
        resp = self.client.get('/events?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['events']), 2)
        self.assertEqual(len(resp.context['paginationList']), 2)
        self.assertTemplateUsed(resp, 'events/event.html')

    def test_view_url_events_show_exists_at_desired_location(self):
        resp = self.client.get('/events/test_alias_event_1_1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'events/event-note.html')

    def test_view_url_events_show_404_exists_at_desired_location(self):
        resp = self.client.get('/events/test_event_25_1/')
        self.assertEqual(resp.status_code, 404)

    def test_view_url_events_change_not_auth_exists_at_desired_location(self):
        resp = self.client.get('/edit_event/test_alias_event_1_1')
        self.assertEqual(resp.status_code, 403)

    def test_view_url_events_change_auth_user_exists_at_desired_location(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        resp = self.client.get('/edit_event/test_alias_event_1_1')
        self.assertEqual(resp.status_code, 404)

    def test_view_url_events_change_auth_staff_exists_at_desired_location(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        resp = self.client.get('/edit_event/test_alias_event_1_1')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_events_change_auth_staff_404_exists_at_desired_location(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        resp = self.client.get('/edit_event/test_alias_event_25_1')
        self.assertEqual(resp.status_code, 404)

    def test_view_url_events_delete_not_auth_exists_at_desired_location(self):
        resp = self.client.get('/delete_event/test_alias_event_5_1')
        self.assertEqual(resp.status_code, 403)

    def test_view_url_events_delete_auth_user_exists_at_desired_location(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        resp = self.client.get('/delete_event/test_alias_event_5_1')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/account/')

    def test_view_url_events_delete_auth_staff_exists_at_desired_location(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        resp = self.client.get('/delete_event/test_alias_event_5_1')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/account/')

    def test_view_url_events_delete_auth_staff_404_exists_at_desired_location(self):
        login = self.client.login(username='test9', password='Test123Qaz')
        resp = self.client.get('/delete_event/test_alias_event_25_1')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/account/')

    def test_view_url_events_add_comment_auth_accessible_by_name(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        resp = self.client.post(reverse('events:add_comment'), {'alias': 'test_alias_event_3_1', 'comment': 'test_comment', 'parent-id':'0'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Comment.objects.get(user=self.user, event=Event.objects.get(alias='test_alias_event_3_1')).user.id, self.user.id)
        self.assertEqual(resp.url, "/events/test_alias_event_3_1/")

    def test_view_url_events_add_comment_not_auth_accessible_by_name(self):
        resp = self.client.post(reverse('events:add_comment'), {'alias': 'test_alias_event_3_1', 'comment': 'test_comment', 'parent-id':'0'})
        self.assertEqual(resp.status_code, 403)

    def test_view_url_events_add_comment_auth_not_valid_alias_accessible_by_name(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        resp = self.client.post(reverse('events:add_comment'), {'alias': 'test_alias_event_30_1', 'comment': 'test_comment', 'parent-id':'0'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/")

    def test_view_url_events_add_comment_auth_not_valid_comment_accessible_by_name(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        count = Comment.objects.count()
        resp = self.client.post(reverse('events:add_comment'), {'alias': 'test_alias_event_4_1', 'parent-id':'0'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(count, Comment.objects.count())
        self.assertEqual(resp.url, "/events/test_alias_event_4_1/")

    def test_view_url_events_add_comment_auth_not_valid_parent_accessible_by_name(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        count = Comment.objects.count()
        resp = self.client.post(reverse('events:add_comment'), {'alias': 'test_alias_event_4_1', 'comment': 'test', 'parent-id':'10'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(count, Comment.objects.count())
        self.assertEqual(resp.url, "/")

    def test_view_url_events_edit_comment_auth_not_valid_auth_accessible_by_name(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'), event=Event.objects.get(alias='test_alias_event_1_1'))
        resp = self.client.post(reverse('events:edit_comment', kwargs={'id': comment.id}), {'comment': 'test_comment', 'alias':'test_alias_event_1_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/")

    def test_view_url_events_edit_comment_auth_not_valid_id_accessible_by_name(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        resp = self.client.post(reverse('events:edit_comment', kwargs={'id': 30}), {'comment': 'test_comment', 'alias':'test_alias_event_1_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/")

    def test_view_url_events_edit_comment_not_auth_accessible_by_name(self):
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'),
                                      event=Event.objects.get(alias='test_alias_event_1_1'))
        resp = self.client.post(reverse('events:edit_comment', kwargs={'id': comment.id}), {'comment': 'test_comment', 'alias':'test_alias_event_1_1'})
        self.assertEqual(resp.status_code, 403)

    def test_view_url_events_edit_comment_auth_not_valid_data_accessible_by_name(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'), event=Event.objects.get(alias='test_alias_event_1_1'))
        resp = self.client.post(reverse('events:edit_comment', kwargs={'id': comment.id}), {'alias':'test_alias_event_1_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/")

    def test_view_url_events_edit_comment_auth_not_valid_alias_accessible_by_name(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'), event=Event.objects.get(alias='test_alias_event_1_1'))
        resp = self.client.post(reverse('events:edit_comment', kwargs={'id': comment.id}), {'comment': 'test', 'alias':'test_alias_event_15_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/")

    def test_view_url_events_edit_comment_auth_valid_accessible_by_name(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'), event=Event.objects.get(alias='test_alias_event_1_1'))
        resp = self.client.post(reverse('events:edit_comment', kwargs={'id': comment.id}), {'comment': 'test_comment', 'alias':'test_alias_event_1_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/events/test_alias_event_1_1/")

    def test_view_url_events_delete_comment_auth_not_valid_auth_accessible_by_name(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'), event=Event.objects.get(alias='test_alias_event_1_1'))
        resp = self.client.post(reverse('events:delete_comment', kwargs={'id': comment.id}), {'comment': 'test_comment', 'alias':'test_event_1_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/")

    def test_view_url_events_edit_delete_auth_not_valid_id_accessible_by_name(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        resp = self.client.post(reverse('events:delete_comment', kwargs={'id': 30}), {'comment': 'test_comment', 'alias':'test_alias_event_1_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/")

    def test_view_url_events_delete_comment_not_auth_accessible_by_name(self):
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'),
                                      event=Event.objects.get(alias='test_alias_event_1_1'))
        resp = self.client.post(reverse('events:delete_comment', kwargs={'id': comment.id}), {'alias':'test_alias_event_1_1'})
        self.assertEqual(resp.status_code, 403)

    def test_view_url_events_delete_comment_auth_not_valid_data_accessible_by_name(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'), event=Event.objects.get(alias='test_alias_event_1_1'))
        resp = self.client.post(reverse('events:delete_comment', kwargs={'id': comment.id}), { })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/")

    def test_view_url_events_delete_comment_auth_valid_accessible_by_name(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'), event=Event.objects.get(alias='test_alias_event_1_1'))
        resp = self.client.post(reverse('events:delete_comment', kwargs={'id': comment.id}), {'alias':'test_alias_event_1_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/events/test_alias_event_1_1/")

    '''
        Article
    '''

    def test_view_url_article_index_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['events']), 5)
        self.assertEqual(len(resp.context['paginationList']), 2)
        self.assertTemplateUsed(resp, 'events/index.html')

    def test_view_url_article_index_accessible_by_name(self):
        resp = self.client.get(reverse('events:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['events']), 5)
        self.assertEqual(len(resp.context['paginationList']), 2)
        self.assertTemplateUsed(resp, 'events/index.html')

    def test_view_url_article_index_page_exists_at_desired_location(self):
        resp = self.client.get('/?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['events']), 2)
        self.assertEqual(len(resp.context['paginationList']), 2)
        self.assertTemplateUsed(resp, 'events/index.html')

    def test_view_url_article_show_exists_at_desired_location(self):
        resp = self.client.get('/test_alias_event_1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'events/article.html')

    def test_view_url_article_show_404_exists_at_desired_location(self):
        resp = self.client.get('/test_event_25_1/')
        self.assertEqual(resp.status_code, 404)

    def test_view_url_article_change_not_auth_exists_at_desired_location(self):
        resp = self.client.get('/edit_event/test_alias_event_1')
        self.assertEqual(resp.status_code, 403)

    def test_view_url_article_change_auth_user_exists_at_desired_location(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        resp = self.client.get('/edit_event/test_alias_event_1')
        self.assertEqual(resp.status_code, 404)

    def test_view_url_article_change_auth_staff_exists_at_desired_location(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        resp = self.client.get('/edit_event/test_alias_event_1')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_article_change_auth_staff_404_exists_at_desired_location(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        resp = self.client.get('/edit_event/test_alias_event_25')
        self.assertEqual(resp.status_code, 404)

    def test_view_url_article_delete_not_auth_exists_at_desired_location(self):
        resp = self.client.get('/delete_event/test_alias_event_5')
        self.assertEqual(resp.status_code, 403)

    def test_view_url_article_delete_auth_user_exists_at_desired_location(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        resp = self.client.get('/delete_event/test_alias_event_5')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/account/')

    def test_view_url_article_delete_auth_staff_exists_at_desired_location(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        resp = self.client.get('/delete_event/test_alias_event_5')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/account/')

    def test_view_url_article_delete_auth_staff_404_exists_at_desired_location(self):
        login = self.client.login(username='test9', password='Test123Qaz')
        resp = self.client.get('/delete_event/test_alias_event_25')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/account/')

    def test_view_url_article_add_comment_auth_accessible_by_name(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        resp = self.client.post(reverse('events:add_comment'), {'alias': 'test_alias_event_3', 'comment': 'test_comment', 'parent-id':'0'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Comment.objects.get(user=self.user, event=Event.objects.get(alias='test_alias_event_3')).user.id, self.user.id)
        self.assertEqual(resp.url, "/test_alias_event_3/")

    def test_view_url_article_add_comment_not_auth_accessible_by_name(self):
        resp = self.client.post(reverse('events:add_comment'), {'alias': 'test_alias_event_3', 'comment': 'test_comment', 'parent-id':'0'})
        self.assertEqual(resp.status_code, 403)

    def test_view_url_article_add_comment_auth_not_valid_alias_accessible_by_name(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        resp = self.client.post(reverse('events:add_comment'), {'alias': 'test_alias_event_30', 'comment': 'test_comment', 'parent-id':'0'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/")

    def test_view_url_article_add_comment_auth_not_valid_comment_accessible_by_name(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        count = Comment.objects.count()
        resp = self.client.post(reverse('events:add_comment'), {'alias': 'test_alias_event_4', 'parent-id':'0'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(count, Comment.objects.count())
        self.assertEqual(resp.url, "/test_alias_event_4/")

    def test_view_url_article_add_comment_auth_not_valid_parent_accessible_by_name(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        count = Comment.objects.count()
        resp = self.client.post(reverse('events:add_comment'), {'alias': 'test_alias_event_4', 'comment': 'test', 'parent-id':'10'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(count, Comment.objects.count())
        self.assertEqual(resp.url, "/")

    def test_view_url_article_edit_comment_auth_not_valid_auth_accessible_by_name(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'), event=Event.objects.get(alias='test_alias_event_1'))
        resp = self.client.post(reverse('events:edit_comment', kwargs={'id': comment.id}), {'comment': 'test_comment', 'alias':'test_alias_event_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/")

    def test_view_url_article_edit_comment_auth_not_valid_id_accessible_by_name(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        resp = self.client.post(reverse('events:edit_comment', kwargs={'id': 30}), {'comment': 'test_comment', 'alias':'test_alias_event_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/")

    def test_view_url_article_edit_comment_not_auth_accessible_by_name(self):
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'),
                                      event=Event.objects.get(alias='test_alias_event_1'))
        resp = self.client.post(reverse('events:edit_comment', kwargs={'id': comment.id}), {'comment': 'test_comment', 'alias':'test_alias_event_1'})
        self.assertEqual(resp.status_code, 403)

    def test_view_url_article_edit_comment_auth_not_valid_data_accessible_by_name(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'), event=Event.objects.get(alias='test_alias_event_1'))
        resp = self.client.post(reverse('events:edit_comment', kwargs={'id': comment.id}), {'alias':'test_alias_event_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/")

    def test_view_url_article_edit_comment_auth_not_valid_alias_accessible_by_name(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'), event=Event.objects.get(alias='test_alias_event_1'))
        resp = self.client.post(reverse('events:edit_comment', kwargs={'id': comment.id}), {'comment': 'test', 'alias':'test_alias_event_15'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/")

    def test_view_url_article_edit_comment_auth_valid_accessible_by_name(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'), event=Event.objects.get(alias='test_alias_event_1'))
        resp = self.client.post(reverse('events:edit_comment', kwargs={'id': comment.id}), {'comment': 'test_comment', 'alias':'test_alias_event_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/test_alias_event_1/")

    def test_view_url_article_delete_comment_auth_not_valid_auth_accessible_by_name(self):
        login = self.client.login(username='test8', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'), event=Event.objects.get(alias='test_alias_event_1'))
        resp = self.client.post(reverse('events:delete_comment', kwargs={'id': comment.id}), {'comment': 'test_comment', 'alias':'test_event_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/")

    def test_view_url_article_edit_delete_auth_not_valid_id_accessible_by_name(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        resp = self.client.post(reverse('events:delete_comment', kwargs={'id': 30}), {'comment': 'test_comment', 'alias':'test_alias_event_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/")

    def test_view_url_article_delete_comment_not_auth_accessible_by_name(self):
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'),
                                      event=Event.objects.get(alias='test_alias_event_1'))
        resp = self.client.post(reverse('events:delete_comment', kwargs={'id': comment.id}), {'alias':'test_alias_event_1'})
        self.assertEqual(resp.status_code, 403)

    def test_view_url_article_delete_comment_auth_not_valid_data_accessible_by_name(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'), event=Event.objects.get(alias='test_alias_event_1'))
        resp = self.client.post(reverse('events:delete_comment', kwargs={'id': comment.id}), { })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/")

    def test_view_url_article_delete_comment_auth_valid_accessible_by_name(self):
        login = self.client.login(username='Beta4', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta4'), event=Event.objects.get(alias='test_alias_event_1'))
        resp = self.client.post(reverse('events:delete_comment', kwargs={'id': comment.id}), {'alias':'test_alias_event_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/test_alias_event_1/")