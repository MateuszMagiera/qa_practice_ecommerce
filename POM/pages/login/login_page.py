from super_secure.credentials.login_credentials import correct, incorrect
from locators.pages.login import login_page


class LoginPage:
    def __init__(self,browser):
        self.browser = browser

    def login(self,username, password):
        page = self.browser.new_page()
        page.goto(login_page.url)
        page.fill("#email", correct["email"])
        page.fill("#password", correct["password"])
        page.click(login_page.submit_button)
        return page