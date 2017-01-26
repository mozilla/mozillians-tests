#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.base import Base


class GroupInfoPage(Base):

    _delete_group_button = (By.CSS_SELECTOR, '.button.delete.right')
    _description_locator = (By.CSS_SELECTOR, '.group-description')
    _irc_channel_locator = (By.ID, 'group-irc')

    def delete_group(self):
        self.wait_for_element_visible(*self._delete_group_button)
        self.selenium.find_element(*self._delete_group_button).click()
        from pages.groups_page import GroupsPage
        return GroupsPage(self.base_url, self.selenium)

    @property
    def description(self):
        return self.selenium.find_element(*self._description_locator).text

    @property
    def irc_channel(self):
        return self.selenium.find_element(*self._irc_channel_locator).text
