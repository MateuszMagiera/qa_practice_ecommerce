import time

from playwright.sync_api import expect
from super_secure.credentials.login_credentials import correct
from utils.UtilsHelpers import browser
from POM.pages.login.login_page import LoginPage

print("Rozpoczynam test login successfully")
def test_login_successfully(browser):
    print(f"Browser fixture type: {type(browser)}")
    page = browser.new_page()
    print("Nowa strone utworzona")
    login = LoginPage(page)
    login.login(username=correct['email'], password=correct['password'])
    time.sleep(5)
    expect(page.get_by_text("SHOPPING CART")).to_be_visible()
