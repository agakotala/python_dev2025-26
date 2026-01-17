class Pracownik:
    def __init__(self, imie: str, pensja_podstawowa: float):
        self.imie = imie                      # przechodzi przez property -> walidacja
        self.pensja_podstawowa = pensja_podstawowa  # przechodzi przez property -> walidacja


    @property
    def imie(self) -> str:
        return self.__imie

    @imie.setter
    def imie(self, wartosc: str) -> None:
        if not isinstance(wartosc, str) or not wartosc.strip():
            raise ValueError("Imię musi być niepustym napisem.")
        self.__imie = wartosc.strip()

    # --- pensja_podstawowa ---
    @property
    def pensja_podstawowa(self) -> float:
        return self.__pensja_podstawowa

    @pensja_podstawowa.setter
    def pensja_podstawowa(self, wartosc: float) -> None:
        try:
            wartosc = float(wartosc)
        except (TypeError, ValueError):
            raise ValueError("Pensja podstawowa musi być liczbą.")
        if wartosc <= 0:
            raise ValueError("Pensja podstawowa musi być większa od 0.")
        self.__pensja_podstawowa = wartosc

    # --- logika ---
    def wyplata_miesieczna(self) -> float:
        return self.pensja_podstawowa

    def info(self) -> str:
        return (
            f"Pracownik: {self.imie}, pensja podstawowa: {self.pensja_podstawowa:.2f}, "
            f"wypłata: {self.wyplata_miesieczna():.2f}"
        )


class Programista(Pracownik):
    def __init__(self, imie: str, pensja_podstawowa: float, nadgodziny: int = 0):
        super().__init__(imie, pensja_podstawowa)
        self.nadgodziny = nadgodziny

    @property
    def nadgodziny(self) -> int:
        return self.__nadgodziny

    @nadgodziny.setter
    def nadgodziny(self, wartosc: int) -> None:
        if not isinstance(wartosc, int):
            raise ValueError("Liczba nadgodzin musi być liczbą całkowitą.")
        if wartosc < 0:
            raise ValueError("Liczba nadgodzin musi być >= 0.")
        self.__nadgodziny = wartosc

    def wyplata_miesieczna(self) -> float:
        stawka_za_godzine = (self.pensja_podstawowa / 160) * 1.5
        return self.pensja_podstawowa + self.nadgodziny * stawka_za_godzine

    def info(self) -> str:
        return (
            f"Programista: {self.imie}, pensja podstawowa: {self.pensja_podstawowa:.2f}, "
            f"nadgodziny: {self.nadgodziny}, wypłata: {self.wyplata_miesieczna():.2f}"
        )


class Sprzedawca(Pracownik):
    def __init__(self, imie: str, pensja_podstawowa: float, prowizja: float = 0.0):
        super().__init__(imie, pensja_podstawowa)
        self.prowizja = prowizja

    @property
    def prowizja(self) -> float:
        return self.__prowizja

    @prowizja.setter
    def prowizja(self, wartosc: float) -> None:
        try:
            wartosc = float(wartosc)
        except (TypeError, ValueError):
            raise ValueError("Prowizja musi być liczbą.")
        if wartosc < 0:
            raise ValueError("Prowizja musi być >= 0.")
        self.__prowizja = wartosc

    def wyplata_miesieczna(self) -> float:
        return self.pensja_podstawowa + self.prowizja

    def info(self) -> str:
        return (
            f"Sprzedawca: {self.imie}, pensja podstawowa: {self.pensja_podstawowa:.2f}, "
            f"prowizja: {self.prowizja:.2f}, wypłata: {self.wyplata_miesieczna():.2f}"
        )


class ListaPlac:
    def __init__(self):
        self.__pracownicy = []

    def dodaj(self, pracownik: Pracownik) -> None:
        if not isinstance(pracownik, Pracownik):
            raise TypeError("Można dodać tylko obiekt klasy Pracownik (lub klasy dziedziczącej).")
        self.__pracownicy.append(pracownik)

    def koszt_calkowity(self) -> float:
        return sum(p.wyplata_miesieczna() for p in self.__pracownicy)

    def pokaz(self) -> None:
        for p in self.__pracownicy:
            print(p.info())


def main():
    # --- tworzenie obiektów ---
    p1 = Pracownik("Jan Kowalski", 5000)
    pr1 = Programista("Ala Nowak", 8000, nadgodziny=10)
    s1 = Sprzedawca("Olek Zielinski", 4500, prowizja=1200)

    print("=== INFORMACJE ===")
    print(p1.info())
    print(pr1.info())
    print(s1.info())

    # --- Lista płac (bonus) ---
    lista = ListaPlac()
    lista.dodaj(p1)
    lista.dodaj(pr1)
    lista.dodaj(s1)

    print("\n=== LISTA PŁAC ===")
    lista.pokaz()
    print(f"\nCałkowity koszt miesięczny: {lista.koszt_calkowity():.2f}")

    # --- testy walidacji ---
    print("\n=== TESTY WALIDACJI ===")
    testy = [
        ("Puste imię", lambda: Pracownik("", 1000)),
        ("Ujemna pensja", lambda: Pracownik("X", -1)),
        ("Ujemne nadgodziny", lambda: Programista("Dev", 5000, -5)),
        ("Ujemna prowizja", lambda: Sprzedawca("Sales", 4000, -200)),
    ]

    for opis, funkcja in testy:
        try:
            funkcja()
        except Exception as e:
            print(f"{opis} -> OK, złapano: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
