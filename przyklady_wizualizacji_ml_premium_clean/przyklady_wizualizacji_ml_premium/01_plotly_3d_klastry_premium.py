"""
Przykład PREMIUM 1: Interaktywny eksplorator klastrów 3D w Plotly.

Ten skrypt robi więcej niż prosty wykres punktowy.
Pokazuje pełny mini-workflow analizy grupowania:
1. generuje dane 3D o różnej gęstości i różnym położeniu,
2. skaluje dane, żeby odległości w KMeans miały sens,
3. trenuje model KMeans,
4. liczy jakościowe miary klastrowania,
5. buduje bogaty, interaktywny wykres 3D,
6. zapisuje wynik do samodzielnego pliku HTML,
7. wypisuje podsumowanie klastrów do konsoli.

Uruchomienie:
    python 01_plotly_3d_klastry_premium.py

Wymagane biblioteki:
    pip install numpy pandas scikit-learn plotly
"""

from pathlib import Path  # Importujemy Path, aby wygodnie budować ścieżki do katalogów i plików wynikowych bez ręcznego składania tekstu.

import numpy as np  # Importujemy NumPy, bo będzie potrzebny do operacji numerycznych, liczenia odległości i pracy na macierzach.
import pandas as pd  # Importujemy pandas, ponieważ wygodnie przechowuje dane tabelaryczne i ułatwia późniejsze raportowanie wyników.
import plotly.graph_objects as go  # Importujemy graph_objects, bo daje pełną kontrolę nad każdym elementem bogatego wykresu 3D.
from sklearn.cluster import KMeans  # Importujemy KMeans, ponieważ ten algorytm będzie grupował punkty na podstawie podobieństwa.
from sklearn.datasets import make_blobs  # Importujemy make_blobs, aby łatwo wygenerować syntetyczny zbiór danych z wyraźnymi skupiskami.
from sklearn.metrics import calinski_harabasz_score  # Importujemy tę metrykę, żeby dodatkowo ocenić separację klastrów.
from sklearn.metrics import davies_bouldin_score  # Importujemy tę metrykę, żeby pokazać jeszcze jedną perspektywę oceny jakości grupowania.
from sklearn.metrics import silhouette_score  # Importujemy silhouette score, bo to jedna z najbardziej intuicyjnych miar jakości klastrowania.
from sklearn.preprocessing import StandardScaler  # Importujemy standaryzację, aby wszystkie cechy miały porównywalną skalę.

RANDOM_STATE = 42  # Ustalamy stałe ziarno losowości, aby dane i wynik modelu były odtwarzalne przy każdym uruchomieniu.
N_SAMPLES = 700  # Określamy liczbę obserwacji; większa liczba daje gęstszy i atrakcyjniejszy wykres.
N_CLUSTERS = 5  # Określamy liczbę klastrów, których będzie szukał model KMeans.
OUTPUT_DIR = Path(__file__).resolve().parent / "wyniki"  # Tworzymy ścieżkę do katalogu wynikowego obok skryptu, aby wszystkie artefakty były w jednym miejscu.
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  # Tworzymy katalog, jeśli jeszcze nie istnieje, aby zapis plików nie zakończył się błędem.

centers = [  # Definiujemy ręcznie położenie centrów, aby skupiska były bardziej malownicze niż przy pełnej losowości.
    (-7.0, -5.0, -2.0),  # Pierwsze centrum umieszczamy w lewej dolnej części przestrzeni 3D.
    (-2.5, 4.0, 3.5),  # Drugie centrum ustawiamy wyżej i bardziej z tyłu, aby klastry dobrze się rozdzielały w przestrzeni.
    (3.0, -1.0, 5.5),  # Trzecie centrum przesuwamy w dodatnie wartości osi X i Z.
    (7.5, 5.0, -4.0),  # Czwarte centrum ląduje daleko po prawej stronie i niżej na osi Z.
    (1.5, 7.0, -7.0),  # Piąte centrum ustawiamy wysoko na osi Y i nisko na osi Z, żeby scena była bardziej trójwymiarowa.
]

cluster_std = [0.90, 1.50, 1.10, 1.80, 1.20]  # Ustawiamy różne odchylenia standardowe, aby klastry miały różną gęstość i wyglądały bardziej realistycznie.

