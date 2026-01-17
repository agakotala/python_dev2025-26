from __future__ import annotations  # pozwala używać nazw klas w adnotacjach zanim zostaną zdefiniowane
import asyncio  # biblioteka do async/await i pętli zdarzeń
import hashlib  # biblioteka do hashowania (np. do generowania ID)
import random  # losowość (symulacja płatności / popularności)
from abc import ABC, abstractmethod  # ABC = klasy abstrakcyjne, abstractmethod = wymuszanie implementacji
from dataclasses import dataclass  # dataclass upraszcza klasy “danych”
from datetime import datetime, timedelta  # obsługa dat i różnic czasu
from enum import Enum, auto  # Enum do stałych, auto do automatycznej numeracji
from functools import wraps  # wraps zachowuje metadane funkcji w dekoratorach
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple  # typy pomocnicze do adnotacji


# ========================= 1) DEKORATORY FUNKCJI/METOD =========================  # nagłówek sekcji
def loguj_wywolanie(poziom: str = "INFO") -> Callable:  # dekorator z parametrem (poziom logowania)
    def dekorator(funkcja: Callable) -> Callable:  # właściwy dekorator, który dostaje dekorowaną funkcję
        @wraps(funkcja)  # kopiuje __name__, docstring itd. z oryginalnej funkcji
        def wrapper(*args, **kwargs):  # opakowanie przechwytujące wywołanie
            znacznik_czasu = datetime.now().strftime("%H:%M:%S")  # tworzy czytelny timestamp
            print(f"[{poziom}] {znacznik_czasu} -> {funkcja.__qualname__}()")  # loguje nazwę i czas
            try:  # blok obsługi wyjątków, żeby zalogować błędy
                return funkcja(*args, **kwargs)  # wywołuje oryginalną funkcję z tymi samymi argumentami
            except Exception as e:  # łapie dowolny wyjątek
                print(f"[{poziom}] !! {type(e).__name__}: {e}")  # loguje typ i treść wyjątku
                raise  # ponownie rzuca wyjątek (nie ukrywa błędu)
        return wrapper  # zwraca opakowaną funkcję
    return dekorator  # zwraca dekorator (bo to dekorator “parametryzowany”)


def cache_ttl(ttl_s: int = 10) -> Callable:  # dekorator cache’ujący wynik na ttl_s sekund
    def dekorator(funkcja: Callable) -> Callable:  # dekorator dostaje funkcję
        pamiec: Dict[str, Tuple[datetime, Any]] = {}  # słownik: klucz -> (czas_zapisu, wynik)

        @wraps(funkcja)  # zachowanie metadanych funkcji
        def wrapper(*args, **kwargs):  # opakowanie funkcji
            surowy_klucz = (funkcja.__qualname__, args, tuple(sorted(kwargs.items())))  # elementy klucza cache
            klucz = hashlib.md5(repr(surowy_klucz).encode()).hexdigest()  # skraca klucz do hash MD5
            teraz = datetime.now()  # bieżący czas do porównania TTL

            if klucz in pamiec:  # jeśli coś już jest w cache
                ts, wynik = pamiec[klucz]  # pobiera czas i wynik
                if (teraz - ts).total_seconds() < ttl_s:  # jeśli nie minął TTL
                    print(f"    (cache hit: {funkcja.__name__})")  # loguje trafienie w cache
                    return wynik  # zwraca zapamiętany wynik bez ponownego liczenia

            wynik = funkcja(*args, **kwargs)  # liczy wynik normalnie, bo cache pusty lub wygasł
            pamiec[klucz] = (teraz, wynik)  # zapisuje świeży wynik do cache

            wygasle = [k for k, (t, _) in pamiec.items() if (teraz - t).total_seconds() >= ttl_s]  # lista wygasłych kluczy
            for k in wygasle:  # iteruje po wygasłych
                del pamiec[k]  # usuwa wygasłe wpisy

            return wynik  # zwraca wynik funkcji
        return wrapper  # zwraca opakowanie
    return dekorator  # zwraca dekorator


