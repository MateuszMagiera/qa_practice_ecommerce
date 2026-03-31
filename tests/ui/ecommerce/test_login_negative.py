import allure
import pytest
from playwright.sync_api import expect

from data.test_data import incorrect_credentials_error_message
from POM.pages.login.login_page import LoginPage
from super_secure.credentials.login_credentials import correct, incorrect


@pytest.mark.regression
@allure.title("E-commerce: Login with Invalid Credentials")
@allure.description("This test verifies that an error message is displayed for various incorrect login combinations.")
@allure.feature("Authentication")
@allure.story("As a user, I see an error when I use invalid credentials")
@pytest.mark.parametrize(
    "email, password",
    [
        (incorrect["email"], correct["password"]),
        (correct["email"], incorrect["password"]),
        (incorrect["email"], incorrect["password"]),
    ],
)
def test_login_with_invalid_credentials(browser, email, password):
    """Verify that an error message is displayed for various incorrect login combinations."""
    with allure.step("Initialize page and Page Objects"):
        page = browser.new_page()
        login = LoginPage(page)

    with allure.step(f"Attempt login with email: {email}"):
        login.login(username=email, password=password)

    with allure.step("Verify that the error message is displayed"):
        expect(page.get_by_text(incorrect_credentials_error_message)).to_be_visible()
