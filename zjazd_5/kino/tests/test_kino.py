import pytest
from datetime import datetime
from kino_oop_demo import (
    Film,
    Gatunek,
    Miejsce,
    Seans,
    Kino,
    StrategiaPopularnosci,
    StrategiaGatunku,
    CenaBazowa,
    DopłataPremium,
    PromocjaSroda,
    WalidatorWiek,
    WalidatorMiejsc
)

@pytest.fixture
def film_komedia():
    return Film(
        tytul = "Test Komedia",
        gatunek=Gatunek.KOMEDIA,
        cena_bazowa=30.0,
        limit_wiek=0
    )

@pytest.fixture
def film_limit_16():
    return Film(
        tytul = "Test 16+",
        gatunek=Gatunek.DRAMAT,
        cena_bazowa=35.0,
        limit_wiek=16  #kluczowy element wiek min 16
    )

@pytest.fixture
def miejsca():
    return [
        Miejsce(rzad=1, numer=1, premium=True), #miejsce premium
        Miejsce(rzad=1, numer=4, premium=False) #miejsce standard
    ]

@pytest.fixture
def seans(film_komedia):
    start = datetime(2026, 1 , 14, 20, 0 ,0) #start filmu w środe 14/01/2026 znizka
    wszystkie = [
        Miejsce(rzad=1, numer=n, premium=(n <=2))  #dla nr 1 - 2 premium, reszta standard
        for n in range(1, 9)
    ]
    return Seans(
        film = film_komedia,
        start = start,
        sala="Sala-1",
        miejsca=wszystkie
    )

@pytest.fixture
def kino(seans, film_komedia):
    k = Kino(strategia=StrategiaPopularnosci())
    k.dodaj_film(film_komedia)
    k.dodaj_seans(seans)
    return k

def test_film_nie_pozwala_na_ujemna_cene():
    with pytest.raises(ValueError):
        Film(
            tytul="X",
            gatunek=Gatunek.AKCJA,
            cena_bazowa=-1.0 #ujemna cena ma na celu wyrzucic error
        )

def test_film_ucina_za_dlugi_tytul():
    long_title = "A" * 200
    f = Film(
        tytul = long_title, #za dlugi tytul
        gatunek=Gatunek.SCIFI,
        cena_bazowa=10.0
    )
    assert len(f.tytul) <= 45

def test_walidator_wiek_rzuca_gdy_za_mlody(film_limit_16, seans, miejsca):
    w = WalidatorWiek()
    with pytest.raises(ValueError):
        w.sprawdz(
            film=film_limit_16,
            wiek=15,  #wiek ponizej limitu - powinien wyrzucic blad wieku
            seans=seans,
            miejsca=miejsca,
        )

def test_walidator_miejsc_rzuca_go_zajete(seans, miejsca):
    seans.zajmij(miejsca[0])
    w = WalidatorMiejsc()
    with pytest.raises(ValueError):
        w.sprawdz(
            film=seans.film,
            wiek=18,
            seans=seans,
            miejsca=miejsca  #powinien wyrzucic blad, bo lista zawiera zajete miejsce
        )

def test_cena_premium_plus_promocja_sroda(seans):
    miejsce_premium = Miejsce(rzad=1, numer=1, premium=True) #powinna zadzialac doplata
    base = CenaBazowa()
    kalk = PromocjaSroda(DopłataPremium(base)) #skladanie dekoratorow najpierw doplata premium, potem pormo sroda
    #baza 30 + 15 (premium) = 45, sroda(promo 20%) => 45*0.8 = 36
    cena = kalk.policz(seans.film, miejsce_premium, seans.start)
    assert cena == 36.0 #sprawdzamy czy cena dobrze sie policzyla, oczekujemy wynik 36

def test_strategia_gatunku_filtruje(kino, film_komedia):
    from kino_oop_demo import Film, Gatunek
    film_inny = Film(tytul="Inny", gatunek=Gatunek.AKCJA, cena_bazowa=25.0)
    kino.dodaj_film(film_inny)

    kino.zmien_strategie(StrategiaGatunku(Gatunek.KOMEDIA))
    rec = kino.polec_filmy(limit=10)

    assert all(f.gatunek == Gatunek.KOMEDIA for f in rec)
    assert film_komedia in rec

@pytest.mark.asyncio
async def test_kup_bilety_sukces_zajmuje_miejsca(monkeypatch, kino, seans, miejsca):
    import kino_oop_demo
    monkeypatch.setattr(
        kino_oop_demo.random,
        "random",
        lambda: 0.0  # Zwracamy zawsze 0.0, czyli warunek sukcesu zawsze spełniony
    )

    kalk = CenaBazowa()
    rez = await kino.kup_bilety(
        seans_id=seans.id,
        wiek=18,
        miejsca=miejsca,
        kalk=kalk
    )

    assert rez.status.value == "potwierdzona"
    assert all(not seans.czy_wolne(m) for m in miejsca)


@pytest.mark.asyncio
async def test_kup_bilety_fail_zwalnia_miejsca(monkeypatch, kino, seans, miejsca):  # Test: porażka płatności
    import kino_oop_demo
    monkeypatch.setattr(
        kino_oop_demo.random,
        "random",
        lambda: 0.99  # płatność zawsze nieudana
    )
    kalk = CenaBazowa()
    with pytest.raises(RuntimeError):
        await kino.kup_bilety(
            seans_id=seans.id,
            wiek=18,
            miejsca=miejsca,
            kalk=kalk
        )
    assert all(seans.czy_wolne(m) for m in miejsca)


def test_promocja_sroda_nie_dziala_w_czwartek(seans):
    from datetime import datetime
    from kino_oop_demo import CenaBazowa, DopłataPremium, PromocjaSroda, Miejsce
    czwartek = datetime(2026, 1, 15, 20, 0 ,0)
    miejsce_premium = Miejsce(rzad=1, numer=1, premium=True)
    base = CenaBazowa()
    kalk = PromocjaSroda(DopłataPremium(base))
    cena = kalk.policz(seans.film, miejsce_premium, czwartek)
    assert cena == 45.0  #cena bez zniki a z doplata premium

def test_generator_seansow_tworzyl_seanse_poprawnie(kino):
    from kino_oop_demo import Seans
    gen = kino.generuj_seanse(ile=3)

    s1 = next(gen)
    s2 = next(gen)
    s3 = next(gen)

    assert isinstance(s1, Seans)
    assert s1.film is not None
    assert isinstance(s1.sala, str) and s1.sala.startswith("Sala-")

    assert (s2.start - s1.start).total_seconds() == 2 * 3600 #czy seanse startuja co 2h
    assert (s3.start - s2.start).total_seconds() == 2 * 3600