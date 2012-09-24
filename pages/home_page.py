#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.base import Base


class Home(Base):

    _sign_in_with_browserid_locator = (By.ID, 'create_profile')


    def __init__(self, testsetup, open_url=True):
        Base.__init__(self, testsetup)
        if open_url:
            self.selenium.get(self.base_url)

    def click_create_profile_button(self):
        self.selenium.find_element(*self._sign_in_with_browserid_locator).click()
