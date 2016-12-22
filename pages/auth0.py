# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from pages.page import Page


class Auth0(Page):

    _login_with_email_button_locator = (By.CSS_SELECTOR, '.auth0-lock-passwordless-button.auth0-lock-passwordless-big-button')
    _email_input_locator = (By.CSS_SELECTOR, '.auth0-lock-passwordless-pane>div>div>input')
    _send_email_button_locator = (By.CSS_SELECTOR, '.auth0-lock-passwordless-submit')

    def request_login_link(self, username):
        self.wait_for_element_visible(*self._login_with_email_button_locator)
        self.selenium.find_element(*self._login_with_email_button_locator).click()
        self.wait_for_element_visible(*self._email_input_locator)
        self.selenium.find_element(*self._email_input_locator).send_keys(username)
        self.selenium.find_element(*self._send_email_button_locator).click()
