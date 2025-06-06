from playwright.sync_api import expect
from utils.UtilsHelpers import browser


def test_login_successfully(browser):
    page = browser.new_page()
    page.goto("https://qa-practice.netlify.app/auth_ecommerce")
    page.fill("#email", "admin@admin.com")
    page.fill("#password", "admin123")
    page.click("#submitLoginBtn")
    expect(page.get_by_text("SHOPPING CART")).to_be_visible()
