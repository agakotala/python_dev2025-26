# ===========================================================  # Sekcja nagłówkowa pomaga szybko zidentyfikować temat ćwiczenia.
# PRZYKŁAD 01: REGRESJA LINIOWA NA DANYCH DIABETES              # Tytuł informuje, że będziemy przewidywać wartość ciągłą.
# ===========================================================  # Ozdobna linia kończy nagłówek pliku.

import matplotlib.pyplot as plt  # Importujemy matplotlib do narysowania wykresu porównującego wartości rzeczywiste i przewidywane.
import pandas as pd  # Importujemy pandas do wygodnego tworzenia tabeli z wynikami.
from sklearn.datasets import load_diabetes  # Importujemy gotowy zbiór danych regresyjnych z biblioteki scikit-learn.
import numpy as np  # Importujemy NumPy, aby policzyć pierwiastek z błędu średniokwadratowego.
from sklearn.linear_model import LinearRegression  # Importujemy klasyczny model regresji liniowej.
from sklearn.metrics import mean_absolute_error  # Importujemy średni błąd bezwzględny do oceny jakości przewidywań.
from sklearn.metrics import mean_squared_error  # Importujemy średni błąd kwadratowy do oceny dużych odchyleń.
from sklearn.metrics import r2_score  # Importujemy metrykę R^2 pokazującą, ile wariancji wyjaśnia model.
from sklearn.model_selection import train_test_split  # Importujemy funkcję do podziału danych na trening i test.

zbior = load_diabetes(as_frame=True)  # Wczytujemy zbiór diabetes w formie gotowej ramki danych pandas.
X = zbior.data  # Do zmiennej X zapisujemy cechy wejściowe opisujące pacjentów.
y = zbior.target  # Do zmiennej y zapisujemy wartość docelową, którą model ma przewidywać.

print("KSZTAŁT CECH:", X.shape)  # Wypisujemy liczbę wierszy i kolumn cech, aby znać rozmiar zbioru.
print("KSZTAŁT CELU:", y.shape)  # Wypisujemy liczbę obserwacji w zmiennej docelowej.

X_train, X_test, y_train, y_test = train_test_split(  # Rozdzielamy dane na część do nauki i część do końcowej oceny.
    X,  # Przekazujemy cechy wejściowe.
    y,  # Przekazujemy wartości docelowe.
    test_size=0.2,  # Rezerwujemy 20% obserwacji na zbiór testowy.
    random_state=42,  # Ustawiamy ziarno, aby podział był odtwarzalny.
)  # Zamykamy wywołanie funkcji train_test_split.

model = LinearRegression()  # Tworzymy obiekt modelu regresji liniowej z domyślnymi parametrami.
model.fit(X_train, y_train)  # Uczymy model zależności pomiędzy cechami a wartością docelową na danych treningowych.

y_pred = model.predict(X_test)  # Obliczamy przewidywania modelu dla niewidzianego wcześniej zbioru testowego.

mae = mean_absolute_error(y_test, y_pred)  # Liczymy przeciętny błąd bezwzględny wyrażony w jednostkach zmiennej celu.
mse = mean_squared_error(y_test, y_pred)  # Liczymy średni błąd kwadratowy, który mocniej karze duże pomyłki.
rmse = np.sqrt(mse)  # Wyznaczamy pierwiastek z MSE ręcznie, aby wrócić do oryginalnej skali celu.
r2 = r2_score(y_test, y_pred)  # Sprawdzamy, jaką część zmienności danych wyjaśnia model.

print("\nWSPÓŁCZYNNIKI MODELU:")  # Dodajemy nagłówek dla współczynników regresji.
wspolczynniki = pd.Series(model.coef_, index=X.columns)  # Budujemy serię pandas łączącą nazwy cech z wagami modelu.
print(wspolczynniki.sort_values(ascending=False))  # Sortujemy współczynniki malejąco, aby łatwiej znaleźć najsilniejsze wpływy.

print("\nWYRAZ WOLNY MODELU:", model.intercept_)  # Pokazujemy wyraz wolny, czyli przewidywanie bazowe bez wpływu cech.

print("\nMETRYKI OCENY:")  # Dodajemy nagłówek dla podsumowania jakości modelu.
print("MAE:", round(mae, 3))  # Wypisujemy średni błąd bezwzględny zaokrąglony do trzech miejsc.
print("MSE:", round(mse, 3))  # Wypisujemy średni błąd kwadratowy.
print("RMSE:", round(rmse, 3))  # Wypisujemy RMSE, który jest łatwiejszy do interpretacji niż MSE.
print("R^2:", round(r2, 3))  # Wypisujemy współczynnik determinacji.

wyniki = pd.DataFrame({  # Tworzymy tabelę porównującą wartości rzeczywiste i przewidywane.
    "rzeczywiste": y_test.values,  # Do pierwszej kolumny wpisujemy prawdziwe wartości ze zbioru testowego.
    "przewidywane": y_pred,  # Do drugiej kolumny wpisujemy prognozy modelu.
})  # Zamykamy definicję ramki danych z wynikami.

wyniki["blad"] = wyniki["rzeczywiste"] - wyniki["przewidywane"]  # Dodajemy kolumnę z błędem, aby zobaczyć kierunek odchyleń.
print("\nPIERWSZE 10 REKORDÓW WYNIKÓW:")  # Informujemy, że za chwilę pokażemy przykładowe wyniki.
print(wyniki.head(10))  # Wyświetlamy pierwsze dziesięć rekordów porównania.

plt.figure(figsize=(8, 6))  # Tworzymy obszar rysunku o czytelnym rozmiarze.
plt.scatter(y_test, y_pred, alpha=0.7)  # Rysujemy wykres punktowy: oś X to wartości rzeczywiste, oś Y to przewidywania.
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()])  # Dodajemy linię idealnego dopasowania y = x.
plt.xlabel("Wartości rzeczywiste")  # Opisujemy oś poziomą, aby było jasne, co przedstawia.
plt.ylabel("Wartości przewidywane")  # Opisujemy oś pionową.
plt.title("Regresja liniowa: rzeczywiste vs przewidywane")  # Ustawiamy tytuł wykresu.
plt.tight_layout()  # Dopasowujemy marginesy, aby elementy wykresu się nie nachodziły.
plt.show()  # Wyświetlamy wykres na ekranie.

print("\nINTERPRETACJA:")  # Rozpoczynamy sekcję interpretacji wyników.
print("Im bliżej punktów do linii przekątnej, tym lepsze przewidywania modelu.")  # Wyjaśniamy sens wykresu punktowego.
print("Regresja liniowa zakłada liniową zależność pomiędzy cechami a celem.")  # Przypominamy podstawowe założenie modelu.
print("Jeżeli zależność nie jest liniowa, warto rozważyć cechy wielomianowe lub inny model.")  # Wskazujemy naturalny kolejny krok analizy.