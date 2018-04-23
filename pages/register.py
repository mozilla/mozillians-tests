# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.base import Base


class Register(Base):

    _full_name_field_locator = (By.ID, 'id_full_name')
    _privacy_locator = (By.ID, 'id_optin')
    _create_profile_button_locator = (By.CSS_SELECTOR, '#form-submit-registration')
    _recaptcha_checkbox_locator = (By.CSS_SELECTOR, '.recaptcha-checkbox-checkmark')
    _recaptcha_checkbox_checked = (By.CSS_SELECTOR, '.recaptcha-checkbox-checked')

    _country_countainer_locator = (By.ID, 'select2-id_country-container')
    _input_locator = (By.CSS_SELECTOR, '.select2-search__field')
    _country_results_list_locator = (By.CSS_SELECTOR, '#select2-id_country-results > li.select2-results__option--highlighted')
    _first_country_search_result_locator = (By.CSS_SELECTOR, '#select2-id_country-results > li.select2-results__option--highlighted:first-child')
    _region_container_locator = (By.ID, "select2-id_region-container")
    _region_results_list_locator = (By.CSS_SELECTOR, '#select2-id_region-results > li.select2-results__option--highlighted')
    _first_region_search_result_locator = (By.CSS_SELECTOR, '#select2-id_region-results > li.select2-results__option--highlighted:first-child')
    _city_container_locator = (By.ID, "select2-id_city-container")
    _city_results_list_locator = (By.CSS_SELECTOR, '#select2-id_city-results > li.select2-results__option--highlighted')
    _first_city_search_result_locator = (By.CSS_SELECTOR, '#select2-id_city-results > li.select2-results__option--highlighted:first-child')

    @property
    def loaded(self):
        return self.is_element_present(
            By.CSS_SELECTOR, 'html.js body#edit-profile')

    @property
    def privacy_error_message(self):
        return self.find_element(*self._privacy_locator).get_attribute('validationMessage')

    def set_full_name(self, full_name):
        element = self.find_element(*self._full_name_field_locator)
        element.send_keys(full_name)

    def select_country(self, country):
        self.find_element(*self._country_countainer_locator).click()
        self.find_element(*self._input_locator).send_keys(country)
        self.wait.until(expected.presence_of_element_located(
            self._first_country_search_result_locator))
        countries_list = self.find_elements(*self._country_results_list_locator)
        country_item = next(item for item in countries_list if country == item.text)
        country_item.click()

    def select_region(self, region):
        self.find_element(*self._region_container_locator).click()
        self.find_element(*self._input_locator).send_keys(region)
        self.wait.until(expected.presence_of_element_located(
            self._first_region_search_result_locator))
        regions_list = self.find_elements(*self._region_results_list_locator)
        region_item = next(item for item in regions_list if region in item.text)
        region_item.click()

    def select_city(self, city):
        self.find_element(*self._city_container_locator).click()
        self.find_element(*self._input_locator).send_keys(city)
        self.wait.until(expected.presence_of_element_located(
            self._first_city_search_result_locator))
        cities_list = self.find_elements(*self._city_results_list_locator)
        city_item = next(item for item in cities_list if city in item.text)
        city_item.click()

    def check_privacy(self):
        self.find_element(*self._privacy_locator).click()

    def check_recaptcha(self):
        recaptcha_iframe_locator = (By.CSS_SELECTOR, '.g-recaptcha iframe')
        recaptcha_iframe = self.find_element(*recaptcha_iframe_locator)
        self.selenium.execute_script("arguments[0].scrollIntoView();", recaptcha_iframe)
        # To be removed when bug https://bugzilla.mozilla.org/show_bug.cgi?id=1314462 is fixed
        self.selenium.switch_to_frame(recaptcha_iframe)
        self.wait.until(expected.visibility_of_element_located(
            self._recaptcha_checkbox_locator)).click()
        self.wait.until(lambda s: self.find_element(*self._recaptcha_checkbox_checked))
        self.selenium.switch_to_default_content()

    def click_create_profile_button(self, leavepage=True):
        self.find_element(*self._create_profile_button_locator).click()
        if not leavepage:
            return self
        else:
            from pages.profile import Profile
            return Profile(self.selenium, self.base_url)
