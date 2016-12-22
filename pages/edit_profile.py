#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import random
from pages.base import Base
from pages.profile import Profile
from pages.groups_page import GroupsPage
from selenium.webdriver.common.keys import Keys


class EditProfile(Base):

    _acknowledge_deletion_checkbox_locator = (By.CSS_SELECTOR, '.acknowledge')
    _cancel_button_locator = (By.CSS_SELECTOR, 'a.cancel')
    _update_button_locator = (By.ID, 'form-submit')
    _full_name_field_locator = (By.ID, 'id_full_name')
    _website_field_locator = (By.ID, 'id_externalaccount_set-0-identifier')
    _bio_field_locator = (By.ID, 'id_bio')
    _skills_field_locator = (By.CSS_SELECTOR, '#id_skills + ul input')
    _groups_locator = (By.CSS_SELECTOR, "#groups .tagit-label")
    _skills_locator = (By.CSS_SELECTOR, "#skills .tagit-label")
    _voucher_name_locator = (By.CSS_SELECTOR, '#vouches .vouched')
    _username_field_locator = (By.ID, 'id_username')
    _delete_profile_button_locator = (By.CSS_SELECTOR, '.delete')
    _delete_skill_buttons_locator = (By.CSS_SELECTOR, '#skills .tagit-close')
    _select_month_locator = (By.ID, 'id_date_mozillian_month')
    _select_year_locator = (By.ID, 'id_date_mozillian_year')
    _month_locator = (By.CSS_SELECTOR, '#id_date_mozillian_month > option')
    _year_locator = (By.CSS_SELECTOR, '#id_date_mozillian_year > option')
    _selected_month_locator = (By.CSS_SELECTOR, '#id_date_mozillian_month > option[selected="selected"]')
    _selected_year_locator = (By.CSS_SELECTOR, '#id_date_mozillian_year > option[selected="selected"]')
    _find_group_page = (By.PARTIAL_LINK_TEXT, 'find the group')
    _services_bugzilla_locator = (By.ID, 'services-bugzilla-url')
    _services_mozilla_reps_locator = (By.ID, 'services-mozilla-reps')

    def click_update_button(self):
        self.selenium.find_element(*self._update_button_locator).click()
        return Profile(self.base_url, self.selenium)

    def click_cancel_button(self):
        self.selenium.find_element(*self._cancel_button_locator).click()

    def click_find_group_link(self):
        self.selenium.find_element(*self._find_group_page).click()
        return GroupsPage(self.base_url, self.selenium)

    def set_full_name(self, full_name):
        element = self.selenium.find_element(*self._full_name_field_locator)
        element.clear()
        element.send_keys(full_name)

    def set_website(self, website):
        element = self.selenium.find_element(*self._website_field_locator)
        element.clear()
        element.send_keys(website)

    def set_bio(self, biography):
        element = self.selenium.find_element(*self._bio_field_locator)
        element.clear()
        element.send_keys(biography)

    def add_skill(self, skill_name):
        element = self.selenium.find_element(*self._skills_field_locator)
        element.send_keys(skill_name)
        element.send_keys(Keys.RETURN)

    @property
    def vouched_by(self):
        return self.selenium.find_element(*self._voucher_name_locator).text

    @property
    def username(self):
        return self.selenium.find_element(*self._username_field_locator).text

    def click_delete_profile_button(self):
        self.selenium.find_element(*self._acknowledge_deletion_checkbox_locator).click()
        self.selenium.find_element(*self._delete_profile_button_locator).click()
        from pages.confirm_profile_delete import ConfirmProfileDelete
        return ConfirmProfileDelete(self.base_url, self.selenium)

    def select_month(self, option_month):
        element = self.selenium.find_element(*self._select_month_locator)
        select = Select(element)
        select.select_by_value(option_month)

    def select_year(self, option_year):
        element = self.selenium.find_element(*self._select_year_locator)
        select = Select(element)
        select.select_by_value(option_year)

    @property
    def month(self):
        return self.selenium.find_element(*self._selected_month_locator).text

    @property
    def year(self):
        return self.selenium.find_element(*self._selected_year_locator).text

    @property
    def months_values(self):
        return [month.get_attribute('value') for month in self.selenium.find_elements(*self._month_locator)]

    def select_random_month(self):
        return self.select_month(random.choice(self.months_values[1:]))

    @property
    def years_values(self):
        return [year.get_attribute('value') for year in self.selenium.find_elements(*self._year_locator)]

    @property
    def groups(self):
        groups = self.selenium.find_elements(*self._groups_locator)
        return [groups[i].text for i in range(0, len(groups))]

    @property
    def skills(self):
        skills = self.selenium.find_elements(*self._skills_locator)
        return [skills[i].text for i in range(0, len(skills))]

    @property
    def delete_skill_buttons(self):
        return self.selenium.find_elements(*self._delete_skill_buttons_locator)

    def select_random_year(self):
        return self.select_year(random.choice(self.years_values[1:]))

    def get_services_urls(self):
        locs = [self._services_bugzilla_locator, self._services_mozilla_reps_locator]
        urls = []

        for element in locs:
            url = self.selenium.find_element(*element).get_attribute('href')
            urls.append(url)

        return urls
