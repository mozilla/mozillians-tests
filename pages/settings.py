#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from pages.base import Base
from pages.groups_page import GroupsPage
from pages.page import PageRegion


class Settings(Base):
    _profile_tab_locator = (By.ID, 'profile')
    _profile_button_locator = (By.CSS_SELECTOR, '#profile-tab > a')

    _you_and_mozilla_tab_locator = (By.ID, 'youandmozilla')
    _you_and_mozilla_button_locator = (By.CSS_SELECTOR, '#youandmozilla-tab > a')

    _groups_tab_locator = (By.ID, 'mygroups')
    _groups_button_locator = (By.CSS_SELECTOR, '#mygroups-tab > a')

    _external_accounts_tab_locator = (By.ID, 'extaccounts')
    _external_accounts_button_locator = (By.CSS_SELECTOR, '#extaccounts-tab > a')

    _developer_tab_locator = (By.ID, 'developer')
    _developer_button_locator = (By.CSS_SELECTOR, '#developer-tab > a')

    @property
    def profile(self):
        self.selenium.find_element(*self._profile_button_locator).click()
        return self.ProfileTab(self.base_url, self.selenium,
                               self.selenium.find_element(*self._profile_tab_locator))

    @property
    def you_and_mozilla(self):
        self.selenium.find_element(*self._you_and_mozilla_button_locator).click()
        return self.YouAndMozilla(self.base_url, self.selenium,
                                  self.selenium.find_element(*self._you_and_mozilla_tab_locator))

    @property
    def groups(self):
        self.selenium.find_element(*self._groups_button_locator).click()
        return self.Groups(self.base_url, self.selenium,
                           self.selenium.find_element(*self._groups_tab_locator))

    @property
    def external_accounts(self):
        self.selenium.find_element(*self._external_accounts_button_locator).click()
        return self.ExternalAccountsTab(self.base_url, self.selenium,
                                        self.selenium.find_element(*self._external_accounts_tab_locator))

    @property
    def developer(self):
        self.selenium.find_element(*self._developer_button_locator).click()
        return self.DeveloperTab(self.base_url, self.selenium,
                                 self.selenium.find_element(*self._developer_tab_locator))

    def create_group(self, group_name):
        groups = self.groups.click_find_group_link()
        create_group = groups.click_create_group_main_button()
        create_group.create_group_name(group_name)
        group = create_group.click_create_group_submit()
        return group

    class ProfileTab(PageRegion):
        _basic_info_form_locator = (By.CSS_SELECTOR, 'form.edit-profile:nth-child(1)')
        _skills_form_locator = (By.CSS_SELECTOR, 'form.edit-profile:nth-child(3)')
        _delete_account_form_locator = (By.CSS_SELECTOR, 'div.panel-danger')

        @property
        def basic_information(self):
            return self.EditProfileForm(self.base_url, self.selenium,
                                        self._root_element.find_element(*self._basic_info_form_locator))

        @property
        def skills(self):
            return self.SkillsForm(self.base_url, self.selenium,
                                   self._root_element.find_element(*self._skills_form_locator))

        @property
        def delete_account(self):
            return self.DeleteAccount(self.base_url, self.selenium,
                                      self._root_element.find_element(*self._delete_account_form_locator))

        class EditProfileForm (PageRegion):

            _full_name_field_locator = (By.ID, 'id_full_name')
            _bio_field_locator = (By.ID, 'id_bio')
            _update_locator = (By.ID, 'form-submit-basic')

            def set_full_name(self, full_name):
                element = self._root_element.find_element(*self._full_name_field_locator)
                element.clear()
                element.send_keys(full_name)

            def set_bio(self, biography):
                element = self._root_element.find_element(*self._bio_field_locator)
                element.clear()
                element.send_keys(biography)

            def click_update(self):
                self._root_element.find_element(*self._update_locator).click()

        class DeleteAccount(PageRegion):

            _delete_acknowledgement_locator = (By.CSS_SELECTOR, '#delete-checkbox')
            _delete_profile_button_locator = (By.ID, 'delete-profile')

            def check_acknowledgement(self):
                self._root_element.find_element(*self._delete_acknowledgement_locator).click()

            @property
            def is_delete_button_enabled(self):
                return 'disabled' not in self._root_element.find_element(*self._delete_profile_button_locator).get_attribute('class')

            def click_delete_profile(self):
                self._root_element.find_element(*self._delete_profile_button_locator).click()
                from pages.confirm_profile_delete import ConfirmProfileDelete
                return ConfirmProfileDelete(self.base_url, self.selenium)

        class SkillsForm(PageRegion):
            _skills_locator = (By.CSS_SELECTOR, '#skills .select2-selection__choice')
            _skills_field_locator = (By.CSS_SELECTOR, '#skills input')
            _delete_skill_buttons_locator = (By.CSS_SELECTOR, '#skills .select2-selection__choice__remove')
            _skills_first_result_locator = (By.CSS_SELECTOR, '.select2-results li:not(.loading-results):first-child')
            _update_locator = (By.ID, 'form-submit-skills')

            @property
            def skills(self):
                # Return skills list with leading `x` button stripped
                skills = self._root_element.find_elements(*self._skills_locator)
                return [skills[i].text[1:] for i in range(0, len(skills))]

            def add_skill(self, skill_name):
                element = self._root_element.find_element(*self._skills_field_locator)
                element.send_keys(skill_name)
                self.wait_for_element_present(*self._skills_first_result_locator)
                element.send_keys(Keys.RETURN)

            @property
            def delete_skill_buttons(self):
                return self._root_element.find_elements(*self._delete_skill_buttons_locator)

            def click_update(self):
                self._root_element.find_element(*self._update_locator).click()

    class YouAndMozilla(PageRegion):

        _contributions_form_locator = (By.CSS_SELECTOR, 'form.edit-profile:nth-child(1)')

        @property
        def contributions(self):
            return self.Contributions(self.base_url, self.selenium,
                                      self._root_element.find_element(*self._contributions_form_locator))

        class Contributions(PageRegion):

            _select_month_locator = (By.ID, 'id_date_mozillian_month')
            _select_year_locator = (By.ID, 'id_date_mozillian_year')
            _month_locator = (By.CSS_SELECTOR, '#id_date_mozillian_month > option')
            _year_locator = (By.CSS_SELECTOR, '#id_date_mozillian_year > option')
            _selected_month_locator = (By.CSS_SELECTOR, '#id_date_mozillian_month > option[selected="selected"]')
            _selected_year_locator = (By.CSS_SELECTOR, '#id_date_mozillian_year > option[selected="selected"]')
            _update_locator = (By.ID, 'form-submit-contribution')

            def select_month(self, option_month):
                element = self._root_element.find_element(*self._select_month_locator)
                select = Select(element)
                select.select_by_value(option_month)

            def select_year(self, option_year):
                element = self._root_element.find_element(*self._select_year_locator)
                select = Select(element)
                select.select_by_value(option_year)

            @property
            def month(self):
                # Return selected month text
                return self._root_element.find_element(*self._selected_month_locator).text

            @property
            def year(self):
                # Return selected year text
                return self._root_element.find_element(*self._selected_year_locator).text

            @property
            def months_values(self):
                # Return all month values
                return [month.get_attribute('value') for month in self._root_element.find_elements(*self._month_locator)]

            @property
            def years_values(self):
                # Return all year values
                return [year.get_attribute('value') for year in self._root_element.find_elements(*self._year_locator)]

            def select_random_month(self):
                return self.select_month(random.choice(self.months_values[1:]))

            def select_random_year(self):
                return self.select_year(random.choice(self.years_values[1:]))

            def click_update(self):
                self._root_element.find_element(*self._update_locator).click()

    class Groups(PageRegion):

        _find_group_page = (By.PARTIAL_LINK_TEXT, 'find the group')

        @property
        def is_find_group_link_visible(self):
            return self.is_element_visible(*self._find_group_page)

        def click_find_group_link(self):
            self.selenium.find_element(*self._find_group_page).click()
            return GroupsPage(self.base_url, self.selenium)

    class ExternalAccountsTab(PageRegion):

        _external_accounts_form_locator = (By.CSS_SELECTOR, '#extaccounts > form > div:nth-child(2)')
        _irc_form_locator = (By.CSS_SELECTOR, '#extaccounts > form > div:nth-child(3)')

        @property
        def external_accounts_form(self):
            return self.ExternalAccounts(self.base_url, self.selenium,
                                         self._root_element.find_element(*self._external_accounts_form_locator))

        @property
        def irc_form(self):
            return self.Irc(self.base_url, self.selenium, self._root_element.find_element(*self._irc_form_locator))

        class ExternalAccounts(PageRegion):
            _add_account_locator = (By.ID, 'accounts-addfield')
            _account_row_locator = (By.CSS_SELECTOR, 'div.externalaccount-fieldrow')

            @property
            def is_displayed(self):
                return self._root_element.is_displayed()

            def count_external_accounts(self):
                return len(self._root_element.find_elements(*self._account_row_locator))

            def click_add_account(self):
                self._root_element.find_element(*self._add_account_locator).click()

        class Irc(PageRegion):
            _irc_nickname_locator = (By.ID, 'id_ircname')
            _update_locator = (By.ID, 'form-submit-irc')

            @property
            def nickname(self):
                return self._root_element.find_element(*self._irc_nickname_locator).get_attribute('value')

            @property
            def is_displayed(self):
                return self._root_element.is_displayed()

            def update_nickname(self, new_nickname):
                element = self._root_element.find_element(*self._irc_nickname_locator)
                element.clear()
                element.send_keys(new_nickname)

            def click_update(self):
                self._root_element.find_element(*self._update_locator).click()

    class DeveloperTab(PageRegion):

        _services_bugzilla_locator = (By.ID, 'services-bugzilla-url')
        _services_mozilla_reps_locator = (By.ID, 'services-mozilla-reps')

        def get_services_urls(self):
            locs = [self._services_bugzilla_locator, self._services_mozilla_reps_locator]
            urls = []

            for element in locs:
                url = self._root_element.find_element(*element).get_attribute('href')
                urls.append(url)

            return urls
