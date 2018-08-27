# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.github import Github


class Auth0(Page):

    _email_locator = (By.ID, 'field-email-signup')
    _enter_locator = (By.ID, 'enter-initial-signup')
    _send_email_locator = (By.CSS_SELECTOR, 'button[data-handler=send-passwordless-link]')
    _login_with_github_button_locator = (By.CSS_SELECTOR, '#initial-login-signup button[data-handler="authorise-github"]')

    def request_login_link(self, username):
        self.wait.until(expected.visibility_of_element_located(
            self._email_locator)).send_keys(username)
        self.find_element(*self._enter_locator).click()
        self.wait.until(expected.visibility_of_element_located(
            self._send_email_locator)).click()

    def click_login_with_github(self):
        self.find_element(*self._login_with_github_button_locator).click()
        return Github(self.selenium, self.base_url)
