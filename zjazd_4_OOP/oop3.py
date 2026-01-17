from builtins import float, ValueError


class KontoBankowe:

    def __init__(self, wlasciciel: str, saldo_start: float = 0.0) -> None:
        if not wlasciciel:
            raise ValueError("Właściciel nie może być pusty.")
        if not (saldo_start >= 0):
            raise ValueError("Saldo startowe nie może być ujemne.")
        self.wlasciciel = wlasciciel
        self._saldo = float(saldo_start) #enkapsulacja (pole wewnętrzne)
    @property
    def saldo(self) -> float:
        return self._saldo
    def wplata(self, kwota: float) -> None:
        if kwota <= 0:
            raise ValueError ("Kwota wpłaty musi być > 0.")
        self._saldo += float(kwota)
    def wyplata(self, kwota: float) -> None:
        if kwota <= 0:
            raise ValueError("Kwota wypłaty musi być > 0.")
        if kwota > self._saldo:
            raise ValueError("Brak środków.")
        self._saldo -= float(kwota)

class KontoOszczednosciowe(KontoBankowe):
    def __init__(self, wlasciciel: str, saldo_start: float = 0.0, limit_dzienny: float = 200.0) -> None:
        super().__init__(wlasciciel, saldo_start)
        self._limit_dzienny = float(limit_dzienny)
        self._wyplacono_dzis = 0.0
    @property
    def limit_dzienny(self) -> float:
        return self._limit_dzienny
    @limit_dzienny.setter
    def limit_dzienny(self, nowy_limit: float) -> None:
        nowy_limit = float(nowy_limit)
        if nowy_limit <= 0:
            raise ValueError("Limit dzienny musi być > 0.")
        self._limit_dzienny = nowy_limit
    def wyplata(self, kwota: float) -> None:
        kwota = float(kwota)
        if self._wyplacono_dzis + kwota > self._limit_dzienny:
            raise ValueError("Przekroczono limit dzienny wypłat.")
        super().wyplata(kwota)

        self._wyplacono_dzis += kwota
    def reset_dnia(self) -> None:
        self._wyplacono_dzis = 0.0

konto = KontoOszczednosciowe("Jan", saldo_start=500, limit_dzienny=300)
print("Saldo:", konto.saldo)
konto.wyplata(50)
print("Saldo po wypłacie 50zł:", konto.saldo)

konto.limit_dzienny = 200
print("Nowy limit:", konto.limit_dzienny)

try:
    konto.wyplata(260)
except ValueError as e:
    print("Błąd", e)