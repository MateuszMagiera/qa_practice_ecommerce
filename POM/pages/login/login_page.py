from locators.pages.login import login_page


class LoginPage:
    def __init__(self, page):
        self.page = page

    def _navigate_and_submit(self, username, password):
        """Navigate to the login page, fill credentials and click submit."""
        self.page.goto(login_page.url, wait_until="domcontentloaded")
        self.page.fill(login_page.email, username)
        self.page.fill(login_page.password, password)
        self.page.click(login_page.submit_button)
        self.page.wait_for_load_state("domcontentloaded")

    def login(self, username, password):
        """Log in and wait for the shopping page to be fully loaded."""
        self._navigate_and_submit(username, password)
        self.page.locator(".shop-item-button:visible").first.wait_for(state="visible")

    def attempt_login(self, username, password):
        """Submit login form WITHOUT waiting for the shopping page.
        Use this for negative/mock tests where login is expected to fail."""
        self._navigate_and_submit(username, password)
