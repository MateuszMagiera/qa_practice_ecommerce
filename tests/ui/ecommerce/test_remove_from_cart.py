from playwright.sync_api import expect
import allure
from POM.pages.login.login_page import LoginPage
from POM.pages.cart.cart_page import CartPage
from POM.pages.home.home_page import HomePage
from data.test_data import test_products
from super_secure.credentials.login_credentials import correct

@allure.title("E-commerce: Remove Product from Cart")
@allure.description("This test verifies the full process of removing a product from the shopping cart after it has been added.")
@allure.feature("Shopping Cart")
@allure.story("As a logged-in user, I can remove a product from my cart")
def test_remove_phone_from_cart(browser):
    """
    Verifies that a product can be added to the cart and then successfully removed.
    """
    with allure.step("Initialize page and Page Objects"):
        page = browser.new_page()
        login_page = LoginPage(page)
        home_page = HomePage(page)
        cart_page = CartPage(page)
        product_to_test = test_products[0]

    with allure.step(f"Log in as user: {correct['email']}"):
        login_page.login(username=correct['email'], password=correct['password'])

    with allure.step(f"Add product '{product_to_test['name']}' to the cart"):
        home_page.add_product_to_cart(product_to_test["name"])

    with allure.step(f"Remove product '{product_to_test['name']}' from the cart"):
        cart_page.remove_product(product_to_test["name"])

    with allure.step("Verify that the product has been removed from the cart"):
        cart_page.expect_product_to_be_removed(product_to_test["name"])
