# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import Base


class Home(Base):

    _groups_link_locator = (By.CSS_SELECTOR, 'section.groups > a')
    _functional_areas_link_locator = (By.CSS_SELECTOR, 'section.functional-areas > a')

    @property
    def is_groups_link_visible(self):
        return self.is_element_displayed(*self._groups_link_locator)

    @property
    def is_functional_areas_link_visible(self):
        return self.is_element_displayed(*self._functional_areas_link_locator)

    def wait_for_user_login(self):
        # waits to see if user gets logged back in
        # if not then all ok
        try:
            self.wait.until(lambda s: self.is_user_loggedin)
        except Exception:
            pass
