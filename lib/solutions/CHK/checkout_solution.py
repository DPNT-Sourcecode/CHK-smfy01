from collections import Counter
from dataclasses import dataclass
from typing import List

class CartException(Exception):
    pass

class NonexistentItemException(CartException):
    pass

@dataclass
class CartItem:
    item: str
    quantity: int

    def total_cost(self) -> int:
        return PRICES[self.item] * self.quantity

@dataclass
class Cart:
    items: List[CartItem]

    def total_cost(self) -> int:
        return sum((item.total_cost for item in self.items))


PRICES = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15
}


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    try:
        cart = parse_cart(skus)
    except CartException:
        return -1

def parse_cart(skus) -> Cart:
    if not skus:
        return []

    cart = Counter(skus)

    if set(cart) - set(PRICES.keys()):
        raise NonexistentItemException()

    items = [CartItem(item=item, quantity=quantity) for item, quantity in cart.items()]
    return Cart(items=items)


def price_of_sku(sku: string, quantity: int) -> int:





