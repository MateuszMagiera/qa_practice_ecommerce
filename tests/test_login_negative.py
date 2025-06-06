from utils.UtilsHelpers import browser, go_to_page_insert_credentials_assert_message
from playwright.sync_api import expect
from time import sleep


def test_login_incorrect_email(browser):
    (go_to_page_insert_credentials_assert_message
     (browser, "https://qa-practice.netlify.app/auth_ecommerce", "a@eeadsaw.com", "admin123", "Bad credentials! Please try again! Make sure that you've registered."))


def test_login_incorrect_password(browser):
    (go_to_page_insert_credentials_assert_message
     (browser, "https://qa-practice.netlify.app/auth_ecommerce", "admin@admin.com", "!nC0R3cT", "Bad credentials! Please try again! Make sure that you've registered."))
