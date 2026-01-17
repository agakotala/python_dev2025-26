class KontoBankowe:
    def __init__(self, wlasciciel: str) -> None:
        if not wlasciciel:
            raise ValueError("Właściciel nie może być pusty.")
        self.wlasciciel = wlasciciel
        self._saldo = 0.0

    def wplata(self, kwota: float) -> None:
        if kwota <= 0:
            raise ValueError("Kwota wpłaty musi być większa od 0.")
        self._saldo += kwota

    def wyplata(self, kwota: float) -> None:
        if kwota <= 0:
            raise ValueError("Kwota wypłaty musi być większa od 0.")
        if kwota > self._saldo:
            raise ValueError("Brak wystarczających środków na koncie.")
        self._saldo -= kwota

    def pobierz_saldo(self) -> float:
        return self._saldo


class Bankomat:
    def uruchom(self, konto: KontoBankowe) -> None:
        while True:
            print("\n--- BANKOMAT ---")
            print("1. Wpłata")
            print("2. Wypłata")
            print("3. Sprawdź saldo")
            print("4. Zakończ")

            wybor = input("Wybierz opcję (1-4): ").strip()

            if wybor == "1":
                try:
                    kwota = float(input("Podaj kwotę wpłaty: "))
                    konto.wplata(kwota)
                    print(f"Wpłacono: {kwota:.2f} zł")
                except ValueError as e:
                    print(f"Błąd: {e}")

            elif wybor == "2":
                try:
                    kwota = float(input("Podaj kwotę wypłaty: "))
                    konto.wyplata(kwota)
                    print(f"Wypłacono: {kwota:.2f} zł")
                except ValueError as e:
                    print(f"Błąd: {e}")

            elif wybor == "3":
                saldo = konto.pobierz_saldo()
                print(f"Saldo: {saldo:.2f} zł")

            elif wybor == "4":
                print("Do widzenia!")
                break

            else:
                print("Nieprawidłowy wybór. Wpisz 1, 2, 3 albo 4.")


konto = KontoBankowe("Jan")
Bankomat().uruchom(konto)