# ========================= 2) DESKRYPTORY (WALIDACJA PÓL) =========================  # nagłówek sekcji
class LiczbaNieujemna:  # deskryptor wymuszający liczbę >= 0
    def __init__(self, nazwa: str):  # konstruktor deskryptora
        self._magazyn = f"_{nazwa}"  # nazwa pola w instancji, gdzie będzie trzymana wartość

    def __get__(self, obiekt, typ=None) -> float:  # getter deskryptora
        if obiekt is None:  # gdy odczyt przez klasę (np. Klasa.pole)
            return self  # zwraca deskryptor
        return getattr(obiekt, self._magazyn, 0.0)  # zwraca wartość z obiektu albo 0.0 gdy brak

    def __set__(self, obiekt, wartosc: float) -> None:  # setter deskryptora
        if not isinstance(wartosc, (int, float)):  # sprawdza typ
            raise TypeError("Wartość musi być liczbą")  # błąd typu, jeśli nie liczba
        if wartosc < 0:  # sprawdza czy nieujemna
            raise ValueError("Wartość musi być >= 0")  # błąd wartości, jeśli ujemna
        setattr(obiekt, self._magazyn, float(wartosc))  # zapisuje do obiektu jako float

    def __delete__(self, obiekt):  # próba usunięcia pola
        raise AttributeError("Nie można usunąć tej właściwości")  # blokuje del obiekt.pole


class TekstOgraniczony:  # deskryptor ograniczający długość tekstu
    def __init__(self, max_dl: int = 40):  # konstruktor z limitem
        self.max_dl = max_dl  # zapisuje maksymalną długość
        self._dane: Dict[int, str] = {}  # magazyn: id(obiektu) -> tekst

    def __get__(self, obiekt, typ=None) -> str:  # getter deskryptora
        if obiekt is None:  # jeśli dostęp przez klasę
            return self  # zwraca deskryptor
        return self._dane.get(id(obiekt), "")  # zwraca tekst albo pusty string

    def __set__(self, obiekt, wartosc: str) -> None:  # setter deskryptora
        if not isinstance(wartosc, str):  # sprawdza typ
            raise TypeError("Wartość musi być str")  # błąd jeśli nie string
        if len(wartosc) > self.max_dl:  # jeśli za długie
            wartosc = wartosc[: self.max_dl]  # ucina do limitu
        self._dane[id(obiekt)] = wartosc  # zapisuje pod id obiektu

    def __delete__(self, obiekt):  # usuwanie wartości
        self._dane.pop(id(obiekt), None)  # usuwa wpis jeśli istnieje


# ========================= 3) ENUMY =========================  # nagłówek sekcji
class Gatunek(Enum):  # enum gatunków filmu
    AKCJA = auto()  # automatyczna wartość
    DRAMAT = auto()  # automatyczna wartość
    KOMEDIA = auto()  # automatyczna wartość
    SCIFI = auto()  # automatyczna wartość

    def __str__(self) -> str:  # ładny napis dla enuma
        return self.name.title()  # np. "AKCJA" -> "Akcja"


class StatusRezerwacji(Enum):  # enum statusów rezerwacji
    UTWORZONA = "utworzona"  # rezerwacja powstała
    OPLACONA = "oplacona"  # płatność przeszła
    POTWIERDZONA = "potwierdzona"  # rezerwacja finalnie zatwierdzona
    ANULOWANA = "anulowana"  # rezerwacja anulowana


# ========================= 4) BAZOWA ENCJA (ABC) =========================  # nagłówek sekcji
class Encja(ABC):  # abstrakcyjna klasa bazowa dla obiektów “biznesowych”
    def __init__(self, id: Optional[str] = None):  # konstruktor z opcjonalnym ID
        self._id = id or hashlib.md5(str(datetime.now()).encode()).hexdigest()[:10]  # generuje krótkie ID gdy brak
        self._utworzono = datetime.now()  # zapisuje czas utworzenia
        self._zmodyfikowano = datetime.now()  # zapisuje czas modyfikacji

    @property  # property: dostęp jak do pola, a nie metody
    def id(self) -> str:  # getter ID
        return self._id  # zwraca identyfikator

    @property  # property dynamiczne
    def wiek_s(self) -> int:  # wiek
        return int((datetime.now() - self._utworzono).total_seconds())  # różnica czasu w sekundach

    def dotknij(self) -> None:  # metoda aktualizująca “zmodyfikowano”
        self._zmodyfikowano = datetime.now()  # ustawia nowy czas modyfikacji

    @abstractmethod  # wymusza implementację w klasach potomnych
    def to_dict(self) -> Dict[str, Any]:  # serializacja do słownika
        raise NotImplementedError  # sygnał: musi być nadpisane

    @classmethod  # metoda klasowa (alternatywny konstruktor)
    @abstractmethod  # wymusza implementację
    def from_dict(cls, data: Dict[str, Any]) -> Encja:  # odtwarzanie obiektu ze słownika
        raise NotImplementedError  # sygnał: musi być nadpisane


