import pytest
import allure
from playwright.sync_api import Playwright, APIRequestContext, Browser, Response, APIResponse

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> 'AllureLoggingAPIRequestContext':
    """
    Fixture that creates a new APIRequestContext for API tests and wraps it with Allure logging.
    """
    request_context = playwright.request.new_context()
    yield AllureLoggingAPIRequestContext(request_context)
    request_context.dispose()


class AllureLoggingAPIRequestContext:
    """
    A wrapper around Playwright's APIRequestContext that automatically logs
    request and response details to Allure report steps.
    """
    def __init__(self, request_context: APIRequestContext):
        self._request_context = request_context

    def _log_request(self, method: str, url: str, **kwargs):
        with allure.step(f"API Request: {method} {url}"):
            allure.attach(f"Method: {method}\nURL: {url}", name="Request Details", attachment_type=allure.attachment_type.TEXT)
            if 'headers' in kwargs and kwargs['headers']:
                allure.attach(str(kwargs['headers']), name="Request Headers", attachment_type=allure.attachment_type.TEXT)
            if 'data' in kwargs and kwargs['data']:
                allure.attach(str(kwargs['data']), name="Request Body (form data)", attachment_type=allure.attachment_type.TEXT)
            if 'json' in kwargs and kwargs['json']:
                allure.attach(str(kwargs['json']), name="Request Body (JSON)", attachment_type=allure.attachment_type.JSON)

    def _log_response(self, response: Response):
        with allure.step(f"API Response: {response.status} {response.status_text}"):
            allure.attach(f"Status: {response.status} {response.status_text}", name="Response Status", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(response.headers), name="Response Headers", attachment_type=allure.attachment_type.TEXT)
            try:
                # Try to attach as JSON if possible, otherwise as plain text
                allure.attach(response.text(), name="Response Body", attachment_type=allure.attachment_type.JSON)
            except Exception:
                allure.attach(response.text(), name="Response Body", attachment_type=allure.attachment_type.TEXT)

    def get(self, url: str, **kwargs) -> APIResponse:
        self._log_request("GET", url, **kwargs)
        response = self._request_context.get(url, **kwargs)
        self._log_response(response)
        return response

    def post(self, url: str, **kwargs) -> APIResponse:
        self._log_request("POST", url, **kwargs)
        response = self._request_context.post(url, **kwargs)
        self._log_response(response)
        return response

    def delete(self, url: str, **kwargs) -> APIResponse:
        self._log_request("DELETE", url, **kwargs)
        response = self._request_context.delete(url, **kwargs)
        self._log_response(response)
        return response

    # Delegate any other methods not explicitly overridden to the underlying APIRequestContext
    def __getattr__(self, name):
        return getattr(self._request_context, name)