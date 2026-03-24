from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json, os

COOKIES_FILE = "google_cookies.json"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

driver.get("https://www.google.com")

# --- 1) Wczytaj cookies, jeśli już je masz ---
if os.path.exists(COOKIES_FILE):
    with open(COOKIES_FILE, "r", encoding="utf-8") as f:
        cookies = json.load(f)

    for c in cookies:
        # czasem Selenium/Chrome nie lubi sameSite z get_cookies()
        c.pop("sameSite", None)

        # jeżeli cookie ma domenę, która nie pasuje idealnie, czasem pomaga ją usunąć:
        # c.pop("domain", None)

        try:
            driver.add_cookie(c)
        except Exception:
            pass

    driver.refresh()

# --- 2) Jeśli baner nadal jest, kliknij i zapisz cookies ---
try:
    accept_btn = wait.until(EC.element_to_be_clickable((By.ID, "L2AGLb")))
    accept_btn.click()

    with open(COOKIES_FILE, "w", encoding="utf-8") as f:
        json.dump(driver.get_cookies(), f, ensure_ascii=False, indent=2)

except Exception:
    # brak banera = OK
    pass

print("Nazwa strony:", driver.title)

# --- 3) Szukanie ---
search_field = wait.until(EC.presence_of_element_located((By.NAME, "q")))
search_field.clear()
search_field.send_keys("Wrocław wypadek rosomak")
search_field.send_keys(Keys.ENTER)
