from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
import time

from news.models import News, Comment
from account.models import User
from histories.models import History



class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    def setUp(self):
        User.objects.create_user(
            email="beta30@example.com",
            username="Beta30",
            password="Test123Qaz",
            first_name="test",
            last_name="ing",
            phone='375291324567'
        )
        for i in range(7):
            News.objects.create(
                title=f'test_news_{i}s',
                alias=f'test_news_{i}s',
                user=User.objects.get(username='Beta30'),
                article=f'test{i}',
                meta_title=f'test{i}',
                meta_keywords=f'test{i}',
                meta_description=f'test{i}',
                is_show=True
            )
        Comment.objects.create(
            comment='test_comment_1',
            user=User.objects.get(username='Beta30'),
            news=News.objects.get(alias='test_news_1s')
        )
        for i in range(7):
            History.objects.create(
                title=f'test_history_{i}s',
                alias=f'test_history_{i}s',
                user=User.objects.get(username='Beta30'),
                article=f'test{i}',
                meta_title=f'test{i}',
                meta_keywords=f'test{i}',
                meta_description=f'test{i}',
                is_show=True
            )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_news(self):
        self.selenium.get(f"{self.live_server_url}/news/")
        time.sleep(3)
        self.selenium.find_element(By.XPATH, '//a[text()="Подробнее"]').click()

    def test_history(self):
        self.selenium.get(f"{self.live_server_url}/history/")
        time.sleep(3)
        self.selenium.find_element(By.XPATH, '//a[text()="Подробнее"]').click()