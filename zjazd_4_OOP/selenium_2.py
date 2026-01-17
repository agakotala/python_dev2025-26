# scripts/01_checkboxes.py
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://the-internet.herokuapp.com/checkboxes"

driver = webdriver.Chrome()
driver.get(URL)

checkboxes = driver.find_elements(By.CSS_SELECTOR, "#checkboxes input")
cb1, cb2 = checkboxes

# checkbox 1 ma być zaznaczony
if not cb1.is_selected():
    cb1.click()

# checkbox 2 ma być odznaczony
if cb2.is_selected():
    cb2.click()

# asercje
assert cb1.is_selected()
assert not cb2.is_selected()

driver.quit()
print("OK")
