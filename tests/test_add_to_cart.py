import time

import pytest
from playwright.sync_api import expect
from utils.UtilsHelpers import browser, construct_add_to_cart_button_locator, calculate_total_price
from super_secure.credentials.login_credentials import correct
from POM.pages.login.login_page import LoginPage
from POM.pages.home.home_page import HomePage
from data.test_data import test_products


@pytest.mark.parametrize("product", test_products)
def test_add_to_cart_phone(browser, product):
    page = browser.new_page()
    login = LoginPage(page)
    login.login(username=correct['email'], password=correct['password'])
    phone = construct_add_to_cart_button_locator(product["name"])
    page.click(phone)
    expect(page.locator(".cart-item-image")).to_be_visible()
    expect(page.locator(".cart-item-title")).to_have_text(product["name"])
    expect(page.locator(".cart-price.cart-column").nth(1)).to_have_text(product["price"])
    expect(page.locator(".cart-quantity-input")).to_have_value("1")
    expect(page.locator(".btn.btn-danger")).to_have_text("REMOVE")


def test_add_to_cart_all_phones(browser):
    page = browser.new_page()
    login = LoginPage(page)
    login.login(username=correct['email'], password=correct['password'])
    formatted_total_price = calculate_total_price(test_products)
    home = HomePage(page)
    home.add_all_phones_to_cart(products_list=test_products, product_locator='name')
    products_total_price = page.locator(".cart-total-price").text_content()
    assert formatted_total_price == products_total_price

