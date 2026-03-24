from builtins import Exception

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

try:
    driver.get("https://the-internet.herokuapp.com/login")
    print(f"Tytuł strony: {driver.title}")
    print(f"URL: {driver.current_url}")

    wait = WebDriverWait(driver, 10)

    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    username_field.send_keys("tomsmith") #testowy login
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("SuperSecretPassword")

    login_button = driver.find_element(By.CLASS_NAME, "radius")

    login_button.click()

    time.sleep(2)

    success_message = driver.find_element(By.ID, "flash")

    print(f"Koumnikat: {success_message.text}")

    if "You logged into a secure area!" in success_message.text:
        print("Logowanie udane!")
    else:
        print("Logowanie nieudane!")

    driver.save_screenshot("logowanie.png")

except Exception as e:
    print(f"Wystąpił błąd: {e}")

    driver.save_screenshot("logowanie_error.png")

finally:
    time.sleep(5)
    driver.quit()