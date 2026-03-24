"""
Przykład PREMIUM 3: Rozbudowany dashboard porównujący modele klasyfikacyjne.

Ten skrypt buduje bogatszy dashboard niż zwykłe porównanie accuracy:
1. generuje zbiór klasyfikacyjny,
2. dzieli dane na trening i test,
3. trenuje kilka modeli,
4. liczy zestaw metryk jakości,
5. wybiera najlepszy model według F1,
6. tworzy interaktywny dashboard HTML z wieloma panelami,
7. zapisuje także tabelę wyników do CSV.

Dashboard zawiera:
- porównanie metryk modeli,
- macierz pomyłek najlepszego modelu,
- krzywe ROC,
- krzywe Precision-Recall,
- ważność cech,
- analizę wpływu progu decyzyjnego na precision / recall / F1.

Uruchomienie:
    python 03_dashboard_porownanie_modeli_premium.py

Wymagane biblioteki:
    pip install numpy pandas scikit-learn plotly
"""

from pathlib import Path  # Importujemy Path, aby wygodnie zarządzać katalogami i plikami wynikowymi.

import numpy as np  # Importujemy NumPy do obliczeń numerycznych i pracy na tablicach.
import pandas as pd  # Importujemy pandas, aby wygodnie budować i zapisywać tabele wyników.
import plotly.graph_objects as go  # Importujemy graph_objects, bo daje pełną kontrolę nad złożonym dashboardem.
from plotly.subplots import make_subplots  # Importujemy make_subplots, ponieważ dashboard będzie składał się z wielu paneli.
from sklearn.datasets import make_classification  # Importujemy generator danych klasyfikacyjnych, aby przygotować powtarzalny przykład.
from sklearn.ensemble import GradientBoostingClassifier  # Importujemy Gradient Boosting jako jeden z mocniejszych klasyfikatorów drzewiastych.
from sklearn.ensemble import RandomForestClassifier  # Importujemy Random Forest, aby mieć model zespołowy z ważnością cech.
from sklearn.linear_model import LogisticRegression  # Importujemy regresję logistyczną jako klasyczny, interpretowalny punkt odniesienia.
from sklearn.metrics import accuracy_score  # Importujemy accuracy do oceny ogólnego odsetka trafnych klasyfikacji.
from sklearn.metrics import auc  # Importujemy funkcję AUC do pola pod krzywą ROC i PR.
from sklearn.metrics import confusion_matrix  # Importujemy macierz pomyłek, aby zobaczyć rozkład trafień i błędów.
from sklearn.metrics import f1_score  # Importujemy F1, bo dobrze równoważy precision i recall.
from sklearn.metrics import precision_recall_curve  # Importujemy krzywą Precision-Recall, szczególnie ważną przy ocenie klasy pozytywnej.
from sklearn.metrics import precision_score  # Importujemy precision, aby mierzyć „czystość” klasy pozytywnej.
from sklearn.metrics import recall_score  # Importujemy recall, aby mierzyć, ile pozytywnych przypadków zostało wykrytych.
from sklearn.metrics import roc_auc_score  # Importujemy ROC AUC, aby mierzyć jakość rozróżniania klas niezależnie od pojedynczego progu.
from sklearn.metrics import roc_curve  # Importujemy przebieg krzywej ROC.
from sklearn.model_selection import train_test_split  # Importujemy podział danych na zbiór treningowy i testowy.
from sklearn.neighbors import KNeighborsClassifier  # Importujemy KNN jako model oparty o odległość.
from sklearn.pipeline import Pipeline  # Importujemy Pipeline, aby łączyć skalowanie z modelem w jednym, bezpiecznym workflow.
from sklearn.preprocessing import StandardScaler  # Importujemy StandardScaler, bo część modeli wymaga danych o podobnej skali.
from sklearn.svm import SVC  # Importujemy SVC jako mocny model brzegowy z możliwością zwracania prawdopodobieństw.

