import strawberry
from typing import List
from datetime import datetime

@strawberry.type
class Student:
    id: int
    imie: str
    nazwisko: str
    kierunek: str
    rok_studiow: int

@strawberry.type
class Przedmiot:
    id: int
    nazwa: str
    prowadzacy: str

@strawberry.type
class Ocena:
    id: int
    student_id: int
    przedmiot_id: int
    ocena: float
    data: str
    komentarz: str

@strawberry.type
class StatystykiStudenta:
    student: Student
    srednia_ocen: float
    liczba_ocen: int
    najlepsza_ocena: float
    najgorsza_ocena: float


studenci = [
    Student(id=1, imie="Anna", nazwisko="Kowalska", kierunek="Informatyka", rok_studiow=2),
    Student(id=2, imie="Jan", nazwisko="Nowak", kierunek="Matematyka", rok_studiow=3),
    Student(id=3, imie="Katarzyna", nazwisko="Kowal", kierunek="Fizyka",rok_studiow=1),
]

przedmioty = [
    Przedmiot(id=1, nazwa="Programowanie", prowadzacy="Dr Nowak"),
    Przedmiot(id=2, nazwa="Bazy danych", prowadzacy="Dr Kowalczyk"),
    Przedmiot(id=3, nazwa="Algebra", prowadzacy="Prof. Adamski"),
]

oceny = [
    Ocena(id=1, student_id=1, przedmiot_id=1, ocena=5.0, data="12-12-2025", komentarz="Bardzo dobry"),
    Ocena(id=2, student_id=1, przedmiot_id=2, ocena=4.5, data="03-10-2025", komentarz="Dobry plus"),
    Ocena(id=3, student_id=2, przedmiot_id=3, ocena=3.5, data="12-11-2025", komentarz="Dostateczny plus"),
    Ocena(id=4, student_id=2, przedmiot_id=2, ocena=4.0, data="25-11-2025", komentarz="Dobry"),
    Ocena(id=5, student_id=3, przedmiot_id=1, ocena=2.0, data="03-12-2025", komentarz="Niezaliczone"),
]

@strawberry.type
class Query:
    #pobierz wszystkich stduentow
    @strawberry.field
    def studenci(self) -> List[Student]:
        return studenci
    #pobierz studenta po ID
    @strawberry.field
    def student(self, id:int) -> Student:
        for s in studenci:
            if s.id == id:
                return s

        raise ValueError(f"Student o ID {id} nie istnieje")
    #pobierz wsyztskie przedmioty
    @strawberry.field
    def przedmioty(self) -> List[Przedmiot]:
        return przedmioty
    #pobierz oceny studenta
    @strawberry.field
    def oceny_studenta(self, student_id: int) -> List[Ocena]:
        return [o for o in oceny if o.student_id == student_id]
    #pobierz statystyki studenta
    @strawberry.field
    def statystyki_studenta(self, student_id: int) -> StatystykiStudenta:
        oceny_studenta = [o.ocena for o in oceny if o.student_id == student_id]
        if not oceny_studenta:
            raise ValueError(f"Student o ID {student_id} nie ma ocen")

        student = None
        for s in studenci:
            if s.id == student_id:
                student = s
                break

        return StatystykiStudenta(
            student=student, #obiekt student
            srednia_ocen=sum(oceny_studenta)/ len(oceny_studenta), #srednia ocen
            liczba_ocen=len(oceny_studenta), #liczba ocen
            najgorsza_ocena=min(oceny_studenta), #najgorsza ocena
            najlepsza_ocena=max(oceny_studenta) #najlepsza ocena
        )

@strawberry.type
class Mutation:
    #dodaj nowego studenta
    @strawberry.mutation
    def dodaj_studenta(self, imie: str, nazwisko: str, kierunek: str, rok_studiow: int) -> Student:
        nowy_id = max([s.id for s in studenci])+1 if studenci else 1
        nowy_student = Student(
            id=nowy_id,
            imie=imie,
            nazwisko=nazwisko,
            kierunek=kierunek,
            rok_studiow=rok_studiow,
        )

        studenci.append(nowy_student)
        return nowy_student
    #dodaj nowa ocene
    @strawberry.mutation
    def dodaj_ocene(self, student_id: int, przedmiot_id: int, ocena: float, komentarz: str = "" ) -> Ocena:
        if not any(s.id == student_id for s in studenci):
            raise ValueError(f"Student o ID {student_id} nie istnieje")
        if not any(p.id == przedmiot_id for p in przedmioty):
            raise ValueError(f"Przedmiot o ID {przedmiot_id} nie istnieje")

        nowy_id = max([o.id for o in oceny]) + 1 if oceny else 1

        nowa_ocena = Ocena(
            id=nowy_id,
            student_id=student_id,
            przedmiot_id=przedmiot_id,
            ocena=ocena,
            data=datetime.now().strftime("%Y-%m-%d"),
            komentarz=komentarz,
        )
        oceny.append(nowa_ocena)
        return nowa_ocena
    @strawberry.mutation
    def aktualizuj_ocene(self, ocena_id: int, nowa_ocena: float, nowy_komentarz: str = "" ) -> Ocena:
        for o in oceny:
            if o.id == ocena_id:
                o.ocena = nowa_ocena
                return o
        raise ValueError(f"Ocena o ID {ocena_id} nie istnieje")

schemat = strawberry.Schema(query=Query, mutation=Mutation)

if __name__ == '__main__':
    from strawberry.asgi import GraphQL
    from uvicorn import run
    app = GraphQL(schemat)

    print("SCHEMAT OCEN STUDENTÓW - GraphQL")
    print("Serwer działa na: http://127.0.0.1:8002")
    print("GraphQL: http://127.0.0.1:8002/graphql")
    print("\nDostępne zapytania (Queries):")
    print("1. studenci - Pobierz wszystkich studentów")
    print("2. student(id: 1) - Pobierz studenta")
    print("3. przedmioty - Pobierz przedmioty")
    print("4. ocenyStudenta(studentId: 1) - Pobierz oceny")
    print("5. statystykiStudenta(studentId: 1) - Pobierz statystyki")

    print("\nDostępne mutacje (Mutation):")
    print("1. dodajStudenta(..) - Dodaj studenta")
    print("2. dodajOcene(..) - Dodaj ocene")
    print("3. aktualizuj_ocene(..) - Aktualizuj ocene")

    run(app, host="127.0.0.1", port=8002)
