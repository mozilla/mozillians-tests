#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

from pages.page import Page


class MozilliansBasePage(Page):

    _profile_menu_locator = (By.ID, 'profile_menu')
    _view_profile_menu_item_locator = (By.ID, 'profile')
    _settings_menu_item_locator = (By.ID, 'edit_profile')
    _invite_menu_item_locator = (By.ID, 'invite')
    _join_us_link_locator = (By.ID, 'register')  # is this needed anymore?
    _login_link_locator = (By.ID, 'create_profile')
    _logout_menu_item_locator = (By.ID, 'logout')
    _language_selector_locator = (By.ID, 'language')
    _language_selection_ok_button = (By.CSS_SELECTOR, '#language-switcher button')
    _search_box_locator = (By.NAME, 'q')
    _search_btn_locator = (By.ID, 'quick-search-btn')  # is this needed anymore?
    _about_link_locator = (By.CSS_SELECTOR, '#footer-links a:nth-child(1)')
    _csrf_token_locator = (By.NAME, 'csrfmiddlewaretoken')

    @property
    def page_title(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        return self.selenium.title

    def click_options(self):
        self.selenium.find_element(*self._profile_menu_locator).click()

    def click_invite_menu_item(self):
        self.selenium.find_element(*self._invite_menu_item_locator).click()
        return MozilliansInvitePage(self.testsetup)

    def click_browserid_link(self):
        self.selenium.find_element(*self._login_link_locator).click()
        return MozilliansLoginPage(self.testsetup)

    @property
    def is_browserid_link_present(self):
        return self.is_element_present(*self._login_link_locator)

    def click_logout_menu_item(self):
        self.click_options()
        self.selenium.find_element(*self._logout_menu_item_locator).click()

    @property
    def is_logout_menu_item_present(self):
        return self.is_element_present(*self._logout_menu_item_locator)

    @property
    def is_csrf_token_present(self):
        return self.is_element_present(*self._csrf_token_locator)

    def click_view_profile_menu_item(self):
        self.selenium.find_element(*self._view_profile_menu_item_locator).click()
        return MozilliansProfilePage(self.testsetup)

    def click_settings_menu_item(self):
        self.selenium.find_element(*self._settings_menu_item_locator).click()

    def click_about_link(self):
        self.selenium.find_element(*self._about_link_locator).click()
        return MozilliansAboutPage(self.testsetup)

    def search_for(self, search_term):
        term = self.selenium.find_element(*self._search_box_locator)
        term.send_keys(search_term)
        term.send_keys(Keys.RETURN)
        return MozilliansSearchPage(self.testsetup)

    @property
    def is_search_box_present(self):
        return self.is_element_present(*self._search_box_locator)

    def select_language(self, lang_code):
        element = self.selenium.find_element(*self._language_selector_locator)
        select = Select(element)
        select.select_by_value(lang_code)


class MozilliansStartPage(MozilliansBasePage):

    _sign_in_with_browserid_locator = (By.ID, 'create_profile')

    def __init__(self, testsetup, open_url=True):
        MozilliansBasePage.__init__(self, testsetup)
        if open_url:
            self.selenium.get(self.base_url)

    def click_create_profile_button(self):
        self.selenium.find_element(*self._sign_in_with_browserid_locator).click()


class MozilliansSearchPage(MozilliansBasePage):

    _result_locator = (By.CSS_SELECTOR, '.well .result')
    _search_button_locator = (By.CSS_SELECTOR, '.btn.primary:nth-of-type(1)')
    _advanced_options_button_locator = (By.CSS_SELECTOR, '.btn.primary:nth-of-type(2)')
    _advanced_options_locator = (By.CSS_SELECTOR, '.search-options')
    _non_vouched_only_checkbox_locator = (By.ID, 'id_nonvouched_only')
    _with_photos_only_checkbox_locator = (By.ID, 'id_picture_only')
    _no_results_locator = (By.ID, 'not-found')

    @property
    def results_count(self):
        return len(self.selenium.find_elements(*self._result_locator))

    @property
    def no_results_message_shown(self):
        return "The Mozillian you are looking for is not in the directory" in self.selenium.find_element(*self._no_results_locator).text

    def search_for(self, search_term):
        element = self.selenium.find_element(*self._search_box_locator)
        element.send_keys(search_term)
        self.selenium.find_element(*self._search_button_locator).click()

    def toggle_advanced_options(self):
        self.selenium.find_element(*self._advanced_options_button_locator).click()

    @property
    def advanced_options_shown(self):
        return self.is_element_visible(*self._advanced_options_locator)

    def check_non_vouched_only(self):
        self.selenium.find_element(*self._non_vouched_only_checkbox_locator).click()

    def check_with_photos_only(self):
        self.selenium.find_elemennt(*self._with_photos_only_checkbox_locator).click()


class MozilliansAboutPage(MozilliansBasePage):

    _privacy_section_locator = (By.ID, 'privacy')
    _get_involved_section_locator = (By.ID, 'get-involved')

    @property
    def is_privacy_section_present(self):
        return self.is_element_present(*self._privacy_section_locator)

    @property
    def is_get_involved_section_present(self):
        return self.is_element_present(*self._get_involved_section_locator)


class MozilliansLoginPage(MozilliansBasePage):

    def login(self, user='user'):
        credentials = self.testsetup.credentials[user]
        from browserid import BrowserID
        pop_up = BrowserID(self.selenium, self.timeout)
        pop_up.sign_in(credentials['email'], credentials['password'])
        WebDriverWait(self.selenium, 20).until(lambda s: s.find_element(*self._logout_locator))


class MozilliansProfilePage(MozilliansBasePage):

    _edit_my_profile_button_locator = (By.ID, 'edit-profile')
    _name_locator = (By.CSS_SELECTOR, '#profile-info h2')
    _email_locator = (By.CSS_SELECTOR, '#profile-info a[href^="mailto:"]')
    _username_locator = (By.CSS_SELECTOR, '#profile-info dd:nth-of-type(2)')
    _website_locator = (By.CSS_SELECTOR, '#profile-info > dl > dd > a[href^="http"]')
    _vouched_by_locator = (By.CSS_SELECTOR, '#profile-info .vouched')
    _biography_locator = (By.ID, 'bio')

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

    def click_edit_my_profile_button(self):
        self.selenium.find_element(*self._edit_my_profile_button_locator).click()
        return MozilliansEditProfilePage(self.testsetup)


class MozilliansEditProfilePage(MozilliansBasePage):

    _cancel_button_locator = (By.CSS_SELECTOR, "#edit_controls a")
    _update_button_locator = (By.CSS_SELECTOR, "#edit_controls button")

    #edit your profile tabs locators
    _profile_tab_locator = (By.CSS_SELECTOR, '.nav.nav-tabs > li:nth-of-type(1) > a')
    _skills_tab_locator = (By.CSS_SELECTOR, '.nav.nav-tabs > li:nth-of-type(2) > a')
    _vouches_tab_locator = (By.CSS_SELECTOR, '.nav.nav-tabs > li:nth-of-type(3) > a')
    _account_tab_locator = (By.CSS_SELECTOR, '.nav.nav-tabs > li:nth-of-type(4) > a')

    def click_update_button(self):
        self.selenium.find_element(*self._update_button_locator).click()
        return MozilliansProfilePage(self.testsetup)

    def click_cancel_button(self):
        self.selenium.find_element(*self._cancel_button_locator).click()

    def go_to_tab(self, tab_name):
        if tab_name is "profile":
            self.selenium.find_element(*self._profile_tab_locator).click()
            return self.ProfileTab(self)
        elif tab_name is "skills":
            self.sel.find_element(*self._skills_tab_locator).click()
            return self.SkillsAndGroupsTab(self)
        elif tab_name is "vouches":
            self.sel.find_element(*self._vouches_tab_locator).click()
            return self.VouchesAndInvitesTab(self)
        elif tab_name is "account":
            self.sel.find_element(*self._account_tab_locator).click()
            return self.AccountTab(self)

    class ProfileTab(MozilliansBasePage):

        _first_name_field_locator = (By.ID, 'id_first_name')
        _last_name_field_locator = (By.ID, 'id_last_name')
        _website_field_locator = (By.ID, 'id_website')
        _bio_field_locator = (By.ID, 'id_bio')

        def set_first_name(self, first_name):
            element = self.selenium.find_element(*self._first_name_field_locator)
            element.send_keys(first_name)

        def set_last_name(self, last_name):
            element = self.selenium.find_element(*self._last_name_field_locator)
            element.send_keys(last_name)

        def set_website(self, website):
            element = self.selenium.find_element(*self._website_field_locator)
            element.send_keys(website)

        def set_bio(self, biography):
            element = self.selenium.send_keys(*self._bio_field_locator)
            element.send_keys(biography)

    class SkillsAndGroupsTab(MozilliansBasePage):

        _groups_field_locator = (By.CSS_SELECTOR, '#id_groups + ul input')
        _skills_field_locator = (By.CSS_SELECTOR, '#id_skills + ul input')

        def add_group(self, group_name):
            element = self.selenium.find_element(*self._group_field_locator)
            element.send_keys(group_name)

        def add_skill(self, skill_name):
            element = self.selenium.send_keys(*self._skill_field_locator)
            element.send_keys(skill_name)

    class VouchesAndInvitesTab(MozilliansBasePage):

        _voucher_name_locator = (By.CSS_SELECTOR, '#vouches .vouched')

        @property
        def vouched_by(self):
            return self.selenium.find_element(*self._voucher_name_locator).text

    class AccountTab(MozilliansBasePage):

        _username_field_locator = (By.ID, 'id_username')
        _browserid_mail_locator = (By.CSS_SELECTOR, '.control-group:nth-of-type(2) .label-text')
        _delete_profile_button_locator = (By.CSS_SELECTOR, '.btn.btn-danger')
        _browserid_link_locator = (By.CSS_SELECTOR, 'a[href*=browserid]')

        @property
        def username(self):
            return self.selenium.find_element(*self._username_field_locator).text

        @property
        def browserid_email(self):
            return self.selenium.find_element(*self._browserid_mail_locator).text

        def click_delete_profile_button(self):
            self.selenium.find_element(*self._delete_profile_button_locator).click()
            return MozilliansConfirmProfileDeletePage(self.testsetup)

        @property
        def is_browserid_link_present(self):
            return self.is_element_present(*self._browserid_link_locator)


class MozilliansConfirmProfileDeletePage(MozilliansBasePage):

    _delete_button_locator = (By.ID, 'delete-action')
    _cancel_button_locator = (By.ID, 'cancel-action')
    _confirm_profile_delete_text_locator = (By.CSS_SELECTOR, '#main > h1')

    @property
    def is_confirm_text_present(self):
        return self.is_element_visible(*self._confirm_profile_delete_text)

    @property
    def is_delete_button_present(self):
        return self.is_element_present(*self._delete_button_locator)

    @property
    def is_cancel_button_present(self):
        return self.is_element_present(*self._cancel_button_locator)


class MozilliansInvitePage(MozilliansBasePage):

    _recipient_field_locator = (By.ID, 'id_recipient')
    _send_invite_button_locator = (By.CSS_SELECTOR, '#main button')
    _error_text_locator = (By.CSS_SELECTOR, '.errorlist > li')

    def invite(self, email):
        input_field = self.selenium.find_element(*self._recipient_field_locator)
        input_field.send_keys(email)
        self.selenium.find_element(*self._send_invite_button_locator).click()
        return MozilliansInviteSuccessPage(self.testsetup)

    @property
    def error_text_message(self):
        return self.selenium.find_element(*self._error_text_locator).text


class MozilliansInviteSuccessPage(MozilliansBasePage):

    _success_message_locator = (By.CSS_SELECTOR, '#main > h1')
    _invite_another_mozillian_link_locator = (By.CSS_SELECTOR, '#main > p > a')

    def is_mail_address_present(self, address):
        return self.sel.is_text_present(address)

    @property
    def is_success_message_present(self):
        return 'Invitation Sent!' in self.selenium.find_element(*self._success_message).text

    @property
    def is_invite_another_mozillian_link_present(self):
        return self.is_element_present(*self._invite_another_mozillian_link_locator)