X, y_true = make_blobs(  # Generujemy syntetyczne dane w formie chmury punktów z kilkoma skupiskami.
    n_samples=N_SAMPLES,  # Podajemy liczbę rekordów, które mają zostać wygenerowane.
    centers=centers,  # Podajemy ręcznie przygotowane centra klastrów.
    cluster_std=cluster_std,  # Określamy rozrzut punktów wokół każdego środka.
    n_features=3,  # Tworzymy dokładnie trzy cechy, ponieważ chcemy pokazać dane bezpośrednio na wykresie 3D.
    random_state=RANDOM_STATE,  # Ustawiamy ziarno losowości dla pełnej powtarzalności zbioru.
)

scaler = StandardScaler()  # Tworzymy obiekt standaryzacji, ponieważ KMeans używa odległości i jest wrażliwy na skalę cech.
X_scaled = scaler.fit_transform(X)  # Uczymy skalowanie na danych i jednocześnie przekształcamy dane do wspólnej skali.

kmeans = KMeans(  # Tworzymy model KMeans, który będzie przypisywał punkty do najbliższych centrów.
    n_clusters=N_CLUSTERS,  # Informujemy model, ile klastrów ma znaleźć.
    n_init=30,  # Zwiększamy liczbę losowych startów, aby zmniejszyć ryzyko słabego lokalnego optimum.
    random_state=RANDOM_STATE,  # Ustawiamy ziarno losowości, aby także sam model był odtwarzalny.
)

cluster_labels = kmeans.fit_predict(X_scaled)  # Uczymy model na danych i od razu pobieramy numer klastra przypisany do każdego punktu.
cluster_centers_scaled = kmeans.cluster_centers_  # Pobieramy współrzędne środków klastrów w przeskalowanej przestrzeni cech.
cluster_centers_original = scaler.inverse_transform(cluster_centers_scaled)  # Cofamy standaryzację środków, aby dało się je interpretować także w oryginalnej skali.

silhouette = silhouette_score(X_scaled, cluster_labels)  # Liczymy silhouette score; im bliżej 1, tym punkty są lepiej dopasowane do swoich klastrów.
calinski = calinski_harabasz_score(X_scaled, cluster_labels)  # Liczymy indeks Calinskiego-Harabasza; wyższa wartość zwykle oznacza lepszą separację.
davies = davies_bouldin_score(X_scaled, cluster_labels)  # Liczymy indeks Daviesa-Bouldina; niższa wartość zwykle oznacza lepszą jakość klastrowania.
inertia = kmeans.inertia_  # Odczytujemy sumę kwadratów odległości od centroidów, czyli podstawową miarę wewnętrznego rozproszenia klastrów.

point_distances = np.linalg.norm(  # Liczymy odległość każdego punktu od centroidu klastra, do którego został przypisany.
    X_scaled - cluster_centers_scaled[cluster_labels],  # Dla każdego punktu odejmujemy współrzędne odpowiedniego centroidu.
    axis=1,  # Liczymy normę po osi cech, czyli jedną odległość dla każdego rekordu.
)

cluster_names = {  # Tworzymy mapę nazw klastrów, aby legenda i hover były bardziej eleganckie niż same numery.
    0: "Klaster A",  # Nadajemy nazwę pierwszemu klastrowi.
    1: "Klaster B",  # Nadajemy nazwę drugiemu klastrowi.
    2: "Klaster C",  # Nadajemy nazwę trzeciemu klastrowi.
    3: "Klaster D",  # Nadajemy nazwę czwartemu klastrowi.
    4: "Klaster E",  # Nadajemy nazwę piątemu klastrowi.
}

cluster_colors = [  # Definiujemy ręcznie kolory, aby scena wyglądała bardziej „premium” i spójnie.
    "#4C78A8",  # Stonowany niebieski dla pierwszego klastra.
    "#F58518",  # Pomarańczowy dla drugiego klastra.
    "#54A24B",  # Zielony dla trzeciego klastra.
    "#E45756",  # Czerwony dla czwartego klastra.
    "#B279A2",  # Fioletowy dla piątego klastra.
]

