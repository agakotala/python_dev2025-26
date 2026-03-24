#Page Object Model
from builtins import Exception

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_field_id = "user-name"
        self.password_field_id = "password"
        self.login_button_id = "login-button"
        self.error_box_css = '[data-test="error"]'
        self.login_url = "https://www.saucedemo.com/"
        self.after_login_url = "https://www.saucedemo.com/inventory.html"
        self.wait = WebDriverWait(self.driver, 10)

    def open(self):
        self.driver.get(self.login_url)

    def close(self):
        self.driver.quit()

    def wait_for_page_ready(self):  #storna jest załadowana i mozna z niej korzystac
        self.wait.until(EC.visibility_of_element_located((By.ID, self.username_field_id)))

    def enter_username(self, username):
        field = self.driver.find_element(By.ID, self.username_field_id)

        field.clear()
        field.send_keys(username)

    def enter_password(self, password):
        field = self.driver.find_element(By.ID, self.password_field_id)
        field.clear()
        field.send_keys(password)


    def click_login(self):
        button = self.driver.find_element(By.ID, self.login_button_id)
        button.click()

    def login(self, username, password):
        self.wait_for_page_ready()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def wait_until_logged_in(self):
        self.wait.until(EC.url_to_be(self.after_login_url))

    def wait_for_error_message(self):
        return self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.error_box_css)))

    def get_error_text(self):
        error_element = self.wait_for_error_message()

        return error_element.text

    def is_error_displayed(self):
        try:
            self.wait_for_error_message()
            return True
        except Exception:
            return False

    def wait_until_login_fails(self):
        self.wait_for_error_message()



