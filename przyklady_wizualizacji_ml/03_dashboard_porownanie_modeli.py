"""
Przykład 3: Interaktywny dashboard porównujący modele klasyfikacyjne.

Co pokazuje ten skrypt:
1. Wczytanie przykładowego zbioru danych do klasyfikacji.
2. Podział na zbiór treningowy i testowy.
3. Uczenie kilku modeli klasyfikacyjnych.
4. Porównanie ich jakości:
   - Accuracy,
   - Precision,
   - Recall,
   - F1-score,
   - AUC ROC.
5. Zbudowanie jednego interaktywnego dashboardu HTML z:
   - wykresem słupkowym metryk,
   - macierzą pomyłek najlepszego modelu,
   - krzywymi ROC wszystkich modeli,
   - słupkami ważności cech dla lasu losowego.

Uruchomienie:
    python 03_dashboard_porownanie_modeli.py

Wymagane biblioteki:
    pip install numpy pandas scikit-learn plotly
"""

import numpy as np  # Importujemy NumPy do operacji na tablicach i wygodnego przygotowania danych pomocniczych.
import pandas as pd  # Importujemy pandas, aby wygodnie zbudować tabelę z metrykami modeli.
from sklearn.datasets import load_breast_cancer  # Importujemy gotowy zbiór danych do klasyfikacji binarnej.
from sklearn.model_selection import train_test_split  # Importujemy funkcję do podziału danych na część treningową i testową.
from sklearn.pipeline import Pipeline  # Importujemy Pipeline, aby elegancko połączyć skalowanie i model w jeden obiekt.
from sklearn.preprocessing import StandardScaler  # Importujemy standaryzację, bo część modeli działa lepiej na danych przeskalowanych.
from sklearn.linear_model import LogisticRegression  # Importujemy regresję logistyczną jako prosty model bazowy do klasyfikacji.
from sklearn.neighbors import KNeighborsClassifier  # Importujemy k-NN jako model oparty na sąsiadach.
from sklearn.ensemble import RandomForestClassifier  # Importujemy las losowy jako mocniejszy model drzewowy.
from sklearn.metrics import accuracy_score  # Importujemy accuracy do oceny ogólnej skuteczności klasyfikacji.
from sklearn.metrics import precision_score  # Importujemy precision, aby oceniać jakość pozytywnych predykcji.
from sklearn.metrics import recall_score  # Importujemy recall, aby sprawdzać, ile klas pozytywnych zostało wykrytych.
from sklearn.metrics import f1_score  # Importujemy F1-score, który równoważy precision i recall.
from sklearn.metrics import roc_auc_score  # Importujemy AUC, aby porównać jakość rankingową modeli.
from sklearn.metrics import roc_curve  # Importujemy roc_curve, aby narysować krzywe ROC dla wszystkich modeli.
from sklearn.metrics import confusion_matrix  # Importujemy macierz pomyłek, która pokazuje strukturę błędów klasyfikatora.
from plotly.subplots import make_subplots  # Importujemy narzędzie do budowania figury z wieloma panelami.
import plotly.graph_objects as go  # Importujemy obiekty wykresów Plotly, aby mieć pełną kontrolę nad dashboardem.

RANDOM_STATE = 42  # Ustalamy ziarno losowości, aby podział danych i modele były odtwarzalne.

data = load_breast_cancer()  # Wczytujemy klasyczny zbiór danych medycznych do klasyfikacji łagodnych i złośliwych zmian.
X = data.data  # Pobieramy macierz cech wejściowych.
y = data.target  # Pobieramy etykiety klas.
feature_names = data.feature_names  # Zachowujemy nazwy cech, bo przydadzą się do wizualizacji ważności cech.

