# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.base import Base


class CreateGroupPage(Base):

    _create_group_name = (By.NAME, 'name')
    _create_group_form = (By.CSS_SELECTOR, 'form.add-group')
    _create_group_submit_button = (By.CSS_SELECTOR, 'form.add-group .btn-primary')
    _access_group_radio_button = (By.ID, 'id_is_access_group_0')

    @property
    def is_access_group_present(self):
        return self.is_element_present(*self._access_group_radio_button)

    def create_group_name(self, group_name):
        self.wait.until(expected.visibility_of_element_located(
            self._create_group_name)).send_keys(group_name)

    def click_create_group_submit(self):
        self.wait.until(expected.visibility_of_element_located(self._create_group_form))
        self.find_element(*self._create_group_submit_button).click()
        from pages.edit_group import EditGroupPage
        return EditGroupPage(self.selenium, self.base_url)
