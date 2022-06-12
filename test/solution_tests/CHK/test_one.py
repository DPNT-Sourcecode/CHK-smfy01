from solutions.CHK.checkout_solution import checkout

def test_empty_invalid():
    assert checkout("") == -1

def test_single_product_no_offer():
    assert checkout("C") == 20

def test_multiple_products_no_offer():
    assert checkout("A,B") == 80

def test_
