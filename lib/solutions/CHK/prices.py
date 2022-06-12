UNIT_COSTS = {"A": 50, "B": 30, "C": 20, "D": 15, "E": 40, "F": 10}

DISCOUNT_OFFERS = {
    "A": {
        # Deliberately sorted desc
        5: DiscountOffer(item="A", quantity=5, cost=200),
        3: DiscountOffer(item="A", quantity=3, cost=130),
    },
    "B": {2: DiscountOffer(item="B", quantity=2, cost=45)},
}

FREEBIE_OFFERS = {
    "E": FreeOffer(item="E", quantity=2, free_item="B", free_quantity=1),
    "F": FreeOffer(item="F", quantity=2, free_item="F", free_quantity=1),
}