RANDOM_STATE = 42  # Ustalamy ziarno losowości dla pełnej powtarzalności całego eksperymentu.
OUTPUT_DIR = Path(__file__).resolve().parent / "wyniki"  # Definiujemy katalog na pliki HTML i CSV obok skryptu.
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  # Tworzymy katalog wynikowy, jeśli jeszcze nie istnieje.

X, y = make_classification(  # Generujemy syntetyczny problem klasyfikacji binarnej.
    n_samples=1600,  # Tworzymy 1600 rekordów, aby modele miały sensowny materiał do nauki i testu.
    n_features=14,  # Ustawiamy 14 cech wejściowych, co daje sensowny kompromis między prostotą a realizmem.
    n_informative=8,  # Osiem cech rzeczywiście niesie sygnał klasyfikacyjny.
    n_redundant=3,  # Trzy cechy są redundantne, czyli częściowo powielają informację.
    n_repeated=0,  # Nie tworzymy cech dosłownie powtórzonych.
    n_classes=2,  # Definiujemy klasyfikację binarną: klasa 0 oraz klasa 1.
    n_clusters_per_class=2,  # Każda klasa będzie miała po dwa naturalne skupiska, co czyni problem ciekawszym.
    class_sep=1.35,  # Kontrolujemy separację klas; umiarkowanie wysoka wartość daje realistyczny poziom trudności.
    flip_y=0.03,  # Wprowadzamy trochę szumu etykiet, aby zadanie nie było idealnie łatwe.
    random_state=RANDOM_STATE,  # Ustawiamy ziarno losowości dla generatora danych.
)

feature_names = [f"cecha_{i}" for i in range(X.shape[1])]  # Tworzymy listę nazw cech, aby raport i wykresy były czytelne.

X_train, X_test, y_train, y_test = train_test_split(  # Dzielimy dane na część treningową i testową.
    X,  # Przekazujemy macierz cech wejściowych.
    y,  # Przekazujemy etykiety klas.
    test_size=0.30,  # Zostawiamy 30% danych na uczciwy test końcowy.
    stratify=y,  # Zachowujemy proporcje klas w obu zbiorach.
    random_state=RANDOM_STATE,  # Zapewniamy odtwarzalny podział.
)

models = {  # Definiujemy słownik modeli, które chcemy porównać.
    "Logistic Regression": Pipeline(  # Regresję logistyczną opakowujemy w pipeline ze skalowaniem.
        [
            ("scaler", StandardScaler()),  # Najpierw standaryzujemy dane, aby model działał stabilniej numerycznie.
            ("model", LogisticRegression(max_iter=3000, random_state=RANDOM_STATE)),  # Potem uczymy regresję logistyczną z wyższym limitem iteracji.
        ]
    ),
    "KNN": Pipeline(  # KNN również wymaga skalowania, bo bazuje bezpośrednio na odległościach.
        [
            ("scaler", StandardScaler()),  # Standaryzujemy dane wejściowe.
            ("model", KNeighborsClassifier(n_neighbors=15)),  # Ustawiamy 15 sąsiadów, by model był gładszy i stabilniejszy.
        ]
    ),
    "SVC": Pipeline(  # SVC także opakowujemy w pipeline.
        [
            ("scaler", StandardScaler()),  # Skalujemy cechy, ponieważ SVC jest wrażliwy na różnice skali.
            ("model", SVC(kernel="rbf", probability=True, C=2.5, gamma="scale", random_state=RANDOM_STATE)),  # Włączamy probability=True, aby móc liczyć ROC i analizować progi.
        ]
    ),
    "Random Forest": RandomForestClassifier(  # Random Forest nie wymaga skalowania, więc tworzymy go bez pipeline.
        n_estimators=350,  # Używamy 350 drzew, aby model był stabilny i dawał gładniejsze wyniki.
        max_depth=None,  # Nie ograniczamy głębokości, pozwalając drzewom dopasować złożone zależności.
        min_samples_leaf=2,  # Wymuszamy minimum 2 rekordów w liściu, aby ograniczyć nadmierne przeuczenie.
        random_state=RANDOM_STATE,  # Ustawiamy ziarno losowości dla odtwarzalności.
        n_jobs=-1,  # Pozwalamy modelowi korzystać ze wszystkich rdzeni CPU dla szybszego treningu.
    ),
    "Gradient Boosting": GradientBoostingClassifier(  # Dodajemy klasyczny boosting drzew decyzyjnych.
        n_estimators=220,  # Ustawiamy sensowną liczbę etapów boostingu.
        learning_rate=0.06,  # Ustawiamy dość mały learning rate, by model uczył się bardziej stopniowo.
        max_depth=3,  # Głębokość słabych modeli ustawiamy umiarkowanie, aby zachować równowagę między elastycznością a generalizacją.
        random_state=RANDOM_STATE,  # Ustawiamy ziarno losowości dla powtarzalności.
    ),
}

