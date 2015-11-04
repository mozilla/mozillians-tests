#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.base import Base


class GroupInfoPage(Base):

    _delete_group_button = (By.CSS_SELECTOR, '.button.delete.right')

    def delete_group(self):
        self.selenium.find_element(*self._delete_group_button).click()
        from pages.groups_page import GroupsPage
        return GroupsPage(self.base_url, self.selenium)
