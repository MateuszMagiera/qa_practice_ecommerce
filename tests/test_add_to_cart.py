import pytest
from playwright.sync_api import expect
from utils.UtilsHelpers import browser, construct_add_to_cart_button_locator
from locators.pages.login.login_page import url
from super_secure.credentials.login_credentials import correct

test_products = [
    {
        "name": "Apple iPhone 12, 128GB, Black",
        "price": "$905.99"
    },
    {
        "name": "Samsung Galaxy A32, 128GB, White",
        "price": "$286.99"
    },
    {
        "name": "Apple iPhone 13, 128GB, Blue",
        "price": "$918.99"
    },
    {
        "name": "Nokia 105, Black",
        "price": "$19.99"
    }

]


@pytest.mark.parametrize("product", test_products)
def test_add_to_cart_iphone_12(browser, product):
    page = browser.new_page()
    page.goto(url)
    page.fill("#email", correct['email'])
    page.fill("#password", correct['password'])
    page.click("#submitLoginBtn")
    phone = construct_add_to_cart_button_locator(product["name"])
    page.click(phone)
    expect(page.locator(".cart-item-image")).to_be_visible()
    expect(page.locator(".cart-item-title")).to_have_text(product["name"])
    expect(page.locator(".cart-price.cart-column").nth(1)).to_have_text(product["price"])
    expect(page.locator(".cart-quantity-input")).to_have_value("1")
    expect(page.locator(".btn.btn-danger")).to_have_text("REMOVE")
