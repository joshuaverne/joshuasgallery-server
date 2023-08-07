from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class LoginTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def testLogin(self):
        successful_login_msg = 'Homepage'

        self.selenium.get('http://localhost:8000/login')

        username_field = self.selenium.find_element(By.ID, 'id_username')
        password_field = self.selenium.find_element(By.ID, 'id_password')

        submit_btn = self.selenium.find_element(By.XPATH, "//button[@type='submit']")

        username_field.send_keys('testuser')
        password_field.send_keys('mypw1234')

        submit_btn.send_keys(Keys.RETURN)

        assert successful_login_msg in self.selenium.page_source

    def testFailedLogin(self):
        failed_login_msg = 'Invalid username or password.'

        self.selenium.get('http://localhost:8000/login')

        username_field = self.selenium.find_element(By.ID, 'id_username')
        password_field = self.selenium.find_element(By.ID, 'id_password')

        submit_btn = self.selenium.find_element(By.XPATH, "//button[@type='submit']")

        username_field.send_keys('nonexistantuser')
        password_field.send_keys('notarealpassword')

        submit_btn.send_keys(Keys.RETURN)

        assert failed_login_msg in self.selenium.page_source


class NavTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def login(self):
        self.selenium.get('http://localhost:8000/login')

        username_field = self.selenium.find_element(By.ID, 'id_username')
        password_field = self.selenium.find_element(By.ID, 'id_password')

        submit_btn = self.selenium.find_element(By.XPATH, "//button[@type='submit']")

        username_field.send_keys('testuser')
        password_field.send_keys('mypw1234')

        submit_btn.send_keys(Keys.RETURN)

    def testGalleryDash(self):
        gallery_text = "Dashboard"

        self.login()
        nav_btn = self.selenium.find_element(By.ID, "navbar_toggle_button")

        if nav_btn.is_displayed():
            nav_btn.click()

        self.selenium.find_element(By.ID, "nav_link_my_gallery").click()

        assert gallery_text in self.selenium.page_source


