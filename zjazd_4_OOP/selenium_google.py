from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

time.sleep(1)

driver.get("https://pl.wikipedia.org/wiki/Wikipedia:Strona_g%C5%82%C3%B3wna")

print('Nazwa strony', driver.title)

time.sleep(10)

button1_accept = driver.find_element('id', 'L2AGLb')

print(button1_accept)

button1_accept.click()



time.sleep(10)

search_field = driver.find_element('name', 'q')

search_field.send_keys('Wrocław wypadek rosomak')

time.sleep(10)

search_button = driver.find_element('name', 'btnK')

search_field.send_keys(Keys.ENTER)

time.sleep(10)