X_train, X_test, y_train, y_test = train_test_split(  # Dzielimy dane na część treningową i testową.
    X,  # Przekazujemy cechy wejściowe.
    y,  # Przekazujemy etykiety klas.
    test_size=0.25,  # Rezerwujemy 25% danych na uczciwy test jakości modeli.
    random_state=RANDOM_STATE,  # Ustalamy ziarno losowości podziału.
    stratify=y,  # Zachowujemy proporcje klas w obu częściach zbioru, co jest ważne przy klasyfikacji.
)

models = {  # Budujemy słownik modeli, aby potem łatwo przejść po nich w pętli.
    "Regresja logistyczna": Pipeline([  # Dla regresji logistycznej tworzymy pipeline: najpierw skala, potem model.
        ("scaler", StandardScaler()),  # Standaryzujemy dane, bo regresja logistyczna korzysta na cechach o podobnej skali.
        ("model", LogisticRegression(max_iter=3000, random_state=RANDOM_STATE)),  # Tworzymy model z większym limitem iteracji dla stabilnej zbieżności.
    ]),
    "k-NN": Pipeline([  # Dla k-NN także używamy pipeline, bo odległości są bardzo wrażliwe na skalę cech.
        ("scaler", StandardScaler()),  # Skaluje dane przed liczeniem odległości sąsiadów.
        ("model", KNeighborsClassifier(n_neighbors=9)),  # Ustawiamy liczbę sąsiadów na 9 jako rozsądny kompromis.
    ]),
    "Random Forest": RandomForestClassifier(  # Las losowy zwykle nie wymaga skalowania, więc tworzymy go bez pipeline.
        n_estimators=300,  # Ustawiamy liczbę drzew na 300, aby model był stabilniejszy.
        max_depth=None,  # Pozwalamy drzewom rosnąć swobodnie, chyba że dane same ograniczą wzrost.
        random_state=RANDOM_STATE,  # Ustalamy ziarno losowości.
    ),
}

results = []  # Tworzymy pustą listę, do której będziemy odkładać metryki każdego modelu.
roc_curves = {}  # Tworzymy słownik na dane do wykresów ROC.
trained_models = {}  # Tworzymy słownik, aby zachować wytrenowane modele do dalszej analizy.
predictions = {}  # Tworzymy słownik na klasy przewidywane przez każdy model.
probabilities = {}  # Tworzymy słownik na prawdopodobieństwa klasy pozytywnej.

for model_name, model in models.items():  # Przechodzimy po wszystkich modelach, aby trenować i oceniać je w ten sam sposób.
    model.fit(X_train, y_train)  # Uczymy bieżący model na zbiorze treningowym.
    y_pred = model.predict(X_test)  # Generujemy przewidywane klasy dla zbioru testowego.
    y_proba = model.predict_proba(X_test)[:, 1]  # Pobieramy prawdopodobieństwa klasy pozytywnej potrzebne do AUC i ROC.

    accuracy = accuracy_score(y_test, y_pred)  # Liczymy accuracy, czyli udział poprawnych klasyfikacji.
    precision = precision_score(y_test, y_pred)  # Liczymy precision, aby ocenić "czystość" pozytywnych przewidywań.
    recall = recall_score(y_test, y_pred)  # Liczymy recall, aby sprawdzić wykrywalność klasy pozytywnej.
    f1 = f1_score(y_test, y_pred)  # Liczymy średnią harmoniczną precision i recall.
    auc = roc_auc_score(y_test, y_proba)  # Liczymy AUC na podstawie prawdopodobieństw.

    fpr, tpr, _ = roc_curve(y_test, y_proba)  # Wyznaczamy punkty krzywej ROC: false positive rate i true positive rate.

    results.append({  # Zapisujemy metryki modelu jako pojedynczy rekord tabeli wyników.
        "model": model_name,  # Zapamiętujemy nazwę modelu, aby dało się go potem podpisać na wykresach.
        "accuracy": accuracy,  # Odkładamy accuracy.
        "precision": precision,  # Odkładamy precision.
        "recall": recall,  # Odkładamy recall.
        "f1": f1,  # Odkładamy F1-score.
        "auc": auc,  # Odkładamy AUC.
    })

    roc_curves[model_name] = (fpr, tpr)  # Zapamiętujemy przebieg krzywej ROC dla danego modelu.
    trained_models[model_name] = model  # Przechowujemy wytrenowany model, bo będzie potrzebny do dalszej analizy.
    predictions[model_name] = y_pred  # Zapamiętujemy predykcje klas dla modelu.
    probabilities[model_name] = y_proba  # Zapamiętujemy prawdopodobieństwa klasy pozytywnej.

