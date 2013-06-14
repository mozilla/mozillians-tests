#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.base import Base


class InviteSuccess(Base):

    _success_message_locator = (By.CSS_SELECTOR, '.alert.alert-success')

    @property
    def success_message(self):
        return self.selenium.find_element(*self._success_message_locator).text
