from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from account.models import User

class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.user = User.objects.create_user(
            email="testsel@example.com",
            username="testSel",
            is_active=True,
            password="Test123Qaz",
            first_name="test",
            last_name="ing",
            phone='375291324567'
        )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get(f"{self.live_server_url}/account/login/")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("testSel")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("Test123Qaz")
        time.sleep(3)
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        WebDriverWait(self.selenium, 3).until(EC.presence_of_element_located((By.XPATH, '//button[@title="Найти"]')))

    def test_register(self):
        self.selenium.get(f"{self.live_server_url}/account/register/")
        first_name_input = self.selenium.find_element(By.NAME, "first_name")
        first_name_input.send_keys("Ivan")
        last_name_input = self.selenium.find_element(By.NAME, "last_name")
        last_name_input.send_keys("Ivanovich")
        email_input = self.selenium.find_element(By.NAME, "email")
        email_input.send_keys("ivan@test.com")
        phone_input = self.selenium.find_element(By.NAME, "phone")
        phone_input.send_keys("+375291234567")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("ivanus")
        password1_input = self.selenium.find_element(By.NAME, "password1")
        password1_input.send_keys("Test123Qaz")
        password2_input = self.selenium.find_element(By.NAME, "password2")
        password2_input.send_keys("Test123Qaz")
        time.sleep(3)
        self.selenium.find_element(By.XPATH, '//input[@type="checkbox"]').click()
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        WebDriverWait(self.selenium, 3).until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]')))