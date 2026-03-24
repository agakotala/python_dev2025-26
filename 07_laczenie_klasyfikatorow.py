# =====================================================================  # Nagłówek informuje, że przykład dotyczy ensemble learning.
# PRZYKŁAD 07: ŁĄCZENIE KLASYFIKATORÓW - VOTING, RANDOM FOREST, ADABOOST  # Tytuł pokazuje trzy popularne podejścia zespołowe.
# =====================================================================  # Linia dekoracyjna zamyka blok tytułowy.

import pandas as pd  # Importujemy pandas do prezentacji wyników w zwartej tabeli.
from sklearn.datasets import load_breast_cancer  # Importujemy zbiór danych do klasyfikacji binarnej.
from sklearn.ensemble import AdaBoostClassifier  # Importujemy AdaBoost, który wzmacnia słabsze klasyfikatory.
from sklearn.ensemble import RandomForestClassifier  # Importujemy las losowy, czyli zespół wielu drzew.
from sklearn.ensemble import VotingClassifier  # Importujemy klasyfikator głosujący, który łączy różne modele.
from sklearn.linear_model import LogisticRegression  # Importujemy regresję logistyczną jako jeden z bazowych modeli.
from sklearn.metrics import accuracy_score  # Importujemy accuracy do porównania modeli.
from sklearn.metrics import f1_score  # Importujemy F1-score do oceny balansu precision i recall.
from sklearn.model_selection import train_test_split  # Importujemy funkcję do podziału danych.
from sklearn.neighbors import KNeighborsClassifier  # Importujemy KNN jako drugi model bazowy.
from sklearn.pipeline import Pipeline  # Importujemy Pipeline do łączenia skalowania z modelami.
from sklearn.preprocessing import StandardScaler  # Importujemy standaryzację potrzebną np. dla KNN i regresji logistycznej.
from sklearn.tree import DecisionTreeClassifier  # Importujemy drzewo jako bazowy model do AdaBoost.

zbior = load_breast_cancer()  # Wczytujemy zbiór danych do rozpoznawania dwóch klas.
X = zbior.data  # Cechy wejściowe opisują obserwacje.
y = zbior.target  # Etykieta klasy informuje, do której grupy należy obiekt.

X_train, X_test, y_train, y_test = train_test_split(  # Dzielimy dane na część treningową i testową.
    X,  # Przekazujemy cechy wejściowe.
    y,  # Przekazujemy etykiety klas.
    test_size=0.2,  # Ustalamy udział zbioru testowego.
    random_state=42,  # Zapewniamy powtarzalność eksperymentu.
    stratify=y,  # Zachowujemy proporcje klas.
)  # Kończymy podział danych.

log_reg = Pipeline(steps=[  # Tworzymy pierwszy model bazowy: regresję logistyczną.
    ("skalowanie", StandardScaler()),  # Skalujemy cechy przed modelem liniowym.
    ("model", LogisticRegression(max_iter=1000, random_state=42)),  # Dodajemy sam klasyfikator logistyczny.
])  # Kończymy pipeline dla regresji logistycznej.

knn = Pipeline(steps=[  # Tworzymy drugi model bazowy: KNN.
    ("skalowanie", StandardScaler()),  # Skalujemy cechy, bo KNN używa odległości.
    ("model", KNeighborsClassifier(n_neighbors=7)),  # Ustawiamy liczbę sąsiadów równą 7.
])  # Kończymy pipeline dla KNN.

random_forest = RandomForestClassifier(  # Tworzymy las losowy, czyli zespół wielu drzew decyzyjnych.
    n_estimators=200,  # Ustawiamy liczbę drzew w lesie.
    max_depth=5,  # Ograniczamy maksymalną głębokość, aby zmniejszyć ryzyko przeuczenia.
    random_state=42,  # Ustawiamy ziarno losowe.
)  # Kończymy konfigurację lasu losowego.

adaboost = AdaBoostClassifier(  # Tworzymy model AdaBoost oparty na słabszych klasyfikatorach.
    estimator=DecisionTreeClassifier(max_depth=1, random_state=42),  # Używamy płytkiego drzewa jako bazowego ucznia.
    n_estimators=100,  # Ustalamy liczbę kolejnych klasyfikatorów wzmacnianych przez AdaBoost.
    random_state=42,  # Zapewniamy powtarzalność treningu.
)  # Kończymy konfigurację AdaBoost.

voting = VotingClassifier(  # Tworzymy klasyfikator głosujący, który łączy kilka różnych modeli.
    estimators=[  # Podajemy listę modeli, które będą głosować.
        ("log_reg", log_reg),  # Dodajemy regresję logistyczną jako pierwszy głos.
        ("knn", knn),  # Dodajemy KNN jako drugi głos.
        ("rf", random_forest),  # Dodajemy las losowy jako trzeci głos.
    ],  # Kończymy listę estymatorów.
    voting="soft",  # Wybieramy głosowanie miękkie, czyli średnią z prawdopodobieństw klas.
)  # Kończymy konfigurację modelu VotingClassifier.

modele = {  # Tworzymy słownik wszystkich modeli, które chcemy porównać.
    "Regresja logistyczna": log_reg,  # Dodajemy pierwszy model bazowy.
    "KNN": knn,  # Dodajemy drugi model bazowy.
    "Random Forest": random_forest,  # Dodajemy model zespołowy baggingowy.
    "AdaBoost": adaboost,  # Dodajemy model zespołowy boostingowy.
    "VotingClassifier": voting,  # Dodajemy model łączący kilka klasyfikatorów.
}  # Zamykamy słownik modeli.

wyniki = []  # Tworzymy pustą listę na rekordy wyników.

for nazwa, model in modele.items():  # Iterujemy po wszystkich modelach, aby użyć identycznej procedury oceny.
    model.fit(X_train, y_train)  # Uczymy dany model na zbiorze treningowym.
    y_pred = model.predict(X_test)  # Generujemy klasy przewidywane dla zbioru testowego.
    accuracy = accuracy_score(y_test, y_pred)  # Liczymy accuracy dla danego modelu.
    f1 = f1_score(y_test, y_pred)  # Liczymy F1-score dla klasyfikacji binarnej.
    wyniki.append({  # Odkładamy wynik modelu do listy.
        "model": nazwa,  # Zapisujemy nazwę modelu.
        "accuracy": round(accuracy, 3),  # Zapisujemy accuracy po zaokrągleniu.
        "f1": round(f1, 3),  # Zapisujemy F1-score po zaokrągleniu.
    })  # Kończymy słownik wyniku.

tabela = pd.DataFrame(wyniki).sort_values(by="f1", ascending=False)  # Tworzymy tabelę wyników i sortujemy malejąco po F1.
print(tabela)  # Wyświetlamy uporządkowane porównanie modeli.

print("\nINTERPRETACJA:")  # Rozpoczynamy sekcję wniosków.
print("Modele zespołowe często działają lepiej niż pojedynczy klasyfikator, bo łączą różne perspektywy patrzenia na dane.")  # Wyjaśniamy sens ensemble learning.
print("Random Forest redukuje wariancję dzięki wielu drzewom uczonym na losowych podzbiorach cech i danych.")  # Tłumaczymy intuicję lasu losowego.
print("AdaBoost wzmacnia trudne przypadki, skupiając się na obserwacjach błędnie sklasyfikowanych wcześniej.")  # Wyjaśniamy mechanikę boostingu.
print("VotingClassifier łączy kilka modeli i podejmuje decyzję zbiorową, co bywa bardziej stabilne niż decyzja pojedynczego modelu.")  # Podsumowujemy ideę głosowania.