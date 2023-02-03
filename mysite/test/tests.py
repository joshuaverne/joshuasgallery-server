from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class LoginTest(LiveServerTestCase):

    def testLogin(self):
        failed_login_msg = 'Please enter the correct username and password for a staff account.'

        selenium = webdriver.Chrome()

        selenium.get('http://localhost:8000/admin')

        username_field = selenium.find_element(By.ID, 'id_username')
        password_field = selenium.find_element(By.ID, 'id_password')

        submit_btn = selenium.find_element(By.XPATH, "//input[@type='submit']")

        username_field.send_keys('notRealUsername')
        password_field.send_keys('notRealPassword')

        submit_btn.send_keys(Keys.RETURN)

        assert failed_login_msg in selenium.page_source