results = []  # Tworzymy pustą listę, do której będziemy odkładać metryki wszystkich modeli.
roc_curves = {}  # Tutaj będziemy trzymać przebiegi ROC dla każdego modelu.
pr_curves = {}  # Tutaj będziemy trzymać przebiegi Precision-Recall dla każdego modelu.
trained_models = {}  # Tutaj przechowamy gotowe, wytrenowane obiekty modeli.
predictions = {}  # Tutaj zapiszemy przewidziane etykiety klas dla każdego modelu.
probabilities = {}  # Tutaj zapiszemy prawdopodobieństwa klasy pozytywnej dla każdego modelu.

for model_name, model in models.items():  # Iterujemy po wszystkich modelach zdefiniowanych w słowniku.
    model.fit(X_train, y_train)  # Uczymy bieżący model na zbiorze treningowym.
    y_pred = model.predict(X_test)  # Generujemy przewidziane etykiety klas dla zbioru testowego.
    y_proba = model.predict_proba(X_test)[:, 1]  # Pobieramy prawdopodobieństwo klasy pozytywnej, potrzebne do ROC, PR i analizy progów.

    accuracy = accuracy_score(y_test, y_pred)  # Liczymy accuracy modelu na zbiorze testowym.
    precision = precision_score(y_test, y_pred)  # Liczymy precision modelu.
    recall = recall_score(y_test, y_pred)  # Liczymy recall modelu.
    f1 = f1_score(y_test, y_pred)  # Liczymy F1 modelu.
    roc_auc = roc_auc_score(y_test, y_proba)  # Liczymy ROC AUC, korzystając z prawdopodobieństw.

    fpr, tpr, _ = roc_curve(y_test, y_proba)  # Liczymy przebieg ROC dla bieżącego modelu.
    precision_curve, recall_curve, _ = precision_recall_curve(y_test, y_proba)  # Liczymy przebieg Precision-Recall.
    pr_auc = auc(recall_curve, precision_curve)  # Liczymy pole pod krzywą Precision-Recall.

    results.append(  # Dopisujemy komplet metryk jednego modelu do listy wyników.
        {
            "model": model_name,  # Zapisujemy nazwę modelu.
            "accuracy": accuracy,  # Zapisujemy accuracy.
            "precision": precision,  # Zapisujemy precision.
            "recall": recall,  # Zapisujemy recall.
            "f1": f1,  # Zapisujemy F1.
            "roc_auc": roc_auc,  # Zapisujemy ROC AUC.
            "pr_auc": pr_auc,  # Zapisujemy PR AUC.
        }
    )

    roc_curves[model_name] = (fpr, tpr)  # Zapamiętujemy krzywą ROC modelu.
    pr_curves[model_name] = (recall_curve, precision_curve)  # Zapamiętujemy krzywą Precision-Recall modelu.
    trained_models[model_name] = model  # Zapamiętujemy wytrenowany model.
    predictions[model_name] = y_pred  # Zapamiętujemy dyskretne predykcje klas.
    probabilities[model_name] = y_proba  # Zapamiętujemy prawdopodobieństwa klasy pozytywnej.