# ========================= 5) MODELE: FILM, MIEJSCE, SEANS =========================  # nagłówek sekcji
class Film(Encja):  # klasa Film dziedzicząca Encja
    tytul = TekstOgraniczony(max_dl=45)  # deskryptor: tytuł max 45 znaków
    cena_bazowa = LiczbaNieujemna("cena_bazowa")  # deskryptor: cena nieujemna

    def __init__(self, tytul: str, gatunek: Gatunek, cena_bazowa: float, limit_wiek: int = 0, **kw):  # konstruktor filmu
        super().__init__(kw.get("id"))  # inicjalizuje Encja (ID)
        self.tytul = tytul  # zapis tytułu przez deskryptor (ucina jeśli trzeba)
        self.gatunek = gatunek  # zapis gatunku (zwykłe pole)
        self.cena_bazowa = cena_bazowa  # zapis ceny przez deskryptor (walidacja >=0)
        self.limit_wiek = limit_wiek  # minimalny wiek widza
        self._wyswietlenia = 0  # statystyka: ile razy pokazano w rekomendacjach
        self._zakupy = 0  # statystyka: ile biletów sprzedano na ten film

    def dodaj_wyswietlenie(self) -> None:  # inkrementuje wyświetlenia
        self._wyswietlenia += 1  # zwiększa licznik

    def dodaj_zakup(self, ile: int) -> None:  # zwiększa liczbę zakupów
        self._zakupy += ile  # dodaje ilość

    @property  # property dynamiczne
    def wynik_popularnosci(self) -> float:  # “ranking” filmu
        swiezosc = 100 / (self.wiek_s + 60)  # świeżość maleje z czasem (unikamy dzielenia przez 0)
        return round((self._wyswietlenia / 10) + (self._zakupy * 5) + swiezosc, 2)  # suma wagowa statystyk

    def to_dict(self) -> Dict[str, Any]:  # implementacja abstrakcyjnej serializacji
        return {  # zwraca słownik z danymi filmu
            "id": self.id,  # ID filmu
            "tytul": self.tytul,  # tytuł filmu
            "gatunek": self.gatunek.name,  # gatunek jako nazwa enuma
            "cena_bazowa": float(self.cena_bazowa),  # cena jako float
            "limit_wiek": self.limit_wiek,  # ograniczenie wiekowe
        }  # koniec słownika

    @classmethod  # metoda klasowa
    def from_dict(cls, data: Dict[str, Any]) -> Film:  # tworzy film ze słownika
        return cls(  # zwraca nową instancję
            id=data.get("id"),  # ID jeśli jest
            tytul=data["tytul"],  # tytuł obowiązkowy
            gatunek=Gatunek[data["gatunek"]],  # mapowanie string -> enum
            cena_bazowa=data["cena_bazowa"],  # cena
            limit_wiek=data.get("limit_wiek", 0),  # limit wiekowy z domyślną wartością
        )  # koniec tworzenia


@dataclass  # dataclass dla prostych danych
class Miejsce:  # pojedyncze miejsce na sali
    rzad: int  # numer rzędu
    numer: int  # numer miejsca
    premium: bool = False  # czy miejsce premium (dopłata)


@dataclass  # dataclass
class PozycjaBiletu:  # pozycja w rezerwacji (linie “koszyka”)
    film: Film  # referencja do filmu
    seans_id: str  # ID seansu
    miejsce: Miejsce  # miejsce na sali
    cena: float  # finalna cena za to miejsce


