# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base import Base


class Profile(Base):
    URL_TEMPLATE = '/{locale}/u/{username}'

    _profile_photo_locator = (By.CSS_SELECTOR, '#profile-stats > div.profile-photo img')
    _name_locator = (By.CSS_SELECTOR, 'h1.p-name')
    _email_locator = (By.CSS_SELECTOR, '.email')
    _irc_nickname_locator = (By.CSS_SELECTOR, '.nickname')
    _website_locator = (By.CSS_SELECTOR, '.url')
    _vouched_by_locator = (By.CSS_SELECTOR, '#profile-info .vouched')
    _biography_locator = (By.CSS_SELECTOR, '#bio > .note > p')
    _skills_locator = (By.ID, 'skills')
    _groups_locator = (By.CSS_SELECTOR, 'div#groups')
    _languages_locator = (By.ID, 'languages')
    _location_locator = (By.ID, 'location')
    _city_locator = (By.CSS_SELECTOR, '#location .locality')
    _region_locator = (By.CSS_SELECTOR, '#location .region')
    _country_locator = (By.CSS_SELECTOR, '#location .country-name')
    _profile_message_locator = (By.CSS_SELECTOR, '.alert')
    _view_as_locator = (By.ID, 'view-privacy-mode')

    @property
    def loaded(self):
        return self.is_element_present(By.CSS_SELECTOR, 'html.js body#profile')

    def view_profile_as(self, view_as):
        element = self.find_element(*self._view_as_locator)
        select = Select(element)
        select.select_by_visible_text(view_as)

    @property
    def name(self):
        return self.find_element(*self._name_locator).text

    @property
    def biography(self):
        return self.find_element(*self._biography_locator).text

    @property
    def email(self):
        return self.find_element(*self._email_locator).text

    @property
    def irc_nickname(self):
        return self.find_element(*self._irc_nickname_locator).text

    @property
    def website(self):
        return self.find_element(*self._website_locator).text

    @property
    def vouched_by(self):
        return self.find_element(*self._vouched_by_locator).text

    @property
    def skills(self):
        return self.find_element(*self._skills_locator).text.split('\n')[1]

    @property
    def groups(self):
        return self.find_element(*self._groups_locator).text.split('\n')[1]

    @property
    def location(self):
        return self.find_element(*self._location_locator).text

    @property
    def city(self):
        return self.find_element(*self._city_locator).text

    @property
    def region(self):
        return self.find_element(*self._region_locator).text

    @property
    def country(self):
        return self.find_element(*self._country_locator).text

    def click_profile_city_filter(self):
        self.find_element(*self._city_locator).click()
        from location_search_results import LocationSearchResults
        return LocationSearchResults(self.selenium, self.base_url)

    def click_profile_region_filter(self,):
        self.find_element(*self._region_locator).click()
        from location_search_results import LocationSearchResults
        return LocationSearchResults(self.selenium, self.base_url)

    def click_profile_country_filter(self):
        self.find_element(*self._country_locator).click()
        from location_search_results import LocationSearchResults
        return LocationSearchResults(self.selenium, self.base_url)

    @property
    def languages(self):
        return self.find_element(*self._languages_locator).text.split('\n')[1]

    @property
    def profile_message(self):
        return self.find_element(*self._profile_message_locator).text

    @property
    def is_groups_present(self):
        return self.is_element_present(*self._groups_locator)

    @property
    def is_skills_present(self):
        return self.is_element_present(*self._skills_locator)
