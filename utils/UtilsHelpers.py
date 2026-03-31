def construct_add_to_cart_button_locator(page, text):
    return page.locator(".shop-item").filter(has_text=text).locator("button:visible", has_text="ADD TO CART")


def calculate_total_price(products):
    product_prices = [product["price"] for product in products]
    raw_products = [product.replace("$", "") for product in product_prices]
    converted_products = [float(product) for product in raw_products]
    return f"${sum(converted_products):.2f}"