class Seans(Encja):  # seans jako encja (ma własne ID i czas)
    def __init__(self, film: Film, start: datetime, sala: str, miejsca: List[Miejsce], **kw):  # konstruktor seansu
        super().__init__(kw.get("id"))  # inicjalizuje Encja
        self.film = film  # przypisuje film
        self.start = start  # czas rozpoczęcia
        self.sala = sala  # nazwa/identyfikator sali
        self._wszystkie_miejsca = list(miejsca)  # kopia listy miejsc
        self._zajete: set[Tuple[int, int]] = set()  # zbiór zajętych (rzad, numer)

    def czy_wolne(self, miejsce: Miejsce) -> bool:  # sprawdza dostępność miejsca
        return (miejsce.rzad, miejsce.numer) not in self._zajete  # wolne jeśli nie ma w zajętych

    def zajmij(self, miejsce: Miejsce) -> None:  # zajmuje miejsce
        self._zajete.add((miejsce.rzad, miejsce.numer))  # dodaje do zajętych

    def zwolnij(self, miejsce: Miejsce) -> None:  # zwalnia miejsce
        self._zajete.discard((miejsce.rzad, miejsce.numer))  # usuwa z zajętych bez błędu gdy brak

    def to_dict(self) -> Dict[str, Any]:  # serializacja seansu
        return {  # słownik reprezentujący seans
            "id": self.id,  # ID seansu
            "film_id": self.film.id,  # ID filmu
            "start": self.start.isoformat(),  # start w ISO
            "sala": self.sala,  # sala
            "zajete": list(self._zajete),  # zajęte miejsca jako lista par
        }  # koniec słownika

    @classmethod  # metoda klasowa
    def from_dict(cls, data: Dict[str, Any]) -> Seans:  # odtwarzanie seansu (tu uproszczone)
        raise NotImplementedError("Odtwarzanie seansu wymaga mapowania filmów i miejsc")  # sygnalizuje brak implementacji


# ========================= 6) STRATEGY: REKOMENDACJE =========================  # nagłówek sekcji
class StrategiaRekomendacji(ABC):  # interfejs strategii
    @abstractmethod  # wymusza implementację
    def polec(self, filmy: List[Film], limit: int = 3) -> List[Film]:  # metoda zwracająca rekomendacje
        raise NotImplementedError  # do nadpisania

    @abstractmethod  # wymusza implementację
    def nazwa(self) -> str:  # nazwa strategii
        raise NotImplementedError  # do nadpisania


class StrategiaPopularnosci(StrategiaRekomendacji):  # strategia oparta o popularność
    @loguj_wywolanie("DEBUG")  # loguje wywołania
    @cache_ttl(ttl_s=5)  # cache na 5 sekund
    def polec(self, filmy: List[Film], limit: int = 3) -> List[Film]:  # rekomenduje top filmy
        posortowane = sorted(filmy, key=lambda f: f.wynik_popularnosci, reverse=True)  # sortuje malejąco po wyniku
        for f in posortowane[:limit]:  # przechodzi po top wynikach
            f.dodaj_wyswietlenie()  # zwiększa “wyświetlenia” bo film został pokazany użytkownikowi
        return posortowane[:limit]  # zwraca top limit

    def nazwa(self) -> str:  # nazwa strategii
        return "Popularność"  # zwraca opis


class StrategiaGatunku(StrategiaRekomendacji):  # strategia preferująca jeden gatunek
    def __init__(self, preferowany: Gatunek):  # konstruktor z preferowanym gatunkiem
        self.preferowany = preferowany  # zapisuje preferencję

    def polec(self, filmy: List[Film], limit: int = 3) -> List[Film]:  # wybiera filmy wg gatunku
        filtrowane = [f for f in filmy if f.gatunek == self.preferowany]  # filtruje po preferowanym gatunku
        posortowane = sorted(filtrowane, key=lambda f: f.wynik_popularnosci, reverse=True)  # sortuje po popularności
        for f in posortowane[:limit]:  # dla top filmów
            f.dodaj_wyswietlenie()  # dodaje wyświetlenie
        return posortowane[:limit]  # zwraca top limit

    def nazwa(self) -> str:  # nazwa strategii
        return f"Gatunek: {self.preferowany}"  # zwraca nazwę z gatunkiem


