"""
System zarządzania biblioteką z wykorzystaniem zaawansowanych koncepcji OOP:
- Dziedziczenie wielokrotne
- Abstrakcja
- Enkapsulacja
- Polimorfizm
- Metody specjalne
- Właściwości (property)
- Metaklasy
- Wzorce projektowe (Singleton, Factory, Observer)
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Union
from datetime import datetime, timedelta
from enum import Enum
import uuid


# ============================================
# 1. ENUM - Typy książek
# ============================================
class BookType(Enum):
    """Enum definiujący typy książek w systemie"""
    FICTION = "Fiction"
    NON_FICTION = "Non-Fiction"
    SCIENTIFIC = "Scientific"
    MAGAZINE = "Magazine"

    def __str__(self) -> str:
        """Reprezentacja string enuma"""
        return self.value


# ============================================
# 2. KLASY ABSTRAKCYJNE
# ============================================
class LibraryItem(ABC):
    """
    Abstrakcyjna klasa bazowa dla wszystkich pozycji w bibliotece.
    Wymusza implementację kluczowych metod w klasach pochodnych.
    """

    def __init__(self, title: str, author: str, year: int):
        """
        Inicjalizuje podstawowe atrybuty pozycji bibliotecznej

        Args:
            title (str): Tytuł pozycji
            author (str): Autor pozycji
            year (int): Rok wydania
        """
        self._title = title  # Pole prywatne (enkapsulacja)
        self._author = author
        self._year = year
        self._item_id = str(uuid.uuid4())  # Unikalny identyfikator
        self._is_available = True  # Status dostępności

    @abstractmethod
    def get_description(self) -> str:
        """Abstrakcyjna metoda - musi być zaimplementowana w klasach dziedziczących"""
        pass

    @property
    def title(self) -> str:
        """Getter dla tytułu z użyciem dekoratora @property"""
        return self._title

    @title.setter
    def title(self, value: str):
        """Setter dla tytułu z walidacją"""
        if not value or not isinstance(value, str):
            raise ValueError("Title must be a non-empty string")
        self._title = value

    @property
    def is_available(self) -> bool:
        """Właściwość tylko do odczytu dla statusu dostępności"""
        return self._is_available

    def borrow(self) -> bool:
        """
        Metoda do wypożyczania pozycji.
        Zwraca True jeśli operacja się powiodła.
        """
        if self._is_available:
            self._is_available = False
            return True
        return False

    def return_item(self) -> None:
        """Metoda do zwracania pozycji do biblioteki"""
        self._is_available = True

    def __str__(self) -> str:
        """Magiczna metoda definiująca stringową reprezentację obiektu"""
        return f"{self._title} by {self._author} ({self._year})"

    def __eq__(self, other: object) -> bool:
        """Magiczna metoda porównująca dwa obiekty po ID"""
        if not isinstance(other, LibraryItem):
            return False
        return self._item_id == other._item_id

    def __lt__(self, other: 'LibraryItem') -> bool:
        """Magiczna metoda porównująca dwa obiekty po roku wydania"""
        return self._year < other._year


# ============================================
# 3. DZIEDZICZENIE WIELOPOZIOMOWE
# ============================================
class Book(LibraryItem):
    """
    Klasa reprezentująca książkę, dziedzicząca po LibraryItem.
    Rozszerza funkcjonalność o dodatkowe atrybuty.
    """

    def __init__(self, title: str, author: str, year: int,
                 book_type: BookType, pages: int):
        """
        Inicjalizuje obiekt Book

        Args:
            title, author, year: parametry z klasy bazowej
            book_type (BookType): Typ książki z enum
            pages (int): Liczba stron
        """
        super().__init__(title, author, year)  # Wywołanie konstruktora klasy bazowej
        self._book_type = book_type
        self._pages = pages
        self._current_reader = None  # Aktualny czytelnik

    def get_description(self) -> str:
        """Implementacja metody abstrakcyjnej z klasy bazowej"""
        return (f"Book: {self._title}, Type: {self._book_type}, "
                f"Pages: {self._pages}")

    @property
    def book_type(self) -> BookType:
        """Getter dla typu książki"""
        return self._book_type

    def borrow(self, reader_name: str) -> bool:
        """
        Przeciążenie metody borrow z klasy bazowej.
        Dodaje informację o czytelniku.
        """
        if super().borrow():  # Wywołanie metody z klasy bazowej
            self._current_reader = reader_name
            return True
        return False

    def return_item(self) -> None:
        """Przeciążenie metody return_item"""
        super().return_item()
        self._current_reader = None

    # Metoda klasowa - alternatywny konstruktor
    @classmethod
    def create_from_dict(cls, data: Dict) -> 'Book':
        """
        Metoda klasowa tworząca obiekt Book z słownika.
        Wzorzec Factory Method.
        """
        return cls(
            title=data['title'],
            author=data['author'],
            year=data['year'],
            book_type=BookType(data['book_type']),
            pages=data['pages']
        )


# ============================================
# 4. DZIEDZICZENIE WIELOKROTNE (MIXIN)
# ============================================
class DigitalContentMixin:
    """
    Mixin dodający funkcjonalność dla treści cyfrowych.
    Mixin nie dziedziczy po LibraryItem, to niezależna klasa.
    """

    def __init__(self, file_size: float, **kwargs):
        """
        Inicjalizuje mixin dla treści cyfrowych

        Args:
            file_size (float): Rozmiar pliku w MB
        """
        super().__init__(**kwargs)  # Ważne dla wielokrotnego dziedziczenia
        self._file_size = file_size
        self._download_count = 0

    def download(self) -> str:
        """Metoda do pobierania cyfrowej wersji"""
        self._download_count += 1
        return f"Downloading {self._file_size}MB"

    @property
    def download_count(self) -> int:
        """Getter dla licznika pobrań"""
        return self._download_count


class Ebook(Book, DigitalContentMixin):
    """
    Klasa reprezentująca ebook, dziedzicząca zarówno po Book jak i DigitalContentMixin.
    Przykład dziedziczenia wielokrotnego.
    """

    def __init__(self, title: str, author: str, year: int,
                 book_type: BookType, pages: int,
                 file_size: float, format: str):
        """
        Inicjalizuje obiekt Ebook

        Args:
            format (str): Format pliku (epub, pdf, mobi)
        """
        # Kolejność wywołania __init__ jest ważna w wielokrotnym dziedziczeniu
        Book.__init__(self, title, author, year, book_type, pages)
        DigitalContentMixin.__init__(self, file_size)
        self._format = format

    def get_description(self) -> str:
        """Przesłonięcie metody z uwzględnieniem cyfrowej natury"""
        base_desc = super().get_description()
        return f"{base_desc}, Format: {self._format}, Size: {self._file_size}MB"

    def borrow(self, reader_name: str) -> bool:
        """
        Dla ebooka 'wypożyczenie' oznacza udostępnienie do pobrania.
        Przeciążenie metody borrow.
        """
        self._current_reader = reader_name
        self._download_count += 1
        return True  # Ebooki są zawsze dostępne


# ============================================
# 5. WZORZEC SINGLETON (Biblioteka główna)
# ============================================
class LibrarySingleton:
    """
    Implementacja wzorca Singleton dla głównej biblioteki.
    Gwarantuje istnienie tylko jednej instancji biblioteki.
    """
    _instance = None  # Pole klasowe przechowujące instancję

    def __new__(cls):
        """
        Przesłonięcie metody __new__ do kontroli tworzenia instancji.
        __new__ jest wywoływane przed __init__.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """
        Inicjalizacja singletona.
        __init__ jest wywoływane za każdym razem, więc potrzebujemy flagi.
        """
        if not self._initialized:
            self._items: List[LibraryItem] = []
            self._members: Dict[str, 'Member'] = {}
            self._initialized = True

    def add_item(self, item: LibraryItem) -> None:
        """Dodaje pozycję do biblioteki"""
        self._items.append(item)

    def find_item(self, title: str) -> List[LibraryItem]:
        """Wyszukuje pozycje po tytule"""
        return [item for item in self._items if title.lower() in item.title.lower()]

    def register_member(self, member: 'Member') -> None:
        """Rejestruje członka biblioteki"""
        self._members[member.member_id] = member

    @property
    def total_items(self) -> int:
        """Zwraca całkowitą liczbę pozycji"""
        return len(self._items)

    @property
    def available_items(self) -> List[LibraryItem]:
        """Zwraca listę dostępnych pozycji"""
        return [item for item in self._items if item.is_available]


