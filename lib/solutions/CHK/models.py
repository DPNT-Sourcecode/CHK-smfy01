from dataclasses import dataclass
from typing import Dict, Optional, Set, Tuple


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
            offer_total, remainder = offer.apply(quantity_remaining)

            total_cost += offer_total

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
    items: Dict[str, CartItem]

    @staticmethod
    def _apply_freebie_offers(items) -> None:
        """Calculate FreebieOffers (mutating the items where required)"""
        have_freebie_offer = set(items).intersection(FREEBIE_OFFERS)

        for item in have_freebie_offer:
            offer = FREEBIE_OFFERS[item]

            offer.apply(items[item], items.get(offer.free_item))

    @staticmethod
    def _apply_group_offers(items) -> int:
        """Calculate GroupOffers (mutating the items where required) and
        return the total cost of the GroupOffers"""
        total_group_discount = 0
        for group_offer in GROUP_OFFERS:
            total_group_discount += group_offer.apply(items)

        return total_group_discount

    def total_cost(self) -> int:
        # Clone items before calculating total, so this is a "pure"(ish) function
        # In reality we could have a separate CartCheckout object (which
        # you could recreate at each step, with a running total)
        items = {k: v for k, v in self.items.items()}

        self._apply_freebie_offers(items)

        total_group_discount = self._apply_group_offers(items)

        print("items", items)

        return total_group_discount + sum(
            (item.total_cost() for item in items.values())
        )


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

        return total_cost, remainder


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

    def _apply_self_freebie(self, item: CartItem):
        quantity_of_offer = item.quantity // (self.quantity + self.free_quantity)

        item.quantity -= quantity_of_offer * self.free_quantity

    def _apply_other_item_freebie(
        self, item: CartItem, item_to_discount: Optional[CartItem]
    ):
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

    def apply(self, item: CartItem, item_to_discount: Optional[CartItem]):
        if self.free_item != self.item:
            return self._apply_other_item_freebie(item, item_to_discount)

        return self._apply_self_freebie(item)


@dataclass
class GroupOffer:
    items: Set[str]
    quantity: int
    cost: int

    @classmethod
    def create(cls, items: Set[str], cost: int) -> "GroupOffer":
        return GroupOffer(items=items, cost=cost, quantity=3)

    def apply(self, cart_items: Dict[str, CartItem]) -> int:
        """Reduce the quantity of the relevant items as many times as possible to apply the discount.
        NB: If more than the group buy is added to these items, this logic needs updating"""
        total_quantity_valid_for_offer = 0
        applicable_items = set()
        for item, cart_item in cart_items.items():
            if not item in self.items:
                continue

            total_quantity_valid_for_offer += cart_item.quantity
            applicable_items.add(item)

        quantity_of_offer = total_quantity_valid_for_offer // self.quantity

        if not quantity_of_offer:
            return 0

        total_price = quantity_of_offer * self.cost

        # Each item may have a unique price, so we need to figure out which
        # items should be removed in descending price to minimise the
        # final cart cost
        items_in_descending_price = sorted(
            applicable_items, key=lambda item: UNIT_COSTS[item], reverse=True
        )

        quantity_to_remove = quantity_of_offer * self.quantity

        for item in items_in_descending_price:
            cart_item = cart_items[item]

            if cart_item.quantity >= quantity_to_remove:
                cart_item.quantity -= quantity_to_remove
                return total_price

            quantity_to_remove -= cart_item.quantity
            cart_item.quantity = 0

        return total_price


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
    "K": 70,
    "L": 90,
    "M": 15,
    "N": 40,
    "O": 10,
    "P": 50,
    "Q": 30,
    "R": 50,
    "S": 20,
    "T": 20,
    "U": 40,
    "V": 50,
    "W": 20,
    "X": 17,
    "Y": 20,
    "Z": 21,
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
    "K": {2: DiscountOffer(item="K", quantity=2, cost=120)},
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

GROUP_OFFERS = [GroupOffer.create(items=set("STXYZ"), cost=45)]


