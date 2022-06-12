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

    def offer_cost(self) -> int:
        # Try largest offer first, then decrease offer quantity
        item_offers = OFFERS[self.item].values()
        quantity_remaining = self.quantity
        total = 0
        for offer in item_offers:
            quantity_of_offer, remainder = divmod(quantity_remaining, offer.quantity)

            if quantity_of_offer > 0:
                total += offer.cost * quantity_of_offer

            if remainder == 0:
                return total

            quantity_remaining = remainder

        # After all offers applied, we may have some left at unit price
        return UNIT_COSTS[self.item] * remainder + total

    def total_cost(self) -> int:
        if not self.is_on_offer():
            return UNIT_COSTS[self.item] * self.quantity

        return self.offer_cost()


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


UNIT_COSTS = {"A": 50, "B": 30, "C": 20, "D": 15}

OFFERS = {
    "A": {
        # Deliberately sorted desc
        5: Offer(item="A", quantity=5, cost=200),
        3: Offer(item="A", quantity=3, cost=130),
    },
    "B": {2: Offer(item="B", quantity=2, cost=45)},
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

    if set(cart) - set(UNIT_COSTS.keys()):
        raise NonexistentItemException()

    items = [CartItem(item=item, quantity=quantity) for item, quantity in enumerate(cart.items()]
    return Cart(items=items)
