#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base import Base


class Profile(Base):

    _profile_photo_locator = (By.CSS_SELECTOR, '.profile-photo > img')
    _name_locator = (By.CSS_SELECTOR, 'h1.p-name')
    _email_locator = (By.CSS_SELECTOR, '.u-email.email')
    _website_locator = (By.CSS_SELECTOR, '.u-url.url > a')
    _vouched_by_locator = (By.CSS_SELECTOR, '#profile-info .vouched')
    _biography_locator = (By.CSS_SELECTOR, '#bio > p')
    _skills_locator = (By.ID, 'skills')
    _languages_locator = (By.ID, 'languages')
    _location_locator = (By.ID, 'location')
    _city_locator = (By.CSS_SELECTOR, '#location > a:nth-child(2)')
    _region_locator = (By.CSS_SELECTOR, '#location > a:nth-child(3)')
    _country_locator = (By.CSS_SELECTOR, '#location > a:nth-child(4)')
    _your_profile_locator = (By.CSS_SELECTOR, '.alert')

    def __init__(self, testsetup):
        Base.__init__(self, testsetup)
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: self.is_element_visible(*self._profile_photo_locator))

    @property
    def name(self):
        return self.selenium.find_element(*self._name_locator).text

    @property
    def biography(self):
        return self.selenium.find_element(*self._biography_locator).text

    @property
    def email(self):
        return self.selenium.find_element(*self._email_locator).text

    @property
    def website(self):
        return self.selenium.find_element(*self._website_locator).text

    @property
    def vouched_by(self):
        return self.selenium.find_element(*self._vouched_by_locator).text

    @property
    def skills(self):
        return self.selenium.find_element(*self._skills_locator).text.split('\n')[1]

    @property
    def location(self):
        return self.selenium.find_element(*self._location_locator).text

    @property
    def city(self):
        return self.find_element(*self._city_locator).text

    @property
    def region(self):
        return self.find_element(*self._region_locator).text

    @property
    def country(self):
        return self.find_element(*self._country_locator).text

    def click_city_name(self, **kwargs):
        self.find_element(*self._city_locator).click()
        from location_search_results import LocationSearchResults
        return LocationSearchResults(self.testsetup, **kwargs)

    def click_region_name(self, **kwargs):
        self.find_element(*self._region_locator).click()
        from location_search_results import LocationSearchResults
        return LocationSearchResults(self.testsetup, **kwargs)

    def click_country_name(self, **kwargs):
        self.find_element(*self._country_locator).click()
        from location_search_results import LocationSearchResults
        return LocationSearchResults(self.testsetup, **kwargs)

    @property
    def languages(self):
        return self.selenium.find_element(*self._languages_locator).text.split('\n')[1]

    @property
    def profile_message(self):
        return self.selenium.find_element(*self._your_profile_locator).text
