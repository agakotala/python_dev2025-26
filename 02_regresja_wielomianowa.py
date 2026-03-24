# ===============================================================  # Nagłówek oddziela przykład od innych materiałów.
# PRZYKŁAD 02: REGRESJA WIELOMIANOWA DLA ZALEŻNOŚCI NIELINIOWEJ      # Tytuł mówi, że modelujemy zależność zakrzywioną.
# ===============================================================  # Linia dekoracyjna poprawia czytelność.

import matplotlib.pyplot as plt  # Importujemy bibliotekę do tworzenia wykresów.
import numpy as np  # Importujemy NumPy do generowania danych i obliczeń numerycznych.
from sklearn.linear_model import LinearRegression  # Importujemy bazowy model regresji liniowej.
from sklearn.metrics import mean_squared_error  # Importujemy metrykę MSE do porównania jakości dopasowania.
from sklearn.model_selection import train_test_split  # Importujemy funkcję do podziału na trening i test.
from sklearn.pipeline import Pipeline  # Importujemy Pipeline, aby połączyć tworzenie cech i uczenie modelu.
from sklearn.preprocessing import PolynomialFeatures  # Importujemy generator cech wielomianowych.

generator = np.random.default_rng(seed=42)  # Tworzymy generator losowy z ustalonym ziarnem dla powtarzalności.
X = np.linspace(-3, 3, 120).reshape(-1, 1)  # Budujemy jednowymiarowe dane wejściowe równomiernie rozłożone na osi X.
szum = generator.normal(0, 1.5, size=120)  # Generujemy losowy szum, aby dane były bardziej realistyczne.
y = 2 * (X[:, 0] ** 2) + 3 * X[:, 0] + 4 + szum  # Definiujemy prawdziwą zależność kwadratową i dodajemy zakłócenia.

X_train, X_test, y_train, y_test = train_test_split(  # Dzielimy dane na część treningową i testową.
    X,  # Przekazujemy dane wejściowe.
    y,  # Przekazujemy wartości docelowe.
    test_size=0.25,  # Rezerwujemy 25% próbek na ocenę końcową.
    random_state=42,  # Ustawiamy stałe ziarno dla odtwarzalności eksperymentu.
)  # Zamykamy podział danych.

model_liniowy = LinearRegression()  # Tworzymy zwykły model liniowy do porównania z podejściem wielomianowym.
model_liniowy.fit(X_train, y_train)  # Uczymy model liniowy na danych treningowych.
y_pred_liniowy = model_liniowy.predict(X_test)  # Obliczamy przewidywania zwykłego modelu liniowego.

model_wielomianowy = Pipeline(steps=[  # Budujemy pipeline, aby cały proces był uporządkowany i bezpieczny.
    ("cechy_wielomianowe", PolynomialFeatures(degree=2, include_bias=False)),  # Rozszerzamy wejście o x oraz x^2.
    ("regresja", LinearRegression()),  # Na nowych cechach uczymy klasyczny model liniowy.
])  # Kończymy definicję pipeline.

model_wielomianowy.fit(X_train, y_train)  # Uczymy model wielomianowy na danych treningowych.
y_pred_wielomianowy = model_wielomianowy.predict(X_test)  # Obliczamy przewidywania modelu wielomianowego na teście.

mse_liniowy = mean_squared_error(y_test, y_pred_liniowy)  # Liczymy błąd MSE dla prostego modelu liniowego.
mse_wielomianowy = mean_squared_error(y_test, y_pred_wielomianowy)  # Liczymy błąd MSE dla modelu z cechami wielomianowymi.

print("MSE modelu liniowego:", round(mse_liniowy, 3))  # Pokazujemy błąd modelu liniowego, aby mieć punkt odniesienia.
print("MSE modelu wielomianowego:", round(mse_wielomianowy, 3))  # Pokazujemy błąd modelu wielomianowego.

siatka = np.linspace(X.min(), X.max(), 300).reshape(-1, 1)  # Tworzymy gęstą siatkę punktów do narysowania gładkich krzywych.
pred_siatka_liniowa = model_liniowy.predict(siatka)  # Obliczamy wartości modelu liniowego na siatce punktów.
pred_siatka_wielomianowa = model_wielomianowy.predict(siatka)  # Obliczamy wartości modelu wielomianowego na siatce punktów.

plt.figure(figsize=(9, 6))  # Tworzymy figurę o wystarczająco dużym rozmiarze.
plt.scatter(X[:, 0], y, alpha=0.5, label="Dane obserwowane")  # Rysujemy punkty danych jako tło całego przykładu.
plt.plot(siatka[:, 0], pred_siatka_liniowa, linewidth=2, label="Regresja liniowa")  # Rysujemy prostą dopasowaną przez model liniowy.
plt.plot(siatka[:, 0], pred_siatka_wielomianowa, linewidth=2, label="Regresja wielomianowa stopnia 2")  # Rysujemy krzywą modelu wielomianowego.
plt.xlabel("Zmienna X")  # Opisujemy oś poziomą.
plt.ylabel("Zmienna y")  # Opisujemy oś pionową.
plt.title("Porównanie regresji liniowej i wielomianowej")  # Dodajemy tytuł całego wykresu.
plt.legend()  # Włączamy legendę, aby rozróżnić obie linie.
plt.tight_layout()  # Dopasowujemy układ wykresu do okna.
plt.show()  # Wyświetlamy gotową wizualizację.

print("\nWNIOSKI:")  # Rozpoczynamy sekcję interpretacji wyników.
print("Regresja liniowa próbuje dopasować prostą, dlatego słabiej opisuje krzywą zależność.")  # Tłumaczymy ograniczenie modelu liniowego.
print("Regresja wielomianowa tworzy dodatkowe cechy, np. x^2, dzięki czemu lepiej modeluje zakrzywienie.")  # Wyjaśniamy mechanizm poprawy dopasowania.
print("Zbyt wysoki stopień wielomianu może jednak prowadzić do przeuczenia.")  # Ostrzegamy przed nadmierną złożonością modelu.