results_df = pd.DataFrame(results).sort_values("f1", ascending=False).reset_index(drop=True)  # Budujemy tabelę wyników i sortujemy ją od najlepszego F1.
best_model_name = results_df.loc[0, "model"]  # Odczytujemy nazwę modelu, który wygrał według F1.
best_model = trained_models[best_model_name]  # Pobieramy obiekt najlepszego modelu.
best_predictions = predictions[best_model_name]  # Pobieramy etykiety przewidziane przez najlepszy model.
best_probabilities = probabilities[best_model_name]  # Pobieramy prawdopodobieństwa klasy pozytywnej dla najlepszego modelu.

cm = confusion_matrix(y_test, best_predictions)  # Liczymy macierz pomyłek dla najlepszego modelu.

feature_importance_model = trained_models["Random Forest"]  # Wybieramy Random Forest jako źródło interpretowalnych ważności cech.
feature_importances = feature_importance_model.feature_importances_  # Odczytujemy wektor ważności cech.
importance_df = pd.DataFrame(  # Budujemy tabelę ważności cech.
    {"cecha": feature_names, "waznosc": feature_importances}  # Łączymy nazwy cech z ich wagami w modelu.
).sort_values("waznosc", ascending=False).head(10)  # Sortujemy malejąco i zostawiamy 10 najważniejszych cech.

thresholds = np.linspace(0.05, 0.95, 91)  # Tworzymy gęstą siatkę progów decyzyjnych od 0.05 do 0.95.
threshold_precision = []  # Tu będziemy zapisywać precision najlepszego modelu dla kolejnych progów.
threshold_recall = []  # Tu będziemy zapisywać recall dla kolejnych progów.
threshold_f1 = []  # Tu będziemy zapisywać F1 dla kolejnych progów.

for threshold in thresholds:  # Iterujemy po wszystkich progach, aby sprawdzić ich wpływ na zachowanie modelu.
    threshold_pred = (best_probabilities >= threshold).astype(int)  # Zamieniamy prawdopodobieństwa na decyzję klasową według bieżącego progu.
    threshold_precision.append(precision_score(y_test, threshold_pred, zero_division=0))  # Liczymy precision dla danego progu i zapisujemy wynik.
    threshold_recall.append(recall_score(y_test, threshold_pred, zero_division=0))  # Liczymy recall dla danego progu i zapisujemy wynik.
    threshold_f1.append(f1_score(y_test, threshold_pred, zero_division=0))  # Liczymy F1 dla danego progu i zapisujemy wynik.

best_threshold_index = int(np.argmax(threshold_f1))  # Szukamy indeksu progu, dla którego F1 jest najwyższe.
best_threshold = thresholds[best_threshold_index]  # Odczytujemy konkretną wartość najlepszego progu.

fig = make_subplots(  # Tworzymy figurę składającą się z 6 paneli.
    rows=2,  # Definiujemy dwa wiersze paneli.
    cols=3,  # Definiujemy trzy kolumny paneli.
    subplot_titles=(  # Ustawiamy tytuły poszczególnych paneli dashboardu.
        "Porównanie metryk modeli",  # Panel 1: metryki wszystkich modeli.
        f"Macierz pomyłek: {best_model_name}",  # Panel 2: confusion matrix zwycięzcy.
        "Krzywe ROC",  # Panel 3: ROC wszystkich modeli.
        "Krzywe Precision-Recall",  # Panel 4: PR wszystkich modeli.
        "Top 10 ważności cech (Random Forest)",  # Panel 5: ważność cech.
        f"Analiza progu dla {best_model_name}",  # Panel 6: wpływ progu na precision/recall/F1.
    ),
    specs=[  # Określamy typ wykresu w każdym panelu.
        [{"type": "bar"}, {"type": "heatmap"}, {"type": "scatter"}],  # Pierwszy wiersz: słupki, heatmapa, linie.
        [{"type": "scatter"}, {"type": "bar"}, {"type": "scatter"}],  # Drugi wiersz: linie, słupki, linie.
    ],
    horizontal_spacing=0.08,  # Dodajemy trochę większy odstęp poziomy dla wygody czytania.
    vertical_spacing=0.11,  # Dodajemy odstęp pionowy między rzędami paneli.
)