results_df = pd.DataFrame(results).sort_values("f1", ascending=False)  # Zamieniamy listę wyników na tabelę i sortujemy ją od najlepszego F1.
best_model_name = results_df.iloc[0]["model"]  # Odczytujemy nazwę modelu, który uzyskał najlepszy wynik F1.
best_model = trained_models[best_model_name]  # Pobieramy obiekt najlepszego modelu.
best_model_predictions = predictions[best_model_name]  # Pobieramy predykcje najlepszego modelu na zbiorze testowym.

cm = confusion_matrix(y_test, best_model_predictions)  # Liczymy macierz pomyłek dla najlepszego modelu.

rf_model = trained_models["Random Forest"]  # Pobieramy las losowy, bo z niego odczytamy ważność cech.
rf_importances = rf_model.feature_importances_  # Odczytujemy wektor ważności cech obliczony przez model.
importance_df = pd.DataFrame({  # Budujemy tabelę z nazwami cech i ich ważnością.
    "cecha": feature_names,  # W pierwszej kolumnie zapisujemy nazwy cech.
    "waznosc": rf_importances,  # W drugiej kolumnie zapisujemy numeryczne ważności.
}).sort_values("waznosc", ascending=False).head(10)  # Sortujemy malejąco i zostawiamy 10 najważniejszych cech, aby wykres był czytelny.

fig = make_subplots(  # Tworzymy figurę z czterema panelami, które razem złożą się na prosty dashboard.
    rows=2,  # Definiujemy dwa wiersze paneli.
    cols=2,  # Definiujemy dwie kolumny paneli.
    subplot_titles=(  # Ustawiamy tytuły dla każdego panelu osobno.
        "Porównanie metryk modeli",  # Tytuł lewego górnego panelu.
        f"Macierz pomyłek: {best_model_name}",  # Tytuł prawego górnego panelu, zależny od najlepszego modelu.
        "Krzywe ROC",  # Tytuł lewego dolnego panelu.
        "Najważniejsze cechy (Random Forest)",  # Tytuł prawego dolnego panelu.
    ),
    specs=[  # Opisujemy typ wykresu w każdym polu siatki.
        [{"type": "bar"}, {"type": "heatmap"}],  # W pierwszym wierszu chcemy słupki oraz mapę cieplną.
        [{"type": "scatter"}, {"type": "bar"}],  # W drugim wierszu chcemy wykres liniowy i słupki poziome.
    ],
    horizontal_spacing=0.12,  # Zwiększamy poziomy odstęp między kolumnami dla lepszej czytelności.
    vertical_spacing=0.12,  # Zwiększamy pionowy odstęp między wierszami.
)

metric_names = ["accuracy", "precision", "recall", "f1", "auc"]  # Tworzymy listę metryk, które chcemy pokazać na wykresie słupkowym.

