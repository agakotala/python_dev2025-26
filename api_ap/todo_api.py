from fastapi import FastAPI
from starlette.responses import HTMLResponse

app = FastAPI()

todo_list = []

class Zadanie:
    def __init__(self, id: int, tytul: str, opis: str, zrobione: bool = False):
        self.id = id
        self.tytul = tytul
        self.opis = opis
        self.zrobione = zrobione

todo_list.append(Zadanie(1, "Zrobić zakupy", "Mleko, chleb jajka"))
todo_list.append(Zadanie(2, "Nauczyć się Pythona", "Przeczytać dokumentację FastAPI"))
todo_list.append(Zadanie(3, "Posprzątać pokój", "Odkurzyć i umyć podłogę"))

@app.get("/")
def witaj():
    return{"wiadomość": "Witaj w API Listy Zadań!", "autor": "Twoje API"}

@app.get("/zadania/")
def pobierz_wszystkie_zadania():
    return{"zadania": [vars(z) for z in todo_list]}

@app.get("/zadania/{id_zadania}")
def pobierz_zadanie(id_zadania: int):
    for zadanie in todo_list:
        if zadanie.id == id_zadania:
            return vars(zadanie)
    return {"error": "Zadnie nie znalezione"}

@app.post("/zadania/dodaj")
def dodaj_zadanie(tytul: str, opis: str):
    max_id = max([z.id for z in todo_list]) if todo_list else 0

    nowe_zadanie = Zadanie(
        id = max_id +1,
        tytul = tytul,
        opis = opis,
        zrobione = False
    )

    todo_list.append(nowe_zadanie)

    return {"sukces": True, "nowe_zadanie": vars(nowe_zadanie)}

@app.put("/zadania/{id_zadania}/zrobione")
def oznacz_zrobione(id_zadania: int):
    for zadanie in todo_list:
        if zadanie.id == id_zadania:
            zadanie.zrobione = True
            return{"sukces": True, "nowe_zadanie": vars(zadanie)}
    return {"error": "Zadanie nie znalezione"}

@app.delete("/zadania/{id_zadania}/usun")
def usun_zadanie(id_zadania: int):
    for i, zadanie in enumerate(todo_list):
        if zadanie.id == id_zadania:
            usuniete = todo_list.pop(i)
            return {"sukces": True, "usuniete": vars(usuniete)}
    return {"error": "Zadanie nie znalezione"}

@app.get("/zadania/filtruj/{status}")
def filtruj_zadania(status: str):
    if status == "zrobione":
        zadania = [z for z in todo_list if z.zrobione]
    elif status == "niezrobione":
        zadania = [z for z in todo_list if not z.zrobione]
    else:
        return {"error": "Nieprawidłowy status"}

    return {"zadania": [vars(z) for z in zadania]}

if __name__ == "__main__":
    import uvicorn

    print("API LISTY ZADAŃ - FASTAPI")
    print("Serwer działa na: http://127.0.0.1:8004")
    print("Dokumentacja: http://127.0.0.1:8004/docs")
    print("\nDostępne endpointy:")
    print("1. GET /     - Strona główna")
    print("2. GET /zadania/    - Pobierz wszystkie zadania")
    print("3. GET /zadania/{id} - Pobierz pojedyncze zadanie")
    print("4. POST /zadania/dodaj  - Dodaj nowe zadanie")
    print("5. PUT /zadania/{id}/zrobione - Oznacz jako zrobione")
    print("6. DELETE /zadania/{id}/usun  - Usuń zadanie")
    print("7. GET /zadania/filtruj/{status} - Filtruj zadania")

    uvicorn.run(app, host="127.0.0.1", port=8004)