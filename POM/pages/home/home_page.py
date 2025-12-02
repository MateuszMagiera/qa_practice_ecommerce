from playwright.sync_api import Page
from utils.UtilsHelpers import construct_add_to_cart_button_locator


class HomePage:

    def __init__(self, page: Page):
        self.page = page

    def add_product_to_cart(self, product_name: str):
        """Finds a product by name on the home page and clicks its 'ADD TO CART' button."""
        add_button_locator = construct_add_to_cart_button_locator(product_name)
        self.page.click(add_button_locator)

    def add_all_phones_to_cart(self, products_list: list, product_locator: str):
        """Iterates through a list of products and adds each one to the cart."""
        for product in products_list:
            self.add_product_to_cart(product[product_locator])