import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


def go_to_page_insert_credentials_assert_message(browser,url,email,password,message):
    page = browser.new_page()
    page.goto(url)
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("#submitLoginBtn")
    expect(page.get_by_text(message)).to_be_visible()