metric_columns = ["accuracy", "precision", "recall", "f1", "roc_auc", "pr_auc"]  # Tworzymy listę metryk do panelu porównawczego.

for _, row in results_df.iterrows():  # Iterujemy po każdym wierszu tabeli wyników, aby dodać słupki dla jednego modelu.
    fig.add_trace(  # Dodajemy ślad słupkowy dla metryk pojedynczego modelu.
        go.Bar(  # Wykorzystujemy wykres słupkowy, bo dobrze pokazuje porównanie wielu miar jednocześnie.
            x=metric_columns,  # Na osi X ustawiamy nazwy metryk.
            y=[row[col] for col in metric_columns],  # Na osi Y ustawiamy wartości metryk dla bieżącego modelu.
            name=row["model"],  # Ustawiamy nazwę śladu zgodną z nazwą modelu.
            hovertemplate="Model: %{fullData.name}<br>Metryka: %{x}<br>Wartość: %{y:.4f}<extra></extra>",  # Budujemy czytelny hover z nazwą modelu i metryką.
        ),
        row=1,  # Umieszczamy ślad w pierwszym wierszu.
        col=1,  # Umieszczamy ślad w pierwszej kolumnie.
    )

fig.add_trace(  # Dodajemy heatmapę z macierzą pomyłek najlepszego modelu.
    go.Heatmap(  # Wybieramy heatmapę, bo dobrze oddaje natężenie wartości w komórkach macierzy.
        z=cm,  # Przekazujemy wartości macierzy pomyłek.
        x=["Pred 0", "Pred 1"],  # Podpisujemy kolumny jako klasy przewidziane.
        y=["True 0", "True 1"],  # Podpisujemy wiersze jako klasy rzeczywiste.
        text=cm,  # Przekazujemy liczby, aby móc je wyświetlić bezpośrednio na komórkach.
        texttemplate="%{text}",  # Mówimy Plotly, aby w komórkach pokazał zawartość pola text.
        colorscale="Blues",  # Wybieramy klasyczną niebieską skalę dla macierzy pomyłek.
        hovertemplate="%{y}<br>%{x}<br>Liczba przypadków: %{z}<extra></extra>",  # Konfigurujemy opis hover dla komórek.
    ),
    row=1,  # Umieszczamy heatmapę w pierwszym wierszu.
    col=2,  # Umieszczamy heatmapę w drugiej kolumnie.
)

for model_name, (fpr, tpr) in roc_curves.items():  # Iterujemy po wszystkich modelach i ich przebiegach ROC.
    roc_auc_value = results_df.loc[results_df["model"] == model_name, "roc_auc"].iloc[0]  # Odczytujemy ROC AUC bieżącego modelu.
    fig.add_trace(  # Dodajemy linię ROC modelu.
        go.Scatter(  # Używamy wykresu liniowego dla przebiegu ROC.
            x=fpr,  # Na osi X odkładamy false positive rate.
            y=tpr,  # Na osi Y odkładamy true positive rate.
            mode="lines",  # Rysujemy linię ciągłą.
            name=f"ROC: {model_name} (AUC={roc_auc_value:.3f})",  # W legendzie pokazujemy nazwę modelu i AUC.
            hovertemplate="%{fullData.name}<br>FPR: %{x:.4f}<br>TPR: %{y:.4f}<extra></extra>",  # Konfigurujemy hover dla krzywej ROC.
            showlegend=False,  # Wyłączamy powtarzanie legendy w tym panelu, bo legenda i tak jest już bogata.
        ),
        row=1,  # Umieszczamy ślad w pierwszym wierszu.
        col=3,  # Umieszczamy ślad w trzeciej kolumnie.
    )

