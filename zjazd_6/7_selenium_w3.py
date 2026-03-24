from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.w3schools.com/")
time.sleep(3)
menu = driver.find_element('id', 'navbtn_tutorials')
# menu.click()
HTMLtutorial = driver.find_element(By.XPATH,'html/body/div[2]/div[2]/div/nav[1]/div[1]/div/div[2]/div[1]/div[1]/a[2]')
# HTMLtutorial.click()

webdriver.ActionChains(driver).move_to_element(menu).click().move_to_element(HTMLtutorial).click().perform()
HTML_forms_attributes = driver.find_element(By.XPATH, '//*[@id="leftmenuinnerinner"]/a[42]')
HTML_forms_attributes.click()
time.sleep(1)
tryityourself = driver.find_element(By.XPATH, '//*[@id="main"]/div[3]/a')
tryityourself.click()
time.sleep(3)

currentWindowName = driver.current_window_handle
windowNames = driver.window_handles
print(currentWindowName)
print(windowNames)

for window in windowNames:
    if window != currentWindowName:
        driver.switch_to.window(window)

driver.switch_to.frame(driver.find_element(By.ID,'iframeResult'))
firstName = driver.find_element(By.ID, 'fname')

time.sleep(2)
if firstName.is_enabled():
    firstName.clear()
    firstName.send_keys('Kamil')
else:
    print('Nie da się wpisać')

time.sleep(2)

driver.quit()