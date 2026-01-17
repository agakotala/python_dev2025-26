from fastapi import FastAPI, HTTPException

app = FastAPI(title="Prosty Kalkulator REST")

@app.get("/")
def witaj():
    return {"wiadomość": "Kalkulator REST API", "dostępne operacje": [
        "/dodaj/{a}/{b}",
        "/odejmij/{a}/{b}",
        "/pomnoz/{a}/{b}",
        "/podziel/{a}/{b}",
        "/potega/{a}/{b}",
        "/pierwiastek/{a}/{b}",
        "/historia"
    ]}

@app.get("/dodaj/{a}/{b}")
def dodaj(a:float, b:float):
    """Dodawanie dwóch liczb"""
    wynik = a + b
    zapisz_operacje(f"{a} + {b} = {wynik}")
    return {"operacja": "dodawanie", "a": a, "b": b, "wynik": wynik}

@app.get("/odejmij/{a}/{b}")
def odejmij(a:float, b:float):
    """Odejmowanie dwóch liczb"""
    wynik = a - b
    zapisz_operacje(f"{a} - {b} = {wynik}")
    return {"operacja": "odejmowanie", "a": a, "b": b, "wynik": wynik}

@app.get("/pomnoz/{a}/{b}")
def pomnoz(a:float, b:float):
    """Mnożenie dwóch liczb"""
    wynik = a * b
    zapisz_operacje(f"{a} * {b} = {wynik}")
    return {"operacja": "mnożenie", "a": a, "b": b, "wynik": wynik}

@app.get("/podziel/{a}/{b}")
def podziel(a:float, b:float):
    """Dzielenie dwóch liczb"""
    if b == 0:
        raise HTTPException(status_code=400, detail="Nie można dzielić przez 0!")
    wynik = a / b
    zapisz_operacje(f"{a} / {b} = {wynik}")
    return {"operacja": "dzielenie", "a": a, "b": b, "wynik": wynik}

@app.get("/potega/{a}/{b}")
def potega(a:float, b:float):
    """Potęgowanie: a do potęgi b"""
    wynik = a ** b
    zapisz_operacje(f"{a} ** {b} = {wynik}")
    return {"operacja": "potęgowanie", "a": a, "b": b, "wynik": wynik}

@app.get("/pierwiastek/{a}/{b}")
def pierwiastek(a:float, b:float):
    """Pierwiastek kwadratowy"""
    if a < 0:
        raise HTTPException(status_code=400, detail="Nie można obliczyć pierwiastka z liczby ujemnej")
    import math
    wynik = math.sqrt(a)
    zapisz_operacje(f"√{a} = {wynik}")
    return {"operacja": "pierwiastek", "liczba": a, "wynik": wynik}

@app.get("/oblicz/{wyrazenie}")
def oblicz_wyrazenie(wyrazenie: str):
    """Dowolne wyrażenie matematyczne"""
    try:
        dozwolone_znaki = set("0123456789+-*/.() ")
        if not all(z in dozwolone_znaki for z in wyrazenie):
            raise ValueError("Niedozwolone znaki w wyrażeniu")

        wynik = eval(wyrazenie)
        zapisz_operacje(f"{wyrazenie} = {wynik}")
        return {"wyrażenie": wyrazenie, "wynik": wynik}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Błąd obliczeń: {str(e)}")


historia = []

def zapisz_operacje(operacja: str):
    import datetime

    historia.append({
        "czas": datetime.datetime.now().strftime("%H:%M:%S"),
        "operacja": operacja,
    })

    if len(historia) > 20:
        historia.pop(0)

@app.get("/historia")
def pokaz_historie(limit: int = 10):
    """Pokaż historię operacji"""
    return {"historia": historia[-limit:], "liczba operacji": len(historia)}

if __name__ == "__main__":
    import uvicorn

    print("Kalkulator prosty REST API")
    print("Serwer działa na: http://127.0.0.1:8010")
    print("Dokumentacja: http://127.0.0.1:8010/docs")
    print("\nPrzykłady użycia:")
    print("1. Dodawanie:      /dodaj/10/5")
    print("2. Odejmowanie:    /odejmij/10/5")
    print("3. Mnożenie:       /pomnoz/10/5")
    print("4. Dzielenie:      /podziel/10/5")
    print("5. Potęgowanie:    /potega/2/3")
    print("6. Pierwiastek:    /pierwiastek/25")
    print("7. Wyrażenie:      /oblicz/(10+5)*2")
    print("8. Historia:       /historia")

    uvicorn.run(app, host="127.0.0.1", port=8010)
