"""
Przykład 2: Efektowna powierzchnia regresji 3D z użyciem PyVista.

Co pokazuje ten skrypt:
1. Generowanie danych dla problemu regresji z dwoma cechami wejściowymi.
2. Dopasowanie regresji wielomianowej do danych.
3. Wygenerowanie siatki punktów i przewidywanie wartości modelu na całej powierzchni.
4. Wyświetlenie:
   - punktów treningowych,
   - półprzezroczystej powierzchni modelu,
   - konturów wysokości,
   - dodatkowych osi i siatki pomocniczej.

Uruchomienie:
    python 02_pyvista_powierzchnia_regresji.py

Wymagane biblioteki:
    pip install numpy scikit-learn pyvista
"""

import numpy as np  # Importujemy NumPy, bo będzie potrzebny do generowania danych, siatki i operacji numerycznych.
import pyvista as pv  # Importujemy PyVista, ponieważ odpowiada za efektowną wizualizację 3D.
from sklearn.preprocessing import PolynomialFeatures  # Importujemy generator cech wielomianowych, aby model mógł dopasować zakrzywioną powierzchnię.
from sklearn.linear_model import LinearRegression  # Importujemy regresję liniową, która po rozszerzeniu cech stanie się regresją wielomianową.

RANDOM_STATE = 42  # Ustalamy ziarno losowości, aby dane były powtarzalne.
rng = np.random.default_rng(RANDOM_STATE)  # Tworzymy nowoczesny generator liczb losowych NumPy dla większej kontroli nad losowością.

n_samples = 250  # Ustalamy liczbę obserwacji, aby było ich dość dużo do pokazania chmury punktów.
x1 = rng.uniform(-3.0, 3.0, n_samples)  # Losujemy pierwszą cechę w określonym zakresie, aby pokryć dość szeroki obszar przestrzeni.
x2 = rng.uniform(-3.0, 3.0, n_samples)  # Losujemy drugą cechę z tego samego zakresu, aby dane były rozłożone na płaszczyźnie.

noise = rng.normal(0.0, 1.2, n_samples)  # Dodajemy szum losowy, żeby zadanie było bardziej realistyczne i nieidealnie gładkie.
y = (  # Definiujemy zależność celu od dwóch cech.
    3.5  # Dodajemy wyraz wolny, żeby powierzchnia nie zaczynała się od zera.
    + 1.8 * x1  # Dodajemy liniowy wpływ pierwszej cechy.
    - 2.2 * x2  # Dodajemy liniowy wpływ drugiej cechy z przeciwnym znakiem.
    + 0.9 * x1**2  # Dodajemy składnik kwadratowy pierwszej cechy, aby powierzchnia była zakrzywiona.
    - 0.6 * x2**2  # Dodajemy składnik kwadratowy drugiej cechy, aby uzyskać bardziej złożony kształt.
    + 0.7 * x1 * x2  # Dodajemy interakcję między cechami, żeby model uchwycił zależność mieszającą obie osie.
    + noise  # Dodajemy losowy szum, aby dane przypominały bardziej rzeczywisty problem regresji.
)

X = np.column_stack([x1, x2])  # Łączymy obie cechy w jedną macierz wejściową o dwóch kolumnach.

poly = PolynomialFeatures(degree=2, include_bias=False)  # Tworzymy transformację wielomianową stopnia 2 bez dodatkowej kolumny stałej.
X_poly = poly.fit_transform(X)  # Rozszerzamy zbiór cech o składniki kwadratowe i interakcje.

model = LinearRegression()  # Tworzymy model regresji liniowej, który na rozszerzonych cechach zadziała jak regresja wielomianowa.
model.fit(X_poly, y)  # Uczymy model na danych treningowych.

grid_size = 80  # Ustalamy liczbę punktów siatki wzdłuż każdej osi; większa wartość daje gładszą powierzchnię.
x1_grid = np.linspace(x1.min(), x1.max(), grid_size)  # Tworzymy równomierny zakres wartości pierwszej cechy dla siatki predykcyjnej.
x2_grid = np.linspace(x2.min(), x2.max(), grid_size)  # Tworzymy równomierny zakres wartości drugiej cechy dla siatki predykcyjnej.
X1_mesh, X2_mesh = np.meshgrid(x1_grid, x2_grid)  # Tworzymy dwuwymiarową siatkę wszystkich kombinacji wartości x1 i x2.

grid_points = np.column_stack([X1_mesh.ravel(), X2_mesh.ravel()])  # Spłaszczamy siatkę do listy punktów, aby przekazać je modelowi.
grid_points_poly = poly.transform(grid_points)  # Rozszerzamy punkty siatki o te same cechy wielomianowe co dane treningowe.
y_pred_grid = model.predict(grid_points_poly)  # Obliczamy przewidywaną wartość modelu dla każdego punktu siatki.
Y_mesh = y_pred_grid.reshape(X1_mesh.shape)  # Przywracamy wyniki do kształtu siatki 2D, aby dało się zbudować powierzchnię 3D.

