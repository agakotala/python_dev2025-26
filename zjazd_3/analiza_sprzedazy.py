import csv

import re

from collections import defaultdict, Counter, namedtuple

import statistics


# DEFINICJA GŁÓWNEJ FUNKCJI ANALIZY SPRZEDAŻY
def analiza_sprzedazy_zaawansowana():
    """
    Zaawansowana analiza danych sprzedaży z użyciem różnych technik Python
    """

    # 1. NAMEDTUPLE dla transakcji - tworzenie struktury danych
    Transakcja = namedtuple('Transakcja', ['id', 'produkt', 'ilosc', 'cena', 'przychod'])

    transakcje = []

    # 2. WCZYTANIE I WALIDACJA DANYCH - blok try-except zabezpiecza przed crashami
    try:
        with open('sprzedaz.csv', 'r', encoding='utf-8-sig') as plik:
            czytnik = csv.DictReader(plik)

            for wiersz in czytnik:

                try:
                    # OBSŁUGA POTENCJALNEGO BOM W NAGŁÓWKACH
                    # Domyślne nazwy kluczy (bez BOM)
                    klucz_id = 'transakcja_id'
                    klucz_produkt = 'produkt'
                    klucz_ilosc = 'ilość'
                    klucz_cena = 'cena'

                    # Sprawdź czy nagłówki mają BOM - \ufeff to znak BOM w Unicode
                    # Jeśli w słowniku wiersz istnieje klucz z BOM, użyj tego klucza
                    if '\ufefftransakcja_id' in wiersz:
                        klucz_id = '\ufefftransakcja_id'  # Użyj klucza z BOM
                    if '\ufeffprodukt' in wiersz:
                        klucz_produkt = '\ufeffprodukt'  # Użyj klucza z BOM
                    if '\ufeffilość' in wiersz:
                        klucz_ilosc = '\ufeffilość'  # Użyj klucza z BOM
                    if '\ufeffcena' in wiersz:
                        klucz_cena = '\ufeffcena'  # Użyj klucza z BOM

                    # Pobranie i konwersja danych z odpowiednich kluczy
                    id_transakcji = int(wiersz[klucz_id])
                    produkt = wiersz[klucz_produkt]
                    ilosc = int(wiersz[klucz_ilosc])
                    cena = float(wiersz[klucz_cena])
                    przychod = ilosc * cena

                    # WALIDACJA DANYCH ZA POMOCĄ WYRAŻEŃ REGULARNYCH

                    if not re.match(r'^[A-E]$', produkt):
                        continue  # Pomijaj nieprawidłowe produkty - przejdź do następnego wiersza

                    if ilosc < 1 or ilosc > 9:
                        continue  # Pomijaj nieprawidłowe ilości - przejdź do następnego wiersza

                    transakcja = Transakcja(id_transakcji, produkt, ilosc, cena, przychod)
                    transakcje.append(transakcja)  # Dodanie utworzonego obiektu do listy

                except (ValueError, KeyError) as e:
                    continue  # Pomijaj błędne wiersze - przejdź do następnego wiersza

    except FileNotFoundError:  # Gdy plik nie istnieje
        print("Błąd: Plik 'sprzedaz.csv' nie został znaleziony!")
        return
    except Exception as e:
        print(f"Błąd podczas czytania pliku: {e}")
        return


    if not transakcje:
        print("Brak danych do analizy!")
        return

    # 3. PODSTAWOWE STATYSTYKI SPRZEDAŻY - obliczenia na wszystkich danych

    print("=== PODSTAWOWE STATYSTYKI SPRZEDAŻY ===")  # Nagłówek sekcji

    print(f"Liczba transakcji: {len(transakcje)}")

    print(f"Łączny przychód: {sum(t.przychod for t in transakcje):.2f} zł")

    print(f"Średnia wartość transakcji: {statistics.mean(t.przychod for t in transakcje):.2f} zł")

    print(f"Łączna liczba sprzedanych sztuk: {sum(t.ilosc for t in transakcje)}")

    # 4. ANALIZA PRODUKTÓW Z DEFAULTDICT I COUNTER - grupowanie według produktów

    print("\n=== ANALIZA PRODUKTÓW ===")


    przychody_produktow = defaultdict(float)

    ilosci_produktow = defaultdict(int)
    transakcje_produktow = defaultdict(int)


    for transakcja in transakcje:
        przychody_produktow[transakcja.produkt] += transakcja.przychod

        ilosci_produktow[transakcja.produkt] += transakcja.ilosc


        transakcje_produktow[transakcja.produkt] += 1

    print("Ranking produktów według przychodu:")

    for produkt, przychod in sorted(przychody_produktow.items(), key=lambda x: x[1], reverse=True):
        print(f"  Produkt {produkt}: {przychod:.2f} zł "
              f"({ilosci_produktow[produkt]} szt., {transakcje_produktow[produkt]} trans.)")

    # 5. ANALIZA EFEKTYWNOŚCI PRODUKTÓW - szczegółowe metryki per produkt

    print("\n=== EFEKTYWNOŚĆ PRODUKTÓW ===")


    for produkt in sorted(przychody_produktow.keys()):
        transakcje_dla_produktu = [t for t in transakcje if t.produkt == produkt]


        if transakcje_dla_produktu:

            srednia_ilosc = statistics.mean(t.ilosc for t in transakcje_dla_produktu)

            srednia_cena = statistics.mean(t.cena for t in transakcje_dla_produktu)

            sredni_przychod = statistics.mean(t.przychod for t in transakcje_dla_produktu)

            # Wyświetlenie szczegółowych statystyk produktu

            print(f"Produkt {produkt}:")
            print(f"  Średnia ilość/szt.: {srednia_ilosc:.1f}")
            print(f"  Średnia cena: {srednia_cena:.2f} zł")
            print(f"  Średni przychód/trans.: {sredni_przychod:.2f} zł")

    # 6. ANALIZA WIELKOŚCI TRANSAKCJI - rozkład według liczby sztuk

    print("\n=== ANALIZA WIELKOŚCI TRANSAKCJI ===")

    transakcje_wedlug_ilosci = Counter(t.ilosc for t in transakcje)

    print("Rozkład transakcji według liczby sztuk:")

    for ilosc, liczba in sorted(transakcje_wedlug_ilosci.items()):
        procent = (liczba / len(transakcje)) * 100
        print(f"  {ilosc} sztuk: {liczba} transakcji ({procent:.1f}%)")

    # 7. ANALIZA WARTOŚCI TRANSAKCJI - statystyki wartości przychodów

    print("\n=== ANALIZA WARTOŚCI TRANSAKCJI ===")

    wartosci_transakcji = [t.przychod for t in transakcje]

    # Podstawowe statystyki opisowe wartości transakcji

    print(f"Minimalna wartość: {min(wartosci_transakcji):.2f} zł")  # Najniższa transakcja
    print(f"Maksymalna wartość: {max(wartosci_transakcji):.2f} zł")  # Najwyższa transakcja
    print(f"Średnia wartość: {statistics.mean(wartosci_transakcji):.2f} zł")  # Średnia arytmetyczna
    print(f"Mediana wartości: {statistics.median(wartosci_transakcji):.2f} zł")  # Wartość środkowa


    print("\n=== TOP 10 NAJWARTEŚCIOWSZYCH TRANSAKCJI ===")

    top_transakcje = sorted(transakcje, key=lambda x: x.przychod, reverse=True)[:10]

    # Wyświetlenie top 10 z formatowaniem i numeracją

    for i, transakcja in enumerate(top_transakcje, 1):
        print(f"{i:2d}. ID:{transakcja.id:4d} | {transakcja.przychod:7.2f} zł | "
              f"Produkt {transakcja.produkt} | {transakcja.ilosc} szt. × {transakcja.cena} zł")

    # 9. ANALIZA CZĘSTOTLIWOŚCI SPRZEDAŻY - statystyki czasowe

    print("\n=== CZĘSTOTLIWOŚĆ SPRZEDAŻY ===")


    if transakcje:  # Jeśli są jakieś transakcje
        pierwsza_transakcja = min(t.id for t in transakcje)
        ostatnia_transakcja = max(t.id for t in transakcje)

        print(f"Zakres transakcji: ID {pierwsza_transakcja} - {ostatnia_transakcja}")
        print(f"Średnia liczba transakcji na produkt: {len(transakcje) / len(przychody_produktow):.1f}")

    # 10. ZAAWANSOWANA ANALIZA - KORELACJE - prosty przegląd zakresów

    print("\n=== ANALIZA KORELACJI ===")


    for produkt in sorted(przychody_produktow.keys()):

        transakcje_produktu = [t for t in transakcje if t.produkt == produkt]


        if len(transakcje_produktu) > 1:

            ilosci = [t.ilosc for t in transakcje_produktu]  # Lista ilości
            przychody = [t.przychod for t in transakcje_produktu]  # Lista przychodów


            if max(ilosci) > min(ilosci):

                print(f"Produkt {produkt}: ilość {min(ilosci)}-{max(ilosci)} szt., "
                      f"przychód {min(przychody):.2f}-{max(przychody):.2f} zł")



if __name__ == "__main__":
    analiza_sprzedazy_zaawansowana()
