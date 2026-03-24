import random


# funkcja do stworzenia planszy 10x10
def stworz_plansze():
    return [["." for _ in range(10)] for _ in range(10)]


# funkcja do wyświetlania planszy
def wyswietl_plansze(plansza):
    print(" A B C D E F G H I J")
    for i, wiersz in enumerate(plansza):
        print(f"{i}", end="")
        for pole in wiersz:
            print(pole, end=" ")
        print()


# funkcja do umieszczenia statku na planszy
def umiesc_statek(plansza, dlugosc):
    while True:
        kierunek = random.choice(["poziomy", "pionowy"])
        if kierunek == "poziomy":
            wiersz = random.randint(0, 9)
            kolumna = random.randint(0, 10 - dlugosc)

            if all(plansza[wiersz][kolumna + i] == "." for i in range(dlugosc)):
                for i in range(dlugosc):
                    plansza[wiersz][kolumna + i] = "S"
                break
        else:
            wiersz = random.randint(0, 10 - dlugosc)
            kolumna = random.randint(0, 9)

            if all(plansza[wiersz + i][kolumna] == "." for i in range(dlugosc)):
                for i in range(dlugosc):
                    plansza[wiersz + i][kolumna] = "S"
                break


def liter_na_liczbe(litera):
    return ord(litera.upper()) - ord('A')


# główna funkcja gry

def graj_w_statki():
    print("Witaj w grze w STATKI")
    print("Twoim zadaniem jest zatopić wszystkie statki")
    print("Plansza: '.' - nieznane pole, 'X' - trafienie, 'O' - pudło")
    print("Wprowadzaj ruchy w fromacie: A5, B3, C8, itd.")

    plansza_gracza = stworz_plansze()
    plansza_komputera = stworz_plansze()

    statki = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for statek in statki:
        umiesc_statek(plansza_komputera, statek)

    pozostale_statki = sum(statki)
    ruchy = 0

    while pozostale_statki > 0:
        print(f"\n--- Ruch {ruchy + 1} ---")
        wyswietl_plansze(plansza_gracza)

        while True:
            try:
                ruch = input("\nPodaj swój ruch (np. A5): ").strip()

                if len(ruch) < 2:
                    print("Nieprawdiłowy ruch! Wprowadź np. A5")
                    continue

                kolumna = liter_na_liczbe(ruch[0])
                wiersz = int(ruch[1:])

                if 0 <= wiersz <= 9 and 0 <= kolumna <= 9:
                    if plansza_gracza[wiersz][kolumna] in ["X", "O"]:
                        print("Już strzelałeś w to pole! Wybierz inne.")
                        continue
                    break
                else:
                    print("Współrzędne poza planszą! Użyj A-J i 0-9")
            except (ValueError, IndexError):
                print("Nieprawidłowy ruch! Wprowadź np. A5")

        ruchy += 1
        if plansza_komputera[wiersz][kolumna] == "S":
            print("TRAFIONE")
            plansza_gracza[wiersz][kolumna] = "X"
            plansza_komputera[wiersz][kolumna] = "X"
            pozostale_statki -= 1
            print(f"Pozostało statków do zatopienia: {pozostale_statki}")
        else:
            print("PUDŁO")
            plansza_gracza[wiersz][kolumna] = "O"

    print(f"\nGRATULACJE!")
    print(f"Zatopiłeś wszystkie statki w {ruchy} ruchach")
    print("Oto plansza komuptera z pokazanymi statkami:")

    for i in range(10):
        for j in range(10):
            if plansza_gracza[i][j] == "S":
                plansza_gracza[i][j] = "S"

    wyswietl_plansze(plansza_gracza)


if __name__ == "__main__":
    graj_w_statki()
