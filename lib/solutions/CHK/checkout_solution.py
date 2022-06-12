from dataclasses import dataclass
from typing import List

class CartException(Exception):
    pass

class NonexistentItemException(Exception):
    pass

@dataclass
class SKU:
    item: str
    quantity: int

    def total_cost(self) -> int:
        return PRICES[self.item] * self.quantity


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
    except

def parse_cart(skus) -> List[SKU]:
    if not skus:
        return []

    if



def price_of_sku(sku: string, quantity: int) -> int:



