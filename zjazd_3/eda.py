import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#df = pd.read_csv('dane_csv.csv', delimiter=None, header='infer', index_col=None, usecols=None, dtype=None, true_values=['T', 'Tak'], false_values=['N', 'Nie'], skipinitialspace=True, skiprows=2, nrows=None, na_filter=True, skip_blank_lines=True, dayfirst=True,thousands=None, decimal=',', quetechar="", doublequote=True, comment='#', encoding=None, encoding_errors='strict', on_bad_lines='error', float_precision=None)

url="https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-03-31/beers.csv"

try:
    df=pd.read_csv(url)
    print('Dane pobrane')
except Exception as e:
    print(f'Błąd {e}')
    print('Używam danych zapasowych')
    data = {
        'nazwa': ['IPA', 'IPA', 'Lager', 'Stout', 'Pilsner', 'Wheat', 'Porter', 'Ale', 'Bock'],
        'alkohol': [6.5, 6.5, 5.0, 7.2, 4.8, 5.2, 5.8, 5.5, 6.8],
        'goryczka': [65, 65, np.nan, 45, 30, 15, 40, 35, 25],
        'ocena': [4.2, 4.2, 3.8, 4.5, 3.9, 3.7, 4.1, 4.0, 4.3],
        'styl': ['IPA', 'IPA', 'Lager', 'Ciemne', 'Lager', np.nan, 'Ciemne', 'Jasne', 'Ciemne']
    }
    df = pd.DataFrame(data)

#podstawowe informacje
print('\n' + '='*50)
print('PODSTAWOWE INFORMACJE')
print('='*50)

print(f'Wymiary danych: {df.shape}')
print(f'Liczba wierszy: {df.shape[0]}') #shape[0] liczba wierszy
print(f'Liczba kolumn: {df.shape[1]}') #shape[1] liczba kolumn

print('\n' + '='*50)
print('PODGLĄD DANYCH')
print('='*50)

print('Pierwsze 5 piw:')
print(df.head())
print('5 ostatnich piw:')
print(df.tail())

print('\n' + '='*50)
print('TYPY DANYCH')
print('='*50)

print(f'\n{df.info()}')
#statystki numeryczne

print('\n' + '='*50)
print('STATYSTYKI NUMERYCZNE')
print('='*50)

kolumny_numeryczne = df.select_dtypes(include='number').columns
if len(kolumny_numeryczne) > 0:
    print('Statystyki dla cech numerycznych:')
    print(df[kolumny_numeryczne].describe())
else:
    print('Brak kolumn numerycznych w danych')

#statystyki kategoryczne
print('\n' + '='*50)
print('STATYSTYKI KATEGORYCZNE')
print('='*50)

kolumny_tekstowe = df.select_dtypes(include='object').columns
if len(kolumny_tekstowe) > 0:
    for kolumna in kolumny_tekstowe:
        print(f'\nKolumna: {kolumna}')
        print(f'Unikalnych wartości: {df[kolumna].unique()}')
        print(f'Liczba unikalnych wartości: {len(df[kolumna].unique())}')
        print('3 najczęstsze wartości:')
        print(df[kolumna].value_counts().head(3))
else:
    print('Brak kolumn kategorycznych w danych')

#brakujące wartości

print('\n' + '='*50)
print('BRAKUJĄCE WARTOŚCI')
print('='*50)

brakujace = df.isna().sum()
if brakujace.sum() > 0:
    print('Kolumny z brakującymi wartościami:')
    for kolumna in df.columns:
        if df[kolumna].isna().sum() > 0:
            braki_liczbowo = df[kolumna].isnull().sum()
            braki_procentowo = (braki_liczbowo / len(df)) * 100
            print(f'{kolumna}: {braki_liczbowo} ({braki_procentowo:.2f}%)')

