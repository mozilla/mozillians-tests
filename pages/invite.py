#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.base import Base


class Invite(Base):

    _recipient_field_locator = (By.ID, 'id_recipient')
    _send_invite_button_locator = (By.CSS_SELECTOR, '#main button')
    _error_text_locator = (By.CSS_SELECTOR, '.errorlist > li')

    @property
    def error_text_message(self):
        return self.selenium.find_element(*self._error_text_locator).text

    def invite(self, email):
        input_field = self.selenium.find_element(*self._recipient_field_locator)
        input_field.send_keys(email)
        self.selenium.find_element(*self._send_invite_button_locator).click()
        from pages.invite_success import InviteSuccess
        return InviteSuccess(self.testsetup)
