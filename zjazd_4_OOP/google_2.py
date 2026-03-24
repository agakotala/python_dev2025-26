from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome()

try:
    driver.get("https://www.google.com/")
    print('Nazwa strony:', driver.title)
    button1_accept = driver.find_element('id', 'L2AGLb')
    print(button1_accept)
    button1_accept.click()

    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys("Selenium Python Tutorial")
    search_box.send_keys(Keys.RETURN)

    time.sleep(3)
    print(f"Tytuł storny: {driver.title}")
    driver.save_screenshot("wyniki_wyszukiwania.png")

finally:
    driver.quit()