#wizualizacje
print("\n" + '='*50)
print("TWORZENIE WYKRESÓW")
print("="*50)
#wykres1
if 'alkohol' in df.columns and False:
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 3, 1)
    plt.title('Rozkład zawartości alkoholu')
    plt.xlabel('Zawartość alkoholu w (%)')
    plt.ylabel('Liczba piw')
    plt.tight_layout()
    plt.hist(df.alkohol)

    plt.subplot(1, 3, 2)
    plt.title('Rozkład zawartości alkoholu')
    plt.xlabel('Zawartość alkoholu w (%)')
    plt.ylabel('Liczba piw')
    plt.tight_layout()
    df['alkohol'].hist(bins=10, color='lightblue', edgecolor='black')

    plt.subplot(1, 3, 3)
    df.boxplot(column='alkohol', grid=False)
    plt.title('Boxplot: Zawartość alkoholu')
    plt.show()
#wykres2
if 'ocena' in df.columns and False:
    plt.figure(figsize=(8, 5))
    df['ocena'].hist(bins=8, color='lightgreen', edgecolor='black', alpha=0.7)
    plt.title('Rozkład ocen piw')
    plt.xlabel('Ocena w skali 1 - 5')
    plt.ylabel('Liczba piw')
    plt.grid(axis='y', alpha=0.3)
    plt.show()

#wykres3
if 'alkohol' in df.columns and 'ocena' in df.columns and False:
    plt.figure(figsize=(8, 6))
    plt.scatter(df['alkohol'], df['ocena'], alpha=0.6, s=60, color='purple')
    plt.title('Zależność między zawartością alkoholu a oceną')
    plt.xlabel('Zawartość alko (%)')
    plt.ylabel('Ocena')
    plt.grid(True, alpha=0.3)
    z = np.polyfit(df['alkohol'], df['ocena'], 1)
    p = np.poly1d(z)
    plt.plot(df['alkohol'], p(df['alkohol']), color='red')
    plt.show()
#wykres4
if 'styl' in df.columns and False:
    plt.figure(figsize=(10, 6))
    df['styl'].value_counts().plot(kind='bar', color='orange', edgecolor='black')
    plt.title('Popularność stylów piw')
    plt.xlabel('Styl piwa')
    plt.ylabel('Liczba piw')
    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

if len(kolumny_numeryczne) >= 2 and False:
    plt.figure(figsize=(8, 6))
    macierz_korelacji = df[kolumny_numeryczne].corr()
    sns.heatmap(macierz_korelacji, annot=True, cmap='rocket', center=0)
    plt.title('Korelacje między cechami numerycznymi')
    plt.tight_layout()
    plt.show()

print("\n" + '='*50)
print("ANALIZA DUPLIKATÓW")
print("="*50)

duplikaty = df.duplicated()
if duplikaty.sum() > 0:
    print(f'Znaleziono {duplikaty.sum()} zduplikowanych wierszy')
    print('Zduplikowane wiersze: ')
    print(df[duplikaty])
else:
    print('Brak duplikatów')
#podsumowanie analizy
print("="*50)
print("PODSUMOWANIE ANALIZY")
print("="*50)

print(f"Przeanalizowano {len(df)} piw")
print(f"Liczba cech: {len(df.columns)}")

if len(kolumny_numeryczne) > 0:
    print("Znalezione cechy numerycze:", list(kolumny_numeryczne))

if len(kolumny_numeryczne) > 0:
    print("Znalezione cechy kategoryczne:", list(kolumny_tekstowe))

if 'ocena' in df.columns and 'nazwa' in df.columns:
    print('\nTop 3 najwyżej ocenianie piwa')
    najlepsze = df.nlargest(3, 'ocena')[['nazwa', 'ocena']]
    print(najlepsze)

if 'alkohol' in df.columns and 'nazwa' in df.columns:
    print("\n3 piwa z najwyższą zawartością alkoholu")
    mocne = df.nlargest(3, 'alkohol')[['nazwa', 'alkohol']]
    print(mocne)

print("\n"+"="*50)
