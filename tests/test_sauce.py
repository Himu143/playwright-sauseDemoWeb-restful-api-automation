import re
import pytest
from playwright.sync_api import expect
from pages.sauce_pages import (
    SauceLoginPage,
    ProductsPage,
    CartPage,
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
)

# ---------------------------------------------
# SauceDemo tests (pytest friendly)
# ---------------------------------------------

@pytest.fixture(autouse=True)
def navigate_home(page):
    # ensure we always start from login page for every test
    page.goto("https://www.saucedemo.com/")
    yield


def test_successful_login(page):
    login = SauceLoginPage(page)
    login.login("standard_user", "secret_sauce")
    # optional pause if you want to observe behavior or wait for rotation
    login.wait(1000)  # milliseconds pause
    # after successful login, should reach inventory page
    expect(page).to_have_url(re.compile("inventory.html"))



def test_locked_out_user(page):
    login = SauceLoginPage(page)
    login.login("locked_out_user", "secret_sauce")
    login.wait(1000)
    error = login.get_error_text()
    assert "locked out" in error.lower()


def test_invalid_login(page):
    login = SauceLoginPage(page)
    login.login("invalid_user", "bad_pass")
    login.wait(1000)
    error = login.get_error_text()
    assert "username and password do not match" in error.lower() or "sorry" in error.lower()


def test_add_and_remove_product(page):
    login = SauceLoginPage(page)
    login.login("standard_user", "secret_sauce")
    products = ProductsPage(page)
    # ensure cart is empty initially
    assert products.badge_count() == 0
    products.add_first_item_to_cart()
    products.wait(1000)  # small delay to let badge update
    assert products.badge_count() == 1
    products.remove_first_item_from_cart()
    products.wait(1000)
    assert products.badge_count() == 0


def test_complete_checkout(page):
    login = SauceLoginPage(page)
    login.login("standard_user", "secret_sauce")
    login.wait(1000)
    products = ProductsPage(page)
    products.add_first_item_to_cart()
    products.wait(1000)
    products.goto_cart()
    products.wait(1000)
    cart = CartPage(page)
    assert cart.items_count() == 1
    cart.click_checkout()
    cart.wait(1000)
    checkout1 = CheckoutStepOnePage(page)
    
    checkout1.submit_info("John", "Doe", "12345")
    checkout1.wait(1000)
    checkout2 = CheckoutStepTwoPage(page)
    checkout2.wait(1000)
    subtotal, tax, total = checkout2.get_prices()
    # price validation
    assert abs(subtotal + tax - total) < 0.01
    checkout2.finish()
    checkout2.wait(1000)
    expect(page).to_have_url(re.compile("checkout-complete.html"))