fig.add_trace(  # Dodajemy linię odniesienia oznaczającą losowy klasyfikator.
    go.Scatter(  # Używamy wykresu liniowego.
        x=[0, 1],  # Linia biegnie od 0 do 1 na osi X.
        y=[0, 1],  # Linia biegnie od 0 do 1 na osi Y.
        mode="lines",  # Rysujemy prostą linię.
        line=dict(dash="dash", color="gray"),  # Ustawiamy styl przerywany, aby było jasne, że to tylko odniesienie.
        name="Losowy klasyfikator",  # Nadajemy nazwę linii pomocniczej.
        hoverinfo="skip",  # Wyłączamy hover, bo ta linia pełni wyłącznie rolę orientacyjną.
        showlegend=False,  # Nie powiększamy legendy kolejnym elementem pomocniczym.
    ),
    row=1,  # Umieszczamy linię w pierwszym wierszu.
    col=3,  # Umieszczamy linię w trzeciej kolumnie, czyli w panelu ROC.
)

for model_name, (recall_curve, precision_curve) in pr_curves.items():  # Iterujemy po wszystkich przebiegach Precision-Recall.
    pr_auc_value = results_df.loc[results_df["model"] == model_name, "pr_auc"].iloc[0]  # Odczytujemy pole pod krzywą PR dla danego modelu.
    fig.add_trace(  # Dodajemy krzywą PR.
        go.Scatter(  # Wybieramy wykres liniowy do przedstawienia zależności precision od recall.
            x=recall_curve,  # Na osi X odkładamy recall.
            y=precision_curve,  # Na osi Y odkładamy precision.
            mode="lines",  # Rysujemy linię ciągłą.
            name=f"PR: {model_name} (AUC={pr_auc_value:.3f})",  # W nazwie śladu pokazujemy model i jego PR AUC.
            hovertemplate="%{fullData.name}<br>Recall: %{x:.4f}<br>Precision: %{y:.4f}<extra></extra>",  # Tworzymy własny hover dla PR.
            showlegend=False,  # Ponownie ograniczamy rozrost legendy.
        ),
        row=2,  # Umieszczamy ślad w drugim wierszu.
        col=1,  # Umieszczamy ślad w pierwszej kolumnie drugiego wiersza.
    )

fig.add_trace(  # Dodajemy poziomy wykres słupkowy z najważniejszymi cechami.
    go.Bar(  # Wybieramy bar chart, bo ważności cech najlepiej porównuje się słupkami.
        x=importance_df["waznosc"],  # Na osi X odkładamy liczbowe ważności cech.
        y=importance_df["cecha"],  # Na osi Y pokazujemy nazwy cech.
        orientation="h",  # Ustawiamy słupki poziome, aby dłuższe nazwy mieściły się wygodniej.
        name="Ważność cech",  # Nadajemy nazwę serii.
        marker=dict(color="#4C78A8"),  # Ustawiamy jednolity, elegancki kolor słupków.
        hovertemplate="Cecha: %{y}<br>Ważność: %{x:.4f}<extra></extra>",  # Budujemy hover z nazwą cechy i jej wartością.
        showlegend=False,  # Ten panel nie potrzebuje dodatkowej legendy.
    ),
    row=2,  # Umieszczamy ślad w drugim wierszu.
    col=2,  # Umieszczamy ślad w drugiej kolumnie.
)

fig.add_trace(  # Dodajemy przebieg precision względem progu.
    go.Scatter(  # Używamy wykresu liniowego.
        x=thresholds,  # Na osi X odkładamy próg decyzyjny.
        y=threshold_precision,  # Na osi Y odkładamy precision dla każdego progu.
        mode="lines",  # Rysujemy linię ciągłą.
        name="Precision vs threshold",  # Nadajemy nazwę przebiegowi.
        hovertemplate="Próg: %{x:.2f}<br>Precision: %{y:.4f}<extra></extra>",  # Konfigurujemy hover.
        showlegend=False,  # Nie dokładamy kolejnej pozycji do i tak już bogatej legendy.
    ),
    row=2,  # Umieszczamy ślad w drugim wierszu.
    col=3,  # Umieszczamy ślad w trzeciej kolumnie.
)