cluster_color_map = {  # Łączymy numer klastra z konkretnym kolorem.
    cluster_id: cluster_colors[cluster_id]  # Dla każdego identyfikatora zapisujemy odpowiadający mu kolor z listy.
    for cluster_id in range(N_CLUSTERS)  # Iterujemy po wszystkich klastrach.
}

df = pd.DataFrame(  # Budujemy tabelę danych, aby łatwo drukować statystyki i tworzyć podpowiedzi hover.
    X,  # Jako zawartość podajemy oryginalne dane wejściowe w skali naturalnej.
    columns=["cecha_x", "cecha_y", "cecha_z"],  # Nadajemy kolumnom czytelne nazwy odnoszące się do osi wykresu.
)

df["cecha_x_scaled"] = X_scaled[:, 0]  # Zapisujemy przeskalowaną pierwszą cechę do osobnej kolumny, aby dało się ją pokazać w hover.
df["cecha_y_scaled"] = X_scaled[:, 1]  # Zapisujemy przeskalowaną drugą cechę.
df["cecha_z_scaled"] = X_scaled[:, 2]  # Zapisujemy przeskalowaną trzecią cechę.
df["klaster_id"] = cluster_labels  # Zapisujemy numer klastra przewidziany przez model.
df["klaster_nazwa"] = df["klaster_id"].map(cluster_names)  # Zamieniamy numer klastra na przyjazną nazwę tekstową.
df["klaster_rzeczywisty"] = y_true  # Dodajemy etykietę „prawdziwego” generatora danych, aby można było porównać ją z wynikiem KMeans.
df["odleglosc_od_centroidu"] = point_distances  # Dodajemy odległość punktu od środka jego klastra jako dodatkową informację diagnostyczną.
df["id_punktu"] = [f"Punkt_{i:03d}" for i in range(len(df))]  # Generujemy identyfikatory punktów, żeby hover wyglądał bardziej profesjonalnie.

cluster_summary = (  # Budujemy tabelę podsumowującą każdy klaster, aby mieć także tekstowe podsumowanie poza wykresem.
    df.groupby(["klaster_id", "klaster_nazwa"], as_index=False)  # Grupujemy rekordy według numeru i nazwy klastra.
    .agg(  # Wyliczamy najważniejsze statystyki dla każdej grupy.
        liczba_punktow=("id_punktu", "count"),  # Liczymy liczbę punktów przypisanych do klastra.
        srednia_odleglosc=("odleglosc_od_centroidu", "mean"),  # Liczymy średnią odległość punktów od centroidu.
        min_x=("cecha_x", "min"),  # Liczymy minimalną wartość pierwszej cechy w klastrze.
        max_x=("cecha_x", "max"),  # Liczymy maksymalną wartość pierwszej cechy.
        min_y=("cecha_y", "min"),  # Liczymy minimalną wartość drugiej cechy.
        max_y=("cecha_y", "max"),  # Liczymy maksymalną wartość drugiej cechy.
        min_z=("cecha_z", "min"),  # Liczymy minimalną wartość trzeciej cechy.
        max_z=("cecha_z", "max"),  # Liczymy maksymalną wartość trzeciej cechy.
    )  # Kończymy agregację podsumowań.
    .sort_values("klaster_id")  # Sortujemy klastry po numerze, aby raport był stabilny i czytelny.
)

fig = go.Figure()  # Tworzymy pustą figurę, do której będziemy ręcznie dodawać wszystkie ślady wykresu.

