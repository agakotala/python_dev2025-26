# ================================================================  # Sekcja nagłówkowa informuje, że poniżej znajduje się kompletny przykład.
# PRZYKŁAD 00: PRZYGOTOWANIE DANYCH DO MODELU UCZENIA MASZYNOWEGO   # Tytuł skryptu mówi jasno, czego dotyczy przykład.
# ================================================================  # Ozdobna linia zamyka nagłówek i ułatwia szybkie skanowanie pliku.

import numpy as np  # Importujemy bibliotekę NumPy do generowania liczb losowych i pracy z wartościami numerycznymi.
import pandas as pd  # Importujemy bibliotekę pandas do tworzenia i przekształcania danych tabelarycznych.
from sklearn.compose import ColumnTransformer  # Importujemy narzędzie do różnego przetwarzania kolumn liczbowych i kategorycznych.
from sklearn.impute import SimpleImputer  # Importujemy klasę do uzupełniania brakujących wartości.
from sklearn.model_selection import train_test_split  # Importujemy funkcję do podziału danych na zbiór treningowy i testowy.
from sklearn.pipeline import Pipeline  # Importujemy Pipeline, aby połączyć kroki przygotowania danych w jedną sekwencję.
from sklearn.preprocessing import OneHotEncoder  # Importujemy kodowanie One-Hot dla cech tekstowych i kategorycznych.
from sklearn.preprocessing import StandardScaler  # Importujemy standaryzację, aby skala cech liczbowych była porównywalna.

generator = np.random.default_rng(seed=42)  # Tworzymy generator liczb losowych z ustalonym ziarnem, aby wyniki były odtwarzalne.

dane = pd.DataFrame({  # Tworzymy przykładową ramkę danych, która przypomina prosty zbiór biznesowy.
    "wiek": generator.integers(18, 65, size=20),  # Losujemy wiek klientów z zakresu od 18 do 64 lat.
    "dochód": generator.normal(loc=6500, scale=1500, size=20).round(0),  # Losujemy miesięczny dochód w złotówkach.
    "miasto": generator.choice(["Warszawa", "Kraków", "Gdańsk"], size=20),  # Losujemy kategorię opisującą miasto klienta.
    "zakup": generator.choice([0, 1], size=20, p=[0.45, 0.55]),  # Tworzymy zmienną docelową informującą, czy klient kupił produkt.
})  # Zamykamy definicję słownika przekazanego do DataFrame.

dane.loc[[1, 5, 12], "dochód"] = np.nan  # Celowo wstawiamy braki w kolumnie dochód, aby pokazać ich obsługę.
dane.loc[[3, 9], "miasto"] = np.nan  # Celowo wstawiamy braki również w kolumnie kategorycznej.
dane.loc[7, "wiek"] = np.nan  # Dodajemy brak w kolumnie liczbowej, aby zobaczyć imputację medianą.

print("\nPIERWSZE WIERSZE DANYCH:")  # Wypisujemy nagłówek, aby wynik w konsoli był czytelny.
print(dane.head())  # Pokazujemy pierwsze pięć rekordów, żeby szybko ocenić strukturę tabeli.

print("\nPODSTAWOWE INFORMACJE O DANYCH:")  # Dodajemy kolejny nagłówek opisujący następny krok eksploracji.
print(dane.info())  # Wyświetlamy typy kolumn i liczbę braków, ponieważ to ważny etap przygotowania danych.

print("\nLICZBA BRAKÓW W KAŻDEJ KOLUMNIE:")  # Informujemy, że za chwilę pokażemy statystykę braków.
print(dane.isna().sum())  # Zliczamy brakujące wartości w każdej kolumnie, aby wiedzieć, co trzeba uzupełnić.

X = dane.drop("zakup", axis=1)  # Tworzymy macierz cech wejściowych, usuwając kolumnę docelową zakup.
y = dane["zakup"]  # Zmienna y przechowuje etykietę klasy, którą model będzie przewidywał.

kolumny_liczbowe = ["wiek", "dochód"]  # Definiujemy listę kolumn liczbowych wymagających imputacji i skalowania.
kolumny_kategoryczne = ["miasto"]  # Definiujemy listę kolumn tekstowych, które trzeba zakodować do postaci numerycznej.