fig.add_trace(  # Dodajemy przebieg recall względem progu.
    go.Scatter(  # Ponownie używamy wykresu liniowego.
        x=thresholds,  # Oś X to próg decyzyjny.
        y=threshold_recall,  # Oś Y to recall.
        mode="lines",  # Rysujemy linię.
        name="Recall vs threshold",  # Nadajemy nazwę serii.
        hovertemplate="Próg: %{x:.2f}<br>Recall: %{y:.4f}<extra></extra>",  # Definiujemy hover.
        showlegend=False,  # Ograniczamy liczbę pozycji legendy.
    ),
    row=2,  # Umieszczamy ślad w drugim wierszu.
    col=3,  # Umieszczamy ślad w trzeciej kolumnie.
)

fig.add_trace(  # Dodajemy przebieg F1 względem progu, bo to według niego wybieramy optimum.
    go.Scatter(  # Wybieramy wykres liniowy.
        x=thresholds,  # Oś X to próg decyzyjny.
        y=threshold_f1,  # Oś Y to F1 dla danego progu.
        mode="lines",  # Rysujemy linię.
        name="F1 vs threshold",  # Nadajemy nazwę przebiegowi.
        hovertemplate="Próg: %{x:.2f}<br>F1: %{y:.4f}<extra></extra>",  # Konfigurujemy hover.
        showlegend=False,  # Nie powiększamy legendy.
    ),
    row=2,  # Umieszczamy ślad w drugim wierszu.
    col=3,  # Umieszczamy ślad w trzeciej kolumnie.
)

fig.add_vline(  # Dodajemy pionową linię pokazującą najlepszy próg według F1.
    x=best_threshold,  # Ustawiamy linię w punkcie najlepszego progu.
    line_dash="dash",  # Rysujemy ją linią przerywaną, aby odróżniała się od krzywych metryk.
    line_color="black",  # Kolor czarny dobrze kontrastuje z wieloma liniami na wykresie.
    annotation_text=f"Najlepszy próg F1 = {best_threshold:.2f}",  # Dodajemy tekst opisujący optymalny próg.
    annotation_position="top left",  # Ustawiamy etykietę blisko górnej części panelu.
    row=2,  # Umieszczamy linię w drugim wierszu.
    col=3,  # Umieszczamy linię w panelu analizy progu.
)

fig.update_xaxes(title_text="Metryka", row=1, col=1)  # Opisujemy oś X panelu porównania metryk.
fig.update_yaxes(title_text="Wartość", range=[0, 1.05], row=1, col=1)  # Opisujemy oś Y panelu metryk i ograniczamy zakres do 0–1.05.
fig.update_xaxes(title_text="False Positive Rate", row=1, col=3)  # Opisujemy oś X panelu ROC.
fig.update_yaxes(title_text="True Positive Rate", row=1, col=3)  # Opisujemy oś Y panelu ROC.
fig.update_xaxes(title_text="Recall", row=2, col=1)  # Opisujemy oś X panelu Precision-Recall.
fig.update_yaxes(title_text="Precision", row=2, col=1)  # Opisujemy oś Y panelu Precision-Recall.
fig.update_xaxes(title_text="Ważność", row=2, col=2)  # Opisujemy oś X panelu ważności cech.
fig.update_yaxes(title_text="Cecha", autorange="reversed", row=2, col=2)  # Odwracamy oś Y, aby najważniejsza cecha była u góry.
fig.update_xaxes(title_text="Próg decyzyjny", row=2, col=3)  # Opisujemy oś X panelu analizy progu.
fig.update_yaxes(title_text="Wartość metryki", range=[0, 1.05], row=2, col=3)  # Opisujemy oś Y panelu analizy progu.

