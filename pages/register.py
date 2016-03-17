#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from pages.base import Base


class Register(Base):

    _error_locator = (By.CSS_SELECTOR, 'div.alert.alert-error')
    _full_name_field_locator = (By.ID, 'id_full_name')
    _map_search_box_locator = (By.ID, 'location_search')
    _country_locator = (By.ID, 'display_country')
    _privacy_locator = (By.ID, 'id_optin')
    _privacy_error_message_locator = (By.CSS_SELECTOR, '.error-message')
    _create_profile_button_locator = (By.CSS_SELECTOR, '#form-submit-registration')

    @property
    def error_message(self):
        return self.selenium.find_element(*self._error_locator).text

    def set_location(self, location):
        element = self.selenium.find_element(*self._map_search_box_locator)
        element.send_keys(location)
        element.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._country_locator).text != "")

    def set_full_name(self, full_name):
        element = self.selenium.find_element(*self._full_name_field_locator)
        element.send_keys(full_name)

    @property
    def privacy_error_message(self):
        return self.selenium.find_element(*self._privacy_error_message_locator).text

    def select_country(self, country):
        element = self.selenium.find_element(*self._country_locator)
        select = Select(element)
        select.select_by_value(country)

    def set_state(self, state_name):
        element = self.selenium.find_element(*self._state_locator)
        element.send_keys(state_name)

    def set_city(self, city_name):
        element = self.selenium.find_element(*self._city_locator)
        element.send_keys(city_name)

    def check_privacy(self):
        self.selenium.find_element(*self._privacy_locator).click()

    def click_create_profile_button(self):
        self.selenium.find_element(*self._create_profile_button_locator).click()
        from pages.profile import Profile
        return Profile(self.base_url, self.selenium)
