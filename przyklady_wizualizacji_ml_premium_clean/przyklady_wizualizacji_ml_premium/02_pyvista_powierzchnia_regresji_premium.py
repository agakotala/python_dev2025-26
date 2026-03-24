"""
Przykład PREMIUM 2: Renderowana powierzchnia regresji 3D w PyVista.

Ten skrypt ma pokazać bardziej „widowiskową” wizualizację regresji:
1. generuje nieliniowe dane z dwoma cechami,
2. dopasowuje regresję wielomianową,
3. liczy podstawowe metryki błędu,
4. buduje siatkę 3D z predykcją modelu,
5. rysuje punkty, powierzchnię, kontury i linie reszt,
6. ustawia kamerę, oświetlenie i zapisuje zrzut sceny.

Uruchomienie:
    python 02_pyvista_powierzchnia_regresji_premium.py

Wymagane biblioteki:
    pip install numpy scikit-learn pyvista vtk
"""

from pathlib import Path  # Importujemy Path, aby wygodnie pracować na ścieżkach katalogów i plików wynikowych.

import numpy as np  # Importujemy NumPy, bo będziemy generować dane, siatki i wykonywać obliczenia numeryczne.
import pyvista as pv  # Importujemy PyVista, ponieważ odpowiada za wizualizację 3D i rendering sceny.
from sklearn.linear_model import LinearRegression  # Importujemy regresję liniową, która po rozszerzeniu cech stworzy model wielomianowy.
from sklearn.metrics import mean_absolute_error  # Importujemy MAE, aby pokazać średni bezwzględny błąd modelu.
from sklearn.metrics import mean_squared_error  # Importujemy MSE, aby policzyć błąd średniokwadratowy i z niego wyprowadzić RMSE.
from sklearn.metrics import r2_score  # Importujemy R2, aby ocenić, jak dobrze model wyjaśnia zmienność danych.
from sklearn.preprocessing import PolynomialFeatures  # Importujemy generator cech wielomianowych, aby model umiał odwzorować zakrzywioną powierzchnię.

RANDOM_STATE = 42  # Ustalamy ziarno losowości, aby dane i wynik były powtarzalne.
N_SAMPLES = 320  # Ustalamy liczbę obserwacji; to kompromis między czytelnością a gęstością danych.
GRID_RESOLUTION = 120  # Ustalamy rozdzielczość siatki powierzchni; większa wartość daje gładszą powierzchnię kosztem obliczeń.
POLY_DEGREE = 3  # Ustawiamy stopień wielomianu; trzeci stopień daje dość elastyczną, ale jeszcze zrozumiałą powierzchnię.
OUTPUT_DIR = Path(__file__).resolve().parent / "wyniki"  # Tworzymy ścieżkę do katalogu z wynikami obok pliku skryptu.
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  # Upewniamy się, że katalog wynikowy istnieje.

rng = np.random.default_rng(RANDOM_STATE)  # Tworzymy generator liczb losowych NumPy, aby wygodnie losować dane wejściowe i szum.

x1 = rng.uniform(-4.0, 4.0, N_SAMPLES)  # Losujemy pierwszą cechę w szerokim zakresie, aby powierzchnia była rozciągnięta w osi X.
x2 = rng.uniform(-4.0, 4.0, N_SAMPLES)  # Losujemy drugą cechę w podobnym zakresie, aby dobrze pokryć płaszczyznę wejściową.
noise = rng.normal(0.0, 1.35, N_SAMPLES)  # Generujemy szum, dzięki któremu problem regresji jest bardziej realistyczny.

y = (  # Definiujemy „prawdziwą” nieliniową zależność celu od dwóch cech wejściowych.
    8.0  # Dodajemy wyraz wolny, aby powierzchnia nie przechodziła przez zero.
    + 1.8 * x1  # Dodajemy wpływ liniowy pierwszej cechy.
    - 2.4 * x2  # Dodajemy wpływ liniowy drugiej cechy z przeciwnym znakiem.
    + 0.65 * x1**2  # Dodajemy składnik kwadratowy pierwszej cechy, który zakrzywia powierzchnię.
    - 0.55 * x2**2  # Dodajemy składnik kwadratowy drugiej cechy z przeciwnym znakiem.
    + 0.45 * x1 * x2  # Dodajemy interakcję cech, żeby model musiał uchwycić zależność łączną.
    - 0.08 * x1**3  # Dodajemy składnik sześcienny, dzięki któremu powierzchnia staje się bardziej „organiczna”.
    + 0.06 * x2**3  # Dodajemy drugi składnik sześcienny, aby krzywizna była bardziej złożona.
    + noise  # Na końcu dokładamy losowy szum, który imituje błędy pomiarowe i naturalne odchylenia.
)

