from playwright.sync_api import expect
from super_secure.credentials.login_credentials import correct
from POM.pages.login.login_page import LoginPage


def test_login_successfully(browser):
    """Verifies that a user can log in successfully and is redirected to the shopping page."""
    page = browser.new_page()
    login = LoginPage(page)
    login.login(username=correct['email'], password=correct['password'])
    expect(page.get_by_text("SHOPPING CART")).to_be_visible()