transformer_liczbowy = Pipeline(steps=[  # Budujemy mini-pipeline dla danych liczbowych.
    ("imputer", SimpleImputer(strategy="median")),  # Braki liczbowe uzupełniamy medianą, bo jest odporna na wartości odstające.
    ("scaler", StandardScaler()),  # Następnie standaryzujemy kolumny, aby miały średnią 0 i odchylenie standardowe 1.
])  # Kończymy definicję sekwencji kroków dla kolumn liczbowych.

transformer_kategoryczny = Pipeline(steps=[  # Budujemy osobny pipeline dla kolumn kategorycznych.
    ("imputer", SimpleImputer(strategy="most_frequent")),  # Braki tekstowe uzupełniamy najczęstszą kategorią.
    ("onehot", OneHotEncoder(handle_unknown="ignore")),  # Kategorie zamieniamy na wektory binarne metodą One-Hot.
])  # Kończymy definicję sekwencji kroków dla kolumn kategorycznych.

preprocessor = ColumnTransformer(transformers=[  # Łączymy oba typy przetwarzania w jeden obiekt.
    ("num", transformer_liczbowy, kolumny_liczbowe),  # Dla kolumn liczbowych używamy przygotowanego transformera liczbowego.
    ("cat", transformer_kategoryczny, kolumny_kategoryczne),  # Dla kolumn tekstowych używamy transformera kategorycznego.
])  # Zamykamy konfigurację ColumnTransformer.

X_train, X_test, y_train, y_test = train_test_split(  # Dzielimy dane na część treningową i testową.
    X,  # Przekazujemy cechy wejściowe.
    y,  # Przekazujemy zmienną docelową.
    test_size=0.25,  # Ustalamy, że 25% obserwacji trafi do zbioru testowego.
    random_state=42,  # Ustawiamy ziarno, aby podział zawsze wyglądał tak samo.
    stratify=y,  # Zachowujemy proporcje klas, żeby trening i test były porównywalne.
)  # Zamykamy wywołanie funkcji podziału danych.

print("\nROZMIAR ZBIORU TRENINGOWEGO:", X_train.shape)  # Pokazujemy rozmiar części treningowej, aby sprawdzić wynik podziału.
print("ROZMIAR ZBIORU TESTOWEGO:", X_test.shape)  # Pokazujemy rozmiar części testowej.

preprocessor.fit(X_train)  # Uczymy obiekt przygotowania danych wyłącznie na zbiorze treningowym, aby uniknąć wycieku danych.
X_train_przygotowane = preprocessor.transform(X_train)  # Przekształcamy dane treningowe zgodnie z nauczonymi regułami.
X_test_przygotowane = preprocessor.transform(X_test)  # Tak samo transformujemy dane testowe, ale bez ponownego uczenia.

print("\nKSZTAŁT DANYCH PO PRZETWORZENIU - TRENING:", X_train_przygotowane.shape)  # Sprawdzamy liczbę kolumn po kodowaniu One-Hot.
print("KSZTAŁT DANYCH PO PRZETWORZENIU - TEST:", X_test_przygotowane.shape)  # Weryfikujemy zgodność struktury zbioru testowego.

nazwy_kolumn_po_transformacji = preprocessor.get_feature_names_out()  # Pobieramy nazwy nowych kolumn po pełnym przekształceniu.
print("\nNAZWY KOLUMN PO TRANSFORMACJI:")  # Dodajemy czytelny nagłówek dla listy cech.
print(nazwy_kolumn_po_transformacji)  # Wypisujemy nazwy cech, żeby zrozumieć efekt One-Hot Encoding.

print("\nPIERWSZY REKORD PO PRZYGOTOWANIU DANYCH:")  # Informujemy, że pokażemy pojedynczy wiersz po transformacji.
print(X_train_przygotowane[0])  # Pokazujemy pierwszy rekord po imputacji, skalowaniu i kodowaniu.

print("\nWNIOSKI:")  # Rozpoczynamy krótkie podsumowanie procesu przygotowania danych.
print("1. Braki zostały uzupełnione różnymi strategiami dla różnych typów kolumn.")  # Podkreślamy znaczenie osobnej obsługi liczb i kategorii.
print("2. Kategorie tekstowe zostały zamienione na cechy numeryczne metodą One-Hot.")  # Wyjaśniamy, dlaczego model może teraz użyć kolumny miasto.
print("3. Dane liczbowe zostały wystandaryzowane, co ułatwia pracę wielu modelom.")  # Zwracamy uwagę na sens skalowania.
print("4. Wszystkie kroki wykonano po podziale danych, aby uniknąć data leakage.")  # Przypominamy o krytycznej zasadzie poprawnego workflow.