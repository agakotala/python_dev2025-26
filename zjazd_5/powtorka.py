import pandas as pd
import matplotlib.pyplot as plt

dane = [
    {"data": "2026-01-01", "sklep": "Warszawa", "produkt": "Kawa", "ilosc": 3, "cena": 12.0},
    {"data": "2026-01-01", "sklep": "Warszawa", "produkt": "Herbata", "ilosc": 2, "cena": 8.0},
    {"data": "2026-01-01", "sklep": "Kraków", "produkt": "Kawa", "ilosc": 1, "cena": 12.0},
    {"data": "2026-01-02", "sklep": "Warszawa", "produkt": "Kawa", "ilosc": 4, "cena": 12.0},
    {"data": "2026-01-02", "sklep": "Kraków", "produkt": "Herbata", "ilosc": 3, "cena": 8.0},
    {"data": "2026-01-03", "sklep": "Kraków", "produkt": "Kawa", "ilosc": None, "cena": 12.0},  # brak ilości
    {"data": "2026-01-03", "sklep": "Gdańsk", "produkt": "Kawa", "ilosc": 2, "cena": 12.0},
    {"data": "2026-01-04", "sklep": "Warszawa", "produkt": "Kawa", "ilosc": 5, "cena": 12.0},
    {"data": "2026-01-04", "sklep": "Gdańsk", "produkt": "Herbata", "ilosc": 4, "cena": 8.0},
]

df = pd.DataFrame(dane)

df["data"] = pd.to_datetime(df["data"])
df["ilosc"] = df["ilosc"].fillna(0) #zmien nan na 0
df["ilosc"] = df["ilosc"].astype(int) #sprawdz czy ilosc jest liczba


df["przychod"] = df["ilosc"] * df["cena"]

dzienny = (
    df.groupby("data", as_index=False)["przychod"]
           .sum()
           .sort_values("data")
)

per_sklep = df.pivot_table(
    index="data",
    columns="sklep",
    values="przychod",
    aggfunc="sum",
    fill_value=0
).sort_index()

dzienny["srednia_7d"] = dzienny["przychod"].rolling(window=7, min_periods=1).mean()

plt.figure()
plt.plot(dzienny["data"], dzienny["przychod"], marker="o", label="Przychód dzienny")
plt.plot(dzienny["data"], dzienny["srednia_7d"], marker="o", label="Średnia krocząca 7 dni")
plt.title("Przychód dzienny i średnia krocząca")
plt.xlabel("Data")
plt.ylabel("Przychód")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

suma_sklepy = per_sklep.sum(axis=0).sort_values(ascending=False)

plt.figure()
plt.bar(suma_sklepy.index, suma_sklepy.values)
plt.title("Łączny przchód per sklep")
plt.xlabel("Sklep")
plt.ylabel("Przychód")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()