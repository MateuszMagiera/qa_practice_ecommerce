from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_total_price_locator = page.locator(".cart-total-price")

    def _get_product_row_locator(self, product_name: str):
        """Returns a locator for the entire row of a specific product in the cart."""
        return self.page.locator(f"//div[contains(@class, 'cart-row') and .//span[text()=\"{product_name}\"]]")

    def remove_product(self, product_name: str):
        """Finds a product by name in the cart and clicks its remove button."""
        product_row = self._get_product_row_locator(product_name)
        product_row.locator("button.btn-danger").click()

    def expect_product_to_be_removed(self, product_name: str):
        """Asserts that a specific product is no longer visible in the cart."""
        product_row = self._get_product_row_locator(product_name)
        expect(product_row).not_to_be_visible()

    def expect_product_is_in_cart(self, product_name: str, price: str, quantity: str = "1"):
        """Asserts that a specific product is visible in the cart with the correct details."""
        product_row = self._get_product_row_locator(product_name)
        expect(product_row).to_be_visible()
        expect(product_row.locator(".cart-item-title")).to_have_text(product_name)
        expect(product_row.locator(".cart-price").first).to_have_text(price)
        expect(product_row.locator(".cart-quantity-input")).to_have_value(quantity)
        expect(product_row.locator(".btn-danger")).to_have_text("REMOVE")