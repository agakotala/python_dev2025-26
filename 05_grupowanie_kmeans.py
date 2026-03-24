# ===============================================================  # Nagłówek mówi, że przechodzimy do uczenia nienadzorowanego.
# PRZYKŁAD 05: GRUPOWANIE DANYCH METODĄ K-MEANS                    # Tytuł wskazuje, że będziemy szukać skupień bez etykiet klas.
# ===============================================================  # Linia dekoracyjna zamyka nagłówek.

import matplotlib.pyplot as plt  # Importujemy matplotlib do narysowania skupień i centroidów.
import pandas as pd  # Importujemy pandas do zbudowania czytelnej tabeli z etykietami klastrów.
from sklearn.cluster import KMeans  # Importujemy algorytm K-Means do grupowania obserwacji.
from sklearn.datasets import make_blobs  # Importujemy generator sztucznych danych z naturalnymi skupieniami.
from sklearn.metrics import silhouette_score  # Importujemy wskaźnik silhouette do oceny jakości grupowania.

X, y_prawdziwe = make_blobs(  # Generujemy przykładowe dane z trzema naturalnymi skupieniami.
    n_samples=300,  # Określamy liczbę obserwacji w zbiorze.
    centers=3,  # Definiujemy liczbę środków skupień w generowanych danych.
    cluster_std=1.2,  # Ustawiamy rozrzut punktów wokół każdego środka.
    random_state=42,  # Ustawiamy ziarno losowe dla powtarzalności.
)  # Zamykamy funkcję generującą dane.

model = KMeans(n_clusters=3, random_state=42, n_init=10)  # Tworzymy model K-Means z trzema klastrami i wieloma startami.
etykiety_klastrow = model.fit_predict(X)  # Uczymy model i jednocześnie pobieramy numer klastra dla każdej obserwacji.
centroidy = model.cluster_centers_  # Pobieramy współrzędne środków znalezionych klastrów.
silhouette = silhouette_score(X, etykiety_klastrow)  # Liczymy miarę silhouette, aby ocenić separację klastrów.

print("WSPÓŁCZYNNIK SILHOUETTE:", round(silhouette, 3))  # Wypisujemy wynik jakości grupowania.

tabela = pd.DataFrame(X, columns=["cecha_1", "cecha_2"])  # Tworzymy tabelę z dwiema cechami dla wygodniejszej prezentacji.
tabela["klaster"] = etykiety_klastrow  # Dodajemy numer przypisanego klastra dla każdego rekordu.
print("\nPIERWSZE 10 OBSERWACJI Z NUMEREM KLASTRA:")  # Dodajemy nagłówek dla prezentacji tabeli.
print(tabela.head(10))  # Wyświetlamy pierwsze dziesięć rekordów z informacją o klastrze.

plt.figure(figsize=(8, 6))  # Tworzymy figurę o wygodnym rozmiarze.
plt.scatter(X[:, 0], X[:, 1], c=etykiety_klastrow, alpha=0.7)  # Rysujemy punkty i kolorujemy je zgodnie z numerem klastra.
plt.scatter(centroidy[:, 0], centroidy[:, 1], marker="X", s=250, linewidths=2)  # Rysujemy centroidy jako duże znaczniki X.
plt.xlabel("Cecha 1")  # Opisujemy oś poziomą.
plt.ylabel("Cecha 2")  # Opisujemy oś pionową.
plt.title("Grupowanie K-Means")  # Ustawiamy tytuł wykresu.
plt.tight_layout()  # Dopasowujemy marginesy całego rysunku.
plt.show()  # Wyświetlamy finalny wykres.

print("\nINTERPRETACJA:")  # Rozpoczynamy sekcję podsumowania.
print("K-Means nie potrzebuje etykiet klas, bo sam szuka podobnych punktów w przestrzeni cech.")  # Wyjaśniamy ideę uczenia nienadzorowanego.
print("Algorytm działa dobrze, gdy klastry są względnie kuliste i podobnej wielkości.")  # Zaznaczamy ważne założenie praktyczne.
print("Liczbę klastrów k zwykle dobiera się eksperymentalnie, np. metodą łokcia lub wskaźnikiem silhouette.")  # Podpowiadamy, jak dobierać parametr k.