X = np.column_stack([x1, x2])  # Łączymy obie cechy wejściowe w jedną macierz, której oczekuje scikit-learn.

poly = PolynomialFeatures(degree=POLY_DEGREE, include_bias=False)  # Tworzymy generator cech wielomianowych bez dodatkowej stałej kolumny bias.
X_poly = poly.fit_transform(X)  # Rozszerzamy dane wejściowe o potęgi i interakcje potrzebne do opisania krzywej powierzchni.

model = LinearRegression()  # Tworzymy model regresji liniowej, który po rozszerzeniu cech stanie się regresją wielomianową.
model.fit(X_poly, y)  # Uczymy model na rozszerzonych cechach i wartościach docelowych.

y_pred_train = model.predict(X_poly)  # Liczymy predykcje modelu dla danych treningowych, aby ocenić jakość dopasowania.
r2 = r2_score(y, y_pred_train)  # Liczymy współczynnik determinacji R2.
mae = mean_absolute_error(y, y_pred_train)  # Liczymy średni bezwzględny błąd modelu.
rmse = np.sqrt(mean_squared_error(y, y_pred_train))  # Liczymy pierwiastek z MSE, czyli RMSE, aby błąd był w tych samych jednostkach co target.
residuals = y - y_pred_train  # Wyznaczamy reszty, czyli różnice między obserwacją a predykcją modelu.

x1_grid = np.linspace(x1.min() - 0.5, x1.max() + 0.5, GRID_RESOLUTION)  # Tworzymy równomierny zakres wartości osi X dla siatki powierzchni.
x2_grid = np.linspace(x2.min() - 0.5, x2.max() + 0.5, GRID_RESOLUTION)  # Tworzymy analogiczny zakres wartości osi Y dla siatki.
xx, yy = np.meshgrid(x1_grid, x2_grid)  # Budujemy pełną siatkę 2D punktów wejściowych, po których policzymy model.

grid_points = np.column_stack([xx.ravel(), yy.ravel()])  # Spłaszczamy siatkę i łączymy współrzędne w macierz wejściową do predykcji.
grid_points_poly = poly.transform(grid_points)  # Rozszerzamy punkty siatki o cechy wielomianowe zgodne z treningiem modelu.
zz = model.predict(grid_points_poly).reshape(xx.shape)  # Liczymy predykcję modelu dla całej siatki i odtwarzamy ją do kształtu 2D.

surface_grid = pv.StructuredGrid(xx, yy, zz)  # Tworzymy uporządkowaną siatkę PyVista, która posłuży jako powierzchnia modelu.
surface_grid["wartosc_modelu"] = zz.ravel(order="F")  # Dodajemy wartości skalarne do powierzchni, aby dało się ją kolorować według wysokości.

point_cloud = pv.PolyData(np.column_stack([x1, x2, y]))  # Budujemy chmurę punktów 3D z rzeczywistych obserwacji treningowych.
point_cloud["reszta"] = residuals  # Dodajemy do punktów wartość reszty, żeby dało się np. kolorować punkty błędem.
point_cloud["target"] = y  # Zachowujemy też docelową wartość y jako dodatkowy atrybut punktu.

sample_size = 50  # Ustalamy liczbę linii reszt, aby pokazać błędy modelu, ale nie przeładować sceny wizualnie.
sample_indices = rng.choice(N_SAMPLES, size=sample_size, replace=False)  # Losujemy podzbiór punktów, dla których narysujemy pionowe odcinki reszt.

residual_segments = []  # Tworzymy pustą listę, do której będziemy odkładać pojedyncze odcinki pokazujące błąd modelu.

