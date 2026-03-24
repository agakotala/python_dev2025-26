# ================================================================  # Nagłówek ułatwia identyfikację celu tego pliku.
# PRZYKŁAD 03: REGRESJA LOGISTYCZNA W ZADANIU KLASYFIKACJI BINARNEJ   # Tytuł podkreśla, że regresja logistyczna służy do klasyfikacji.
# ================================================================  # Linia dekoracyjna domyka nagłówek.

import matplotlib.pyplot as plt  # Importujemy matplotlib do wizualizacji macierzy pomyłek.
from sklearn.datasets import load_breast_cancer  # Importujemy medyczny zbiór danych z dwiema klasami.
from sklearn.linear_model import LogisticRegression  # Importujemy model regresji logistycznej.
from sklearn.metrics import ConfusionMatrixDisplay  # Importujemy wygodne narzędzie do rysowania macierzy pomyłek.
from sklearn.metrics import accuracy_score  # Importujemy accuracy do obliczenia odsetka poprawnych klasyfikacji.
from sklearn.metrics import classification_report  # Importujemy raport zawierający precision, recall i F1-score.
from sklearn.metrics import roc_auc_score  # Importujemy ROC AUC do oceny jakości rankingu prawdopodobieństw.
from sklearn.model_selection import train_test_split  # Importujemy funkcję do podziału danych.
from sklearn.pipeline import Pipeline  # Importujemy Pipeline do połączenia skalowania z modelem.
from sklearn.preprocessing import StandardScaler  # Importujemy skalowanie, bo regresja logistyczna dobrze na nim korzysta.

zbior = load_breast_cancer()  # Wczytujemy zbiór z rozpoznawaniem zmian łagodnych i złośliwych.
X = zbior.data  # Cechy wejściowe opisują pomiary komórek.
y = zbior.target  # Zmienna docelowa przyjmuje dwie klasy: 0 lub 1.

X_train, X_test, y_train, y_test = train_test_split(  # Dzielimy dane na trening i test.
    X,  # Przekazujemy macierz cech.
    y,  # Przekazujemy etykiety klas.
    test_size=0.2,  # Rezerwujemy 20% danych na ocenę końcową.
    random_state=42,  # Zapewniamy odtwarzalność podziału.
    stratify=y,  # Zachowujemy proporcje klas w obu częściach zbioru.
)  # Zamykamy wywołanie funkcji train_test_split.

model = Pipeline(steps=[  # Budujemy pipeline, aby poprawnie połączyć przygotowanie danych z modelem.
    ("skalowanie", StandardScaler()),  # Standaryzujemy cechy, bo mają różne skale i zakresy.
    ("klasyfikator", LogisticRegression(max_iter=1000, random_state=42)),  # Tworzymy model logistyczny z większym limitem iteracji.
])  # Kończymy definicję pipeline.

model.fit(X_train, y_train)  # Uczymy pipeline tylko na danych treningowych.
y_pred = model.predict(X_test)  # Wyznaczamy przewidywane klasy dla zbioru testowego.
y_prob = model.predict_proba(X_test)[:, 1]  # Pobieramy prawdopodobieństwo klasy pozytywnej do metryki ROC AUC.

accuracy = accuracy_score(y_test, y_pred)  # Liczymy odsetek poprawnych decyzji klasyfikatora.
roc_auc = roc_auc_score(y_test, y_prob)  # Liczymy pole pod krzywą ROC dla przewidywanych prawdopodobieństw.

print("ACCURACY:", round(accuracy, 3))  # Wypisujemy accuracy zaokrąglone do trzech miejsc po przecinku.
print("ROC AUC:", round(roc_auc, 3))  # Wypisujemy ROC AUC, który jest odporniejszy na próg decyzyjny.

print("\nRAPORT KLASYFIKACJI:")  # Dodajemy nagłówek dla szczegółowego raportu jakości.
print(classification_report(y_test, y_pred, target_names=zbior.target_names))  # Pokazujemy precision, recall i F1-score dla obu klas.

disp = ConfusionMatrixDisplay.from_predictions(  # Tworzymy macierz pomyłek bez ręcznego liczenia komórek.
    y_test,  # Przekazujemy klasy rzeczywiste.
    y_pred,  # Przekazujemy klasy przewidziane przez model.
    display_labels=zbior.target_names,  # Etykietujemy osie nazwami klas, aby wykres był czytelny.
)  # Kończymy budowę wizualizacji.
disp.ax_.set_title("Macierz pomyłek - regresja logistyczna")  # Ustawiamy tytuł wykresu na osi narysowanej przez obiekt display.
plt.tight_layout()  # Dopasowujemy układ, aby napisy się nie ucinały.
plt.show()  # Wyświetlamy macierz pomyłek.

print("\nINTERPRETACJA:")  # Rozpoczynamy podsumowanie wniosków.
print("Regresja logistyczna zwraca prawdopodobieństwo przynależności do klasy.")  # Wyjaśniamy podstawową ideę modelu.
print("Po ustawieniu progu decyzyjnego, np. 0.5, prawdopodobieństwo zamieniane jest na etykietę klasy.")  # Tłumaczymy, jak z prawdopodobieństw powstaje decyzja.
print("Model jest prosty, szybki i dobrze interpretable, ale może gorzej działać przy mocno nieliniowych granicach decyzyjnych.")  # Pokazujemy mocne i słabe strony metody.