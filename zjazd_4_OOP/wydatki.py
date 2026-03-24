class Wydatek:
    def __init__(self, opis: str, kwota: float) -> None:
        if not opis:
            raise ValueError("Opis nie może być pusty.")
        if kwota <= 0:
            raise ValueError("Kwota musi być większa od 0.")
        self.opis = opis
        self.kwota = float(kwota)

    def __str__(self) -> str:
        return f"{self.opis} — {self.kwota:.2f} zł"

    def __repr__(self) -> str:
        return f"Wydatek(opis={self.opis!r}, kwota={self.kwota!r})"


class ListaWydatkow:
    def __init__(self) -> None:
        self.wydatki = []

    def dodaj(self, wydatek: Wydatek) -> None:
        self.wydatki.append(wydatek)

    def suma(self) -> float:
        return sum(w.kwota for w in self.wydatki)

    def __len__(self) -> int:
        return len(self.wydatki)

    def __str__(self) -> str:
        return f"Wydatków: {len(self)} | Suma: {self.suma():.2f} zł"

    def __repr__(self) -> str:
        return f"ListaWydatkow(liczba={len(self)})"


# --- PRZYKŁAD UŻYCIA ---
lista = ListaWydatkow()
lista.dodaj(Wydatek("Kebab", 18.50))
lista.dodaj(Wydatek("Bilet", 110))
lista.dodaj(Wydatek("Kawa", 12))

print(lista)
print(repr(lista))
print(len(lista))
print(lista.suma())

for w in lista.wydatki:
    print(w)
    print(repr(w))