fig.add_annotation(  # Dodajemy panel informacyjny z nazwą najlepszego modelu i jego najważniejszymi metrykami.
    x=0.5,  # Pozycjonujemy blok mniej więcej centralnie u góry figury.
    y=1.10,  # Ustawiamy go trochę nad siatką subplotów.
    xref="paper",  # Odnosimy pozycję do całej figury.
    yref="paper",  # Tak samo dla osi pionowej.
    showarrow=False,  # Wyłączamy strzałkę, bo to panel informacyjny.
    align="center",  # Wyrównujemy tekst centralnie.
    bgcolor="rgba(255,255,255,0.85)",  # Dodajemy jasne półprzezroczyste tło dla czytelności.
    bordercolor="rgba(0,0,0,0.12)",  # Dodajemy delikatne obramowanie.
    borderwidth=1,  # Włączamy cienką ramkę.
    text=(  # Budujemy treść panelu jako HTML.
        f"<b>Najlepszy model: {best_model_name}</b><br>"  # Pokazujemy nazwę zwycięskiego modelu.
        f"F1 = {results_df.loc[0, 'f1']:.3f} | "  # Pokazujemy F1 zwycięzcy.
        f"ROC AUC = {results_df.loc[0, 'roc_auc']:.3f} | "  # Pokazujemy ROC AUC zwycięzcy.
        f"PR AUC = {results_df.loc[0, 'pr_auc']:.3f} | "  # Pokazujemy PR AUC zwycięzcy.
        f"Najlepszy próg F1 = {best_threshold:.2f}"  # Pokazujemy optymalny próg decyzyjny dla F1.
    ),
)

fig.update_layout(  # Dopieszczamy finalny wygląd całego dashboardu.
    title="Premium dashboard: porównanie modeli klasyfikacyjnych",  # Ustawiamy główny tytuł figury.
    template="plotly_white",  # Wybieramy jasny, elegancki motyw bazowy.
    barmode="group",  # Grupujemy słupki różnych modeli obok siebie dla wygodnego porównania.
    height=1050,  # Nadajemy dashboardowi dużą wysokość, aby każdy panel miał wystarczająco dużo miejsca.
    width=1850,  # Nadajemy dashboardowi dużą szerokość, co poprawia czytelność złożonych paneli.
    legend=dict(  # Konfigurujemy legendę całej figury.
        title="Modele",  # Nadajemy legendzie tytuł.
        orientation="h",  # Ustawiamy legendę poziomo, bo przy wielu modelach zwykle wygląda to lepiej.
        yanchor="bottom",  # Kotwiczymy legendę od dołu.
        y=1.02,  # Umieszczamy legendę tuż nad dashboardem.
        xanchor="left",  # Kotwiczymy legendę od lewej strony.
        x=0.0,  # Ustawiamy legendę przy lewej krawędzi figury.
    ),
    margin=dict(l=50, r=30, t=140, b=50),  # Ustawiamy rozsądne marginesy, w tym większy górny margines na legendę i panel informacyjny.
)

html_path = OUTPUT_DIR / "03_dashboard_porownanie_modeli_premium.html"  # Definiujemy nazwę pliku HTML z dashboardem.
csv_path = OUTPUT_DIR / "03_dashboard_porownanie_modeli_premium_wyniki.csv"  # Definiujemy nazwę pliku CSV z wynikami modeli.
fig.write_html(html_path, include_plotlyjs="cdn")  # Zapisujemy dashboard do pliku HTML, który można otworzyć w przeglądarce.
results_df.to_csv(csv_path, index=False)  # Zapisujemy tabelę wyników do CSV, aby łatwo wykorzystać ją dalej.

print("\n=== TABELA WYNIKÓW MODELI ===")  # Wypisujemy nagłówek tabeli w konsoli.
print(results_df.to_string(index=False))  # Pokazujemy wszystkie metryki modeli w uporządkowanej formie tekstowej.
print("\n=== PODSUMOWANIE NAJLEPSZEGO MODELU ===")  # Wypisujemy dodatkowy nagłówek dla zwycięzcy.
print(f"Najlepszy model według F1 : {best_model_name}")  # Informujemy, który model wygrał.
print(f"Najlepszy próg dla F1     : {best_threshold:.4f}")  # Informujemy, jaki próg dawał najwyższy F1.
print(f"Zapisano dashboard HTML  : {html_path}")  # Informujemy, gdzie zapisano dashboard.
print(f"Zapisano tabelę CSV      : {csv_path}")  # Informujemy, gdzie zapisano tabelę wyników.

fig.show()  # Otwieramy dashboard w domyślnym rendererze Plotly.