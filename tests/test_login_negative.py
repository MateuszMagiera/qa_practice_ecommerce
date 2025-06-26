from super_secure.credentials.login_credentials import correct, incorrect
from utils.UtilsHelpers import browser, go_to_page_insert_credentials_assert_message
from POM.pages.login.login_page import LoginPage
from playwright.sync_api import expect
from data.test_data import incorrect_credentials_error_message


def test_login_incorrect_email(browser):
    page = browser.new_page()
    login = LoginPage(page)
    login.login(username=incorrect['email'], password=correct['password'])
    expect(page.get_by_text(incorrect_credentials_error_message)).to_be_visible()


def test_login_incorrect_password(browser):
    page = browser.new_page()
    login = LoginPage(page)
    login.login(username=incorrect['email'], password=correct['password'])
    expect(page.get_by_text(incorrect_credentials_error_message)).to_be_visible()


def test_incorrect_login_and_password(browser):
    page = browser.new_page()
    login = LoginPage(page)
    login.login(username=incorrect['email'], password=incorrect['password'])
    expect(page.get_by_text(incorrect_credentials_error_message)).to_be_visible()