for cluster_id in range(N_CLUSTERS):  # Iterujemy po wszystkich klastrach, aby każdy dodać jako osobny ślad do legendy.
    cluster_frame = df[df["klaster_id"] == cluster_id]  # Filtrujemy tabelę tak, aby pozostały tylko punkty z bieżącego klastra.

    fig.add_trace(  # Dodajemy ślad punktów należących do jednego klastra.
        go.Scatter3d(  # Wybieramy Scatter3d, bo chcemy pokazać chmurę punktów w trzech wymiarach.
            x=cluster_frame["cecha_x"],  # Oś X otrzymuje wartości pierwszej cechy w skali oryginalnej.
            y=cluster_frame["cecha_y"],  # Oś Y otrzymuje wartości drugiej cechy.
            z=cluster_frame["cecha_z"],  # Oś Z otrzymuje wartości trzeciej cechy.
            mode="markers",  # W tym śladzie rysujemy wyłącznie markery, bo każdy rekord to pojedynczy punkt.
            name=cluster_names[cluster_id],  # Nazwa śladu pojawi się w legendzie i pozwoli włączać/wyłączać widoczność klastra.
            marker=dict(  # Definiujemy wygląd markerów.
                size=5,  # Ustawiamy rozmiar punktu tak, aby był dobrze widoczny, ale nie zasłaniał sąsiadów.
                color=cluster_color_map[cluster_id],  # Każdemu klastrowi przypisujemy spójny kolor.
                opacity=0.82,  # Dodajemy lekką przezroczystość, żeby łatwiej widzieć zagęszczenia punktów.
                line=dict(width=0.5, color="rgba(255,255,255,0.35)"),  # Delikatny obrys sprawia, że punkty lepiej odcinają się od tła.
            ),
            customdata=np.column_stack(  # Budujemy własny pakiet danych, który wykorzystamy potem w hovertemplate.
                [
                    cluster_frame["id_punktu"],  # Przekazujemy identyfikator punktu.
                    cluster_frame["cecha_x_scaled"],  # Przekazujemy przeskalowaną wartość osi X.
                    cluster_frame["cecha_y_scaled"],  # Przekazujemy przeskalowaną wartość osi Y.
                    cluster_frame["cecha_z_scaled"],  # Przekazujemy przeskalowaną wartość osi Z.
                    cluster_frame["odleglosc_od_centroidu"],  # Przekazujemy odległość od centroidu.
                    cluster_frame["klaster_rzeczywisty"],  # Przekazujemy etykietę generatora danych.
                ]
            ),
            hovertemplate=(  # Definiujemy bardzo bogatą podpowiedź po najechaniu na punkt.
                "<b>%{customdata[0]}</b><br>"  # W pierwszej linii pokazujemy identyfikator punktu.
                "Klaster modelu: %{fullData.name}<br>"  # Pokazujemy nazwę klastra przewidzianego przez model.
                "Klaster generatora: %{customdata[5]}<br>"  # Pokazujemy etykietę „prawdziwej” grupy.
                "x (oryg.): %{x:.2f}<br>"  # Pokazujemy oryginalną współrzędną X.
                "y (oryg.): %{y:.2f}<br>"  # Pokazujemy oryginalną współrzędną Y.
                "z (oryg.): %{z:.2f}<br>"  # Pokazujemy oryginalną współrzędną Z.
                "x (scaled): %{customdata[1]:.2f}<br>"  # Pokazujemy przeskalowaną współrzędną X.
                "y (scaled): %{customdata[2]:.2f}<br>"  # Pokazujemy przeskalowaną współrzędną Y.
                "z (scaled): %{customdata[3]:.2f}<br>"  # Pokazujemy przeskalowaną współrzędną Z.
                "Odległość od centroidu: %{customdata[4]:.3f}<extra></extra>"  # Pokazujemy odległość od centroidu i usuwamy domyślny podpis Plotly.
            ),
        )
    )

