import pytest
from playwright.sync_api import Playwright, APIRequestContext

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> APIRequestContext:
    """
    Fixture that creates a new APIRequestContext for API tests.
    """
    request_context = playwright.request.new_context()
    yield request_context
    request_context.dispose()