# ================================================================  # Linia ozdobna oddzielająca nagłówek programu od reszty kodu.
# PRZYKŁAD 06: SZTUCZNA SIEĆ NEURONOWA MLP W ZADANIU KLASYFIKACJI    # Tytuł informuje, że budujemy model MLP do rozpoznawania klas.
# ================================================================  # Zamknięcie sekcji nagłówkowej dla lepszej czytelności skryptu.

import matplotlib.pyplot as plt  # Import biblioteki do tworzenia wykresów; tutaj posłuży do pokazania obrazów cyfr i przebiegu straty.
from sklearn.datasets import load_digits  # Import gotowego zbioru danych z cyframi od 0 do 9 dostępnego w scikit-learn.
from sklearn.metrics import accuracy_score  # Import miary accuracy, czyli odsetka poprawnie sklasyfikowanych przykładów.
from sklearn.metrics import classification_report  # Import funkcji generującej raport precision/recall/F1 dla każdej klasy.
from sklearn.model_selection import train_test_split  # Import funkcji do podziału danych na część treningową i testową.
from sklearn.neural_network import MLPClassifier  # Import klasy wielowarstwowej sieci neuronowej MLP do klasyfikacji.
from sklearn.pipeline import Pipeline  # Import Pipeline, aby połączyć kilka kroków przetwarzania w jeden spójny model.
from sklearn.preprocessing import StandardScaler  # Import skalowania cech; sieci neuronowe zwykle działają lepiej na danych przeskalowanych.

zbior = load_digits()  # Wczytujemy zbiór digits; zawiera obrazy cyfr, ich etykiety i dodatkowe informacje opisowe.
X = zbior.data  # Pobieramy cechy wejściowe; każdy obraz 8x8 został spłaszczony do wektora 64 liczb.
y = zbior.target  # Pobieramy etykiety klas; każda etykieta mówi, jaką cyfrę przedstawia dany obrazek.

print("Kształt X:", X.shape)  # Wyświetlamy rozmiar macierzy cech, aby sprawdzić liczbę próbek i liczbę cech.
print("Kształt y:", y.shape)  # Wyświetlamy rozmiar wektora etykiet, żeby potwierdzić, że liczba etykiet zgadza się z liczbą próbek.
print("Pierwszy rekord X:", X[0])  # Pokazujemy pierwszy przykład w wersji spłaszczonej, czyli 64 wartości pikseli w jednym wierszu.
print("Pierwsza etykieta y:", y[0])  # Sprawdzamy, jaka cyfra odpowiada pierwszemu rekordowi.
print("Dostępne klasy:", set(y))  # Pokazujemy zbiór wszystkich klas obecnych w danych; tu powinny być cyfry 0–9.
print("Obraz 8x8:")  # Wypisujemy nagłówek przed pokazaniem pierwszego obrazu w postaci macierzy.
print(zbior.images[0])  # Pokazujemy pierwszy obraz w naturalnym układzie 8x8, aby łatwiej zrozumieć strukturę danych.

print("Etykieta:", y[0])  # Dla pierwszego obrazu wypisujemy jego prawdziwą klasę, aby porównać obraz z etykietą.
import matplotlib.pyplot as plt  # Ten import jest powtórzony; kod zadziała, ale ta linia nie jest już potrzebna, bo biblioteka została zaimportowana wcześniej.

plt.imshow(zbior.images[0], cmap="gray")  # Wyświetlamy pierwszy obraz jako obraz w odcieniach szarości, żeby zobaczyć cyfrę wizualnie.
plt.title(f"Etykieta: {y[0]}")  # Dodajemy tytuł wykresu z prawdziwą etykietą obrazu.
plt.axis("off")  # Ukrywamy osie, bo przy małym obrazku 8x8 nie wnoszą nic przydatnego.
plt.show()  # Wyświetlamy wykres z pierwszym obrazem.

fig, axes = plt.subplots(2, 5, figsize=(10, 5))  # Tworzymy siatkę 2x5, aby pokazać 10 pierwszych obrazów obok siebie.

for i, ax in enumerate(axes.ravel()):  # Iterujemy po wszystkich osiach wykresu; ravel spłaszcza siatkę 2x5 do jednej listy 10 pól.
    ax.imshow(zbior.images[i], cmap="gray")  # W każdej komórce siatki wyświetlamy kolejny obraz cyfry.
    ax.set_title(f"Label: {y[i]}")  # Nad każdym obrazkiem ustawiamy tytuł z jego etykietą.
    ax.axis("off")  # Ukrywamy osie dla estetyki i czytelności miniaturowych obrazków.

plt.tight_layout()  # Automatycznie dopasowujemy odstępy między wykresami, aby tytuły i obrazki się nie nakładały.
plt.show()  # Wyświetlamy całą siatkę 10 przykładowych cyfr.

