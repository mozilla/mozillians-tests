#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.base import Base

class InviteSuccess(Base):

    _success_message_head_locator = (By.CSS_SELECTOR, '#main > h1')
    _success_message_body_locator = (By.CSS_SELECTOR, '#main > p')
    _invite_another_mozillian_link_locator = (By.CSS_SELECTOR, '#main > p > a')

    @property
    def success_message_body(self):
        return self.selenium.find_element(*self._success_message_body_locator).text

    @property
    def success_message_header(self):
        return  self.selenium.find_element(*self._success_message_head_locator).text

    @property
    def is_invite_another_mozillian_link_present(self):
        return self.is_element_present(*self._invite_another_mozillian_link_locator)
