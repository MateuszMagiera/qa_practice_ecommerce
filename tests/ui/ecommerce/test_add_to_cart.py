import pytest
import allure
from utils.UtilsHelpers import calculate_total_price
from super_secure.credentials.login_credentials import correct
from POM.pages.login.login_page import LoginPage
from POM.pages.home.home_page import HomePage
from POM.pages.cart.cart_page import CartPage
from data.test_data import test_products


@pytest.mark.smoke
@pytest.mark.regression
@allure.title("E-commerce: Add Single Product to Cart")
@allure.description("This test verifies that a single product can be added to the cart and its details are correct.")
@allure.feature("Shopping Cart")
@allure.story("As a logged-in user, I can add a product to my cart")
@pytest.mark.parametrize("product", test_products)
def test_add_to_cart_phone(browser, product):
    """Verifies that a single product can be added to the cart and its details are correct."""
    with allure.step("Initialize page and Page Objects"):
        page = browser.new_page()
        login_page = LoginPage(page)
        home_page = HomePage(page)
        cart_page = CartPage(page)

    with allure.step(f"Log in as user: {correct['email']}"):
        login_page.login(username=correct['email'], password=correct['password'])

    with allure.step(f"Add product '{product['name']}' to the cart"):
        home_page.add_product_to_cart(product["name"])

    with allure.step(f"Verify product '{product['name']}' is in the cart with price {product['price']}"):
        cart_page.expect_product_is_in_cart(product_name=product["name"], price=product["price"])


@pytest.mark.regression
@allure.title("E-commerce: Add All Products to Cart")
@allure.description("This test verifies that all products can be added to the cart and the total price is calculated correctly.")
@allure.feature("Shopping Cart")
@allure.story("As a logged-in user, I can add all products to my cart")
def test_add_to_cart_all_phones(browser):
    """Verifies that all products can be added to the cart and the total price is calculated correctly."""
    with allure.step("Initialize page and Page Objects"):
        page = browser.new_page()
        login_page = LoginPage(page)
        home_page = HomePage(page)

    with allure.step(f"Log in as user: {correct['email']}"):
        login_page.login(username=correct['email'], password=correct['password'])

    with allure.step("Calculate expected total price"):
        formatted_total_price = calculate_total_price(test_products)

    with allure.step("Add all products to the cart"):
        home_page.add_all_phones_to_cart(products_list=test_products, product_locator='name')

    with allure.step(f"Verify total price equals {formatted_total_price}"):
        products_total_price = page.locator(".cart-total-price").text_content()
        assert formatted_total_price == products_total_price, \
            f"Expected total price '{formatted_total_price}', but got '{products_total_price}'"
