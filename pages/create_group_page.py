#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base import Base


class CreateGroupPage(Base):
    
    _create_group_name = (By.NAME, 'name')
    _create_group_submit_button = (By.ID, 'create_group_button')
    
    def create_group_name(self, group_name):
        element = self.selenium.find_element(*self._create_group_name)
        element.send_keys(group_name)
        
    def click_create_group_submit(self):
        self.selenium.find_element(*self._create_group_submit_button).click()
