"""
Przykład 1: Interaktywny wykres 3D klastrów z użyciem Plotly.

Co pokazuje ten skrypt:
1. Tworzenie syntetycznych danych z trzema cechami liczbowymi.
2. Grupowanie danych algorytmem KMeans.
3. Wyświetlenie wyniku w postaci interaktywnego wykresu 3D.
4. Dodanie informacji pomocniczych: nazw punktów, etykiet klastrów i środków klastrów.

Uruchomienie:
    python 01_plotly_3d_klastry.py

Wymagane biblioteki:
    pip install numpy pandas scikit-learn plotly
"""

from sklearn.datasets import make_blobs  # Importujemy generator danych syntetycznych, aby szybko przygotować przykładowy zbiór do klastrowania.
from sklearn.cluster import KMeans  # Importujemy algorytm KMeans, który będzie przypisywał punkty do grup na podstawie podobieństwa.
from sklearn.preprocessing import StandardScaler  # Importujemy standaryzację, aby każda cecha miała porównywalną skalę.
import pandas as pd  # Importujemy pandas, ponieważ wygodnie przechowuje dane tabelaryczne i ułatwia przekazywanie ich do Plotly.
import plotly.express as px  # Importujemy plotly.express, bo pozwala bardzo szybko budować efektowne wykresy interaktywne.
import plotly.graph_objects as go  # Importujemy graph_objects, aby dodać do wykresu niestandardowe elementy, np. środki klastrów.

RANDOM_STATE = 42  # Ustalamy ziarno losowości, żeby wynik był powtarzalny przy każdym uruchomieniu skryptu.
N_SAMPLES = 450  # Ustalamy liczbę obserwacji, aby mieć wystarczająco dużo punktów do atrakcyjnej wizualizacji.
N_CLUSTERS = 4  # Określamy liczbę klastrów, które chcemy znaleźć algorytmem KMeans.

X, y_true = make_blobs(  # Generujemy sztuczny zbiór danych z wyraźnie zarysowanymi skupiskami.
    n_samples=N_SAMPLES,  # Podajemy liczbę rekordów, które mają zostać utworzone.
    centers=N_CLUSTERS,  # Podajemy liczbę rzeczywistych centrów generowanych skupisk.
    n_features=3,  # Tworzymy dokładnie trzy cechy, aby dało się je pokazać bezpośrednio na wykresie 3D.
    cluster_std=1.4,  # Sterujemy rozproszeniem punktów wokół środka klastra; wyższa wartość daje bardziej "miękkie" grupy.
    random_state=RANDOM_STATE,  # Zapewniamy odtwarzalność danych.
)

scaler = StandardScaler()  # Tworzymy obiekt standaryzacji, aby każda cecha była liczona na tej samej skali.
X_scaled = scaler.fit_transform(X)  # Uczymy standaryzację na danych i od razu przekształcamy dane wejściowe.

kmeans = KMeans(  # Tworzymy model KMeans, który będzie szukał centrów klastrów.
    n_clusters=N_CLUSTERS,  # Informujemy model, ile grup ma odszukać.
    n_init=20,  # Uruchamiamy algorytm z wieloma startami, aby zmniejszyć ryzyko słabego lokalnego optimum.
    random_state=RANDOM_STATE,  # Ustalamy ziarno losowości także dla KMeans.
)

cluster_labels = kmeans.fit_predict(X_scaled)  # Trenujemy model i od razu pobieramy przewidywany numer klastra dla każdego punktu.
cluster_centers = kmeans.cluster_centers_  # Odczytujemy współrzędne środków klastrów już w przeskalowanej przestrzeni cech.

df = pd.DataFrame(X_scaled, columns=["cecha_1", "cecha_2", "cecha_3"])  # Zamieniamy macierz danych na tabelę z czytelnymi nazwami kolumn.
df["klaster"] = cluster_labels.astype(str)  # Zamieniamy numer klastra na tekst, aby Plotly traktował go jako kategorię kolorystyczną.
df["klaster_rzeczywisty"] = y_true.astype(str)  # Dodajemy także etykietę "prawdziwego" skupiska, żeby móc ją pokazać w dymku po najechaniu.
df["id_punktu"] = [f"Punkt {i}" for i in range(len(df))]  # Tworzymy prosty identyfikator punktu, który będzie widoczny w podpowiedzi hover.