# ========================= 7) DECORATOR: CENA (DOPŁATY / PROMOCJE) =========================  # nagłówek sekcji
class KalkulatorCeny(ABC):  # interfejs liczenia ceny biletu
    @abstractmethod  # wymusza implementację
    def policz(self, film: Film, miejsce: Miejsce, start: datetime) -> float:  # zwraca cenę biletu
        raise NotImplementedError  # do nadpisania


class CenaBazowa(KalkulatorCeny):  # podstawowy kalkulator ceny
    def policz(self, film: Film, miejsce: Miejsce, start: datetime) -> float:  # liczy cenę bez dodatków
        return float(film.cena_bazowa)  # zwraca bazową cenę filmu


class DekoratorCeny(KalkulatorCeny):  # bazowy dekorator ceny (owija inny kalkulator)
    def __init__(self, wewnetrzny: KalkulatorCeny):  # przyjmuje kalkulator do owinięcia
        self.wewnetrzny = wewnetrzny  # zapamiętuje go

    def policz(self, film: Film, miejsce: Miejsce, start: datetime) -> float:  # domyślnie deleguje
        return self.wewnetrzny.policz(film, miejsce, start)  # wywołuje kalkulator “pod spodem”


class DopłataPremium(DekoratorCeny):  # dekorator: dopłata za miejsce premium
    def policz(self, film: Film, miejsce: Miejsce, start: datetime) -> float:  # nadpisuje liczenie
        cena = super().policz(film, miejsce, start)  # bierze cenę bazową (lub już udekorowaną)
        return cena + (15.0 if miejsce.premium else 0.0)  # dodaje 15 zł, jeśli premium


class PromocjaSroda(DekoratorCeny):  # dekorator: zniżka w środę
    def policz(self, film: Film, miejsce: Miejsce, start: datetime) -> float:  # nadpisuje liczenie
        cena = super().policz(film, miejsce, start)  # bierze cenę z poprzednich dekoratorów
        return round(cena * 0.8, 2) if start.weekday() == 2 else cena  # jeśli środa (2) to -20%


# ========================= 8) CHAIN OF RESPONSIBILITY: WALIDATORY =========================  # nagłówek sekcji
class Walidator(ABC):  # bazowy element łańcucha walidacji
    def __init__(self, nastepny: Optional[Walidator] = None):  # przyjmuje kolejny walidator
        self.nastepny = nastepny  # zapisuje następny element łańcucha

    def ustaw_nastepny(self, nastepny: Walidator) -> Walidator:  # pozwala “dokleić” kolejny walidator
        self.nastepny = nastepny  # ustawia następny
        return nastepny  # zwraca go, żeby wygodnie łańcuchować

    def sprawdz(self, **kontekst) -> None:  # uruchamia walidację dla tego i następnych
        self._sprawdz_lokalnie(**kontekst)  # walidacja konkretnego warunku
        if self.nastepny:  # jeśli jest kolejny walidator
            self.nastepny.sprawdz(**kontekst)  # przekaż dalej

    @abstractmethod  # wymusza implementację reguły
    def _sprawdz_lokalnie(self, **kontekst) -> None:  # metoda z regułą walidacji
        raise NotImplementedError  # do nadpisania


class WalidatorWiek(Walidator):  # waliduje limit wieku filmu
    def _sprawdz_lokalnie(self, **kontekst) -> None:  # implementacja walidacji wieku
        film: Film = kontekst["film"]  # pobiera film z kontekstu
        wiek: int = kontekst["wiek"]  # pobiera wiek użytkownika
        if wiek < film.limit_wiek:  # jeśli za młody
            raise ValueError(f"Film '{film.tytul}' ma limit wieku {film.limit_wiek}+ ")  # przerywa walidację błędem


