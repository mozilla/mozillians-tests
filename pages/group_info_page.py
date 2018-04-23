# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.base import Base


class GroupInfoPage(Base):

    _delete_group_button = (By.CSS_SELECTOR, '.button.delete.right')
    _description_locator = (By.CSS_SELECTOR, '.group-description')
    _irc_channel_locator = (By.ID, 'group-irc')

    @property
    def loaded(self):
        return self.is_element_present(
            By.CSS_SELECTOR, 'html.js body#group-show')

    def delete_group(self):
        self.wait.until(expected.visibility_of_element_located(
            self._delete_group_button)).click()
        from pages.groups_page import GroupsPage
        return GroupsPage(self.selenium, self.base_url)

    @property
    def description(self):
        return self.find_element(*self._description_locator).text

    @property
    def irc_channel(self):
        return self.find_element(*self._irc_channel_locator).text
