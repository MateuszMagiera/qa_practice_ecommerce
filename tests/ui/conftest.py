import os
from datetime import datetime

import allure
import pytest
from playwright.sync_api import expect

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "screenshots")

# Timeouts (ms) — generous enough for slow CI runners hitting an external site.
DEFAULT_TIMEOUT = 60_000
DEFAULT_NAVIGATION_TIMEOUT = 60_000
DEFAULT_EXPECT_TIMEOUT = 30_000

# Increase Playwright's expect() assertion timeout (default is 5s).
# In CI, the external Netlify site renders slowly — 5s is not enough
# for elements to become visible after page transitions.
expect.set_options(timeout=DEFAULT_EXPECT_TIMEOUT)


@pytest.fixture()
def browser(browser):
    """
    Wraps the default pytest-playwright browser fixture to ensure every
    page/context created via browser.new_page() or browser.new_context()
    gets consistent timeout defaults.

    We intentionally do NOT override viewport here. CI logs showed that
    forcing a custom viewport could make core shopping elements render as
    hidden on the external site under test. We only extend timeouts.
    """
    _original_new_page = browser.new_page
    _original_new_context = browser.new_context

    def _new_page_with_defaults(**kwargs):
        page = _original_new_page(**kwargs)
        page.set_default_timeout(DEFAULT_TIMEOUT)
        page.set_default_navigation_timeout(DEFAULT_NAVIGATION_TIMEOUT)
        return page

    def _new_context_with_defaults(**kwargs):
        ctx = _original_new_context(**kwargs)
        ctx.set_default_timeout(DEFAULT_TIMEOUT)
        ctx.set_default_navigation_timeout(DEFAULT_NAVIGATION_TIMEOUT)
        return ctx

    browser.new_page = _new_page_with_defaults
    browser.new_context = _new_context_with_defaults
    return browser


@pytest.fixture()
def page(page):
    """Apply the same timeout defaults to the built-in pytest-playwright page fixture."""
    page.set_default_timeout(DEFAULT_TIMEOUT)
    page.set_default_navigation_timeout(DEFAULT_NAVIGATION_TIMEOUT)
    return page


@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request, browser):
    """
    Automatically captures a full-page screenshot from every open browser page
    when a UI test fails.

    Screenshots are:
    - Saved to /screenshots/ with a descriptive filename:
      <test_name>_<YYYY-MM-DD_HH-MM-SS>.png
    - Attached to the Allure report for easy viewing in the HTML report.

    Scoped to tests/ui/ only — API and GraphQL tests are unaffected.
    Relies on the pytest_runtest_makereport hook in tests/conftest.py
    to expose the test result via request.node.rep_call.
    """
    yield

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        test_name = request.node.name

        for _i, context in enumerate(browser.contexts):
            for _j, page in enumerate(context.pages):
                try:
                    screenshot_bytes = page.screenshot(full_page=True)

                    filename = f"{test_name}_{timestamp}.png"
                    filepath = os.path.join(SCREENSHOTS_DIR, filename)
                    with open(filepath, "wb") as f:
                        f.write(screenshot_bytes)

                    allure.attach(
                        screenshot_bytes,
                        name=f"Screenshot on failure — {test_name}",
                        attachment_type=allure.attachment_type.PNG,
                    )
                except Exception:
                    pass
