import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from zjazd_3.eda import kolumny_numeryczne

# 1. pobieranie danych
url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-03-31/beers.csv"

try:
    df = pd.read_csv(url)
    print('dane pobrane')
except Exception as e:
    print(f'Błąd {e}')
    print('Używam danych zapasowych')
    data = {
        'nazwa': ['IPA','IPA', 'Lager', 'Stout', 'Pilsner', 'Wheat', 'Porter', 'Ale', 'Bock'],
        'alkohol': [6.5, 6.5, 5.0, 7.2, 4.8, 5.2, 5.8, 5.5, 6.8],
        'goryczka': [65, 65, np.nan, 45, 30, 15, 40, 35, 25],
        'ocena': [4.2, 4.2, 3.8, 4.5, 3.9, 3.7, 4.1, 4.0, 4.3],
        'styl': ['IPA', 'IPA', 'Lager', 'Ciemne', 'Lager', np.nan, 'Ciemne', 'Jasne', 'Ciemne']
    }
    df = pd.DataFrame(data)

print(df)

# 2. Podstawowe info
print('\n' + '='*50)
print(f'Wymiary danych: {df.shape}')
print(f'Liczba wierszy: {df.shape[0]}')
print(f'Liczba kolumn: {df.shape[1]}')

# 3. Podgląd danych
print("Pierwsze 5 piw:")
print(df.head())
print("\nOstatnie 5 piw:")
print(df.tail())
# print('\nDescribe')
# print(df.describe())

# 4. Typy danych
print(f'{df.info()}')

# 5. Statystyki numeryczne
kolumny_numeryczne = df.select_dtypes(include='number').columns
if len(kolumny_numeryczne) > 0:
    print('Stasystyki dla chech numerycznych:')
    print(df[kolumny_numeryczne].describe())
else:
    print('Brak kolumn numerycznych w danych')

# 6. Statystyki kategoryczne
print("\n" + "="*50)
print("STATYSTYKI KATEGORYCZNE")
print("="*50)

kolumny_tekstowe = df.select_dtypes(include='object').columns
if len (kolumny_tekstowe) > 0:
    for kolumna in kolumny_tekstowe:
        print(f'\nKolumna: {kolumna}')
        print(f'Liczba unikalnych wartości: {df[kolumna].unique()}')
        print('3 najczęstrzych wartości')
        print(df[kolumna].value_counts().head(3))
else:
    print('Brak kolumn kategorycznych w danych')

# 7. Brakujące wartości
print("\n" + "="*50)
print("BRAKUJĄCE WARTOŚCI")
print("="*50)

brakujace = df.isnull().sum()
if brakujace.sum() > 0:
    print('Kolumny z brakującymi wartościami:')
    for kolumna in df.columns:
        if df[kolumna].isnull().sum() > 0:
            braki_liczbowo = df[kolumna].isnull().sum()
            braki_procentowo = (braki_liczbowo / len(df)) * 100
            print(f'    {kolumna}: {braki_liczbowo} ({braki_procentowo:.1f})%')
