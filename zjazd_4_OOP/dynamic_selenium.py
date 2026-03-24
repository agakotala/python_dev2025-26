from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")

start_button = driver.find_element(By.CSS_SELECTOR, "#start button")
start_button.click()

wait = WebDriverWait(driver, 10)
finish_element = wait.until(EC.visibility_of_element_located((By.ID, "finish")))

assert finish_element.find_element(By.TAG_NAME, "h4").text == "Hello World!"

print("Test zakończony pomyślnie")

driver.quit()