# ============================================
# 6. OBSERWATOR (Wzorzec Observer)
# ============================================
class NotificationObserver(ABC):
    """Interfejs obserwatora w wzorcu Observer"""

    @abstractmethod
    def update(self, message: str) -> None:
        """Metoda wywoływana gdy wystąpi zdarzenie"""
        pass


class EmailNotifier(NotificationObserver):
    """Konkretny obserwator - notyfikacja email"""

    def __init__(self, email: str):
        self._email = email

    def update(self, message: str) -> None:
        """Implementacja metody update"""
        print(f"Sending email to {self._email}: {message}")


class SMSNotifier(NotificationObserver):
    """Konkretny obserwator - notyfikacja SMS"""

    def __init__(self, phone: str):
        self._phone = phone

    def update(self, message: str) -> None:
        """Implementacja metody update"""
        print(f"Sending SMS to {self._phone}: {message}")


class ObservableSubject:
    """Podmiot obserwowany w wzorcu Observer"""

    def __init__(self):
        self._observers: List[NotificationObserver] = []

    def attach(self, observer: NotificationObserver) -> None:
        """Dodaje obserwatora"""
        self._observers.append(observer)

    def detach(self, observer: NotificationObserver) -> None:
        """Usuwa obserwatora"""
        self._observers.remove(observer)

    def notify(self, message: str) -> None:
        """Powiadamia wszystkich obserwatorów"""
        for observer in self._observers:
            observer.update(message)


