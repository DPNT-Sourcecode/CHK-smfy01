import re

LINE_REGEX = r"^| ([A-Z])    | (\d+)\s+| (.*) |$"


def parse_table(table: str):
    prices = {}
    discount_offers = {}
    freebie_offers = {}

    matches = re.finditer(LINE_REGEX, table, re.MULTILINE)

    for match in matches:
        print(match)


parse_table(
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
)
