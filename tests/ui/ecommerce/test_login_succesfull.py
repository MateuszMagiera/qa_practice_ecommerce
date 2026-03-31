import allure
import pytest
from playwright.sync_api import expect

from POM.pages.login.login_page import LoginPage
from super_secure.credentials.login_credentials import correct


@pytest.mark.smoke
@pytest.mark.regression
@allure.title("E-commerce: Successful Login")
@allure.description(
    "This test verifies that a user can log in with valid credentials and is redirected to the shopping page."
)
@allure.feature("Authentication")
@allure.story("As a user, I can log in with correct credentials")
def test_login_successfully(browser):
    """Verifies that a user can log in successfully and is redirected to the shopping page."""
    with allure.step("Initialize page and Page Objects"):
        page = browser.new_page()
        login = LoginPage(page)

    with allure.step(f"Log in as user: {correct['email']}"):
        login.login(username=correct["email"], password=correct["password"])

    with allure.step("Verify that the shopping cart page is displayed"):
        expect(page.locator(".shop-item-button").first).to_be_visible()