# ============================================
# 7. KLASA Z OBSERWATOREM I ZŁOŻONĄ FUNKCJONALNOŚCIĄ
# ============================================
class Member(ObservableSubject):
    """
    Klasa reprezentująca członka biblioteki.
    Dziedziczy po ObservableSubject (wzorzec Observer).
    """

    def __init__(self, name: str, email: str):
        """
        Inicjalizuje członka biblioteki

        Args:
            name (str): Imię i nazwisko
            email (str): Adres email
        """
        super().__init__()
        self._name = name
        self._email = email
        self._member_id = str(uuid.uuid4())[:8]  # Krótsze ID dla członka
        self._borrowed_items: List[LibraryItem] = []
        self._fine_amount: float = 0.0

    @property
    def member_id(self) -> str:
        """Getter dla ID członka"""
        return self._member_id

    def borrow_item(self, item: LibraryItem, days: int = 14) -> bool:
        """
        Metoda do wypożyczania pozycji przez członka

        Args:
            item (LibraryItem): Pozycja do wypożyczenia
            days (int): Okres wypożyczenia w dniach

        Returns:
            bool: True jeśli wypożyczenie się powiodło
        """
        if item.borrow():
            self._borrowed_items.append(item)
            due_date = datetime.now() + timedelta(days=days)
            message = f"{self._name} borrowed '{item.title}' until {due_date.strftime('%Y-%m-%d')}"
            self.notify(message)  # Powiadomienie obserwatorów
            return True
        return False

    def return_item(self, item: LibraryItem) -> None:
        """Metoda do zwracania pozycji"""
        if item in self._borrowed_items:
            item.return_item()
            self._borrowed_items.remove(item)
            message = f"{self._name} returned '{item.title}'"
            self.notify(message)

    def add_fine(self, amount: float) -> None:
        """Dodaje karę dla członka"""
        self._fine_amount += amount
        if self._fine_amount > 0:
            message = f"Fine for {self._name}: ${self._fine_amount:.2f}"
            self.notify(message)

    def __str__(self) -> str:
        """String representation of member"""
        return f"Member: {self._name} (ID: {self._member_id})"