fig.add_trace(  # Dodajemy ślad z centroidami, aby użytkownik widział geometryczne środki klastrów.
    go.Scatter3d(  # Ponownie używamy Scatter3d, bo centroid to też punkt w przestrzeni 3D.
        x=cluster_centers_original[:, 0],  # Na osi X umieszczamy oryginalne współrzędne centroidów po cofnięciu skali.
        y=cluster_centers_original[:, 1],  # Na osi Y umieszczamy drugą współrzędną centroidów.
        z=cluster_centers_original[:, 2],  # Na osi Z umieszczamy trzecią współrzędną centroidów.
        mode="markers+text",  # Chcemy widzieć i marker, i podpis tekstowy przy każdym centroidzie.
        name="Centroidy",  # Nadajemy śladowi nazwę widoczną w legendzie.
        text=[f"C{i}" for i in range(N_CLUSTERS)],  # Tworzymy krótkie podpisy C0, C1, C2... dla kolejnych centroidów.
        textposition="top center",  # Ustawiamy tekst nad markerem, aby nie zasłaniał samego punktu.
        marker=dict(  # Definiujemy wygląd centroidów.
            size=11,  # Centroidy robimy większe niż zwykłe punkty, żeby od razu rzucały się w oczy.
            symbol="diamond",  # Wybieramy kształt rombu, aby łatwo odróżnić centroid od obserwacji.
            color="black",  # Kolor czarny daje mocny kontrast wobec kolorowych punktów klastrów.
            line=dict(width=2, color="white"),  # Dodajemy biały obrys, który poprawia widoczność na ciemniejszym tle.
        ),
        customdata=np.column_stack(  # Przekazujemy dodatkowe dane do hovertemplate centroidów.
            [
                cluster_centers_scaled[:, 0],  # Przeskalowana współrzędna X centroidu.
                cluster_centers_scaled[:, 1],  # Przeskalowana współrzędna Y centroidu.
                cluster_centers_scaled[:, 2],  # Przeskalowana współrzędna Z centroidu.
            ]
        ),
        hovertemplate=(  # Budujemy własną podpowiedź dla centroidów.
            "<b>%{text}</b><br>"  # W pierwszej linii pokazujemy etykietę centroidu.
            "x (oryg.): %{x:.2f}<br>"  # Pokazujemy oryginalną współrzędną X.
            "y (oryg.): %{y:.2f}<br>"  # Pokazujemy oryginalną współrzędną Y.
            "z (oryg.): %{z:.2f}<br>"  # Pokazujemy oryginalną współrzędną Z.
            "x (scaled): %{customdata[0]:.2f}<br>"  # Pokazujemy przeskalowaną współrzędną X.
            "y (scaled): %{customdata[1]:.2f}<br>"  # Pokazujemy przeskalowaną współrzędną Y.
            "z (scaled): %{customdata[2]:.2f}<extra></extra>"  # Pokazujemy przeskalowaną współrzędną Z i wyłączamy dodatkowy podpis.
        ),
    )
)

fig.add_annotation(  # Dodajemy tekstowe podsumowanie metryk bezpośrednio na figurze.
    x=0.01,  # Pozycjonujemy blok informacyjny przy lewej krawędzi całej figury.
    y=0.99,  # Ustawiamy blok blisko górnej krawędzi, żeby od razu rzucał się w oczy.
    xref="paper",  # Korzystamy z układu „paper”, czyli odniesienia do całej figury, a nie do konkretnej osi.
    yref="paper",  # Tak samo dla współrzędnej pionowej.
    align="left",  # Wyrównujemy tekst do lewej, aby łatwo się go czytało.
    showarrow=False,  # Wyłączamy strzałkę, bo to ma być panel informacyjny, a nie wskazanie punktu.
    bgcolor="rgba(255,255,255,0.85)",  # Dodajemy półprzezroczyste jasne tło, aby tekst był czytelny nad wykresem.
    bordercolor="rgba(30,30,30,0.25)",  # Dodajemy delikatne obramowanie panelu informacyjnego.
    borderwidth=1,  # Ustawiamy cienką ramkę, by panel był wyraźny, ale nie ciężki wizualnie.
    text=(  # Tworzymy zawartość panelu w formie wielowierszowego tekstu HTML.
        "<b>Ocena klastrowania</b><br>"  # Nagłówek bloku informacyjnego.
        f"Silhouette: {silhouette:.3f}<br>"  # Pokazujemy silhouette score z trzema miejscami po przecinku.
        f"Calinski-Harabasz: {calinski:.1f}<br>"  # Pokazujemy indeks Calinskiego-Harabasza.
        f"Davies-Bouldin: {davies:.3f}<br>"  # Pokazujemy indeks Daviesa-Bouldina.
        f"Inertia: {inertia:.1f}"  # Pokazujemy inercję modelu.
    ),
)

