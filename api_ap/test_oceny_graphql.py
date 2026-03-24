import requests
import json

from fontTools.tfmLib import PASSTHROUGH
from strawberry.federation import mutation

BASE_URL = "http://localhost:8002/graphql"  #adres serwera

print("Test GraphQL API - SYSTEM OCEN STUDENTÓW")

def test_graphql(query, operation_name=None, variables=None):
    payload = {"query": query}

    if operation_name and "query" in query or "mutation" in query:
        pass
    else:
        operation_name = None

    if variables:
        payload["variables"] = variables
    try:
        headers = {"Content-Type": "application/json"}

        response = requests.post(BASE_URL, json=payload, headers=headers)

        print(f"Zapytanie GraphQL")
        if response.status_code == 200:
            data = response.json()
            payload = response.json()
            print("RAW:", payload)

            if "errors" in payload:
                print("ERRORS:")
                for e in payload["errors"]:
                    print("-", e.get("message"))
                    # często jest też:
                    if "path" in e: print("  path:", e["path"])
                    if "locations" in e: print("  locations:", e["locations"])
                    if "extensions" in e: print("  extensions:", e["extensions"])

            print("Dane:")
            print(payload.get("data"))
            if "errors" in data:
                print(f" Błędy: {data['errors']}")
                return None
            else:
                print("Sukces")
                if "data" in data:
                    formatted = json.dumps(data["data"], indent=2, ensure_ascii=False)
                    print(f"Dane:\n{formatted}")
                return data.get("data")
        else:
            print(f"Błąd HTTP {response.status_code}: {response.text[:100]}")
            return None

    except Exception as e:
        print(f" Wyjątek: {e}")
        return None


query_studenci = """
{
  studenci {
    id
    imie
    nazwisko
    kierunek
    rokStudiow
  }
}
"""
print("\n1. Pobieram listę studentów...")
test_graphql(query_studenci)
query_studenci_z_ocenami = """
{
  student(id: 1) {
    imie
    nazwisko
    kierunek
  }
  ocenyStudenta(student_id: 1) {
    id
    ocena
    data
    komentarz
  }
}
"""

print("2. Pobieram studenta ID 1 z ocenami...")
test_graphql(query_studenci_z_ocenami)

query_statystki = """
{
  statystykiStudenta(student_id: 1) {
    student {
      imie
      nazwisko
    }
    sredniaOcen
    liczbaOcen
    najlepszaOcena
    najgorszaOcena
  }
}
"""
print("3. Pobieram statystki studenta ID 1...")

test_graphql(query_statystki)

mutation_dodaj_studenta = """
mutation DodajNowegoStudenta($imie: String!, $nazwisko: String!, $kierunek: String!, $rokStudiow: Int!) {
  dodajStudenta(imie: $imie, nazwisko: $nazwisko, kierunek: $kierunek, rokStudiow: $rokStudiow) {
    id
    imie
    nazwisko
    kierunek
    rokStudiow
  }
}
"""
variables_student = {
    "imie": "Jan",
    "nazwisko": "Kowalski",
    "kierunek": "Informatyka",
    "rokStudiow": 2
}

print("4. Dodaje nowego studenta...")
test_graphql(mutation_dodaj_studenta, "DodajNowegoStudenta", variables_student)

mutation_dodaj_ocene_simple = """
  dodajOcene(student_id: 1, przedmiot_id: 1, ocena: 4.5, komentarz: "Testowa ocena") {
    id
    student_id
    przedmiot_id
    ocena
    data
    komentarz
  }
}
"""
print("5. Dodaję ocenę dla studenta ID 1...")
test_graphql(mutation_dodaj_ocene_simple)

mutation_dodaj_ocene_simple = """
mutation {
  dodajOcene(studentId: 1, przedmiotId: 1, ocena: 4.5, komentarz: "Testowa ocena") {
    id
    studentId
    przedmiotId
    ocena
    data
    komentarz
  }
}
"""
print("6. Pobieram wszytskie oceny...")
test_graphql(query_wszystkie_oceny)

query_przedmioty = """
{
  przedmioty {
    id
    nazwa
    prowadzacy
  }
}
"""
print("7. Pobieram przedmioty...")
test_graphql(query_przedmioty)

print("WSYZTSKIE TESTY ZAKOŃCZONE")
print(f" Otwórz w przeglądarce: {BASE_URL}")

