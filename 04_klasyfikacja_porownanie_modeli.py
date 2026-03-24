# =====================================================================  # Nagłówek wskazuje, że porównamy różne podejścia do klasyfikacji.
# PRZYKŁAD 04: KLASYFIKACJA - PORÓWNANIE KNN, DRZEWA I REGRESJI LOGISTYCZNEJ  # Tytuł mówi, że celem jest porównanie klasyfikatorów.
# =====================================================================  # Linia zamyka górny blok informacyjny.

import pandas as pd  # Importujemy pandas, aby wygodnie pokazać porównanie wyników w tabeli.
from sklearn.datasets import load_iris  # Importujemy klasyczny zbiór Iris do klasyfikacji wieloklasowej.
from sklearn.linear_model import LogisticRegression  # Importujemy regresję logistyczną jako bazowy klasyfikator liniowy.
from sklearn.metrics import accuracy_score  # Importujemy accuracy, aby policzyć skuteczność modeli.
from sklearn.metrics import f1_score  # Importujemy F1-score do porównania jakości klasyfikacji wieloklasowej.
from sklearn.model_selection import train_test_split  # Importujemy funkcję do podziału danych na trening i test.
from sklearn.neighbors import KNeighborsClassifier  # Importujemy klasyfikator KNN oparty na podobieństwie sąsiadów.
from sklearn.pipeline import Pipeline  # Importujemy Pipeline, aby w jednym obiekcie połączyć skalowanie z modelem.
from sklearn.preprocessing import StandardScaler  # Importujemy standaryzację potrzebną szczególnie dla KNN.
from sklearn.tree import DecisionTreeClassifier  # Importujemy drzewo decyzyjne jako model oparty na regułach.

zbior = load_iris(as_frame=True)  # Wczytujemy zbiór Iris jako ramkę danych.
X = zbior.data  # Zmienna X zawiera cztery cechy opisujące kwiaty.
y = zbior.target  # Zmienna y przechowuje trzy klasy gatunków.

X_train, X_test, y_train, y_test = train_test_split(  # Dzielimy dane na część treningową i testową.
    X,  # Przekazujemy cechy wejściowe.
    y,  # Przekazujemy etykiety klas.
    test_size=0.25,  # Odkładamy 25% obserwacji na test.
    random_state=42,  # Ustawiamy ziarno losowe dla powtarzalności.
    stratify=y,  # Zachowujemy proporcje klas po obu stronach podziału.
)  # Zamykamy wywołanie funkcji train_test_split.

modele = {  # Tworzymy słownik, aby łatwo przejść po kilku klasyfikatorach.
    "Regresja logistyczna": Pipeline(steps=[  # Pierwszy model to pipeline z regresją logistyczną.
        ("skalowanie", StandardScaler()),  # Skalujemy cechy, bo model liniowy lepiej działa na danych o podobnej skali.
        ("model", LogisticRegression(max_iter=1000, random_state=42)),  # Dodajemy klasyfikator logistyczny.
    ]),  # Kończymy definicję pipeline dla regresji logistycznej.
    "KNN": Pipeline(steps=[  # Drugi model to K-nearest neighbors.
        ("skalowanie", StandardScaler()),  # Skalujemy cechy, bo KNN opiera się na odległościach.
        ("model", KNeighborsClassifier(n_neighbors=5)),  # Ustawiamy 5 najbliższych sąsiadów.
    ]),  # Kończymy definicję pipeline dla KNN.
    "Drzewo decyzyjne": DecisionTreeClassifier(max_depth=4, random_state=42),  # Trzeci model to drzewo o ograniczonej głębokości.
}  # Zamykamy słownik modeli.

wyniki = []  # Tworzymy pustą listę, do której będziemy odkładać podsumowania wyników każdego modelu.

for nazwa, model in modele.items():  # Iterujemy po parach: nazwa modelu oraz sam obiekt modelu.
    model.fit(X_train, y_train)  # Uczymy dany model na zbiorze treningowym.
    y_pred = model.predict(X_test)  # Obliczamy przewidywane klasy dla zbioru testowego.
    accuracy = accuracy_score(y_test, y_pred)  # Liczymy odsetek poprawnych klasyfikacji.
    f1 = f1_score(y_test, y_pred, average="macro")  # Liczymy średni F1-score po klasach, traktując wszystkie klasy równo.
    wyniki.append({  # Dodajemy wiersz z wynikami do listy.
        "model": nazwa,  # Zapisujemy nazwę modelu.
        "accuracy": round(accuracy, 3),  # Zapisujemy accuracy po zaokrągleniu.
        "f1_macro": round(f1, 3),  # Zapisujemy F1-score macro po zaokrągleniu.
    })  # Kończymy słownik reprezentujący jeden rekord wyników.

tabela_wynikow = pd.DataFrame(wyniki).sort_values(by="f1_macro", ascending=False)  # Budujemy tabelę i sortujemy modele od najlepszego.
print(tabela_wynikow)  # Wyświetlamy końcowe porównanie wyników.

print("\nWNIOSKI:")  # Dodajemy sekcję interpretacji.
print("1. Regresja logistyczna dobrze działa, gdy granice klas są względnie liniowe.")  # Opisujemy typowy przypadek użycia modelu liniowego.
print("2. KNN porównuje nowe obserwacje do podobnych przypadków z treningu.")  # Wyjaśniamy intuicję działania KNN.
print("3. Drzewo decyzyjne buduje reguły typu 'jeżeli... to...', dlatego jest łatwe do interpretacji.")  # Pokazujemy zaletę drzewa decyzyjnego.
print("4. Porównywanie kilku modeli na tych samych danych to dobra praktyka w klasyfikacji.")  # Podkreślamy znaczenie eksperymentowania.