for idx in sample_indices:  # Iterujemy po wylosowanych punktach, aby dla każdego zbudować osobny odcinek.
    start_point = np.array([x1[idx], x2[idx], y_pred_train[idx]])  # Punkt startowy ustawiamy na powierzchni modelu, czyli w miejscu przewidywania.
    end_point = np.array([x1[idx], x2[idx], y[idx]])  # Punkt końcowy ustawiamy w rzeczywistej obserwacji treningowej.
    residual_line = pv.Line(start_point, end_point)  # Tworzymy linię łączącą predykcję z wartością rzeczywistą.
    residual_segments.append(residual_line)  # Odkładamy gotowy odcinek do listy wszystkich linii reszt.

residual_lines = residual_segments[0]  # Bierzemy pierwszy odcinek jako początek łączonego obiektu.

for segment in residual_segments[1:]:  # Iterujemy po wszystkich pozostałych odcinkach.
    residual_lines = residual_lines.merge(segment)  # Łączymy kolejne odcinki w jeden obiekt, żeby łatwo dodać je do sceny.

contours = surface_grid.contour(  # Wyznaczamy linie konturowe na powierzchni modelu, aby lepiej pokazać jej „topografię”.
    isosurfaces=10  # Prosimy o wygenerowanie dziesięciu poziomic, co zwykle daje dobry kompromis między informacją a czytelnością.
)

pv.set_plot_theme("document")  # Ustawiamy motyw „document”, który daje elegancki, jasny wygląd sceny.
plotter = pv.Plotter(window_size=(1600, 1000), off_screen=False)  # Tworzymy okno renderujące o dużym rozmiarze, aby wynik był czytelny i „premium”.

plotter.set_background("#f6f8fb")  # Ustawiamy jasne tło sceny, dzięki któremu kolory powierzchni i punktów lepiej się wyróżniają.
plotter.add_axes(line_width=2, labels_off=False)  # Dodajemy osie 3D, żeby użytkownik zawsze wiedział, jak jest ustawiona scena.
plotter.show_grid(color="#D9DDE3")  # Włączamy delikatną siatkę pomocniczą, która ułatwia ocenę położenia punktów i powierzchni.

plotter.add_mesh(  # Dodajemy główną powierzchnię regresji do sceny.
    surface_grid,  # Przekazujemy przygotowaną siatkę powierzchni.
    scalars="wartosc_modelu",  # Kolor powierzchni uzależniamy od wysokości przewidywanej przez model.
    cmap="viridis",  # Wybieramy mapę kolorów, która dobrze oddaje przejścia wysokości.
    opacity=0.82,  # Ustawiamy lekką przezroczystość, aby punkty i część wnętrza sceny nadal były widoczne.
    show_edges=False,  # Wyłączamy krawędzie każdej komórki siatki, aby powierzchnia wyglądała gładko i profesjonalnie.
    smooth_shading=True,  # Włączamy wygładzanie cieniowania, aby powierzchnia wyglądała bardziej „renderowo”.
    scalar_bar_args={  # Konfigurujemy pasek kolorów opisujący wysokość modelu.
        "title": "Wartość modelu",  # Nadajemy czytelny tytuł skali kolorów.
        "vertical": True,  # Ustawiamy pionowy pasek, który dobrze pasuje do układu sceny.
        "position_x": 0.88,  # Delikatnie przesuwamy pasek kolorów w prawo.
        "position_y": 0.12,  # Ustawiamy pozycję pionową paska.
        "height": 0.68,  # Ustawiamy wysokość paska, aby nie dominował sceny.
    },
)

plotter.add_mesh(  # Dodajemy rzeczywiste punkty treningowe.
    point_cloud,  # Przekazujemy chmurę punktów jako obiekt PolyData.
    scalars="reszta",  # Kolor punktu uzależniamy od reszty, aby błędy modelu były od razu widoczne wizualnie.
    cmap="coolwarm",  # Wybieramy mapę kolorów dobrze pokazującą wartości dodatnie i ujemne.
    render_points_as_spheres=True,  # Włączamy renderowanie markerów jako kulek, co wygląda bardziej przestrzennie niż płaskie punkty.
    point_size=12,  # Ustawiamy rozmiar punktów tak, aby były dobrze widoczne nad powierzchnią.
    opacity=0.95,  # Zostawiamy prawie pełną nieprzezroczystość, aby dane treningowe były wyraźne.
)

