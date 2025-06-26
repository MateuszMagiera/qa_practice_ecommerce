from super_secure.credentials.login_credentials import correct, incorrect
from locators.pages.login import login_page


class LoginPage:
    def __init__(self,page):
        self.page = page

    def login(self,username, password):
        self.page.goto(login_page.url)
        self.page.fill("#email", username)
        self.page.fill("#password", password)
        self.page.click(login_page.submit_button)
