import time

from playwright.sync_api import expect
import pytest
from POM.pages.login.login_page import LoginPage
from data.test_data import test_products
from super_secure.credentials.login_credentials import correct
from utils.UtilsHelpers import construct_add_to_cart_button_locator,browser, construct_remove_from_cart_button_locator


def test_remove_phone_from_cart(browser):
    page = browser.new_page()
    login = LoginPage(page)
    login.login(username=correct['email'], password=correct['password'])
    phone = construct_add_to_cart_button_locator(test_products[0]["name"])
    print(phone)
    page.click(phone)
    remove_button = construct_remove_from_cart_button_locator(test_products[0]["name"])
    page.click(remove_button)
    expect(page.locator(".cart-item-image")).not_to_be_visible()
    expect(page.locator(".cart-item-title")).not_to_be_visible()
    expect(page.locator(".cart-price.cart-column").nth(2)).not_to_be_visible()
    expect(page.locator(".cart-quantity-input")).not_to_be_visible()
    expect(page.locator(".btn.btn-danger")).not_to_be_visible()
