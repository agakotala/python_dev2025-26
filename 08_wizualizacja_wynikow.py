# =====================================================================  # Nagłówek mówi, że skupimy się na interpretacji i wizualizacji wyników.
# PRZYKŁAD 08: WIZUALIZOWANIE WYNIKÓW - MACIERZ POMYŁEK, ROC, RESIDUALS  # Tytuł wymienia trzy ważne typy wizualizacji.
# =====================================================================  # Linia dekoracyjna kończy sekcję tytułową.

import matplotlib.pyplot as plt  # Importujemy matplotlib do rysowania wykresów oceny modeli.
from sklearn.datasets import load_breast_cancer  # Importujemy zbiór danych do przykładu klasyfikacyjnego.
from sklearn.datasets import load_diabetes  # Importujemy zbiór danych do przykładu regresyjnego.
from sklearn.linear_model import LinearRegression  # Importujemy model regresji liniowej do analizy reszt.
from sklearn.linear_model import LogisticRegression  # Importujemy model regresji logistycznej do ROC i macierzy pomyłek.
from sklearn.metrics import ConfusionMatrixDisplay  # Importujemy narzędzie do wizualizacji macierzy pomyłek.
from sklearn.metrics import RocCurveDisplay  # Importujemy narzędzie do rysowania krzywej ROC.
from sklearn.model_selection import train_test_split  # Importujemy funkcję dzielącą dane na trening i test.
from sklearn.pipeline import Pipeline  # Importujemy Pipeline do połączenia skalowania z modelem logistycznym.
from sklearn.preprocessing import StandardScaler  # Importujemy standaryzację.

# ---------------------- CZĘŚĆ 1: KLASYFIKACJA ----------------------  # Ten komentarz informuje, że zaczynamy blok klasyfikacyjny.

zbior_klasyfikacja = load_breast_cancer()  # Wczytujemy dane do klasyfikacji binarnej.
Xc = zbior_klasyfikacja.data  # Zapisujemy cechy klasyfikacyjne do zmiennej Xc.
yc = zbior_klasyfikacja.target  # Zapisujemy etykiety klas do zmiennej yc.

Xc_train, Xc_test, yc_train, yc_test = train_test_split(  # Dzielimy dane klasyfikacyjne na trening i test.
    Xc,  # Przekazujemy cechy klasyfikacyjne.
    yc,  # Przekazujemy klasy.
    test_size=0.2,  # Rezerwujemy 20% danych na ocenę modelu.
    random_state=42,  # Zapewniamy powtarzalność podziału.
    stratify=yc,  # Zachowujemy proporcje klas.
)  # Kończymy wywołanie funkcji podziału.

model_klasyfikacja = Pipeline(steps=[  # Budujemy pipeline klasyfikacyjny.
    ("skalowanie", StandardScaler()),  # Skalujemy cechy przed regresją logistyczną.
    ("model", LogisticRegression(max_iter=1000, random_state=42)),  # Dodajemy model logistyczny.
])  # Kończymy definicję pipeline.

model_klasyfikacja.fit(Xc_train, yc_train)  # Uczymy model klasyfikacyjny na danych treningowych.
yc_pred = model_klasyfikacja.predict(Xc_test)  # Przewidujemy etykiety dla danych testowych.

ConfusionMatrixDisplay.from_predictions(  # Rysujemy macierz pomyłek bez ręcznego liczenia tabeli.
    yc_test,  # Podajemy prawdziwe etykiety.
    yc_pred,  # Podajemy przewidziane etykiety.
    display_labels=zbior_klasyfikacja.target_names,  # Opisujemy klasy ich nazwami.
)  # Kończymy rysowanie macierzy pomyłek.
plt.title("Macierz pomyłek")  # Nadajemy tytuł pierwszemu wykresowi.
plt.tight_layout()  # Dopasowujemy układ.
plt.show()  # Wyświetlamy macierz pomyłek.

RocCurveDisplay.from_estimator(  # Rysujemy krzywą ROC bez ręcznego liczenia punktów.
    model_klasyfikacja,  # Przekazujemy wytrenowany model.
    Xc_test,  # Przekazujemy cechy ze zbioru testowego.
    yc_test,  # Przekazujemy prawdziwe etykiety.
)  # Kończymy tworzenie wykresu ROC.
plt.title("Krzywa ROC")  # Nadajemy tytuł drugiemu wykresowi.
plt.tight_layout()  # Dopasowujemy marginesy.
plt.show()  # Wyświetlamy krzywą ROC.

# ----------------------- CZĘŚĆ 2: REGRESJA -------------------------  # Ten komentarz oddziela część regresyjną od klasyfikacyjnej.

zbior_regresja = load_diabetes(as_frame=True)  # Wczytujemy zbiór do regresji.
Xr = zbior_regresja.data  # Zapisujemy cechy regresyjne.
yr = zbior_regresja.target  # Zapisujemy wartość docelową dla regresji.

Xr_train, Xr_test, yr_train, yr_test = train_test_split(  # Dzielimy dane regresyjne na trening i test.
    Xr,  # Przekazujemy cechy.
    yr,  # Przekazujemy wartości docelowe.
    test_size=0.2,  # Ustalamy rozmiar zbioru testowego.
    random_state=42,  # Zapewniamy odtwarzalność.
)  # Kończymy podział danych regresyjnych.

model_regresja = LinearRegression()  # Tworzymy model regresji liniowej.
model_regresja.fit(Xr_train, yr_train)  # Uczymy model regresyjny.
yr_pred = model_regresja.predict(Xr_test)  # Wyznaczamy przewidywania modelu.

reszty = yr_test - yr_pred  # Obliczamy residuals, czyli różnicę między wartością prawdziwą a przewidywaną.
plt.figure(figsize=(8, 5))  # Tworzymy figurę dla wykresu reszt.
plt.scatter(yr_pred, reszty, alpha=0.7)  # Na osi X odkładamy przewidywania, a na osi Y błędy modelu.
plt.axhline(y=0, linewidth=2)  # Dodajemy poziomą linię zero, aby łatwo ocenić rozkład błędów.
plt.xlabel("Wartości przewidywane")  # Opisujemy oś X.
plt.ylabel("Reszty")  # Opisujemy oś Y.
plt.title("Wykres reszt dla regresji liniowej")  # Ustawiamy tytuł wykresu.
plt.tight_layout()  # Dopasowujemy układ.
plt.show()  # Wyświetlamy wykres.

print("WIZUALIZACJE GOTOWE.")  # Informujemy użytkownika, że wszystkie trzy typy wizualizacji zostały utworzone.
print("Macierz pomyłek pokazuje rodzaje błędów klasyfikatora.")  # Wyjaśniamy praktyczny sens pierwszej wizualizacji.
print("Krzywa ROC pokazuje kompromis między czułością a odsetkiem fałszywych alarmów.")  # Wyjaśniamy praktyczny sens drugiej wizualizacji.
print("Wykres reszt pozwala sprawdzić, czy błędy regresji są losowe i czy model nie pomija jakiegoś wzorca.")  # Wyjaśniamy sens trzeciej wizualizacji.