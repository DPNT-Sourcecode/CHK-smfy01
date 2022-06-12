from collections import Counter

from .errors import CartException, NonexistentItemException
from .models import Cart, CartItem, UNIT_COSTS


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
        return Cart(items={})

    cart = Counter(skus)

    if set(cart) - set(UNIT_COSTS.keys()):
        raise NonexistentItemException()

    items = [CartItem(item=item, quantity=quantity) for item, quantity in cart.items()]
    return Cart(items={cart_item.item: cart_item for cart_item in items})