fig.update_layout(  # Konfigurujemy finalny wygląd całej figury.
    title="Premium 3D: eksplorator klastrów KMeans z metrykami jakości",  # Ustawiamy główny tytuł wykresu.
    template="plotly_white",  # Wybieramy jasny motyw bazowy jako punkt startowy dla całej estetyki.
    legend=dict(  # Dostosowujemy wygląd legendy.
        title="Widoczne warstwy",  # Nadajemy legendzie czytelny tytuł.
        bgcolor="rgba(255,255,255,0.7)",  # Dodajemy lekko przezroczyste tło, żeby legenda była czytelna niezależnie od położenia.
        bordercolor="rgba(0,0,0,0.1)",  # Ustawiamy delikatny kolor obramowania legendy.
        borderwidth=1,  # Włączamy cienką ramkę legendy.
    ),
    margin=dict(l=0, r=0, b=0, t=70),  # Zmniejszamy marginesy, aby scena 3D zajęła możliwie dużo miejsca.
    scene=dict(  # Konfigurujemy samą scenę 3D.
        bgcolor="rgb(245,247,250)",  # Ustawiamy neutralne tło sceny, które dobrze eksponuje kolory punktów.
        xaxis=dict(  # Doprecyzowujemy wygląd osi X.
            title="Cecha X",  # Nadajemy osi X czytelny tytuł.
            showbackground=True,  # Włączamy tło płaszczyzny osi, aby scena miała więcej głębi.
            backgroundcolor="rgba(76,120,168,0.05)",  # Kolor tła płaszczyzny dobieramy bardzo subtelnie, aby nie dominował nad punktami.
            gridcolor="rgba(0,0,0,0.08)",  # Dodajemy delikatną siatkę pomocniczą.
        ),
        yaxis=dict(  # Konfigurujemy oś Y analogicznie do osi X.
            title="Cecha Y",  # Nadajemy osi Y tytuł.
            showbackground=True,  # Włączamy tło płaszczyzny.
            backgroundcolor="rgba(245,133,24,0.05)",  # Ustawiamy lekko pomarańczowe tło zgodne z estetyką wykresu.
            gridcolor="rgba(0,0,0,0.08)",  # Ustawiamy delikatną siatkę pomocniczą.
        ),
        zaxis=dict(  # Konfigurujemy oś Z.
            title="Cecha Z",  # Nadajemy osi Z tytuł.
            showbackground=True,  # Włączamy tło płaszczyzny osi Z.
            backgroundcolor="rgba(84,162,75,0.05)",  # Ustawiamy subtelny zielony odcień tła.
            gridcolor="rgba(0,0,0,0.08)",  # Włączamy siatkę pomocniczą.
        ),
        camera=dict(  # Ustawiamy domyślną pozycję kamery, aby scena od razu wyglądała atrakcyjnie po otwarciu.
            eye=dict(x=1.7, y=1.55, z=1.25)  # Kamera patrzy z lekkiego ukosu, co dobrze pokazuje relacje przestrzenne.
        ),
    ),
)

html_path = OUTPUT_DIR / "01_plotly_3d_klastry_premium.html"  # Ustalamy nazwę pliku HTML z interaktywną wizualizacją.
csv_path = OUTPUT_DIR / "01_plotly_3d_klastry_premium_podsumowanie.csv"  # Ustalamy nazwę pliku CSV z podsumowaniem klastrów.
fig.write_html(html_path, include_plotlyjs="cdn")  # Zapisujemy wykres do samodzielnego pliku HTML, który można otworzyć w przeglądarce.
cluster_summary.to_csv(csv_path, index=False)  # Zapisujemy podsumowanie klastrów do CSV, aby można było je wykorzystać dalej w analizie.

print("\n=== PODSUMOWANIE KLASTRÓW ===")  # Wypisujemy czytelny nagłówek w konsoli.
print(cluster_summary.to_string(index=False))  # Pokazujemy pełne podsumowanie każdego klastra w formie tabeli.
print("\n=== METRYKI KLASTROWANIA ===")  # Wypisujemy osobny nagłówek dla metryk jakości.
print(f"Silhouette score      : {silhouette:.4f}")  # Pokazujemy silhouette score w konsoli.
print(f"Calinski-Harabasz     : {calinski:.4f}")  # Pokazujemy indeks Calinskiego-Harabasza.
print(f"Davies-Bouldin        : {davies:.4f}")  # Pokazujemy indeks Daviesa-Bouldina.
print(f"Inertia               : {inertia:.4f}")  # Pokazujemy inercję modelu.
print(f"\nZapisano wykres HTML : {html_path}")  # Informujemy, gdzie zapisano interaktywną wizualizację.
print(f"Zapisano raport CSV   : {csv_path}")  # Informujemy, gdzie zapisano podsumowanie tabelaryczne.

fig.show()  # Otwieramy wykres w domyślnym rendererze Plotly, np. w przeglądarce albo w notebooku.