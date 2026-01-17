class Ksiazka:
    def __init__(self, tytul, autor, rok_wydania):
        self.tytul = tytul
        self.autor = autor
        self.rok_wydania = rok_wydania
        self.czy_wypozyczona = False #stan wypożyczenia książki false = dostępna, true = wypozyczona

    def wypozycz(self):
        if self.czy_wypozyczona:
            print(f"Książka '{self.tytul}' jest już wypożyczona.")
        else:
            self.czy_wypozyczona = True
            print(f"Wypożyczono książkę '{self.tytul}'.")
    def zwroc(self):
        if self.czy_wypozyczona:
            self.czy_wypozyczona = False
            print(f"Zwrócono książkę '{self.tytul}'.")
        else:
            print(f"Książka '{self.tytul}' nie była wypożyczona")

    def informacje(self):
        return f"'{self.tytul}' autorstwa {self.autor}, wydana w {self.rok_wydania}"

ksiazka1 = Ksiazka("Hobbit", "J.R.R. Tolkien", 1937)
print(ksiazka1.informacje())
ksiazka1.wypozycz()
ksiazka1.zwroc()
ksiazka1.zwroc()