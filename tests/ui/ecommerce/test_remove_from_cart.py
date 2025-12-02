from playwright.sync_api import expect
from POM.pages.login.login_page import LoginPage
from POM.pages.cart.cart_page import CartPage
from POM.pages.home.home_page import HomePage
from data.test_data import test_products
from super_secure.credentials.login_credentials import correct


def test_remove_phone_from_cart(browser):
    """
    Verifies that a product can be added to the cart and then successfully removed.
    """
    page = browser.new_page()
    login_page = LoginPage(page)
    home_page = HomePage(page)
    cart_page = CartPage(page)
    product_to_test = test_products[0]

    login_page.login(username=correct['email'], password=correct['password'])
    home_page.add_product_to_cart(product_to_test["name"])
    cart_page.remove_product(product_to_test["name"])

    cart_page.expect_product_to_be_removed(product_to_test["name"])