X_train, X_test, y_train, y_test = train_test_split(  # Dzielimy dane na zbiór treningowy i testowy, by uczciwie ocenić model na nieznanych danych.
    X,  # Przekazujemy wszystkie cechy wejściowe jako dane do podziału.
    y,  # Przekazujemy odpowiadające im etykiety klas.
    test_size=0.2,  # Ustalamy, że 20% danych trafi do testu, a 80% zostanie użyte do uczenia modelu.
    random_state=42,  # Ustawiamy ziarno losowe, aby przy każdym uruchomieniu otrzymać ten sam podział danych.
    stratify=y,  # Wymuszamy zachowanie proporcji klas w train i test, co jest ważne przy klasyfikacji wieloklasowej.
)  # Kończymy wywołanie funkcji dzielącej dane.

model = Pipeline(steps=[  # Tworzymy pipeline, czyli sekwencję kroków wykonywanych zawsze w tej samej kolejności.
    ("skalowanie", StandardScaler()),  # Najpierw standaryzujemy cechy, bo MLP jest wrażliwe na skalę danych wejściowych.
    ("mlp", MLPClassifier(  # Następnie definiujemy właściwy model sieci neuronowej MLP.
        hidden_layer_sizes=(64, 32),  # Ustawiamy dwie warstwy ukryte: pierwsza ma 64 neurony, druga 32; model może uczyć się bardziej złożonych zależności.
        activation="relu",  # Wybieramy funkcję aktywacji ReLU, bo dobrze działa w wielu nowoczesnych sieciach i jest obliczeniowo prosta.
        solver="adam",  # Używamy optymalizatora Adam, który zwykle daje dobre wyniki bez bardzo skomplikowanego strojenia.
        alpha=0.0005,  # Dodajemy lekką regularyzację L2, aby ograniczyć ryzyko przeuczenia modelu.
        max_iter=300,  # Pozwalamy modelowi uczyć się maksymalnie przez 300 iteracji, aby miał czas na zbieżność.
        random_state=42,  # Ustawiamy ziarno losowe, by wyniki uczenia były powtarzalne.
    )),  # Zamykamy definicję klasyfikatora MLP jako drugiego kroku pipeline.
])  # Zamykamy definicję całego pipeline.

model.fit(X_train, y_train)  # Uczymy pipeline na danych treningowych; scaler liczy parametry na train, a potem MLP uczy się klasyfikacji.
y_pred = model.predict(X_test)  # Generujemy przewidywania dla danych testowych, których model nie widział podczas uczenia.

accuracy = accuracy_score(y_test, y_pred)  # Obliczamy accuracy, czyli jaki procent przykładów testowych został sklasyfikowany poprawnie.
print("ACCURACY:", round(accuracy, 3))  # Wyświetlamy accuracy zaokrąglone do 3 miejsc po przecinku dla czytelności.

print("\nRAPORT KLASYFIKACJI:")  # Wypisujemy nagłówek sekcji z bardziej szczegółową oceną modelu.
print(classification_report(y_test, y_pred))  # Pokazujemy precision, recall i F1-score osobno dla każdej cyfry, co daje pełniejszy obraz jakości.

krzywa_straty = model.named_steps["mlp"].loss_curve_  # Pobieramy historię wartości funkcji straty z kolejnych iteracji treningu samej sieci MLP.
plt.figure(figsize=(8, 5))  # Tworzymy nową figurę o zadanym rozmiarze pod wykres procesu uczenia.
plt.plot(krzywa_straty)  # Rysujemy zmianę straty w kolejnych iteracjach; zwykle chcemy widzieć trend malejący.
plt.xlabel("Iteracja")  # Opisujemy oś X jako numer iteracji uczenia.
plt.ylabel("Loss")  # Opisujemy oś Y jako wartość funkcji straty, czyli miary błędu modelu podczas nauki.
plt.title("Przebieg uczenia sieci neuronowej MLP")  # Dodajemy tytuł wykresu, aby było jasne, co przedstawia.
plt.tight_layout()  # Dopasowujemy marginesy i rozmieszczenie elementów wykresu.
plt.show()  # Wyświetlamy wykres przebiegu straty.

print("\nINTERPRETACJA:")  # Zaczynamy sekcję tekstowego podsumowania działania modelu.
print("Sieć neuronowa uczy się złożonych, nieliniowych zależności między wejściem a wyjściem.")  # Wyjaśniamy, że MLP potrafi modelować zależności trudniejsze niż modele liniowe.
print("Warstwy ukryte stopniowo budują coraz bardziej abstrakcyjne reprezentacje danych.")  # Tłumaczymy sens warstw ukrytych: uczą się cech pośrednich przydatnych do klasyfikacji.
print("W praktyce sieci zwykle wymagają skalowania danych, strojenia parametrów i kontroli przeuczenia.")  # Dodajemy ważną uwagę praktyczną o wymaganiach pracy z sieciami neuronowymi.