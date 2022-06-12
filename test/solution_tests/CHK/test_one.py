from solutions.CHK.checkout_solution import checkout


def test_missing_item():
    assert checkout("Z") == -1


def test_empty():
    assert checkout("") == 0


def test_single_product_no_offer():
    assert checkout("C") == 20


def test_multiple_products_no_offer():
    assert checkout("AB") == 80


def test_multiple_products_with_exact_offer():
    assert checkout("AAA") == 130


def test_multiple_products_over_offer():
    """offer price for the first 3, full price for the next"""
    assert checkout("AAAA") == 180


def test_multiple_quantity_of_offer():
    """offer price for 4 of the 5, normal price for the last unit"""
    assert checkout("BBBBB") == 120


def test_select_better_offer():
    """250 (5 offer + 1) instead of 260(3 offer x 2)"""
    assert checkout("AAAAAA") == 250


def test_multiple_offers():
    """1x unit price, 1x 3 for 130, 1x 5 for 200"""
    assert checkout("AAAAAAAAA") == 380


def test_get_one_free():
    assert checkout("BEE") == 110


def test_prioritise_free_over_quantity_offer():
    assert checkout("BBEE") == 110





