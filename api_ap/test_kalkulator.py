import requests
import time

BASE_URL = "http://127.0.0.1:8010"

def test_endpoint(endpoint, expected_status=200):
    """Testuj endpoint i wypisz wyniki"""

    try:
        url = f"{BASE_URL}{endpoint}"
        print(f"Test: {url}")

        response = requests.get(url)
        print(f" Status: {response.status_code}")

        if response.status_code == expected_status:
            data = response.json()
            print(f"Wyniki: {data}")
            return True
        else:
            print(f"Błąd: {response.text}")
            return False

    except Exception as e:
        print(f"Wyjątek: {e}")
        return False

print("Kompletny test kalkulatora REST")
test_endpoint("/")

test_endpoint("/dodaj/10/5")
time.sleep(0.2)
test_endpoint("/odejmij/10/5")
time.sleep(0.2)
test_endpoint("/pomnoz/10/5")
time.sleep(0.2)
test_endpoint("/podziel/10/5")
time.sleep(0.2)
test_endpoint("/podziel/10/0", 400)
time.sleep(0.2)
test_endpoint("/potega/2/3")
time.sleep(0.2)
test_endpoint("/potega/10/12")
time.sleep(0.2)
test_endpoint("/pierwiastek/25/2")
time.sleep(0.2)
test_endpoint("/pierwiastek/-25/2", 400)
time.sleep(0.2)
test_endpoint("/oblicz/(10+5)*2")
time.sleep(0.2)
test_endpoint("/oblicz/3.14*2")
time.sleep(0.2)
test_endpoint("/historia")
time.sleep(0.2)

test_endpoint("/historia?limit=3")

print("Testy zakończone")
print(f"Otwórz dokumentację: {BASE_URL}/docs")
