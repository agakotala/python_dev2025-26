import csv
from collections import defaultdict, Counter, namedtuple
import statistics

#definicja głównej funkcji
def analiza_wynagrodzen():
    """Zaawanasowana analiza danycyh wynagrodzen z użyciem różnych technik Python"""

    Pracownik = namedtuple('Pracownik', ['id', 'wiek', 'plec', 'dochod', 'stan_cywilny'])
    pracownicy = []

    try:
        with open('wynagrodzenia.csv', 'r', encoding='utf-8-sig') as plik:
            czytnik = csv.DictReader(plik)

            for wiersz in czytnik:
                try:
                    pracownik = Pracownik(id=int(wiersz['id']),
                                          wiek=int(wiersz['wiek']),
                                          plec=wiersz['płeć'],
                                          dochod=float(wiersz['dochód']),
                                          stan_cywilny=wiersz['stan_cywilny'])
                    pracownicy.append(pracownik)
                except (ValueError, KeyError) as e:
                    print(f"Błąd w wierszu {wiersz.get('id', 'unknown')} : {e}")
                    continue

    except FileNotFoundError:
        print("Błąd: Plik 'wynagrodzenia.csv' nie został znaleziony")
        return
    except Exception as e:
        print(f"Błąd podczas czytania pliku: {e}")
        return
    if not pracownicy:
        print("Brak danych do analizy")

    #podstawowe statystki wynagrodzen
    print("=== PODSTAWOWE STATYSTYKI WYNAGRODZEŃ ===")
    wszystkie_dochody = [p.dochod for p in pracownicy]

    print(f"Liczba pracowników: {len(pracownicy)}")
    print(f"Średnie wynagrodzenie: {statistics.mean(wszystkie_dochody):.2f}zł")
    print(f"Mediana wynagrodzeń: {statistics.median(wszystkie_dochody):.2f}zł")
    print(f"Odchylenie standardowe: {statistics.stdev(wszystkie_dochody):.2f}zł")
    print(f"Minimalne wynagrodzenie: {min(wszystkie_dochody):.2f} zł")
    print(f"Maksymalne wynagrodzenie: {max(wszystkie_dochody):.2f} zł")

    #analiza wg płci
    print("\n=== ANALIZA WEDŁUG PŁCI ===")
    dochody_kobiet = []
    dochody_mezczyzn = []

    for pracownik in pracownicy:
        if pracownik.plec == 'K':
            dochody_kobiet.append(pracownik.dochod)
        else:
            dochody_mezczyzn.append(pracownik.dochod)

    if dochody_kobiet:
        print(f"Kobiety ({len(dochody_kobiet)} osób):")
        print(f"Średnia: {statistics.mean(dochody_kobiet):.2f}zł")
        print(f"Mediana: {statistics.median(dochody_kobiet):.2f}zł")

    if dochody_mezczyzn:
        print(f"Mężczyźni ({len(dochody_mezczyzn)} osób):")
        print(f"Średnia: {statistics.mean(dochody_mezczyzn):.2f}zł")
        print(f"Mediana: {statistics.median(dochody_mezczyzn):.2f}zł")

    print("\n=== ANALIZA PRZEDZIAŁÓW WIEKOWYCH ===")

    przedzialy_wiekowe = defaultdict(list)

    for pracownik in pracownicy:
        if pracownik.wiek < 25:
            przedzial = "18 - 24" #mlodzi pracownicy
        elif pracownik.wiek < 35:
            przedzial = "25 - 34" #mlodzi dorosli
        elif pracownik.wiek < 45:
            przedzial = "35 - 44" #w srednim wieku
        elif pracownik.wiek < 55:
            przedzial = "45 - 54" #starsi
        else:
            przedzial = "55+" #seniorzy

        przedzialy_wiekowe[przedzial].append(pracownik.dochod)
    for przedzial in sorted(przedzialy_wiekowe.keys()):
        dochody = przedzialy_wiekowe[przedzial]
        print(f"{przedzial} lat: {statistics.mean(dochody):.2f}zł (n={len(dochody)})")

        #analiza stanow cywilnych
    print("\n=== ANALIZA STANÓW CYWILNYCH ===")
    stany_cywilne = Counter(p.stan_cywilny for p in pracownicy)
    for stan, liczba in stany_cywilne.most_common():
        procent = (liczba / len(pracownicy)) * 100
        print(f"{stan}: {liczba} osób ({procent:.1f}%)")

    print("\n=== TOP 10 NAJWYŻSZYCH WYNAGRODZEŃ ===")
    top_pracownicy = sorted(pracownicy, key=lambda x: x.dochod, reverse=True)[:10]
    for i, pracownik in enumerate(top_pracownicy, 1):
        print(f"{i:2d}. ID:{pracownik.id:4d} | {pracownik.dochod:8.2f} zł |"
              f" {pracownik.wiek} lat | {pracownik.plec} | {pracownik.stan_cywilny}")
    #analiza rozkladu wynagrodzen
    print("\n=== ROZKŁAD WYNAGRODZEŃ ===")
    max_dochod =  max(wszystkie_dochody)
    przedzialy_dochodowe = defaultdict(int)

    for dochod in wszystkie_dochody:
        if dochod < 3000:
            przedzial = "< 3000 zł" #bardzo niskie wynagrodzenia
        elif dochod < 5000:
            przedzial = "3000 do 5000 zł" #niskie wynagrodzenia
        elif dochod < 7000:
            przedzial = "5000 do 7000 zł" #średnie wynagrodzenia
        elif dochod < 9000:
            przedzial = "7000 do 9000 zł" #wysokie wynagrodzenia
        else:
            przedzial = "powyżej 9000 zł" #bardoz wysokei

        przedzialy_dochodowe[przedzial] += 1

    for przedzial, liczba in sorted(przedzialy_dochodowe.items()):
        procent = (liczba / len(pracownicy)) * 100
        print(f"{przedzial}: {liczba} osób ({procent:.1f}%)")


if __name__ =="__main__":
    analiza_wynagrodzen()

