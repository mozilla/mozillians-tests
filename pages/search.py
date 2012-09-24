#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.base import Base

class Search(Base):

    _result_locator = (By.CSS_SELECTOR, 'div.row > div.result')
    _search_button_locator = (By.CSS_SELECTOR, '.btn.primary:nth-of-type(1)')
    _advanced_options_button_locator = (By.CSS_SELECTOR, '.btn.primary:nth-of-type(2)')
    _advanced_options_locator = (By.CSS_SELECTOR, '.search-options')
    _non_vouched_only_checkbox_locator = (By.ID, 'id_nonvouched_only')
    _with_photos_only_checkbox_locator = (By.ID, 'id_picture_only')
    _no_results_locator_head = (By.ID, 'not-found')
    _no_results_locator_body = (By.CSS_SELECTOR, 'div.well > p:nth-of-type(2)')

    @property
    def results_count(self):
        return len(self.selenium.find_elements(*self._result_locator))

    @property
    def no_results_message_head(self):
        return self.selenium.find_element(*self._no_results_locator_head).text

    @property
    def no_results_message_body(self):
        return self.selenium.find_element(*self._no_results_locator_body).text

    def search_for(self, search_term):
        element = self.selenium.find_element(*self._search_box_locator)
        element.send_keys(search_term)
        self.selenium.find_element(*self._search_button_locator).click()

    def toggle_advanced_options(self):
        self.selenium.find_element(*self._advanced_options_button_locator).click()

    @property
    def advanced_options_shown(self):
        return self.is_element_visible(*self._advanced_options_locator)

    def check_non_vouched_only(self):
        self.selenium.find_element(*self._non_vouched_only_checkbox_locator).click()

    def check_with_photos_only(self):
        self.selenium.find_elemennt(*self._with_photos_only_checkbox_locator).click()
