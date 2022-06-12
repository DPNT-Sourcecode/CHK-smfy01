from dataclasses import dataclass
from typing import List

@dataclass
class SKU:
    item: str
    quantity: int


PRICES = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15
}


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    raise NotImplementedError()

def parse_cart(skus) -> List[SKU]:
    if not skus

def price_of_sku(sku: string, quantity: int) -> int:


