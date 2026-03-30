from locators.pages.login import login_page


class LoginPage:
    def __init__(self,page):
        self.page = page

    def login(self,username, password):
        self.page.goto(login_page.url)
        self.page.fill(login_page.email, username)
        self.page.fill(login_page.password, password)
        self.page.click(login_page.submit_button)
        self.page.wait_for_load_state("networkidle")
