from selenium import webdriver
from POM import LoginPage
# from selenium2 import make_screenshot
import pytest
import pytest_html
import time
import sys

test_data = [
    ('standard_user', 'secret_sauce', 'https://www.saucedemo.com/inventory.html'),
    ('locked_out_user', 'secret_sauce', 'https://www.saucedemo.com/'),
    ('problem_user', 'secret_sauce', 'https://www.saucedemo.com/inventory.html'),
    ('performance_glitch_user', 'secret_sauce', 'https://www.saucedemo.com/inventory.html')
]

@pytest.mark.parametrize('username, password, url', test_data)
def test_login_page(username, password, url):
    driver = webdriver.Chrome()
    page = LoginPage(driver)
    page.open()
    time.sleep(1)
    assert driver.current_url == 'https://www.saucedemo.com/'
    page.enter_username(username)
    page.enter_password(password)
    time.sleep(1)
    page.click_login()
    time.sleep(1)
    try:
        assert driver.current_url == url
    except AssertionError:
        print('Logowanie nie powiodlo sie')
        raise
    else:
        print('Logowanie poprawne')
    finally:
        print('koniec')
        page.close()

@pytest.mark.skip(reason='Jeszcze nie gotowe')
def test_one():
    assert 1 == 2


@pytest.mark.skipif(sys.platform == "win32", reason='test for Linux only')
def test_two():
    assert 1 == 2

@pytest.mark.skipif(sys.version_info < (3, 10), reason='bo tak')
def test_three():
    assert 1 == 2
