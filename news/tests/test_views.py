from django.test import TestCase

# Create your tests here.
from account.models import User
from django.urls import reverse
from news.models import News, Comment

class NewsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            email="beta3@example.com",
            username="Beta3",
            password="Test123Qaz",
            first_name="test",
            last_name="ing",
            phone='375291324567'
        )
        for i in range(7):
            News.objects.create(
                title=f'test_news_{i}',
                alias=f'test_news_{i}',
                user=User.objects.get(username='Beta3'),
                article=f'test{i}',
                meta_title=f'test{i}',
                meta_keywords=f'test{i}',
                meta_description=f'test{i}',
                is_show=True
            )
        Comment.objects.create(
            comment='test_comment_1',
            user=User.objects.get(username='Beta3'),
            news=News.objects.get(alias='test_news_1')
        )

    def setUp(self):
        self.user = User.objects.create_user(
            username="test6",
            email="test6@example.com",
            password="Test123Qaz"
        )

        self.staff = User.objects.create_user(
            username="test7",
            email="test7@example.com",
            password="Test123Qaz",
            is_staff=True,
            is_superuser=True
        )

    def test_view_url_news_index_exists_at_desired_location(self):
        resp = self.client.get('/news/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['news']), 5)
        self.assertEqual(len(resp.context['paginationList']), 2)
        self.assertTemplateUsed(resp, 'news/news.html')

    def test_view_url_news_index_accessible_by_name(self):
        resp = self.client.get(reverse('news:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['news']), 5)
        self.assertEqual(len(resp.context['paginationList']), 2)
        self.assertTemplateUsed(resp, 'news/news.html')

    def test_view_url_news_index_page_exists_at_desired_location(self):
        resp = self.client.get('/news/?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['news']), 2)
        self.assertEqual(len(resp.context['paginationList']), 2)
        self.assertTemplateUsed(resp, 'news/news.html')

    def test_view_url_news_show_exists_at_desired_location(self):
        resp = self.client.get('/news/test_news_1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'news/note.html')

    def test_view_url_news_show_404_exists_at_desired_location(self):
        resp = self.client.get('/news/test_news_25/')
        self.assertEqual(resp.status_code, 404)

    def test_view_url_news_change_not_auth_exists_at_desired_location(self):
        news = News.objects.get(alias='test_news_1')
        resp = self.client.get(f'/admin/news/news/{news.id}/change/')
        self.assertEqual(resp.status_code, 302)

    def test_view_url_news_change_auth_user_exists_at_desired_location(self):
        login = self.client.login(username='test6', password='Test123Qaz')
        news = News.objects.get(alias='test_news_1')
        resp = self.client.get(f'/admin/news/news/{news.id}/change/')
        self.assertEqual(resp.status_code, 302)

    def test_view_url_news_change_auth_staff_exists_at_desired_location(self):
        login = self.client.login(username='test7', password='Test123Qaz')
        news = News.objects.get(alias='test_news_1')
        resp = self.client.get(f'/admin/news/news/{news.id}/change/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_news_change_auth_staff_404_exists_at_desired_location(self):
        login = self.client.login(username='test6', password='Test123Qaz')
        news = News.objects.get(alias='test_news_1')
        resp = self.client.get(f'/admin/news/news/25/change/')
        self.assertEqual(resp.status_code, 302)

    def test_view_url_news_delete_not_auth_exists_at_desired_location(self):
        news = News.objects.get(alias='test_news_5')
        resp = self.client.get(f'/admin/news/news/{news.id}/delete/')
        self.assertEqual(resp.status_code, 302)

    def test_view_url_news_delete_auth_user_exists_at_desired_location(self):
        login = self.client.login(username='test6', password='Test123Qaz')
        news = News.objects.get(alias='test_news_5')
        resp = self.client.get(f'/admin/news/news/{news.id}/delete/')
        self.assertEqual(resp.status_code, 302)

    def test_view_url_news_delete_auth_staff_exists_at_desired_location(self):
        login = self.client.login(username='test7', password='Test123Qaz')
        news = News.objects.get(alias='test_news_5')
        resp = self.client.get(f'/admin/news/news/{news.id}/delete/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_news_delete_auth_staff_404_exists_at_desired_location(self):
        login = self.client.login(username='test7', password='Test123Qaz')
        resp = self.client.get(f'/admin/news/news/25/delete/')
        self.assertEqual(resp.status_code, 302)

    def test_view_url_news_add_comment_auth_accessible_by_name(self):
        login = self.client.login(username='test6', password='Test123Qaz')
        resp = self.client.post(reverse('news:add_comment'), {'alias': 'test_news_3', 'comment': 'test_comment', 'parent-id':'0'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Comment.objects.get(user=self.user, news=News.objects.get(alias='test_news_3')).user.id, self.user.id)
        self.assertEqual(resp.url, "/news/test_news_3/")

    def test_view_url_news_add_comment_not_auth_accessible_by_name(self):
        resp = self.client.post(reverse('news:add_comment'), {'alias': 'test_news_3', 'comment': 'test_comment', 'parent-id':'0'})
        self.assertEqual(resp.status_code, 403)

    def test_view_url_news_add_comment_auth_not_valid_alias_accessible_by_name(self):
        login = self.client.login(username='test6', password='Test123Qaz')
        resp = self.client.post(reverse('news:add_comment'), {'alias': 'test_news_30', 'comment': 'test_comment', 'parent-id':'0'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/news/")

    def test_view_url_news_add_comment_auth_not_valid_comment_accessible_by_name(self):
        login = self.client.login(username='test6', password='Test123Qaz')
        count = Comment.objects.count()
        resp = self.client.post(reverse('news:add_comment'), {'alias': 'test_news_4', 'parent-id':'0'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(count, Comment.objects.count())
        self.assertEqual(resp.url, "/news/test_news_4/")

    def test_view_url_news_add_comment_auth_not_valid_parent_accessible_by_name(self):
        login = self.client.login(username='test6', password='Test123Qaz')
        count = Comment.objects.count()
        resp = self.client.post(reverse('news:add_comment'), {'alias': 'test_news_4', 'comment': 'test', 'parent-id':'10'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(count, Comment.objects.count())
        self.assertEqual(resp.url, "/news/")

    def test_view_url_news_edit_comment_auth_not_valid_auth_accessible_by_name(self):
        login = self.client.login(username='test6', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta3'), news=News.objects.get(alias='test_news_1'))
        resp = self.client.post(reverse('news:edit_comment', kwargs={'id': comment.id}), {'comment': 'test_comment', 'alias':'test_news_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/news/")

    def test_view_url_news_edit_comment_auth_not_valid_id_accessible_by_name(self):
        login = self.client.login(username='Beta3', password='Test123Qaz')
        resp = self.client.post(reverse('news:edit_comment', kwargs={'id': 30}), {'comment': 'test_comment', 'alias':'test_news_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/news/")

    def test_view_url_news_edit_comment_not_auth_accessible_by_name(self):
        comment = Comment.objects.get(user=User.objects.get(username='Beta3'),
                                      news=News.objects.get(alias='test_news_1'))
        resp = self.client.post(reverse('news:edit_comment', kwargs={'id': comment.id}), {'comment': 'test_comment', 'alias':'test_news_1'})
        self.assertEqual(resp.status_code, 403)

    def test_view_url_news_edit_comment_auth_not_valid_data_accessible_by_name(self):
        login = self.client.login(username='Beta3', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta3'), news=News.objects.get(alias='test_news_1'))
        resp = self.client.post(reverse('news:edit_comment', kwargs={'id': comment.id}), {'alias':'test_news_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/news/")

    def test_view_url_news_edit_comment_auth_not_valid_alias_accessible_by_name(self):
        login = self.client.login(username='Beta3', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta3'), news=News.objects.get(alias='test_news_1'))
        resp = self.client.post(reverse('news:edit_comment', kwargs={'id': comment.id}), {'comment': 'test', 'alias':'test_news_15'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/news/")

    def test_view_url_news_edit_comment_auth_valid_accessible_by_name(self):
        login = self.client.login(username='Beta3', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta3'), news=News.objects.get(alias='test_news_1'))
        resp = self.client.post(reverse('news:edit_comment', kwargs={'id': comment.id}), {'comment': 'test_comment', 'alias':'test_news_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/news/test_news_1/")

    def test_view_url_news_delete_comment_auth_not_valid_auth_accessible_by_name(self):
        login = self.client.login(username='test6', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta3'), news=News.objects.get(alias='test_news_1'))
        resp = self.client.post(reverse('news:delete_comment', kwargs={'id': comment.id}), {'comment': 'test_comment', 'alias':'test_news_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/news/")

    def test_view_url_news_edit_delete_auth_not_valid_id_accessible_by_name(self):
        login = self.client.login(username='Beta3', password='Test123Qaz')
        resp = self.client.post(reverse('news:delete_comment', kwargs={'id': 30}), {'comment': 'test_comment', 'alias':'test_news_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/news/")

    def test_view_url_news_delete_comment_not_auth_accessible_by_name(self):
        comment = Comment.objects.get(user=User.objects.get(username='Beta3'),
                                      news=News.objects.get(alias='test_news_1'))
        resp = self.client.post(reverse('news:delete_comment', kwargs={'id': comment.id}), {'alias':'test_news_1'})
        self.assertEqual(resp.status_code, 403)

    def test_view_url_news_delete_comment_auth_not_valid_data_accessible_by_name(self):
        login = self.client.login(username='Beta3', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta3'), news=News.objects.get(alias='test_news_1'))
        resp = self.client.post(reverse('news:delete_comment', kwargs={'id': comment.id}), { })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/news/")

    def test_view_url_news_delete_comment_auth_valid_accessible_by_name(self):
        login = self.client.login(username='Beta3', password='Test123Qaz')
        comment = Comment.objects.get(user=User.objects.get(username='Beta3'), news=News.objects.get(alias='test_news_1'))
        resp = self.client.post(reverse('news:delete_comment', kwargs={'id': comment.id}), {'alias':'test_news_1'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/news/test_news_1/")