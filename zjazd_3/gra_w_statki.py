import random


# 1. Tworzymy planszę 10x10 wypełnioną kropkami (puste pola)
def stworz_plansze():
    return [["." for _ in range(10)] for _ in range(10)]


# 2. Funkcja do wyświetlania planszy
def wyswietl_plansze(plansza):
    print("  A B C D E F G H I J")  # Nagłówki kolumn
    for i, wiersz in enumerate(plansza):
        print(f"{i} ", end="")  # Numer wiersza
        for pole in wiersz:
            print(pole, end=" ")
        print()  # Nowa linia po każdym wierszu


# 3. Funkcja do umieszczania statku na planszy
def umiesc_statek(plansza, dlugosc):
    while True:
        # Losujemy czy statek będzie poziomo czy pionowo
        kierunek = random.choice(["poziomy", "pionowy"])

        if kierunek == "poziomy":
            # Losujemy pozycję startową dla poziomego statku
            wiersz = random.randint(0, 9)
            kolumna = random.randint(0, 10 - dlugosc)

            # Sprawdzamy czy wszystkie pola są wolne
            if all(plansza[wiersz][kolumna + i] == "." for i in range(dlugosc)):
                # Umieszczamy statek (oznaczamy literą 'S')
                for i in range(dlugosc):
                    plansza[wiersz][kolumna + i] = "S"
                break

        else:  # kierunek pionowy
            # Losujemy pozycję startową dla pionowego statku
            wiersz = random.randint(0, 10 - dlugosc)
            kolumna = random.randint(0, 9)

            # Sprawdzamy czy wszystkie pola są wolne
            if all(plansza[wiersz + i][kolumna] == "." for i in range(dlugosc)):
                # Umieszczamy statek (oznaczamy literą 'S')
                for i in range(dlugosc):
                    plansza[wiersz + i][kolumna] = "S"
                break


# 4. Funkcja do konwersji liter na liczby (A=0, B=1, itd.)
def liter_na_liczbe(litera):
    return ord(litera.upper()) - ord('A')


# 5. Główna funkcja gry
def graj_w_statki():
    print("Witaj w grze w STATKI!")
    print("Twoim zadaniem jest zatopić wszystkie statki komputera.")
    print("Plansza: '.' - nieznane pole, 'X' - trafienie, 'O' - pudło")
    print("Wprowadzaj ruchy w formacie: A5, B3, itd.")

    # Tworzymy planszę gracza (do strzałów)
    plansza_gracza = stworz_plansze()

    # Tworzymy ukrytą planszę komputera z statkami
    plansza_komputera = stworz_plansze()

    # Umieszczamy statki komputera: 1x4, 2x3, 3x2, 4x1
    statki = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for statek in statki:
        umiesc_statek(plansza_komputera, statek)

    # Licznik pozostałych statków
    pozostale_statki = sum(statki)
    ruchy = 0

    # Główna pętla gry
    while pozostale_statki > 0:
        print(f"\n--- Ruch {ruchy + 1} ---")
        wyswietl_plansze(plansza_gracza)

        # Gracz wprowadza swój ruch
        while True:
            try:
                ruch = input("\nPodaj swój ruch (np. A5): ").strip()

                # Sprawdzamy czy ruch ma odpowiednią długość
                if len(ruch) < 2:
                    print("Nieprawidłowy ruch! Wprowadź np. A5")
                    continue

                # Zamieniamy literę na liczbę
                kolumna = liter_na_liczbe(ruch[0])
                wiersz = int(ruch[1:])

                # Sprawdzamy czy współrzędne są w zakresie 0-9
                if 0 <= wiersz <= 9 and 0 <= kolumna <= 9:
                    # Sprawdzamy czy już strzelaliśmy w to pole
                    if plansza_gracza[wiersz][kolumna] in ["X", "O"]:
                        print("Już strzelałeś w to pole! Wybierz inne.")
                        continue
                    break
                else:
                    print("Współrzędne poza planszą! Użyj A-J i 0-9")

            except (ValueError, IndexError):
                print("Nieprawidłowy ruch! Wprowadź np. A5")

        # Sprawdzamy wynik strzału
        ruchy += 1
        if plansza_komputera[wiersz][kolumna] == "S":
            print("*** TRAFIENIE! ***")
            plansza_gracza[wiersz][kolumna] = "X"
            plansza_komputera[wiersz][kolumna] = "X"  # Oznaczamy trafienie
            pozostale_statki -= 1
            print(f"Pozostało statków do zatopienia: {pozostale_statki}")
        else:
            print("PUDŁO!")
            plansza_gracza[wiersz][kolumna] = "O"

    # Koniec gry - gracz wygrał
    print(f"\n*** GRATULACJE! ***")
    print(f"Zatopiłeś wszystkie statki w {ruchy} ruchach!")
    print("Oto plansza komputera z pokazanymi statkami:")

    # Pokazujemy planszę komputera z odsłoniętymi statkami
    for i in range(10):
        for j in range(10):
            if plansza_komputera[i][j] == "S":
                plansza_gracza[i][j] = "S"

    wyswietl_plansze(plansza_gracza)


# 6. Uruchamiamy grę jeśli ten plik jest uruchamiany bezpośrednio
if __name__ == "__main__":
    graj_w_statki()