class WalidatorMiejsc(Walidator):  # waliduje czy wszystkie miejsca są wolne
    def _sprawdz_lokalnie(self, **kontekst) -> None:  # implementacja walidacji miejsc
        seans: Seans = kontekst["seans"]  # pobiera seans
        miejsca: List[Miejsce] = kontekst["miejsca"]  # pobiera listę miejsc
        zajete = [m for m in miejsca if not seans.czy_wolne(m)]  # znajduje zajęte miejsca
        if zajete:  # jeśli coś zajęte
            opis = ", ".join([f"R{m.rzad}M{m.numer}" for m in zajete])  # robi opis zajętych
            raise ValueError(f"Miejsca zajęte: {opis}")  # rzuca błąd


# ========================= 9) CONTEXT MANAGER: BLOKADA MIEJSC =========================  # nagłówek sekcji
class BlokadaMiejsc:  # context manager, który “tymczasowo” blokuje miejsca
    def __init__(self, seans: Seans, miejsca: List[Miejsce]):  # przyjmuje seans i miejsca do blokady
        self.seans = seans  # zapisuje seans
        self.miejsca = miejsca  # zapisuje miejsca
        self.zablokowano = False  # flaga czy udało się zablokować

    def __enter__(self) -> BlokadaMiejsc:  # wejście do bloku `with`
        for m in self.miejsca:  # przechodzi po miejscach
            self.seans.zajmij(m)  # oznacza miejsce jako zajęte (blokada)
        self.zablokowano = True  # ustawia flagę sukcesu
        return self  # zwraca siebie (opcjonalne, ale przydatne)

    def __exit__(self, exc_type, exc, tb) -> bool:  # wyjście z `with` (z błędem lub bez)
        if exc_type is not None:  # jeśli w bloku wystąpił wyjątek
            for m in self.miejsca:  # przechodzi po miejscach
                self.seans.zwolnij(m)  # zwalnia miejsca (rollback)
        return False  # False = nie tłumimy wyjątku (ma polecieć dalej)


# ========================= 10) ASYNC: BRAMKA PŁATNOŚCI =========================  # nagłówek sekcji
class BramkaPlatnosci:  # symulowana bramka płatności
    @staticmethod  # statyczna metoda pomocnicza (nie potrzebuje self ani cls)
    def generuj_kod() -> str:  # generuje “kod transakcji”
        return hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]  # krótki hash jako kod

    @loguj_wywolanie("INFO")  # loguje wywołanie płatności
    async def zaplac(self, kwota: float) -> Tuple[bool, str]:  # async: zwraca (czy_sukces, kod)
        await asyncio.sleep(0.7)  # symuluje opóźnienie sieci/API
        sukces = random.random() < 0.9  # 90% szans powodzenia
        kod = self.generuj_kod()  # generuje kod transakcji
        return sukces, kod  # zwraca wynik


# ========================= 11) REZERWACJA (ŁĄCZY WSZYSTKO) =========================  # nagłówek sekcji
class Rezerwacja(Encja):  # rezerwacja jako encja
    def __init__(self, seans: Seans, wiek: int, pozycje: List[PozycjaBiletu], **kw):  # konstruktor rezerwacji
        super().__init__(kw.get("id"))  # inicjalizuje Encja
        self.seans = seans  # zapisuje seans
        self.wiek = wiek  # zapisuje wiek kupującego
        self.pozycje = pozycje  # zapisuje pozycje biletów
        self.status = StatusRezerwacji.UTWORZONA  # ustawia status początkowy
        self.kod_transakcji: Optional[str] = None  # brak kodu na start

    @property  # property dynamiczne
    def suma(self) -> float:  # suma do zapłaty
        return round(sum(p.cena for p in self.pozycje), 2)  # sumuje ceny pozycji

    def to_dict(self) -> Dict[str, Any]:  # serializacja rezerwacji
        return {  # zwraca słownik
            "id": self.id,  # ID rezerwacji
            "seans_id": self.seans.id,  # ID seansu
            "status": self.status.value,  # status jako string
            "suma": self.suma,  # suma
            "kod_transakcji": self.kod_transakcji,  # kod jeśli jest
        }  # koniec słownika

    @classmethod  # metoda klasowa
    def from_dict(cls, data: Dict[str, Any]) -> Rezerwacja:  # odtwarzanie (tu uproszczone)
        raise NotImplementedError("Odtwarzanie rezerwacji wymaga seansu i pozycji")  # brak pełnego rekonstruktora