for model_name in results_df["model"]:  # Dla każdego modelu dodajemy osobny ślad słupkowy do panelu metryk.
    row_data = results_df[results_df["model"] == model_name].iloc[0]  # Wyciągamy pojedynczy wiersz z metrykami aktualnego modelu.
    fig.add_trace(  # Dodajemy serię słupków reprezentujących jakość jednego modelu.
        go.Bar(  # Używamy wykresu słupkowego, bo łatwo porównuje wartości między modelami.
            x=metric_names,  # Na osi X ustawiamy nazwy metryk.
            y=[row_data[m] for m in metric_names],  # Na osi Y ustawiamy wartości metryk w tej samej kolejności.
            name=model_name,  # Nazwa śladu będzie widoczna w legendzie.
            hovertemplate=(  # Budujemy własny dymek hover, aby był bardziej informacyjny.
                "Model: %{fullData.name}<br>"  # Pokazujemy nazwę modelu.
                "Metryka: %{x}<br>"  # Pokazujemy nazwę metryki.
                "Wartość: %{y:.4f}<extra></extra>"  # Pokazujemy wartość metryki z czterema miejscami po przecinku.
            ),
        ),
        row=1,  # Umieszczamy ślad w pierwszym wierszu dashboardu.
        col=1,  # Umieszczamy ślad w pierwszej kolumnie dashboardu.
    )

fig.add_trace(  # Dodajemy macierz pomyłek najlepszego modelu jako heatmapę.
    go.Heatmap(  # Używamy heatmapy, bo dobrze pokazuje liczebności w komórkach macierzy.
        z=cm,  # Przekazujemy wartości macierzy pomyłek.
        x=["Przewidziano 0", "Przewidziano 1"],  # Opisujemy kolumny jako klasy przewidywane.
        y=["Rzeczywiste 0", "Rzeczywiste 1"],  # Opisujemy wiersze jako klasy rzeczywiste.
        text=cm,  # Przekazujemy także liczby, aby dało się je wyświetlić bezpośrednio na komórkach.
        texttemplate="%{text}",  # Mówimy Plotly, by pokazał tekst wpisany w parametrze text.
        hovertemplate=(  # Ustawiamy opis hover dla komórek macierzy.
            "%{y}<br>%{x}<br>Liczba przypadków: %{z}<extra></extra>"  # Pokazujemy dokładny sens komórki i jej wartość.
        ),
        colorscale="Blues",  # Wybieramy niebieską skalę kolorów, która jest czytelna dla heatmapy.
        showscale=True,  # Zostawiamy skalę kolorów, aby łatwo interpretować intensywność.
    ),
    row=1,  # Umieszczamy heatmapę w pierwszym wierszu.
    col=2,  # Umieszczamy heatmapę w drugiej kolumnie.
)

for model_name, (fpr, tpr) in roc_curves.items():  # Dla każdego modelu dodajemy osobną krzywą ROC.
    auc_value = results_df.loc[results_df["model"] == model_name, "auc"].iloc[0]  # Odczytujemy AUC, aby umieścić je w podpisie.
    fig.add_trace(  # Dodajemy linię ROC do odpowiedniego panelu.
        go.Scatter(  # Używamy wykresu liniowego, bo ROC to przebieg zależności między FPR i TPR.
            x=fpr,  # Na osi X umieszczamy false positive rate.
            y=tpr,  # Na osi Y umieszczamy true positive rate.
            mode="lines",  # Rysujemy ciągłą linię, aby przebieg był czytelny.
            name=f"{model_name} (AUC={auc_value:.3f})",  # Rozszerzamy nazwę modelu o wartość AUC.
            hovertemplate=(  # Konfigurujemy okienko hover dla krzywej ROC.
                "Model: %{fullData.name}<br>"  # Pokazujemy nazwę modelu wraz z AUC.
                "FPR: %{x:.4f}<br>"  # Pokazujemy fałszywie pozytywny odsetek.
                "TPR: %{y:.4f}<extra></extra>"  # Pokazujemy prawdziwie pozytywny odsetek.
            ),
        ),
        row=2,  # Umieszczamy ROC w drugim wierszu.
        col=1,  # Umieszczamy ROC w pierwszej kolumnie.
    )

