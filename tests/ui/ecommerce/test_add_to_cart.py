import pytest
from utils.UtilsHelpers import calculate_total_price
from super_secure.credentials.login_credentials import correct
from POM.pages.login.login_page import LoginPage
from POM.pages.home.home_page import HomePage
from POM.pages.cart.cart_page import CartPage
from data.test_data import test_products


@pytest.mark.parametrize("product", test_products)
def test_add_to_cart_phone(browser, product):
    """Verifies that a single product can be added to the cart and its details are correct."""
    page = browser.new_page()
    login_page = LoginPage(page)
    home_page = HomePage(page)
    cart_page = CartPage(page)

    login_page.login(username=correct['email'], password=correct['password'])
    home_page.add_product_to_cart(product["name"])

    cart_page.expect_product_is_in_cart(product_name=product["name"], price=product["price"])


def test_add_to_cart_all_phones(browser):
    """Verifies that all products can be added to the cart and the total price is calculated correctly."""
    page = browser.new_page()
    login_page = LoginPage(page)
    home_page = HomePage(page)

    login_page.login(username=correct['email'], password=correct['password'])
    formatted_total_price = calculate_total_price(test_products)
    home_page.add_all_phones_to_cart(products_list=test_products, product_locator='name') # Ta metoda została już zaktualizowana w HomePage
    products_total_price = page.locator(".cart-total-price").text_content()
    assert formatted_total_price == products_total_price