# ========================= 12) KINO: KOLEKCJE + GENERATOR SEANSÓW =========================  # nagłówek sekcji
class Kino:  # główna klasa systemu
    def __init__(self, strategia: StrategiaRekomendacji):  # konstruktor z strategią rekomendacji
        self._filmy: Dict[str, Film] = {}  # magazyn filmów po ID
        self._seanse: Dict[str, Seans] = {}  # magazyn seansów po ID
        self._strategia = strategia  # zapisuje strategię rekomendacji
        self._bramka = BramkaPlatnosci()  # tworzy bramkę płatności

    def dodaj_film(self, film: Film) -> None:  # dodaje film
        self._filmy[film.id] = film  # zapisuje film do słownika

    def dodaj_seans(self, seans: Seans) -> None:  # dodaje seans
        self._seanse[seans.id] = seans  # zapisuje seans do słownika

    def polec_filmy(self, limit: int = 3) -> List[Film]:  # publiczna metoda rekomendacji
        return self._strategia.polec(list(self._filmy.values()), limit=limit)  # deleguje do strategii

    def zmien_strategie(self, strategia: StrategiaRekomendacji) -> None:  # zmienia strategię w locie
        self._strategia = strategia  # podmienia obiekt strategii

    def generuj_seanse(self, ile: int) -> Generator[Seans, None, None]:  # generator seansów (leniwe tworzenie)
        filmy = list(self._filmy.values())  # bierze listę filmów
        teraz = datetime.now()  # bierze “teraz” jako punkt startowy
        for i in range(ile):  # tworzy żądaną liczbę seansów
            film = random.choice(filmy)  # losuje film
            start = teraz + timedelta(hours=i * 2)  # ustala start co 2 godziny
            miejsca = [Miejsce(rzad=1, numer=n, premium=(n <= 2)) for n in range(1, 9)]  # tworzy miejsca (1..8), 1-2 premium
            yield Seans(film=film, start=start, sala=f"Sala-{random.randint(1,3)}", miejsca=miejsca)  # oddaje seans przez yield

    async def kup_bilety(self, seans_id: str, wiek: int, miejsca: List[Miejsce], kalk: KalkulatorCeny) -> Rezerwacja:  # główna procedura zakupu
        seans = self._seanse[seans_id]  # pobiera seans z magazynu
        film = seans.film  # pobiera film z seansu

        walidator = WalidatorWiek()  # tworzy pierwszy walidator (wiek)
        walidator.ustaw_nastepny(WalidatorMiejsc())  # dokleja drugi walidator (miejsca)
        walidator.sprawdz(film=film, wiek=wiek, seans=seans, miejsca=miejsca)  # uruchamia łańcuch walidacji

        pozycje: List[PozycjaBiletu] = []  # lista pozycji biletów do rezerwacji
        for m in miejsca:  # dla każdego miejsca
            cena = kalk.policz(film, m, seans.start)  # liczy cenę przez kalkulator (Decorator pattern)
            pozycje.append(PozycjaBiletu(film=film, seans_id=seans.id, miejsce=m, cena=cena))  # dodaje pozycję biletu

        with BlokadaMiejsc(seans, miejsca):  # context manager: blokuje miejsca na czas transakcji
            rezerwacja = Rezerwacja(seans=seans, wiek=wiek, pozycje=pozycje)  # tworzy rezerwację
            sukces, kod = await self._bramka.zaplac(rezerwacja.suma)  # async: próbuje zapłacić
            rezerwacja.kod_transakcji = kod  # zapisuje kod transakcji

            if not sukces:  # jeśli płatność nie przeszła
                rezerwacja.status = StatusRezerwacji.ANULOWANA  # ustawia status anulowana
                raise RuntimeError("Płatność odrzucona")  # rzuca błąd (spowoduje rollback miejsc przez __exit__)

            rezerwacja.status = StatusRezerwacji.OPLACONA  # ustawia status opłacona

        rezerwacja.status = StatusRezerwacji.POTWIERDZONA  # po wyjściu z with: miejsca zostają zajęte “na stałe”
        film.dodaj_zakup(len(miejsca))  # aktualizuje statystyki filmu (sprzedane bilety)
        return rezerwacja  # zwraca gotową rezerwację