fig = px.scatter_3d(  # Budujemy interaktywny wykres punktowy 3D.
    df,  # Przekazujemy całą tabelę z cechami i dodatkowymi informacjami.
    x="cecha_1",  # Oś X ma prezentować pierwszą cechę po standaryzacji.
    y="cecha_2",  # Oś Y ma prezentować drugą cechę po standaryzacji.
    z="cecha_3",  # Oś Z ma prezentować trzecią cechę po standaryzacji.
    color="klaster",  # Kolorujemy punkty według klastra przewidzianego przez KMeans.
    hover_name="id_punktu",  # W nagłówku okna hover pokażemy identyfikator punktu.
    hover_data={  # Konfigurujemy dodatkowe dane, które pojawią się po najechaniu kursorem.
        "cecha_1":":.2f",  # Pierwszą cechę pokazujemy z dokładnością do dwóch miejsc po przecinku.
        "cecha_2":":.2f",  # Drugą cechę także pokazujemy z dokładnością do dwóch miejsc po przecinku.
        "cecha_3":":.2f",  # Trzecią cechę także formatujemy czytelnie.
        "klaster": True,  # Wyświetlamy numer klastra przypisanego przez model.
        "klaster_rzeczywisty": True,  # Wyświetlamy również informację o sztucznie wygenerowanej grupie "oryginalnej".
    },
    title="Plotly 3D: grupowanie punktów algorytmem KMeans",  # Ustawiamy tytuł wykresu, aby od razu było wiadomo, co jest prezentowane.
    opacity=0.80,  # Delikatnie zwiększamy przezroczystość punktów, co pomaga przy nakładaniu się markerów.
)

fig.update_traces(  # Modyfikujemy wygląd wszystkich śladów punktowych dodanych przez Plotly Express.
    marker=dict(size=5),  # Ustawiamy rozmiar punktów tak, aby były dobrze widoczne, ale nie zasłaniały całego wykresu.
)

fig.add_trace(  # Dodajemy kolejny ślad do wykresu: środki klastrów znalezione przez KMeans.
    go.Scatter3d(  # Używamy obiektu Scatter3d, bo środki klastrów też chcemy pokazać jako punkty w przestrzeni 3D.
        x=cluster_centers[:, 0],  # Współrzędne X środków klastrów pobieramy z pierwszej kolumny macierzy centrów.
        y=cluster_centers[:, 1],  # Współrzędne Y środków klastrów pobieramy z drugiej kolumny.
        z=cluster_centers[:, 2],  # Współrzędne Z środków klastrów pobieramy z trzeciej kolumny.
        mode="markers+text",  # Chcemy pokazać zarówno sam marker, jak i opis tekstowy przy każdym środku.
        marker=dict(size=10, symbol="diamond", color="black"),  # Środki klastrów wyróżniamy większym, czarnym markerem o kształcie rombu.
        text=[f"Środek {i}" for i in range(N_CLUSTERS)],  # Generujemy etykiety opisujące kolejne środki klastrów.
        textposition="top center",  # Ustawiamy podpis nad markerem, aby nie zasłaniał punktu.
        name="Środki klastrów",  # Nadajemy legendzie czytelną nazwę dodatkowego elementu wykresu.
        hovertemplate=(  # Definiujemy własny szablon podpowiedzi hover dla środków klastrów.
            "<b>%{text}</b><br>"  # W pierwszej linii pogrubiamy nazwę środka.
            "cecha_1: %{x:.2f}<br>"  # Pokazujemy współrzędną X środka z dwoma miejscami po przecinku.
            "cecha_2: %{y:.2f}<br>"  # Pokazujemy współrzędną Y.
            "cecha_3: %{z:.2f}<extra></extra>"  # Pokazujemy współrzędną Z i usuwamy domyślny dodatkowy podpis Plotly.
        ),
    )
)

fig.update_layout(  # Konfigurujemy układ całej figury, aby była bardziej estetyczna i czytelna.
    scene=dict(  # Sekcja "scene" odpowiada za ustawienia sceny 3D.
        xaxis_title="Cecha 1 (po standaryzacji)",  # Opisujemy oś X, aby odbiorca wiedział, co ogląda.
        yaxis_title="Cecha 2 (po standaryzacji)",  # Opisujemy oś Y.
        zaxis_title="Cecha 3 (po standaryzacji)",  # Opisujemy oś Z.
        bgcolor="rgba(245,245,245,1)",  # Ustawiamy jasne tło sceny 3D, co poprawia kontrast markerów.
    ),
    legend_title_text="Legenda",  # Ustawiamy czytelny tytuł legendy.
    margin=dict(l=0, r=0, b=0, t=60),  # Zmniejszamy marginesy, aby wykres zajmował więcej miejsca na ekranie.
)

output_html = "01_plotly_3d_klastry.html"  # Określamy nazwę pliku HTML, do którego zapiszemy gotową wizualizację.
fig.write_html(output_html)  # Zapisujemy wykres jako samodzielny plik HTML, który można otworzyć w dowolnej przeglądarce.
print(f"Zapisano interaktywny wykres do pliku: {output_html}")  # Informujemy użytkownika, gdzie znajduje się wynik.
fig.show()  # Otwieramy wykres w domyślnym trybie renderowania środowiska, np. w przeglądarce lub notebooku.
