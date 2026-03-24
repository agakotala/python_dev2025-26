from builtins import property, float, list, dict, KeyError, ValueError

from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    net: float
    vat: float = 0.08

    @property
    def gross(self) -> float:
        return round(self.net * (1+self.vat),2)

@dataclass
class Customer:
    name: str
    points: int = 0

    def earn_points(self, amount: float) -> None:
        self.points += int(amount)

    def use_points(self, pts: int) -> float:
        pts = min(pts, self.points)

        self.points -= pts
        return round(pts * 0.05, 2)
@dataclass
class CartLine:
    product: Product
    qty: int = 1
    addons: list[Product] = field(default_factory=list)

    def total(self) -> float:
        addons_sum = sum(a.gross for a in self.addons)
        return round((self.product.gross + addons_sum) * self.qty, 2)

class SimpleCafe:
    def __init__(self, name: str):
        self.name = name
        self.menu: dict[str, Product] = {}
        self.addons: dict[str, Product] = {}
        self.stock: dict[str, int] = {}
        self.sales: list[float] = []

    def add_product(self, p: Product, stock: int = 0):
        self.menu[p.name] = p
        self.stock[p.name] = self.stock.get(p.name, 0) + stock

    def add_addon(self, a: Product):
        self.addons[a.name] = a

    def add_to_cart(self, cart: list[CartLine], product_name: str, qty: int = 1, addon_names: list[str] | None = None):
        if product_name not in self.menu:
            raise KeyError(f'Produkt "{product_name}" brak w Menu')
        if self.stock.get(product_name, 0) < qty:
            raise ValueError(f"Brak na stanie: {product_name}")

        addon_list = []
        for n in (addon_names or []):
            if n not in self.addons:
                raise KeyError(f"Nie ma dodatku: {n}")
            addon_list.append(self.addons[n])

        cart.append(CartLine(self.menu[product_name], qty, addon_list))
        self.stock[product_name] -= qty

    def cart_total(self, cart: list[CartLine], customer: Customer | None = None, use_points: int = 0) -> float:
        subtotal = round(sum(line.total() for line in cart), 2)
        discount = customer.use_points(use_points) if customer and use_points > 0 else 0.0
        return max(round(subtotal - discount, 2), 0.0)

    def pay(self, amount: float, method: str, cash_given: float = 0.0, last4: str = "0000") -> str:
        if method == "cash":
            if cash_given < amount:
                raise ValueError("Za mało gotówki.")
            else:
                change = round(cash_given - amount, 2)
                return f"Gotówka OK, reszta: {change:.2f} PLN"
        elif method == "card":
            return f"Karta ****{last4} obciążona {amount:.2f} PLN"
        else:
            raise ValueError("Nieznana metoda płatności (cash/card).")

    def checkout(self, cart: list[CartLine], customer: Customer | None, method: str, use_points: int = 0, **pay_kwargs) -> str:
        amount = self.cart_total(cart, customer, use_points)
        receipt = self.pay(amount, method, **pay_kwargs)

        if customer:
            customer.earn_points(amount)
        self.sales.append(amount)
        cart.clear()
        return f"Opłacono: {amount:.2f} PLN. {receipt}"
    def report(self) -> str:
        return f"{self.name}\nTransakcje: {len(self.sales)}\nSuma: {sum(self.sales):.2f} PLN"

def demo():
    cafe = SimpleCafe("Prosta Kawiarnia")
    cafe.add_product(Product("Espresso", 10.0), stock=10)
    cafe.add_product(Product("Latte", 14.0), stock=5)
    cafe.add_product(Product("Sernik", 20.0, vat=0.05), stock=8) #dodanie produktu z innym vatem
    cafe.add_addon(Product("Syrop waniliowy", 2.5))
    cafe.add_addon(Product("Mleko owsiane", 3.0))

    alice = Customer("Alicja")
    cart = []

    cafe.add_to_cart(cart, "Latte", qty = 2, addon_names = ["Syrop waniliowy"])
    cafe.add_to_cart(cart, "Sernik", qty = 1)
    print(cafe.checkout(cart, alice, method="card", last4="1234"))

    cafe.add_to_cart(cart, "Espresso", qty = 3, addon_names = ["Syrop waniliowy"])
    print(cafe.checkout(cart, alice, method="cash", use_points = 5, cash_given = 100))

    print("Punkty ALicji:", alice.points)
    print("---RAPORT---")
    print(cafe.report())

if __name__ == "__main__":
    demo()