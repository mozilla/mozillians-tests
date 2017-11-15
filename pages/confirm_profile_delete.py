# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import Base


class ConfirmProfileDelete(Base):

    _delete_button_locator = (By.ID, 'delete-action')
    _cancel_button_locator = (By.ID, 'cancel-action')
    _confirm_profile_delete_text_locator = (By.CSS_SELECTOR, '#main > h1')

    @property
    def is_confirm_text_present(self):
        return self.is_element_displayed(*self._confirm_profile_delete_text_locator)

    @property
    def is_delete_button_present(self):
        return self.is_element_present(*self._delete_button_locator)

    @property
    def is_cancel_button_present(self):
        return self.is_element_present(*self._cancel_button_locator)
