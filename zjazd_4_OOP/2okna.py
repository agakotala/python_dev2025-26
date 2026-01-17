from selenium import webdriver
import time

driver = webdriver.Chrome()

try:
    driver.get("https://example.com")

    driver.execute_script("window.open('https://python.org', '_blank');")

    print(f"Liczba otwartych kart: {len(driver.window_handles)}")

    driver.switch_to.window(driver.window_handles[1])

    print(f"Adres drugiej karty: {driver.current_url}")

    time.sleep(5)

finally:
    driver.quit()