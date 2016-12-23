#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.base import Base
from pages.create_group_page import CreateGroupPage


class GroupsPage(Base):

    _create_group_main_button = (By.CLASS_NAME, 'large')
    _alert_message_locator = (By.CSS_SELECTOR, '.alert-info')

    def click_create_group_main_button(self):
        self.selenium.find_element(*self._create_group_main_button).click()
        return CreateGroupPage(self.base_url, self.selenium)

    def wait_for_alert_message(self):
        self.wait_for_element_visible(*self._alert_message_locator)

    def is_group_deletion_alert_present(self):
        return self.is_element_visible(*self._alert_message_locator)
