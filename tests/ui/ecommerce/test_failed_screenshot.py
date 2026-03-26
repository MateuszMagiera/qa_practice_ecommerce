import allure
from POM.pages.login.login_page import LoginPage
from POM.pages.cart.cart_page import CartPage
from POM.pages.home.home_page import HomePage
from data.test_data import test_products
from super_secure.credentials.login_credentials import correct

@allure.title('E-commerce: Failed Screenshot Test')
@allure.description('This test intentionally fails to demonstrate automatic screenshot capture on failure.')
@allure.feature('Shopping Cart')
@allure.story('As a logged-in user, I want to see a failed test with a screenshot')
def test_failed_screenshot(browser):
    """
    Intentionally fails to demonstrate the screenshot-on-failure mechanism.
    The product is added to the cart but never removed — then the test
    asserts it is gone, which fails and triggers the screenshot capture.
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

    with allure.step(f"Intentionally fail — assert product was removed (it was never removed)"):
        cart_page.expect_product_to_be_removed(product_to_test["name"])
