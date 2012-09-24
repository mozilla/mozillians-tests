#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.base import Base

class InviteSuccess(Base):

    _success_message_locator = (By.CSS_SELECTOR, '#main > h1')
    _invite_another_mozillian_link_locator = (By.CSS_SELECTOR, '#main > p > a')

    def is_mail_address_present(self, address):
        return self.selenium.is_text_present(address)

    @property
    def is_success_message_present(self):
        return 'Invitation Sent!' in self.selenium.find_element(*self._success_message).text

    @property
    def is_invite_another_mozillian_link_present(self):
        return self.is_element_present(*self._invite_another_mozillian_link_locator)
