from dataclasses import dataclass
from typing import List, Optional, Set


@dataclass
class CartItem:
    item: str
    quantity: int

    def is_on_offer(self) -> bool:
        return self.item in DISCOUNT_OFFERS

    def offer_cost(self) -> int:
        # Try largest offer first, then decrease offer quantity
        item_offers = DISCOUNT_OFFERS[self.item].values()
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
        # Clone items before calculating total
        items = {item.item: item for item in self.items}
        have_freebie_offer = set(items).intersection(FREEBIE_OFFERS)

        for item in have_freebie_offer:
            offer = FREEBIE_OFFERS[item]

            if offer.free_item != offer.item:
                quantity_of_offer = items[item].quantity // offer.quantity

                if quantity_of_offer == 0:
                    continue

                item_to_discount: Optional[CartItem] = items.get(offer.free_item)
                if not item_to_discount:
                    continue

                # Apply FREEBIE offer
                # Avoid negative quantities
                item_to_discount.quantity = max(
                    0,
                    item_to_discount.quantity
                    - (offer.free_quantity * quantity_of_offer),
                )
            else:
                cart_item = items[item]
                quantity_of_offer = cart_item.quantity // (
                    offer.quantity + offer.free_quantity
                )

                if quantity_of_offer == 0:
                    continue

                cart_item.quantity -= quantity_of_offer * offer.free_quantity

        return sum((item.total_cost() for item in items.values()))


@dataclass
class DiscountOffer:
    item: str
    quantity: int
    cost: int


@dataclass
class FreebieOffer:
    item: str
    quantity: int
    free_item: str
    free_quantity: int


@dataclass
class GroupOffer:
    items: Set[str]


UNIT_COSTS = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
    "E": 40,
    "F": 10,
    "G": 20,
    "H": 10,
    "I": 35,
    "J": 60,
    "K": 80,
    "L": 90,
    "M": 15,
    "N": 40,
    "O": 10,
    "P": 50,
    "Q": 30,
    "R": 50,
    "S": 30,
    "T": 20,
    "U": 40,
    "V": 50,
    "W": 20,
    "X": 90,
    "Y": 10,
    "Z": 50,
}

DISCOUNT_OFFERS = {
    "A": {
        5: DiscountOffer(item="A", quantity=5, cost=200),
        3: DiscountOffer(item="A", quantity=3, cost=130),
    },
    "B": {2: DiscountOffer(item="B", quantity=2, cost=45)},
    "H": {
        10: DiscountOffer(item="H", quantity=10, cost=80),
        5: DiscountOffer(item="H", quantity=5, cost=45),
    },
    "K": {2: DiscountOffer(item="K", quantity=2, cost=150)},
    "P": {5: DiscountOffer(item="P", quantity=5, cost=200)},
    "Q": {3: DiscountOffer(item="Q", quantity=3, cost=80)},
    "V": {
        3: DiscountOffer(item="V", quantity=3, cost=130),
        2: DiscountOffer(item="V", quantity=2, cost=90),
    },
}

FREEBIE_OFFERS = {
    "E": FreebieOffer(item="E", quantity=2, free_item="B", free_quantity=1),
    "F": FreebieOffer(item="F", quantity=2, free_item="F", free_quantity=1),
    "N": FreebieOffer(item="N", quantity=3, free_item="M", free_quantity=1),
    "R": FreebieOffer(item="R", quantity=3, free_item="Q", free_quantity=1),
    "U": FreebieOffer(item="U", quantity=3, free_item="U", free_quantity=1),
}