surface_grid = pv.StructuredGrid(X1_mesh, X2_mesh, Y_mesh)  # Tworzymy uporządkowaną siatkę 3D reprezentującą powierzchnię predykcji modelu.
surface_grid["predykcja"] = Y_mesh.ravel(order="F")  # Dodajemy do siatki wartości pola, aby można było kolorować powierzchnię według wysokości.

points_3d = np.column_stack([x1, x2, y])  # Łączymy dane treningowe w chmurę punktów 3D.
point_cloud = pv.PolyData(points_3d)  # Tworzymy obiekt PolyData, bo PyVista rysuje chmury punktów właśnie w tej postaci.
point_cloud["wartosc_y"] = y  # Do punktów dopinamy wartości celu, aby można było ich użyć do kolorowania lub analizy.

contours = surface_grid.contour(isosurfaces=10)  # Tworzymy linie konturowe na powierzchni, które pomagają dostrzec różnice wysokości.

plotter = pv.Plotter(window_size=(1400, 900))  # Tworzymy okno renderujące o dużym rozmiarze, aby scena była bardziej efektowna.
plotter.set_background("white")  # Ustawiamy białe tło, bo zwykle dobrze eksponuje kolorowaną powierzchnię i czarne osie.

plotter.add_mesh(  # Dodajemy samą powierzchnię predykcji modelu.
    surface_grid,  # Przekazujemy siatkę reprezentującą model regresyjny.
    scalars="predykcja",  # Kolorujemy powierzchnię zgodnie z przewidywaną wartością y.
    opacity=0.78,  # Ustawiamy półprzezroczystość, aby lepiej było widać relację z punktami treningowymi.
    show_edges=False,  # Ukrywamy krawędzie siatki, bo gładka powierzchnia wygląda bardziej elegancko.
    smooth_shading=True,  # Włączamy wygładzanie cieniowania, aby model wyglądał bardziej "premium".
    cmap="viridis",  # Ustawiamy popularną mapę kolorów, która dobrze pokazuje zmiany wysokości.
)

plotter.add_mesh(  # Dodajemy do sceny punkty treningowe.
    point_cloud,  # Przekazujemy chmurę punktów utworzoną z rzeczywistych obserwacji.
    render_points_as_spheres=True,  # Rysujemy punkty jako małe kulki 3D, a nie płaskie markery.
    point_size=12,  # Ustawiamy rozmiar punktów tak, aby były dobrze widoczne na tle powierzchni.
    color="black",  # Nadajemy punktom czarny kolor, aby wyraźnie kontrastowały z kolorową powierzchnią.
)

plotter.add_mesh(  # Dodajemy kontury wysokości jako dodatkową warstwę informacyjną.
    contours,  # Przekazujemy zestaw linii konturowych wygenerowanych na podstawie powierzchni.
    color="white",  # Ustawiamy biały kolor konturów, aby dobrze odcinały się od powierzchni.
    line_width=2,  # Pogrubiamy linie, aby były czytelne.
)

plotter.add_axes()  # Dodajemy osie 3D, dzięki którym łatwiej zorientować się w przestrzeni.
plotter.show_grid(  # Dodajemy siatkę pomocniczą i opisy osi.
    xtitle="Cecha x1",  # Opisujemy oś X jako pierwszą cechę wejściową.
    ytitle="Cecha x2",  # Opisujemy oś Y jako drugą cechę wejściową.
    ztitle="Wartość y",  # Opisujemy oś Z jako wartość przewidywaną lub obserwowaną.
)

plotter.add_text(  # Dodajemy podpis wyjaśniający, co dokładnie przedstawia scena.
    "PyVista 3D: regresja wielomianowa jako powierzchnia predykcji",  # Podajemy tytuł sceny renderowanej w oknie.
    position="upper_left",  # Ustawiamy tekst w lewym górnym rogu, żeby nie zasłaniał środka wykresu.
    font_size=12,  # Dobieramy rozmiar czcionki tak, by był czytelny, ale nienachalny.
)

screenshot_path = "02_pyvista_powierzchnia_regresji.png"  # Ustalamy nazwę pliku graficznego, do którego zapiszemy zrzut sceny.
plotter.show(screenshot=screenshot_path)  # Wyświetlamy okno interaktywne i jednocześnie zapisujemy zrzut ekranu do pliku.
print(f"Zapisano zrzut sceny do pliku: {screenshot_path}")  # Informujemy użytkownika, gdzie trafił zapisany obraz.