fig.add_trace(  # Dodajemy linię odniesienia dla losowego klasyfikatora.
    go.Scatter(  # Ponownie używamy wykresu liniowego.
        x=[0, 1],  # Linia biegnie od punktu (0,0) ...
        y=[0, 1],  # ... do punktu (1,1), co oznacza losową jakość modelu.
        mode="lines",  # Chcemy prostą linię.
        name="Losowy klasyfikator",  # Nadajemy nazwę widoczną w legendzie.
        line=dict(dash="dash"),  # Rysujemy ją linią przerywaną, aby odróżniała się od prawdziwych modeli.
        hoverinfo="skip",  # Wyłączamy hover, bo ta linia ma charakter tylko pomocniczy.
    ),
    row=2,  # Umieszczamy ją w drugim wierszu.
    col=1,  # Umieszczamy ją w pierwszej kolumnie, czyli tam, gdzie krzywe ROC.
)

fig.add_trace(  # Dodajemy wykres słupkowy ważności cech z lasu losowego.
    go.Bar(  # Używamy wykresu słupkowego poziomego, bo długie nazwy cech są wtedy bardziej czytelne.
        x=importance_df["waznosc"],  # Na osi X pokazujemy liczbową ważność cechy.
        y=importance_df["cecha"],  # Na osi Y pokazujemy nazwy cech.
        orientation="h",  # Ustawiamy słupki poziomo.
        name="Ważność cech",  # Nadajemy nazwę śladu.
        hovertemplate=(  # Definiujemy podpowiedź hover dla słupków.
            "Cecha: %{y}<br>"  # Pokazujemy nazwę cechy.
            "Ważność: %{x:.4f}<extra></extra>"  # Pokazujemy wartość ważności z czterema miejscami po przecinku.
        ),
    ),
    row=2,  # Umieszczamy wykres w drugim wierszu.
    col=2,  # Umieszczamy wykres w drugiej kolumnie.
)

fig.update_xaxes(title_text="Metryka", row=1, col=1)  # Opisujemy oś X panelu metryk.
fig.update_yaxes(title_text="Wartość", range=[0, 1.05], row=1, col=1)  # Opisujemy oś Y metryk i ograniczamy ją do sensownego przedziału.
fig.update_xaxes(title_text="False Positive Rate", row=2, col=1)  # Opisujemy oś X wykresu ROC.
fig.update_yaxes(title_text="True Positive Rate", row=2, col=1)  # Opisujemy oś Y wykresu ROC.
fig.update_xaxes(title_text="Ważność", row=2, col=2)  # Opisujemy oś X ważności cech.
fig.update_yaxes(title_text="Cecha", autorange="reversed", row=2, col=2)  # Odwracamy kolejność osi Y, aby najważniejsza cecha była na górze.

fig.update_layout(  # Dopieszczamy wygląd całego dashboardu.
    title="Interaktywny dashboard porównujący modele klasyfikacyjne",  # Ustawiamy główny tytuł całej figury.
    barmode="group",  # Grupujemy słupki różnych modeli obok siebie, aby łatwo je porównywać.
    height=900,  # Ustawiamy dużą wysokość figury, żeby wszystkie panele miały dość miejsca.
    width=1500,  # Ustawiamy dużą szerokość figury dla wygody oglądania.
    legend_title_text="Modele",  # Nadajemy legendzie czytelny tytuł.
)

output_html = "03_dashboard_porownanie_modeli.html"  # Określamy nazwę pliku wynikowego dashboardu.
fig.write_html(output_html)  # Zapisujemy dashboard jako samodzielny plik HTML do uruchomienia w przeglądarce.
print(f"Najlepszy model według F1: {best_model_name}")  # Wypisujemy informację o zwycięskim modelu.
print("Tabela wyników modeli:")  # Dodajemy nagłówek dla tabeli wyników.
print(results_df.to_string(index=False))  # Wypisujemy pełną tabelę metryk w konsoli, aby mieć także tekstowe podsumowanie.
print(f"Zapisano dashboard do pliku: {output_html}")  # Informujemy użytkownika, gdzie znajduje się wygenerowany dashboard.
fig.show()  # Otwieramy dashboard w domyślnym rendererze Plotly.
