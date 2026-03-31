"""
Accessibility (WCAG) audit tests powered by axe-core.

These tests scan pages for accessibility violations (missing labels,
insufficient contrast, missing alt text, etc.) following WCAG 2.1 AA.

Strategy:
    - All violations are logged to Allure (full report + raw JSON).
    - Tests FAIL only on critical/serious violations that are NOT in
      the known-violations baseline. This prevents false failures on
      a 3rd-party app we cannot fix, while still catching NEW regressions.
    - Minor/moderate issues are still visible in the Allure report
      for informational purposes.
"""

import allure
import pytest

from config import BASE_URL
from POM.pages.login.login_page import LoginPage
from super_secure.credentials.login_credentials import correct
from utils.accessibility import filter_by_impact, run_axe_audit

FAIL_ON_IMPACT = ("critical", "serious")

# ──────────────────────────────────────────────────────────────────────
# Known a11y violations in the 3rd-party app under test.
# These are acknowledged issues we cannot fix — they are still logged
# to the Allure report, but won't fail the tests. If the app fixes
# them, the baseline should be updated (remove the entry).
# If a NEW violation appears that is NOT listed here → test FAILS.
# ──────────────────────────────────────────────────────────────────────
KNOWN_VIOLATIONS: dict[str, set[str]] = {
    "Login Page": {
        "button-name",  # Navbar toggle button has no accessible name
        "color-contrast",  # Low-contrast placeholder text in form inputs
        "html-has-lang",  # <html> element missing lang attribute
    },
    "Shopping Page": {
        "button-name",  # Navbar toggle + cart buttons have no accessible name
        "color-contrast",  # Low-contrast text on product cards
        "html-has-lang",  # <html> element missing lang attribute
        "image-alt",  # Product images have no alt text
    },
}


def _get_new_violations(violations: list[dict], page_name: str) -> list[dict]:
    """Return only violations that are NOT in the known baseline."""
    known = KNOWN_VIOLATIONS.get(page_name, set())
    return [v for v in violations if v["id"] not in known]


@pytest.mark.regression
@pytest.mark.a11y
@allure.feature("Accessibility (WCAG)")
class TestAccessibility:
    @allure.story("Login Page Audit")
    @allure.title("a11y: Login page meets WCAG 2.1 AA")
    @allure.description(
        "Runs an axe-core WCAG 2.1 Level AA audit on the login page. "
        "Fails if any NEW critical or serious violations are found beyond the known baseline."
    )
    def test_login_page_accessibility(self, page):
        """Audit the login page for accessibility violations."""
        with allure.step(f"Navigate to login page: {BASE_URL}/auth_ecommerce.html"):
            page.goto(f"{BASE_URL}/auth_ecommerce.html", wait_until="domcontentloaded")

        violations = run_axe_audit(page, page_name="Login Page")
        blocking = filter_by_impact(violations, levels=FAIL_ON_IMPACT)
        new_violations = _get_new_violations(blocking, "Login Page")

        assert len(new_violations) == 0, (
            f"Found {len(new_violations)} NEW critical/serious a11y violation(s) on Login Page:\n"
            + "\n".join(f"  - [{v['impact']}] {v['id']}: {v['description']}" for v in new_violations)
        )

    @allure.story("Shopping Page Audit")
    @allure.title("a11y: Shopping page meets WCAG 2.1 AA")
    @allure.description(
        "Logs in and runs an axe-core WCAG 2.1 Level AA audit on the shopping/cart page. "
        "Fails if any NEW critical or serious violations are found beyond the known baseline."
    )
    def test_shopping_page_accessibility(self, page):
        """Audit the shopping page (post-login) for accessibility violations."""
        login_page = LoginPage(page)

        with allure.step(f"Log in as user: {correct['email']}"):
            login_page.login(username=correct["email"], password=correct["password"])

        violations = run_axe_audit(page, page_name="Shopping Page")
        blocking = filter_by_impact(violations, levels=FAIL_ON_IMPACT)
        new_violations = _get_new_violations(blocking, "Shopping Page")

        assert len(new_violations) == 0, (
            f"Found {len(new_violations)} NEW critical/serious a11y violation(s) on Shopping Page:\n"
            + "\n".join(f"  - [{v['impact']}] {v['id']}: {v['description']}" for v in new_violations)
        )
