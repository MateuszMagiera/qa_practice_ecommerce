import pytest
from playwright.sync_api import sync_playwright, Playwright, APIRequestContext, Browser


@pytest.fixture(scope="function")
def browser() -> Browser:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> APIRequestContext:
    """
    Fixture that creates a new APIRequestContext for API tests.
    """
    request_context = playwright.request.new_context()
    yield request_context
    request_context.dispose()