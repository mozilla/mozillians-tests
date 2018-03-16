# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from pypom import Region
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.select import Select

from pages.base import Base
from pages.groups_page import GroupsPage


class Settings(Base):
    URL_TEMPLATE = '{locale}/user/edit'

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
        self.wait.until(expected.presence_of_element_located(
            self._profile_button_locator)).click()
        return self.ProfileTab(self, self.find_element(*self._profile_tab_locator))

    @property
    def you_and_mozilla(self):
        self.find_element(*self._you_and_mozilla_button_locator).click()
        return self.YouAndMozilla(self, self.find_element(*self._you_and_mozilla_tab_locator))

    @property
    def groups(self):
        self.find_element(*self._groups_button_locator).click()
        return self.Groups(self, self.find_element(*self._groups_tab_locator))

    @property
    def external_accounts(self):
        self.find_element(*self._external_accounts_button_locator).click()
        return self.ExternalAccountsTab(self, self.find_element(*self._external_accounts_tab_locator))

    @property
    def developer(self):
        self.find_element(*self._developer_button_locator).click()
        return self.DeveloperTab(self, self.find_element(*self._developer_tab_locator))

    def create_group(self, group_name):
        groups = self.groups.click_find_group_link()
        create_group = groups.click_create_group_main_button()
        create_group.create_group_name(group_name)
        group = create_group.click_create_group_submit()
        return group

    class ProfileTab(Region):
        _basic_info_form_locator = (By.CSS_SELECTOR, 'form.edit-profile:nth-child(1)')
        _skills_form_locator = (By.CSS_SELECTOR, 'form.edit-profile:nth-child(3)')
        _delete_account_form_locator = (By.CSS_SELECTOR, 'div.panel-danger')

        @property
        def basic_information(self):
            return self.EditProfileForm(self.page, self.find_element(*self._basic_info_form_locator))

        @property
        def skills(self):
            return self.SkillsForm(self.page, self.find_element(*self._skills_form_locator))

        @property
        def delete_account(self):
            return self.DeleteAccount(self.page, self.find_element(*self._delete_account_form_locator))

        class EditProfileForm (Region):

            _full_name_field_locator = (By.ID, 'id_full_name')
            _bio_field_locator = (By.ID, 'id_bio')
            _update_locator = (By.ID, 'form-submit-basic')

            def set_full_name(self, full_name):
                element = self.find_element(*self._full_name_field_locator)
                element.clear()
                element.send_keys(full_name)

            def set_bio(self, biography):
                element = self.find_element(*self._bio_field_locator)
                element.clear()
                element.send_keys(biography)

            def click_update(self):
                el = self.find_element(*self._update_locator)
                el.click()
                self.wait.until(expected.staleness_of(el))
                self.wait.until(expected.presence_of_element_located(
                    self._update_locator))

        class DeleteAccount(Region):

            _delete_acknowledgement_locator = (By.CSS_SELECTOR, '#delete-checkbox')
            _delete_profile_button_locator = (By.ID, 'delete-profile')

            def check_acknowledgement(self):
                self.find_element(*self._delete_acknowledgement_locator).click()

            @property
            def is_delete_button_enabled(self):
                return 'disabled' not in self.find_element(*self._delete_profile_button_locator).get_attribute('class')

            def click_delete_profile(self):
                self.find_element(*self._delete_profile_button_locator).click()
                from pages.confirm_profile_delete import ConfirmProfileDelete
                return ConfirmProfileDelete(self.page.selenium, self.page.base_url)

        class SkillsForm(Region):
            _skills_locator = (By.CSS_SELECTOR, '#skills .select2-selection__choice')
            _skills_field_locator = (By.CSS_SELECTOR, '#skills input')
            _delete_skill_buttons_locator = (By.CSS_SELECTOR, '#skills .select2-selection__choice__remove')
            _skills_first_result_locator = (By.CSS_SELECTOR, '.select2-results li:not(.loading-results):first-child')
            _update_locator = (By.ID, 'form-submit-skills')

            @property
            def skills(self):
                # Return skills list with leading `x` button stripped
                skills = self.find_elements(*self._skills_locator)
                return [skills[i].text[1:] for i in range(0, len(skills))]

            def add_skill(self, skill_name):
                element = self.find_element(*self._skills_field_locator)
                element.send_keys(skill_name)
                self.wait.until(expected.presence_of_element_located(
                    self._skills_first_result_locator))
                element.send_keys(Keys.RETURN)

            @property
            def delete_skill_buttons(self):
                return self.find_elements(*self._delete_skill_buttons_locator)

            def delete_skill(self, skill):
                skill_index = self.skills.index(skill)
                self.delete_skill_buttons[skill_index].click()

            def click_update(self):
                self.find_element(*self._update_locator).click()

    class YouAndMozilla(Region):

        _contributions_form_locator = (By.CSS_SELECTOR, 'form.edit-profile:nth-child(1)')

        @property
        def contributions(self):
            return self.Contributions(self.page, self.find_element(*self._contributions_form_locator))

        class Contributions(Region):

            _select_month_locator = (By.ID, 'id_date_mozillian_month')
            _select_year_locator = (By.ID, 'id_date_mozillian_year')
            _month_locator = (By.CSS_SELECTOR, '#id_date_mozillian_month > option')
            _year_locator = (By.CSS_SELECTOR, '#id_date_mozillian_year > option')
            _update_locator = (By.ID, 'form-submit-contribution')

            def select_month(self, option_month):
                element = self.find_element(*self._select_month_locator)
                select = Select(element)
                select.select_by_visible_text(option_month)

            def select_year(self, option_year):
                element = self.find_element(*self._select_year_locator)
                select = Select(element)
                select.select_by_visible_text(option_year)

            @property
            def month(self):
                # Return selected month text
                return [month.text for month in self.find_elements(*self._month_locator) if month.get_property('selected')]

            @property
            def year(self):
                # Return selected year text
                return [year.text for year in self.find_elements(*self._year_locator) if year.get_property('selected')]

            @property
            def months_values(self):
                # Return all month values
                return [month.text for month in self.find_elements(*self._month_locator)]

            @property
            def years_values(self):
                # Return all year values
                return [year.text for year in self.find_elements(*self._year_locator)]

            def select_random_month(self):
                return self.select_month(random.choice(self.months_values[1:]))

            def select_random_year(self):
                return self.select_year(random.choice(self.years_values[1:]))

            def click_update(self):
                el = self.find_element(*self._update_locator)
                el.click()
                self.wait.until(expected.staleness_of(el))
                self.wait.until(expected.presence_of_element_located(
                    self._update_locator))

    class Groups(Region):

        _find_group_page = (By.PARTIAL_LINK_TEXT, 'find the group')

        @property
        def is_find_group_link_visible(self):
            return self.is_element_displayed(*self._find_group_page)

        def click_find_group_link(self):
            self.find_element(*self._find_group_page).click()
            return GroupsPage(self.page.selenium, self.page.base_url)

    class ExternalAccountsTab(Region):

        _external_accounts_form_locator = (By.CSS_SELECTOR, '#extaccounts > form > div:nth-child(2)')
        _irc_form_locator = (By.CSS_SELECTOR, '#extaccounts > form > div:nth-child(3)')

        @property
        def external_accounts_form(self):
            return self.ExternalAccounts(self.page, self.find_element(*self._external_accounts_form_locator))

        @property
        def irc_form(self):
            return self.Irc(self.page, self.find_element(*self._irc_form_locator))

        class ExternalAccounts(Region):
            _add_account_locator = (By.ID, 'accounts-addfield')
            _account_row_locator = (By.CSS_SELECTOR, 'div.externalaccount-fieldrow')

            @property
            def is_displayed(self):
                return self.root.is_displayed()

            def count_external_accounts(self):
                return len(self.find_elements(*self._account_row_locator))

            def click_add_account(self):
                self.find_element(*self._add_account_locator).click()

        class Irc(Region):
            _irc_nickname_locator = (By.ID, 'id_ircname')
            _update_locator = (By.ID, 'form-submit-irc')

            @property
            def nickname(self):
                return self.find_element(*self._irc_nickname_locator).get_attribute('value')

            @property
            def is_displayed(self):
                return self.root.is_displayed()

            def update_nickname(self, new_nickname):
                element = self.find_element(*self._irc_nickname_locator)
                element.clear()
                element.send_keys(new_nickname)

            def click_update(self):
                el = self.find_element(*self._update_locator)
                el.click()
                self.wait.until(expected.staleness_of(el))
                self.wait.until(expected.presence_of_element_located(
                    self._update_locator))

    class DeveloperTab(Region):

        _services_bugzilla_locator = (By.ID, 'services-bugzilla-url')
        _services_mozilla_reps_locator = (By.ID, 'services-mozilla-reps')

        def get_services_urls(self):
            locs = [self._services_bugzilla_locator, self._services_mozilla_reps_locator]
            urls = []

            for element in locs:
                url = self.find_element(*element).get_attribute('href')
                urls.append(url)

            return urls
