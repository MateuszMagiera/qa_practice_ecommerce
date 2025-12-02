import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


def construct_add_to_cart_button_locator(text):
    locator = f"//span[text()='{text}']//parent::div//div//button[text()='ADD TO CART']"
    return locator


def construct_remove_from_cart_button_locator(text):
    locator = f"//span[text()='{text}']//parent::div//parent::div/div[contains(@class, 'cart-quantity cart-column')]//button[text() = 'REMOVE']"
    return locator


def calculate_total_price(products):
    product_prices = [product['price'] for product in products]
    raw_products = [product.replace('$', '') for product in product_prices]
    converted_products = [float(product) for product in raw_products]
    return f"${sum(converted_products):.2f}"