#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.base import Base


class Profile(Base):

    _edit_my_profile_button_locator = (By.ID, 'edit-profile')
    _name_locator = (By.CSS_SELECTOR, '#profile-info h2')
    _email_locator = (By.CSS_SELECTOR, '#profile-info a[href^="mailto:"]')
    _username_locator = (By.CSS_SELECTOR, '#profile-info dd:nth-of-type(2)')
    _website_locator = (By.CSS_SELECTOR, '#profile-info > dl > dd > a[href^="http"]')
    _vouched_by_locator = (By.CSS_SELECTOR, '#profile-info .vouched')
    _biography_locator = (By.ID, 'bio')

    @property
    def name(self):
        return self.selenium.find_element(*self._name_locator).text

    @property
    def biography(self):
        return self.selenium.find_element(*self._biography_locator).text

    @property
    def email(self):
        return self.selenium.find_element(*self._email_locator).text

    @property
    def website(self):
        return self.selenium.find_element(*self._website_locator).text

    @property
    def vouched_by(self):
        return self.selenium.find_element(*self._vouched_by_locator).text

    def click_edit_my_profile_button(self):
        self.selenium.find_element(*self._edit_my_profile_button_locator).click()
        from pages.edit_profile import EditProfile
        return EditProfile(self.testsetup)
