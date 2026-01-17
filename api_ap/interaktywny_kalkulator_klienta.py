import requests
import json




class IneraktywnyKalkulator:
    def __init__(self, base_url="http://localhost:8010"):
        self.base_url = base_url
        self.historia = []
    def pokaz_menu(self):
        print("INTERAKTYWNY KALKULATOR REST API")
        print("\nWybierz operację:")  # lista opcji dla użytkownika
        print("1. Dodawanie")
        print("2. Odejmowanie")
        print("3. Mnożenie")
        print("4. Dzielenie")
        print("5. Potęgowanie")
        print("6. Pierwiastek kwadratowy")
        print("7. Oblicz wyrażenie")
        print("8. Pokaż historię operacji")
        print("9. Wyjdź")

    def pobierz_liczbe(self, prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Wprowadź poprawne znaki")

    def wykonaj_zapytanie(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Błąd {response.status_code}", "details": response.text}
        except Exception as e:
            return {"error": str(e)}

    def dodaj(self):
        print("DODAWNIE")
        a = self.pobierz_liczbe("Podaj pierwszą liczbę: ")
        b = self.pobierz_liczbe("Podaj drugą liczbę: ")
        wynik = self.wykonaj_zapytanie(f"/dodaj/{a}/{b}")
        self.wyswietl_wynik(f"{a} + {b}", wynik)

    def odejmowanie(self):
        print("ODEJMOWANIE")
        a = self.pobierz_liczbe("Podaj pierwszą liczbę: ")
        b = self.pobierz_liczbe("Podaj drugą liczbę: ")
        wynik = self.wykonaj_zapytanie(f"/odejmij/{a}/{b}")
        self.wyswietl_wynik(f"{a} - {b}", wynik)

    def pomnoz(self):
        print("Mnożenie")
        a = self.pobierz_liczbe("Podaj pierwszą liczbę: ")
        b = self.pobierz_liczbe("Podaj drugą liczbę: ")
        wynik = self.wykonaj_zapytanie(f"/pomnoz/{a}/{b}")
        self.wyswietl_wynik(f"{a} * {b}", wynik)

    def podziel(self):
        print("Dzielenie")
        a = self.pobierz_liczbe("Podaj pierwszą liczbę: ")
        b = self.pobierz_liczbe("Podaj drugą liczbę: ")
        if b == 0:
            print("Nie można dzielić przez 0!")
            return
        wynik = self.wykonaj_zapytanie(f"/podziel/{a}/{b}")
        self.wyswietl_wynik(f"{a} / {b}", wynik)

    def potega(self):
        print("Potęgowanie")
        a = self.pobierz_liczbe("Podaj pierwszą liczbę: ")
        b = self.pobierz_liczbe("Podaj drugą liczbę: ")
        wynik = self.wykonaj_zapytanie(f"/potega/{a}/{b}")
        self.wyswietl_wynik(f"{a} ^ {b}", wynik)

    def pierwiastek(self):
        print("PIERWIASTEK KWADRATOWY")
        a = self.pobierz_liczbe("Podaj liczbę: ")
        if a < 0:
            print("Nie można uzyć liczby ujemnej, wprowadz inna liczbe")
            return
        wynik = self.wykonaj_zapytanie(f"/pierwiastek/{a}")
        self.wyswietl_wynik(f"pierwiastek {a}", wynik)


    def wyrazenie(self):
        print("Wyrażenie Matematyczne")
        wyrazenie = input("Podaj wyrażenie ( np. (45+12)*2): ")

        wyrazenie_zakodowane = requests.untils.quote(wyrazenie)

        wynik = self.wykonaj_zapytanie(f"/oblicz/{wyrazenie_zakodowane}")
        self.wyswietl_wynik(wyrazenie, wynik)


    def historia(self):
        print("Historia Operacji")
        limit = input("Ile ostatnich operacji pokazać? (domyślnie 5): ")
        endpoint = f"/historia"
        if limit.strip():
            endpoint = f"?limit={limit}"
        wynik = self.wykonaj_zapytanie(endpoint)

        if "historia" in wynik:
            print(f"Ostatnie operacje ({len(wynik['historia'])}):")
            for i, op in enumerate(wynik['historia'], 1):
                print(f" {i:2d}.[{op['czas']}] {op['operacja']}")
        else:
            print("Nie udało się pobrać historii")

    def wyswietl_wynik(self, operacja, wynik):
        print(f"Operacja: {operacja}")
        if "wynik" in wynik:
            print(f" WYNIK: {wynik['wynik']}")
            self.historia.append(f"{operacja} = {wynik['wynik']}")


        elif "error" in wynik:
            print(f"Błąd: {wynik['error']}")
            if "details" in wynik:
                print(f"Szczegóły: {wynik['details']}")

        else:
            print(f"Odpowiedź serwera: {json.dumps(wynik, indent=2)}")

    def uruchom(self):
        while True:
            self.pokaz_menu()
            wybor = input("Twój wybój (1-9): ").strip()
            if wybor == "1":
                self.dodaj()
            elif wybor == "2":
                self.odejmij()
            elif wybor == "3":
                self.pomnoz()
            elif wybor == "4":
                self.podziel()
            elif wybor == "5":
                self.potega()
            elif wybor == "6":
                self.pierwiastek()
            elif wybor == "7":
                self.wyrazenie()
            elif wybor == "8":
                self.historia()
            elif wybor == "9":
                print("Do widzenia")

            else:
                print("Nieprawidłowy wybór.")
            input("\nNaciśnij Enter, aby kontynuować")


if __name__ == "__main__":
    kalkulator = IneraktywnyKalkulator()
    kalkulator.uruchom()





