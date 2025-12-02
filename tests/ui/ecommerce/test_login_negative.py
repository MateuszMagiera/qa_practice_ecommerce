import pytest
from playwright.sync_api import expect
from POM.pages.login.login_page import LoginPage
from data.test_data import incorrect_credentials_error_message
from super_secure.credentials.login_credentials import correct, incorrect


@pytest.mark.parametrize("email, password", [
    (incorrect['email'], correct['password']),
    (correct['email'], incorrect['password']),
    (incorrect['email'], incorrect['password'])
])
def test_login_with_invalid_credentials(browser, email, password):
    """Verify that an error message is displayed for various incorrect login combinations."""
    page = browser.new_page()
    login = LoginPage(page)
    login.login(username=email, password=password)
    expect(page.get_by_text(incorrect_credentials_error_message)).to_be_visible()
