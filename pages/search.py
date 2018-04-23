# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.base import Base


class Search(Base):

    _result_locator = (By.CSS_SELECTOR, '#content-wrapper > #main div.result')
    _search_button_locator = (By.CSS_SELECTOR, 'button[type = "submit"]')
    _advanced_options_button_locator = (By.CSS_SELECTOR, '.btn.primary:nth-of-type(2)')
    _advanced_options_locator = (By.CSS_SELECTOR, '.search-options')
    _non_vouched_only_checkbox_locator = (By.ID, 'id_nonvouched_only')
    _with_photos_only_checkbox_locator = (By.ID, 'id_picture_only')
    _no_results_locator_head = (By.ID, 'not-found')
    _no_results_locator_body = (By.CSS_SELECTOR, 'div.well > p:nth-of-type(2)')
    _last_page_number_locator = (By.CSS_SELECTOR, '#pagination-form select option:last-child')
    _group_name_locator = (By.CSS_SELECTOR, '.group-name')

    @property
    def loaded(self):
        return self.is_element_present(By.CSS_SELECTOR, 'html.js body#search')

    @property
    def results_count(self):
        return len(self.find_elements(*self._result_locator))

    @property
    def number_of_pages(self):
        element = self.find_element(*self._last_page_number_locator)
        return element.get_attribute('text')

    @property
    def no_results_message_head(self):
        return self.find_element(*self._no_results_locator_head).text

    @property
    def no_results_message_body(self):
        return self.find_element(*self._no_results_locator_body).text

    @property
    def advanced_options_shown(self):
        return self.is_element_displayed(*self._advanced_options_locator)

    def toggle_advanced_options(self):
        self.find_element(*self._advanced_options_button_locator).click()

    def check_non_vouched_only(self):
        self.find_element(*self._non_vouched_only_checkbox_locator).click()

    def check_with_photos_only(self):
        self.find_element(*self._with_photos_only_checkbox_locator).click()

    @property
    def search_results(self):
        return [self.SearchResult(self, el) for el in self.find_elements(*self._result_locator)]

    def open_group(self, name):
        self.wait.until(expected.visibility_of_element_located(
            (By.CSS_SELECTOR, '.group-name[title="{}"]'.format(name)))).click()
        from pages.group_info_page import GroupInfoPage
        return GroupInfoPage(self.selenium, self.base_url).wait_for_page_to_load()

    class SearchResult(Region):

        _profile_page_link_locator = (By.CSS_SELECTOR, 'li a')
        _name_locator = (By.CSS_SELECTOR, '.result .details h2')

        def open_profile_page(self):
            self.find_element(*self._profile_page_link_locator).click()
            from pages.profile import Profile
            return Profile(self.page.selenium, self.page.base_url).wait_for_page_to_load()

        @property
        def name(self):
            return self.find_element(*self._name_locator).text
