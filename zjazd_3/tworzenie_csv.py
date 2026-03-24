import pandas as pd
import random

random.seed(42) #ziarno losowości

imiona = ["Anna", "Antek", "Agata", "Jan", "Beata", "Ela", "Joanna", "Ewa", "Tomasz", "Sylwia", "Jurek", "Magda", "Ola", "Klaudia"]
miasta = ["Adamczycha", "Warszawa", "Legnica", "Gdańsk", "Pcim", "Kobyla Góra", "Łódź", "Limanowa"]

n = 1000 #liczba rekordów

dane = {
    "imie": [random.choice(imiona) for _ in range(n)],
    "miasto": [random.choice(miasta) for _ in range(n)],
    "dochód": [random.randint(5800, 58200) for _ in range(n)],
    "ma dzieci": [],
    "liczba dzieci": [],
    "ma zwierze": [],
    "jakie zwierze": []
}

for _ in range(n):
    if random.choice([True, False]):
        dane["ma dzieci"].append("Tak") #jesli tak napisz tak
        dane["liczba dzieci"].append(random.randint(1, 4))
    else:
        dane["ma dzieci"].append("Nie")
        dane["liczba dzieci"].append(0)
    if random.choice([True, False]):
        dane["ma zwierze"].append("Tak")
        dane["jakie zwierze"].append(random.choice(["pies", "kot", "słoń", "małpa"]))
    else:
        dane["ma zwierze"].append("Nie")
        dane["jakie zwierze"].append("brak")

df = pd.DataFrame(dane)
df.to_csv("ludzie_i_zwierzeta.csv", index=False, encoding='utf-8-sig')
print("plik zapisany")
