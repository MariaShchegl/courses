from django.test import TestCase
from news.models import News, Comment
from account.models import User

# Create your tests here.
class HistoryModelTest(TestCase):
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
        News.objects.create(
            title='test_news',
            alias='test_news',
            user=User.objects.get(username='Beta2'),
            article='test',
            meta_title='test',
            meta_keywords='test',
            meta_description='test'
        )
        Comment.objects.create(
            comment='test_comment',
            user=User.objects.get(username='Beta2'),
            news=News.objects.get(alias="test_news")
        )

    def test_news_max_length(self):
        news = News.objects.get(alias='test_news')
        max_length_meta_title = news._meta.get_field('meta_title').max_length
        max_length_meta_keywords = news._meta.get_field('meta_keywords').max_length
        max_length_title = news._meta.get_field('title').max_length
        max_length_alias = news._meta.get_field('alias').max_length
        self.assertEquals(max_length_alias, 255)
        self.assertEquals(max_length_title, 255)
        self.assertEquals(max_length_meta_keywords, 255)
        self.assertEquals(max_length_meta_title, 255)

    def test_comment_max_length(self):
        comment = Comment.objects.get(comment="test_comment")
        test_str = comment.news.title + '|' + comment.user.username
        self.assertEquals(str(comment), test_str)