from dataclasses import dataclass
from typing import List, Optional, Set, Tuple


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
        total_cost = 0

        for offer in item_offers:


            quantity_remaining = remainder

        # After all offers applied, we may have some left at unit price
        total_cost += UNIT_COSTS[self.item] * remainder
        return total_cost

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

            offer.apply(items[item], items.get(offer.free_item))

        return sum((item.total_cost() for item in items.values()))


@dataclass
class DiscountOffer:
    item: str
    quantity: int
    cost: int

    @classmethod
    def create(cls, item: str, quantity: int, cost: int) -> "DiscountOffer":
        return DiscountOffer(item=item, quantity=quantity, cost=cost)

    def apply(self, quantity: int) -> Tuple[int, int]:
        quantity_of_offer, remainder = divmod(quantity, self.quantity)

        total_cost = self.cost * quantity_of_offer

        return total_cost, 


@dataclass
class FreebieOffer:
    item: str
    quantity: int
    free_item: str
    free_quantity: int

    @classmethod
    def create(cls, item: str, quantity: int, free_item: str) -> "FreebieOffer":
        """We only offer a single freebie quantity at the moment"""
        return FreebieOffer(
            item=item, quantity=quantity, free_item=free_item, free_quantity=1
        )

    def apply(self, item: CartItem, item_to_discount: Optional[CartItem]):
        if self.free_item != self.item:
            if not item_to_discount:
                return

            quantity_of_offer = item.quantity // self.quantity

            if quantity_of_offer == 0:
                return

            # Apply FREEBIE offer
            # Avoid negative quantities
            item_to_discount.quantity = max(
                0,
                item_to_discount.quantity - (self.free_quantity * quantity_of_offer),
            )
            return

        quantity_of_offer = item.quantity // (self.quantity + self.free_quantity)

        item.quantity -= quantity_of_offer * self.free_quantity


@dataclass
class GroupOffer:
    items: Set[str]
    quantity: int
    cost: int

    @classmethod
    def create(cls, items: Set[str], cost: int) -> "GroupOffer":
        return GroupOffer(items=items, cost=cost, quantity=3)


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
        5: DiscountOffer.create(item="A", quantity=5, cost=200),
        3: DiscountOffer.create(item="A", quantity=3, cost=130),
    },
    "B": {2: DiscountOffer.create(item="B", quantity=2, cost=45)},
    "H": {
        10: DiscountOffer.create(item="H", quantity=10, cost=80),
        5: DiscountOffer.create(item="H", quantity=5, cost=45),
    },
    "K": {2: DiscountOffer.create(item="K", quantity=2, cost=150)},
    "P": {5: DiscountOffer.create(item="P", quantity=5, cost=200)},
    "Q": {3: DiscountOffer.create(item="Q", quantity=3, cost=80)},
    "V": {
        3: DiscountOffer.create(item="V", quantity=3, cost=130),
        2: DiscountOffer.create(item="V", quantity=2, cost=90),
    },
}

FREEBIE_OFFERS = {
    "E": FreebieOffer.create(
        item="E",
        quantity=2,
        free_item="B",
    ),
    "F": FreebieOffer.create(
        item="F",
        quantity=2,
        free_item="F",
    ),
    "N": FreebieOffer.create(
        item="N",
        quantity=3,
        free_item="M",
    ),
    "R": FreebieOffer.create(
        item="R",
        quantity=3,
        free_item="Q",
    ),
    "U": FreebieOffer.create(
        item="U",
        quantity=3,
        free_item="U",
    ),
}

GROUP_OFFERS = [GroupOffer.create(items=set("STXYZ"), cost=45)]



