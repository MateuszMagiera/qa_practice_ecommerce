import os
from datetime import datetime

import pytest
import allure

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "screenshots")


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

        for i, context in enumerate(browser.contexts):
            for j, page in enumerate(context.pages):
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
