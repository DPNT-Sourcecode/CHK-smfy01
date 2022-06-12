import re

from lib.solutions.CHK.models import DiscountOffer

LINE_REGEX = r"^| ([A-Z])    | (\d+)\s+| (.*) |$"

FREEBIE_REGEX = r"(\d)([A-Z]) get one [A-Z] free"
DISCOUNT_REGEX = r"(\d)[A-Z]) for (\d+)"


def parse_table(table: str):
    prices = {}
    discount_offers = {}
    freebie_offers = {}

    for line in table.splitlines():
        matches = re.findall(LINE_REGEX, line)
        item = matches[1][0]
        price = int(matches[2][1])
        offers = matches[3][2]

        prices[item] = price

        if not offers:
            continue

        # Reverse in case of multiple offers for same item
        offers = offers.split(", ").reverse()

        for offer in offers:
            match = re.match(DISCOUNT_REGEX, offer)
            if match:
                discounts = discount_offers.setdefault(item, {})
                quantity = match[0]
                price = match[2]
                discounts[quantity] = DiscountOffer(item=item, quantity=)




    return prices


print(parse_table(
    "| A    | 50    | 3A for 130, 5A for 200 |\n"
    "| B    | 30    | 2B for 45              |\n"
    "| C    | 20    |                        |\n"
    "| D    | 15    |                        |\n"
    "| E    | 40    | 2E get one B free      |\n"
    "| F    | 10    | 2F get one F free      |\n"
    "| G    | 20    |                        |\n"
    "| H    | 10    | 5H for 45, 10H for 80  |\n"
    "| I    | 35    |                        |\n"
    "| J    | 60    |                        |\n"
    "| K    | 80    | 2K for 150             |\n"
    "| L    | 90    |                        |\n"
    "| M    | 15    |                        |\n"
    "| N    | 40    | 3N get one M free      |\n"
    "| O    | 10    |                        |\n"
    "| P    | 50    | 5P for 200             |\n"
    "| Q    | 30    | 3Q for 80              |\n"
    "| R    | 50    | 3R get one Q free      |\n"
    "| S    | 30    |                        |\n"
    "| T    | 20    |                        |\n"
    "| U    | 40    | 3U get one U free      |\n"
    "| V    | 50    | 2V for 90, 3V for 130  |\n"
    "| W    | 20    |                        |\n"
    "| X    | 90    |                        |\n"
    "| Y    | 10    |                        |\n"
    "| Z    | 50    |                        |"
))




