import allure
from playwright.sync_api import Page, expect
from POM.pages.login.login_page import LoginPage
from super_secure.credentials.login_credentials import correct
from data.test_data import internal_server_error_message

# JavaScript that replaces the real checkCredentialsProductsList() with one
# that always displays "Internal Server Error" — simulating a broken backend.
MOCKED_LOGIN_JS = """
function checkCredentialsProductsList() {
    const result = document.getElementById("message");
    result.classList.add('alert-danger');
    result.style.display = "block";
    result.innerHTML = "Internal Server Error";
}
"""


@allure.feature("UI Mocking")
class TestLoginMock:

    @allure.story("Mocking Login Script")
    @allure.title("Test login behavior when server returns 500 Internal Server Error")
    @allure.description(
        "This test intercepts the login.js script and replaces it with a version "
        "that always displays an error, simulating a broken backend. "
        "It verifies that the UI shows the error message even when correct credentials are used."
    )
    def test_login_mocked_500(self, page: Page):
        """Mocks login.js to simulate a server error and verifies the UI displays it."""
        login_page = LoginPage(page)

        with allure.step("Mock login.js to simulate a 500 server error"):
            page.route("**/js/login.js", lambda route: route.fulfill(
                status=200,
                content_type="application/javascript",
                body=MOCKED_LOGIN_JS,
            ))

        with allure.step(f"Attempt login with correct credentials: {correct['email']}"):
            login_page.login(username=correct['email'], password=correct['password'])

        with allure.step("Verify error message is displayed"):
            expect(page.get_by_text(internal_server_error_message)).to_be_visible()