# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.base import Base
from pages.create_group_page import CreateGroupPage


class GroupsPage(Base):

    _create_group_main_button = (By.CLASS_NAME, 'large')
    _alert_message_locator = (By.CSS_SELECTOR, '.alert-info')

    def click_create_group_main_button(self):
        self.find_element(*self._create_group_main_button).click()
        return CreateGroupPage(self.selenium, self.base_url)

    def wait_for_alert_message(self):
        self.wait.until(expected.visibility_of_element_located(
            self._alert_message_locator))

    def is_group_deletion_alert_present(self):
        return self.is_element_displayed(*self._alert_message_locator)

    def create_group(self, group_name):
        create_group = self.click_create_group_main_button()
        create_group.create_group_name(group_name)
        group = create_group.click_create_group_submit()
        return group
