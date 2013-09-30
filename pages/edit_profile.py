#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import random
from pages.base import Base
from pages.profile import Profile


class EditProfile(Base):

    _acknowledge_deletion_checkbox_locator = (By.CSS_SELECTOR, '.acknowledge')
    _cancel_button_locator = (By.CSS_SELECTOR, "#edit_controls a")
    _update_button_locator = (By.CSS_SELECTOR, "#edit_controls button")
    _full_name_field_locator = (By.ID, 'id_full_name')
    _website_field_locator = (By.ID, 'id_website')
    _bio_field_locator = (By.ID, 'id_bio')
    _groups_field_locator = (By.CSS_SELECTOR, '#id_groups + ul input')
    _skills_field_locator = (By.CSS_SELECTOR, '#id_skills + ul input')
    _voucher_name_locator = (By.CSS_SELECTOR, '#vouches .vouched')
    _username_field_locator = (By.ID, 'id_username')
    _browserid_mail_locator = (By.CSS_SELECTOR, '.control-group:nth-of-type(2) .label-text')
    _delete_profile_button_locator = (By.CSS_SELECTOR, '.delete')
    _select_month_locator = (By.ID, 'id_date_mozillian_month')
    _select_year_locator = (By.ID, 'id_date_mozillian_year')
    _month_locator = (By.CSS_SELECTOR, '#id_date_mozillian_month > option')
    _year_locator = (By.CSS_SELECTOR, '#id_date_mozillian_year > option')
    _selected_month_locator = (By.CSS_SELECTOR, '#id_date_mozillian_month > option[selected="selected"]')
    _selected_year_locator=(By.CSS_SELECTOR, '#id_date_mozillian_year > option[selected="selected"]')

    def click_update_button(self):
        self.selenium.find_element(*self._update_button_locator).click()
        return Profile(self.testsetup)

    def click_cancel_button(self):
        self.selenium.find_element(*self._cancel_button_locator).click()

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

    def add_group(self, group_name):
        element = self.selenium.find_element(*self._group_field_locator)
        element.send_keys(group_name)

    def add_skill(self, skill_name):
        element = self.selenium.send_keys(*self._skill_field_locator)
        element.send_keys(skill_name)

    @property
    def vouched_by(self):
        return self.selenium.find_element(*self._voucher_name_locator).text

    @property
    def username(self):
        return self.selenium.find_element(*self._username_field_locator).text

    @property
    def browserid_email(self):
        return self.selenium.find_element(*self._browserid_mail_locator).text

    def click_delete_profile_button(self):
        self.selenium.find_element(*self._acknowledge_deletion_checkbox_locator).click()
        self.selenium.find_element(*self._delete_profile_button_locator).click()
        from pages.confirm_profile_delete import ConfirmProfileDelete
        return ConfirmProfileDelete(self.testsetup)

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

    def select_random_year(self):
        return self.select_year(random.choice(self.years_values[1:]))
