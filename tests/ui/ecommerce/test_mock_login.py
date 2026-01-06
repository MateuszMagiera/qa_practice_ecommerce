import allure
from playwright.sync_api import Page, expect, Route
from POM.pages.login.login_page import LoginPage
from super_secure.credentials.login_credentials import correct
from data.test_data import internal_server_error_message

@allure.feature("UI Mocking")
class TestLoginMock:

    @allure.story("Mocking Login API")
    @allure.title("Test login behavior when API returns 401 (Unauthorized)")
    @allure.description("This test verifies that the UI displays an error message when the login API returns 401, even with correct credentials.")
    def test_login_mocked_401(self, page: Page):
        """
        Testing if errors are server properly. Attempting to log in with correct data but stimulating 500 error.
        """
        login_page = LoginPage(page)

        # Intercepting any request that includes login (any endpoint) and immediately changing its status code to 500.
        with allure.step("Mock login endpoint to return 401 Unauthorized"):
            page.route("**", lambda route: route.fulfill(
                status=500,
                content_type="application/json",
                body='{"error": "Internal Server Error"}'
            ))


        with allure.step(f"Attempt login with correct credentials: {correct['email']}"):
            response = page.goto("https://qa-practice.netlify.app/auth_ecommerce.html")
            print(response.status)


        with allure.step("Verify error message is displayed"):
            expect(page.get_by_text(internal_server_error_message)).to_be_visible()
            expect(page.locator()).to_have_value()