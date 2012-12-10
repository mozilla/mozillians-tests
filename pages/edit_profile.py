#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.base import Base
from pages.profile import Profile


class EditProfile(Base):

    _cancel_button_locator = (By.CSS_SELECTOR, "#edit_controls a")
    _update_button_locator = (By.CSS_SELECTOR, "#edit_controls button")

    #edit your profile tabs locators
    _profile_tab_locator = (By.CSS_SELECTOR, 'div.tabbable > ul.nav > li:nth-of-type(1) > a')
    _skills_tab_locator = (By.CSS_SELECTOR, 'div.tabbable > ul.nav > li:nth-of-type(2) > a')
    _vouches_tab_locator = (By.CSS_SELECTOR, 'div.tabbable > ul.nav > li:nth-of-type(3) > a')
    _account_tab_locator = (By.CSS_SELECTOR, 'div.tabbable > ul.nav > li:nth-of-type(4) > a')

    def click_update_button(self):
        self.selenium.find_element(*self._update_button_locator).click()
        return Profile(self.testsetup)

    def click_cancel_button(self):
        self.selenium.find_element(*self._cancel_button_locator).click()

    def go_to_tab(self, tab_name):
        if tab_name is "profile":
            self.selenium.find_element(*self._profile_tab_locator).click()
            return ProfileTab(self.testsetup)
        elif tab_name is "skills":
            self.selenium.find_element(*self._skills_tab_locator).click()
            return SkillsAndGroupsTab(self.testsetup)
        elif tab_name is "vouches":
            self.selenium.find_element(*self._vouches_tab_locator).click()
            return VouchesAndInvitesTab(self.testsetup)
        elif tab_name is "account":
            self.selenium.find_element(*self._account_tab_locator).click()
            return AccountTab(self.testsetup)


class ProfileTab(EditProfile):

    _full_name_field_locator = (By.ID, 'id_full_name')
    _website_field_locator = (By.ID, 'id_website')
    _bio_field_locator = (By.ID, 'id_bio')

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


class SkillsAndGroupsTab(EditProfile):

    _groups_field_locator = (By.CSS_SELECTOR, '#id_groups + ul input')
    _skills_field_locator = (By.CSS_SELECTOR, '#id_skills + ul input')

    def add_group(self, group_name):
        element = self.selenium.find_element(*self._group_field_locator)
        element.send_keys(group_name)

    def add_skill(self, skill_name):
        element = self.selenium.send_keys(*self._skill_field_locator)
        element.send_keys(skill_name)


class VouchesAndInvitesTab(EditProfile):

    _voucher_name_locator = (By.CSS_SELECTOR, '#vouches .vouched')

    @property
    def vouched_by(self):
        return self.selenium.find_element(*self._voucher_name_locator).text


class AccountTab(EditProfile):

    _username_field_locator = (By.ID, 'id_username')
    _browserid_mail_locator = (By.CSS_SELECTOR, '.control-group:nth-of-type(2) .label-text')
    _delete_profile_button_locator = (By.CSS_SELECTOR, '.btn.btn-danger')
    _browserid_link_locator = (By.CSS_SELECTOR, '#account div.controls > span > a')

    @property
    def username(self):
        return self.selenium.find_element(*self._username_field_locator).text

    @property
    def browserid_email(self):
        return self.selenium.find_element(*self._browserid_mail_locator).text

    @property
    def is_browserid_link_present(self):
        return self.is_element_present(*self._browserid_link_locator)

    def click_delete_profile_button(self):
        self.selenium.find_element(*self._delete_profile_button_locator).click()
        from pages.confirm_profile_delete import ConfirmProfileDelete
        return ConfirmProfileDelete(self.testsetup)