plotter.add_mesh(  # Dodajemy kontury powierzchni jako osobną warstwę.
    contours,  # Przekazujemy obiekt z poziomicami wygenerowanymi z siatki.
    color="black",  # Rysujemy kontury na czarno, aby dobrze odcinały się od kolorowej powierzchni.
    line_width=2,  # Ustawiamy trochę grubszą linię dla czytelności.
    opacity=0.35,  # Kontury robimy częściowo przezroczyste, aby nie dominowały wizualnie.
)

plotter.add_mesh(  # Dodajemy pionowe odcinki pokazujące reszty modelu.
    residual_lines,  # Przekazujemy połączony obiekt z liniami błędów.
    color="#444444",  # Rysujemy je ciemnoszarym kolorem, aby były widoczne, ale nie zbyt ciężkie optycznie.
    line_width=3,  # Ustawiamy linię na tyle grubą, by dobrze pokazywała odchylenia od powierzchni.
    opacity=0.45,  # Zmniejszamy krycie, aby odcinki nie „krzyczały” mocniej niż sama powierzchnia.
)

plotter.add_text(  # Dodajemy tekstowe podsumowanie metryk bezpośrednio w scenie.
    f"R2 = {r2:.3f}\nMAE = {mae:.3f}\nRMSE = {rmse:.3f}\nStopień wielomianu = {POLY_DEGREE}",  # Wstawiamy najważniejsze liczby opisujące dopasowanie modelu.
    position="upper_left",  # Umieszczamy panel metryk w lewym górnym rogu okna.
    font_size=14,  # Wybieramy czytelny, ale nienachalny rozmiar tekstu.
    color="black",  # Czarny tekst na jasnym tle daje najlepszy kontrast.
)

plotter.camera_position = [  # Ustawiamy ręcznie pozycję kamery, aby scena po uruchomieniu wyglądała efektownie.
    (12.0, 11.0, 16.0),  # Pozycja kamery w przestrzeni 3D.
    (0.0, 0.0, np.mean(zz)),  # Punkt, na który patrzy kamera; kierujemy wzrok mniej więcej na środek powierzchni.
    (0.0, 0.0, 1.0),  # Wektor „góry” kamery; dzięki niemu scena nie będzie przekręcona.
]

plotter.enable_anti_aliasing()  # Włączamy wygładzanie krawędzi, aby scena wyglądała bardziej profesjonalnie.

light_main = pv.Light(position=(10, 8, 15), focal_point=(0, 0, np.mean(zz)), color="white", intensity=1.0)  # Dodajemy główne źródło światła padające z góry i z boku.
light_fill = pv.Light(position=(-8, -6, 10), focal_point=(0, 0, np.mean(zz)), color="#f7f4e8", intensity=0.6)  # Dodajemy drugie, cieplejsze światło do delikatnego doświetlenia cieni.
plotter.add_light(light_main)  # Dodajemy główne światło do sceny.
plotter.add_light(light_fill)  # Dodajemy światło uzupełniające.

screenshot_path = OUTPUT_DIR / "02_pyvista_powierzchnia_regresji_premium.png"  # Ustalamy nazwę pliku z zapisanym zrzutem sceny.

print("\n=== METRYKI MODELU ===")  # Wypisujemy nagłówek metryk w konsoli.
print(f"R2   : {r2:.4f}")  # Pokazujemy R2.
print(f"MAE  : {mae:.4f}")  # Pokazujemy MAE.
print(f"RMSE : {rmse:.4f}")  # Pokazujemy RMSE.
print(f"\nPlik PNG po użyciu opcji zapisu: {screenshot_path}")  # Informujemy, gdzie zostanie zapisany screenshot, jeśli użytkownik wywoła zapis.

# Uwaga praktyczna:
# Metoda show() uruchamia okno interaktywne. W wielu środowiskach graficznych można z tego okna
# ręcznie zapisać scenę albo odkomentować poniższą linię i zapisać screenshot automatycznie.
# plotter.screenshot(str(screenshot_path))

plotter.show(title="Premium 3D: powierzchnia regresji wielomianowej")  # Otwieramy interaktywne okno z gotową sceną 3D.