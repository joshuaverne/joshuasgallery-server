from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class LoginTest(LiveServerTestCase):

    def testLogin(self):
        successful_login_msg = 'You\'re at the homepage!'

        selenium = webdriver.Chrome()

        selenium.get('http://localhost:8000/login')

        username_field = selenium.find_element(By.ID, 'id_username')
        password_field = selenium.find_element(By.ID, 'id_password')

        submit_btn = selenium.find_element(By.XPATH, "//button[@type='submit']")

        username_field.send_keys('testuser')
        password_field.send_keys('mypw1234')

        submit_btn.send_keys(Keys.RETURN)

        assert successful_login_msg in selenium.page_source

    def testFailedLogin(self):
        failed_login_msg = 'Invalid username or password.'

        selenium = webdriver.Chrome()

        selenium.get('http://localhost:8000/login')

        username_field = selenium.find_element(By.ID, 'id_username')
        password_field = selenium.find_element(By.ID, 'id_password')

        submit_btn = selenium.find_element(By.XPATH, "//button[@type='submit']")

        username_field.send_keys('nonexistantuser')
        password_field.send_keys('notarealpassword')

        submit_btn.send_keys(Keys.RETURN)

        assert failed_login_msg in selenium.page_source
