from solutions.CHK.checkout_solution import checkout

def test_missing_item():
    assert checkout("E") == -1

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



