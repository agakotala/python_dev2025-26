import csv
from collections import defaultdict, Counter

def analiza_klientow():
    """Funkcja analizująca dane klientów"""

    try:
        with open('klienci.csv', 'r', encoding='utf-8-sig') as plik:
            czytnik = csv.DictReader(plik)
            licznik_imion = Counter()
            klienci_w_miastach = defaultdict(list)
            aktywni_w_miescie = defaultdict(int)
            aktywni_klienci = 0
            total_klienci = 0

            for wiersz in czytnik:
                licznik_imion[wiersz['imię']] += 1
                klienci_w_miastach[wiersz['miasto']].append(wiersz['imię'])
                if wiersz['status'] == '1':
                    aktywni_klienci += 1
                    aktywni_w_miescie[wiersz['miasto']] += 1
                total_klienci += 1
            print(f"\n=== ANALIZA KLIENTÓW ===")
            print(f"Łączna liczba klientów: {total_klienci}")
            print(f"Aktywni klienci: {aktywni_klienci} ({aktywni_klienci / total_klienci * 100:.1f}%)")
            #analiza imion
            print(f"\nNajpopularniejsze imiona:")
            for imie, liczba in licznik_imion.most_common(5):
                print(f"{imie}: {liczba}")

            #analiza miast
            print(f"\nMiasta z największą liczbą klientów:")
            for miasto, liczba in Counter({m: len(k) for m, k in klienci_w_miastach.items()}).most_common(5):
                print(f"{miasto}: {liczba}")

            #analiza aktywności w miastach
            print(f"\nProcent aktywnych klientów w miastach (TOP 5):")
            for miasto, aktywni in Counter(aktywni_w_miescie).most_common(5):
                wszystkich = len(klienci_w_miastach[miasto])
                procent = (aktywni/wszystkich) * 100
                print(f"{miasto} : {procent:.1f}% ({aktywni}/{wszystkich})")

    except Exception as e:
        print(f"Błąd: {e}")

print("\n" + "=" * 50)
analiza_klientow()