# ============================================
# 8. METAKLASY - Przykład zaawansowany
# ============================================
class LibraryMeta(type):
    """
    Metaklasa dla klasy z biblioteką.
    Przykład zaawansowanej koncepcji metaprogramowania.
    """

    def __new__(mcs, name, bases, attrs):
        """
        Metoda tworząca nową klasę

        Args:
            mcs: Klasa metaklasy
            name: Nazwa tworzonej klasy
            bases: Klasa bazowe
            attrs: Atrybuty klasy
        """
        # Dodaj automatycznie atrybut klasy
        attrs['_created_by_meta'] = True
        attrs['creation_date'] = datetime.now()

        # Sprawdź czy klasa ma wymagane metody
        required_methods = ['add_item', 'find_item']
        for method in required_methods:
            if method not in attrs:
                raise TypeError(f"Class must implement {method} method")

        return super().__new__(mcs, name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        """
        Metoda wywoływana przy tworzeniu instancji klasy
        """
        instance = super().__call__(*args, **kwargs)
        print(f"Instance of {cls.__name__} created at {datetime.now()}")
        return instance


class SpecialLibrary(metaclass=LibraryMeta):
    """
    Klasa korzystająca z własnej metaklasy.
    Metaklasa dodaje dodatkowe funkcjonalności.
    """

    def __init__(self, name: str):
        self.name = name
        self.items = []

    def add_item(self, item: LibraryItem) -> None:
        """Dodaje pozycję do biblioteki"""
        self.items.append(item)

    def find_item(self, title: str) -> List[LibraryItem]:
        """Wyszukuje pozycje po tytule"""
        return [item for item in self.items if title.lower() in item.title.lower()]


# ============================================
# 9. PRZYKŁAD UŻYCIA SYSTEMU
# ============================================
def demonstrate_library_system():
    """
    Funkcja demonstrująca działanie całego systemu bibliotecznego.
    Pokazuje interakcje między różnymi komponentami.
    """
    print("=" * 60)
    print("DEMONSTRACJA SYSTEMU BIBLIOTECZNEGO")
    print("=" * 60)

    # 1. Utworzenie instancji biblioteki (Singleton)
    print("\n1. Tworzenie biblioteki (Singleton):")
    library1 = LibrarySingleton()
    library2 = LibrarySingleton()
    print(f"Czy to ta sama instancja? {library1 is library2}")

    # 2. Tworzenie różnych typów książek
    print("\n2. Tworzenie pozycji bibliotecznych:")

    # Tradycyjna książka
    book1 = Book(
        title="Python Advanced Programming",
        author="Jan Kowalski",
        year=2023,
        book_type=BookType.SCIENTIFIC,
        pages=450
    )
    print(f"Book 1: {book1}")
    print(f"Opis: {book1.get_description()}")

    # Ebook z dziedziczeniem wielokrotnym
    ebook1 = Ebook(
        title="Data Science Essentials",
        author="Anna Nowak",
        year=2022,
        book_type=BookType.SCIENTIFIC,
        pages=320,
        file_size=5.2,
        format="PDF"
    )
    print(f"\nEbook 1: {ebook1}")
    print(f"Opis: {ebook1.get_description()}")

    # 3. Dodanie pozycji do biblioteki
    library1.add_item(book1)
    library1.add_item(ebook1)
    print(f"\n3. Biblioteka ma {library1.total_items} pozycje")

    # 4. Tworzenie członka z systemem powiadomień
    print("\n4. Rejestracja członka z powiadomieniami:")
    member1 = Member("Jan Kowalski", "jan@example.com")

    # Dodanie obserwatorów (różne kanały notyfikacji)
    email_notifier = EmailNotifier("jan@example.com")
    sms_notifier = SMSNotifier("+48123456789")

    member1.attach(email_notifier)
    member1.attach(sms_notifier)

    # 5. Wypożyczanie pozycji
    print("\n5. Proces wypożyczenia:")
    success = member1.borrow_item(book1, days=21)
    print(f"Wypożyczenie książki: {'Udane' if success else 'Nieudane'}")

    # 6. Demonstracja polimorfizmu
    print("\n6. Demonstracja polimorfizmu:")
    items = [book1, ebook1]

    for item in items:
        print(f"{item.__class__.__name__}: {item.get_description()}")
        print(f"Dostępna: {item.is_available}")

    # 7. Demonstracja metod specjalnych
    print("\n7. Metody specjalne (magiczne):")
    book2 = Book(
        title="Python Basics",
        author="Jan Kowalski",
        year=2020,
        book_type=BookType.NON_FICTION,
        pages=300
    )

    print(f"Porównanie książek (po roku): {book1 > book2}")
    print(f"String reprezentacja: {str(book1)}")

    # 8. Użycie metody klasowej (Factory Method)
    print("\n8. Tworzenie książki z słownika (Factory Method):")
    book_data = {
        'title': 'Clean Code',
        'author': 'Robert C. Martin',
        'year': 2008,
        'book_type': 'Non-Fiction',
        'pages': 464
    }

    book3 = Book.create_from_dict(book_data)
    print(f"Utworzono: {book3}")

    # 9. Biblioteka z metaklasą
    print("\n9. Biblioteka z metaklasą:")
    special_lib = SpecialLibrary("Special City Library")
    print(f"Data utworzenia klasy: {special_lib.creation_date}")

    print("\n" + "=" * 60)
    print("KONIEC DEMONSTRACJI")
    print("=" * 60)


# ============================================
# 10. KLASA STATYSTYK BIBLIOTEKI (DODATKOWY PRZYKŁAD)
# ============================================
class LibraryStatistics:
    """
    Klasa do zbierania statystyk biblioteki.
    Demonstruje kompozycję i zaawansowane operacje na kolekcjach.
    """

    def __init__(self, library: LibrarySingleton):
        """
        Inicjalizuje obiekt statystyk

        Args:
            library (LibrarySingleton): Instancja biblioteki
        """
        self._library = library

    def get_books_by_type(self) -> Dict[BookType, int]:
        """Zwraca liczbę książek według typu"""
        type_count = {book_type: 0 for book_type in BookType}

        for item in self._library._items:
            if isinstance(item, Book):
                type_count[item.book_type] += 1

        return type_count

    def get_most_popular_author(self) -> Optional[str]:
        """Znajduje autora z największą liczbą pozycji"""
        authors = {}

        for item in self._library._items:
            author = item._author
            authors[author] = authors.get(author, 0) + 1

        if authors:
            return max(authors, key=authors.get)
        return None

    def print_statistics(self) -> None:
        """Wypisuje kompleksowe statystyki"""
        print("\n" + "=" * 40)
        print("STATYSTYKI BIBLIOTEKI")
        print("=" * 40)

        books_by_type = self.get_books_by_type()
        print("\nKsiążki według typu:")
        for book_type, count in books_by_type.items():
            print(f"  {book_type}: {count}")

        popular_author = self.get_most_popular_author()
        print(f"\nNajpopularniejszy autor: {popular_author}")

        available = len(self._library.available_items)
        total = self._library.total_items
        print(f"\nDostępne pozycje: {available}/{total} ({available / total * 100:.1f}%)")


# ============================================
# GŁÓWNY PROGRAM
# ============================================
if __name__ == "__main__":
    # Uruchomienie demonstracji
    demonstrate_library_system()

    # Dodatkowe statystyki
    library = LibrarySingleton()
    stats = LibraryStatistics(library)
    stats.print_statistics()