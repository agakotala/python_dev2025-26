from selenium import webdriver
from POM import LoginPage
# from selenium2 import make_screenshot
# import pytest
import pytest_html
import time

def test_login_page():
    driver = webdriver.Firefox()
    page = LoginPage(driver)
    page.open()
    time.sleep(1)
    try:
        assert driver.current_url == 'https://www.saucedemo1.com/'
    except AssertionError:
        print('Logowanie nie powiodło się')
        raise
    else:
        print('Logowanie powiodło się')
    finally:
        print('koniec')
        page.close()
