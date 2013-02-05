#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base import Base


class Register(Base):

    #edit your profile tabs locators
    _profile_tab_locator = (By.CSS_SELECTOR, 'div.tabbable > ul.nav > li:nth-of-type(1) > a')
    _skills_tab_locator = (By.CSS_SELECTOR, 'div.tabbable > ul.nav > li:nth-of-type(2) > a')
    _location_tab_locator = (By.CSS_SELECTOR, 'div.tabbable > ul.nav > li:nth-of-type(3) > a')

    _error_locator = (By.CSS_SELECTOR, 'div.alert.alert-error')

    @property
    def error_message(self):
        return self.selenium.find_element(*self._error_locator).text

    def go_to_tab(self, tab_name):
        if tab_name is "profile":
            self.selenium.find_element(*self._profile_tab_locator).click()
            return ProfileTab(self.testsetup)
        elif tab_name is "skills":
            self.selenium.find_element(*self._skills_tab_locator).click()
            return SkillsAndGroupsTab(self.testsetup)
        elif tab_name is "location":
            self.selenium.find_element(*self._location_tab_locator).click()
            return LocationTab(self.testsetup)


class ProfileTab(Register):

    _full_name_field_locator = (By.ID, 'id_full_name')
    _website_field_locator = (By.ID, 'id_website')
    _bio_field_locator = (By.ID, 'id_bio')

    _next_button_locator = (By.ID, 'page2button')

    def set_full_name(self, full_name):
        element = self.selenium.find_element(*self._full_name_field_locator)
        element.send_keys(full_name)

    def set_website(self, website):
        element = self.selenium.find_element(*self._website_field_locator)
        element.send_keys(website)

    def set_bio(self, biography):
        element = self.selenium.find_element(*self._bio_field_locator)
        element.send_keys(biography)

    def click_next_button(self):
        self.selenium.find_element(*self._next_button_locator).click()
        return SkillsAndGroupsTab(self.testsetup)


class SkillsAndGroupsTab(Register):

    _skills_field_locator = (By.CSS_SELECTOR, '#id_skills + ul input')
    _language_field_locator = (By.CSS_SELECTOR, '#id_languages + ul input')

    _next_button_locator = (By.ID, 'page3button')
    _previous_button_locator = (By.ID, 'page1button')

    def add_language(self, language_name):
        element = self.selenium.find_element(*self._language_field_locator)
        element.send_keys(language_name)
        # send tab to make the entry "stick"
        element.send_keys("\t")

    def add_skill(self, skill_name):
        element = self.selenium.find_element(*self._skills_field_locator)
        element.send_keys(skill_name)
        # send tab to make the entry "stick"
        element.send_keys("\t")

    def click_next_button(self):
        self.selenium.find_element(*self._next_button_locator).click()
        return LocationTab(self.testsetup)

    def click_previous_button(self):
        self.selenium.find_element(*self._previous_button_locator).click()
        return ProfileTab(self.testsetup)


class LocationTab(Register):

    _country_locator = (By.ID, 'id_country')
    _state_locator = (By.ID, 'id_region')
    _city_locator = (By.ID, 'id_city')
    _privacy_locator = (By.ID, 'id_optin')
    _privacy_error_message_locator = (By.CSS_SELECTOR, 'div.control-group > div.controls > label.checkbox + span.help-inline')
    _create_profile_button_locator = (By.CSS_SELECTOR, 'button.span2.btn-large.btn-primary')

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
        return Profile(self.testsetup)
