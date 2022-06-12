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

    def is_on_offer(self) -> bool:
        return self.item in OFFERS

    def total_cost(self) -> int:
        if not self.is_on_offer():
            return PRICES[self.item] * self.quantity

        offer = OFFERS[self.item]
        quantity_of_offer, remainder = divmod(self.quantity, offer.quantity)

        return PRICES[self.item] * remainder + offer.cost * quantity_of_offer


@dataclass
class Cart:
    items: List[CartItem]

    def total_cost(self) -> int:
        return sum((item.total_cost() for item in self.items))

@dataclass
class Offer:
    item: str
    quantity: int
    cost: int


PRICES = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15
}

OFFERS = {
    "A": Offer(item="A", quantity=3, cost=130),
    "B": Offer(item="B", quantity=2, cost=45)
}


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    try:
        cart = parse_cart(skus)
    except CartException:
        return -1

    return cart.total_cost()

def parse_cart(skus) -> Cart:
    if not skus:
        return Cart(items=[])

    cart = Counter(skus)

    if set(cart) - set(PRICES.keys()):
        raise NonexistentItemException()

    items = [CartItem(item=item, quantity=quantity) for item, quantity in cart.items()]
    return Cart(items=items)

