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
    _recaptcha_checkbox_locator = (By.CSS_SELECTOR, '.recaptcha-checkbox-checkmark')
    _recaptcha_checkbox_checked = (By.CSS_SELECTOR, '.recaptcha-checkbox-checked')

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

    def check_recaptcha(self):
        recaptcha_iframe_locator = (By.CSS_SELECTOR, '.g-recaptcha iframe')
        recaptcha_iframe = self.selenium.find_element(*recaptcha_iframe_locator)
        self.selenium.switch_to_frame(recaptcha_iframe)

        recaptcha_checkbox = self.selenium.find_element(*self._recaptcha_checkbox_locator)
        self.scroll_to_element(recaptcha_checkbox)
        recaptcha_checkbox.click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: self.selenium.find_element(*self._recaptcha_checkbox_checked)
        )
        self.selenium.switch_to_default_content()

    def click_create_profile_button(self, leavepage=True):
        self.selenium.find_element(*self._create_profile_button_locator).click()
        if not leavepage:
            return self
        else:
            from pages.profile import Profile
            return Profile(self.base_url, self.selenium)
