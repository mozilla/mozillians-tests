# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected


class Auth0(Page):

    _login_with_email_button_locator = (By.CSS_SELECTOR, '.auth0-lock-passwordless-button.auth0-lock-passwordless-big-button')
    _email_input_locator = (By.CSS_SELECTOR, '.auth0-lock-passwordless-pane>div>div>input')
    _send_email_button_locator = (By.CSS_SELECTOR, '.auth0-lock-passwordless-submit')

    def request_login_link(self, username):
        self.wait.until(expected.visibility_of_element_located(
            self._login_with_email_button_locator)).click()
        self.wait.until(expected.visibility_of_element_located(
            self._email_input_locator)).send_keys(username)
        self.find_element(*self._send_email_button_locator).click()
