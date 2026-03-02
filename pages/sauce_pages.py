"""
Page objects for SauceDemo application (https://www.saucedemo.com/)
"""
from playwright.sync_api import Page, expect


class SauceLoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("#user-name")
        self.password = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error = page.locator(".error-message-container")

    # simple convenience wrapper around playwright wait
    def wait(self, milliseconds: int):
        """Pause for a fixed number of milliseconds (DEBUG/diagnostic use)."""
        self.page.wait_for_timeout(milliseconds)

    def navigate(self):
        self.page.goto("https://www.saucedemo.com/")

    def login(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()


    def login2(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()


    def get_error_text(self) -> str:
        return self.error.text_content() or ""


class ProductsPage:
    def __init__(self, page: Page):
        self.page = page
        self.inventory_items = page.locator(".inventory_item")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")

    def wait(self, milliseconds: int):
        """Pause for a fixed number of milliseconds (DEBUG only)."""
        self.page.wait_for_timeout(milliseconds)

    def add_first_item_to_cart(self):
        # click the first add-to-cart button
        self.page.locator(".inventory_item").first.locator("button").click()

    def remove_first_item_from_cart(self):
        self.page.locator(".inventory_item").first.locator("button").click()

    def goto_cart(self):
        self.cart_link.click()

    def badge_count(self) -> int:
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.text_content())


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator(".cart_item")
        
        self.checkout_button = page.locator("#checkout")
        
        self.remove_buttons = page.locator("button.cart_button")

    def wait(self, milliseconds: int):
        self.page.wait_for_timeout(milliseconds)

    def items_count(self) -> int:
        return self.cart_items.count()

    def remove_all_items(self):
        # iterate through remove buttons
        count = self.remove_buttons.count()
        for i in range(count):
            self.remove_buttons.nth(i).click()

    def click_checkout(self):
        self.checkout_button.click()


class CheckoutStepOnePage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.locator("#first-name")
        self.last_name = page.locator("#last-name")
        self.postal_code = page.locator("#postal-code")
        self.continue_button = page.locator("#continue")

    def wait(self, milliseconds: int):
        self.page.wait_for_timeout(milliseconds)

    def submit_info(self, first: str, last: str, postal: str):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)
        self.continue_button.click()


class CheckoutStepTwoPage:
    def __init__(self, page: Page):
        self.page = page
        self.finish_button = page.locator("#finish")
        self.subtotal_label = page.locator(".summary_subtotal_label")
        self.tax_label = page.locator(".summary_tax_label")
        self.total_label = page.locator(".summary_total_label")

    def wait(self, milliseconds: int):
        self.page.wait_for_timeout(milliseconds)

    def get_prices(self):
        # parse numeric amounts
        def parse(label):
            text = label.text_content() or ""
            return float(text.replace("Item total:", "").replace("Tax:", "").replace("Total:", "").strip().replace("$", ""))
        return parse(self.subtotal_label), parse(self.tax_label), parse(self.total_label)

    def finish(self):
        self.finish_button.click()

