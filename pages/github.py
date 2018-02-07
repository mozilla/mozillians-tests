import pyotp
from pypom import Page
from selenium.webdriver.common.by import By


class Github(Page):

    _github_username_field_locator = (By.ID, 'login_field')
    _github_password_field_locator = (By.ID, 'password')
    _github_sign_in_button_locator = (By.CSS_SELECTOR, '.btn.btn-primary.btn-block')
    _github_passcode_field_locator = (By.CSS_SELECTOR, 'input[id="otp"]')
    _github_enter_passcode_button_locator = (By.CSS_SELECTOR, '.btn-primary')

    def login_with_github(self, username, password, secret):
        self.find_element(*self._github_username_field_locator).send_keys(username)
        self.find_element(*self._github_password_field_locator).send_keys(password)
        self.find_element(*self._github_sign_in_button_locator).click()
        passcode = pyotp.TOTP(secret).now()
        self.find_element(*self._github_passcode_field_locator).send_keys(passcode)
        self.find_element(*self._github_enter_passcode_button_locator).click()