# ========================= 13) DEMO: URUCHOMIENIE =========================  # nagłówek sekcji
async def demo() -> None:  # funkcja demonstracyjna async
    kino = Kino(strategia=StrategiaPopularnosci())  # tworzy kino z popularnościową strategią

    film1 = Film(tytul="Kosmiczna Ucieczka", gatunek=Gatunek.SCIFI, cena_bazowa=32.0, limit_wiek=12)  # tworzy film SCIFI
    film2 = Film(tytul="Śmiech na Sali", gatunek=Gatunek.KOMEDIA, cena_bazowa=28.0, limit_wiek=0)  # tworzy komedię
    film3 = Film(tytul="Po Godzinach", gatunek=Gatunek.DRAMAT, cena_bazowa=30.0, limit_wiek=16)  # tworzy dramat

    kino.dodaj_film(film1)  # dodaje film do kina
    kino.dodaj_film(film2)  # dodaje film do kina
    kino.dodaj_film(film3)  # dodaje film do kina

    for seans in kino.generuj_seanse(ile=3):  # generator: tworzy 3 seanse “po drodze”
        kino.dodaj_seans(seans)  # dodaje seans do magazynu

    print("\n🎯 Rekomendacje (StrategiaPopularnosci):")  # nagłówek
    for f in kino.polec_filmy(limit=2):  # pobiera 2 rekomendacje
        print(f" - {f.tytul} | {f.gatunek} | wynik={f.wynik_popularnosci}")  # pokazuje wynik

    kino.zmien_strategie(StrategiaGatunku(Gatunek.KOMEDIA))  # zmienia strategię na “gatunek”
    print("\n🎯 Rekomendacje (StrategiaGatunku: Komedia):")  # nagłówek
    for f in kino.polec_filmy(limit=2):  # pobiera rekomendacje
        print(f" - {f.tytul} | {f.gatunek} | wynik={f.wynik_popularnosci}")  # pokazuje wynik

    seans_id = next(iter(kino._seanse.keys()))  # bierze ID pierwszego seansu (dla demo)
    seans = kino._seanse[seans_id]  # pobiera obiekt seansu

    kalk = CenaBazowa()  # podstawowy kalkulator ceny
    kalk = DopłataPremium(kalk)  # dekorator: dolicza premium
    kalk = PromocjaSroda(kalk)  # dekorator: zniżka w środę (jeśli seans w środę)

    miejsca = [Miejsce(rzad=1, numer=1, premium=True), Miejsce(rzad=1, numer=4, premium=False)]  # wybiera 2 miejsca

    print(f"\n🎟️ Próba zakupu na seans: {seans.film.tytul} ({seans.start.strftime('%Y-%m-%d %H:%M')})")  # info o seansie
    try:  # obsługa potencjalnego błędu płatności / walidacji
        rez = await kino.kup_bilety(seans_id=seans_id, wiek=18, miejsca=miejsca, kalk=kalk)  # kup bilety async
        print("✅ Rezerwacja potwierdzona!")  # komunikat sukcesu
        print(f"   ID: {rez.id} | status: {rez.status.value} | suma: {rez.suma} | kod: {rez.kod_transakcji}")  # szczegóły
    except Exception as e:  # łapie błąd
        print(f"❌ Nie udało się kupić biletów: {type(e).__name__}: {e}")  # pokazuje powód

    print("\n📌 Sprawdzenie czy miejsca są zajęte po transakcji:")  # nagłówek
    for m in miejsca:  # iteruje po miejscach
        print(f" - R{m.rzad}M{m.numer}: {'WOLNE' if seans.czy_wolne(m) else 'ZAJĘTE'}")  # pokazuje status


if __name__ == "__main__":  # standardowy “entry point” Pythona
    random.seed(7)  # ustawia ziarno losowości, żeby demo było powtarzalne
    asyncio.run(demo())  # uruchamia funkcję async w pętli zdarzeń
