from utils.UtilsHelpers import construct_add_to_cart_button_locator


class HomePage:

    def __init__(self,page):
        self.page = page

    def add_all_phones_to_cart(self,products_list, product_locator):
        for product in products_list:
            phone = construct_add_to_cart_button_locator(product[product_locator])
            self.page.click(phone)