#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page


class MozilliansBasePage(Page):

    _profile_menu_locator = (By.CSS_SELECTOR, '#profile_menu a')
    _view_profile_menu_item_locator = (By.ID, 'profile')
    _settings_menu_item_locator = (By.ID, 'edit-profile')
    _invite_menu_item_locator = (By.ID, 'invite')
    _join_us_link_locator = (By.ID, 'register')
    _login_link_locator = (By.CSS_SELECTOR,'#create_profile .signin')
    _logout_menu_item_locator = (By.ID, 'logout')
    _language_selector_locator = (By.ID, 'language')
    _language_selection_ok_button = (By.CSS_SELECTOR, '#language-switcher button')
    _search_box_locator = (By.NAME, 'q')
    _search_btn_locator = (By.ID, 'quick-search-btn')
    _about_link_locator = (By.CSS_SELECTOR, '#footer-links a[href*=about]:nth-child(1)')
    _csrf_token_locator = (By.NAME, 'csrfmiddlewaretoken')

    def __init__(self, testsetup):
        Page.__init__(self, testsetup)
        self.sel = self.selenium

    @property
    def page_title(self):
        return self.sel.get_title()

    def open_profile_menu(self):
        self.sel.find_element(*self._profile_menu_locator).click()

    def click_invite_menu_item(self):
        self.sel.find_element(*self._invite_menu_item_locator).click()
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansInvitePage(self.testsetup)

    def click_login_link(self):
        self.sel.find_element(*self._login_link_locator).click()
        return MozilliansLoginPage(self.testsetup)

    @property
    def is_login_link_present(self):
        return self.sel.is_element_present(*self._login_link_locator)

    def click_logout_menu_item(self):
        self.sel.find_element(*self._logout_menu_item_locator).click()
        self.sel.wait_for_page_to_load(self.timeout)

    @property
    def is_logout_menu_item_present(self):
        return self.is_element_present(*self._logout_menu_item_locator)

    @property
    def is_csrf_token_present(self):
        return self.is_element_present(*self._csrf_token_locator)

    def click_view_profile_menu_item(self):
        self.sel.find_element(*self._view_profile_menu_item_locator).click()
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansProfilePage(self.testsetup)

    def click_settings_menu_item(self):
        self.sel.find_element(*self._settings_menu_item_locator).click()

    def click_about_link(self):
        self.sel.find_element(*self._about_link_locator).click()
        return MozilliansAboutPage(self.testsetup)

    def search_for(self, search_term):
        self.sel.type(*self._search_box_locator, search_term)
        self.sel.type_keys(*self._search_box_locator, "\13")
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansSearchPage(self.testsetup)

    @property
    def is_search_box_present(self):
        return self.sel.is_element_present(*self._search_box_locator)

    def select_language(self, lang_code):
        self.sel.select(*self._language_selector_locator, lang_code)
        self.sel.find_element(*self._language_selection_ok_button).click()
        self.sel.wait_for_page_to_load(self.timeout)


class MozilliansStartPage(MozilliansBasePage):

    _create_profile_button_locator = 'css=.browserid-register'

    def __init__(self, testsetup, open_url=True):
        MozilliansBasePage.__init__(self, testsetup)
        if open_url:
            self.sel.get(self.base_url)

    def click_create_profile_button(self):
        self.sel.click(self._create_profile_button_locator)
        self.sel.wait_for_page_to_load(self.timeout)


class MozilliansSearchPage(MozilliansBasePage):

    _result_locator = (By.CSS_SELECTOR, '#main .result')
    _search_button_locator = (By.CSS_SELECTOR, '#search-form .primary')
    _advanced_options_button_locator = (By.ID, 'advanced')
    _advanced_options_locator = (By.CSS_SELECTOR, 'search-options')
    _non_vouched_only_checkbox_locator = (By.ID, 'id_nonvouched_only')
    _with_photos_only_checkbox_locator = (By.ID, 'id_picture_only')

    def __init__(self, testsetup):
        MozilliansBasePage.__init__(self, testsetup)

    @property
    def results_count(self):
        return self.sel.get_css_count(*self._result_locator)

    @property
    def no_results_message_shown(self):
        return self.sel.is_text_present("The Mozillian you are looking for is not in the directory")

    @property
    def too_many_results_message_shown(self):
        return self.sel.is_text_present("Too Many Search Results")

    def search_for(self, search_term):
        self.sel.type(*self._search_box_locator, search_term)
        self.sel.find_element(*self._search_button_locator, search_term)
        self.sel.wait_for_page_to_load(self.timeout)

    def toggle_advanced_options(self):
        self.sel.find_element(*self._advanced_options_button_locator).click()

    @property
    def advanced_options_shown(self):
        return self.sel.is_visible(*self._advanced_options_locator)

    def check_non_vouched_only(self):
        self.sel.check(*self._non_vouched_only_checkbox_locator)

    def check_with_photos_only(self):
        self.sel.check(*self._with_photos_only_checkbox_locator)


class MozilliansAboutPage(MozilliansBasePage):

    _privacy_section_locator = (By.ID, "privacy")
    _get_involved_section_locator = (By.ID, "get-involved")

    def __init__(self, testsetup):
        MozilliansBasePage.__init__(self, testsetup)

    @property
    def is_privacy_section_present(self):
        return self.is_element_present(*self._privacy_section_locator)

    @property
    def is_get_involved_section_present(self):
        return self.is_element_present(*self._get_involved_section_locator)


class MozilliansLoginPage(MozilliansBasePage):

    def log_in(self, user='user'):
        credentials = self.testsetup.credentials[user]
        from browserid import BrowserID
        browserid = BrowserID(self.selenium, self.timeout)
        browserid.sign_in(credentials['email'], credentials['password'])
        self.wait_for_element_present(*self._logout_menu_item_locator)

class MozilliansProfilePage(MozilliansBasePage):

    _edit_my_profile_button_locator = (By.ID, 'edit-profile')
    _name_locator = (By.CSS_SELECTOR, '#profile-info h2')
    _email_locator = (By.CSS_SELECTOR, '#profile-info a[href^="mailto:"]')
    _username_locator = (By.CSS_SELECTOR, '#profile-info dd:nth-child(2)')
    _website_locator = (By.CSS_SELECTOR, '#profile-info dd:nth-child(3) > a')
    _vouched_by_locator = (By.CSS_SELECTOR, '#profile-info .vouched')
    _biography_locator = (By.ID, 'bio')

    @property
    def name(self):
        return self.sel.get_text(*self._name_locator).strip()

    @property
    def biography(self):
        return self.sel.get_text(*self._biography_locator).strip()

    @property
    def email(self):
        return self.sel.get_text(*self._email_locator).strip()

    @property
    def website(self):
        return self.sel.get_text(*self._website_locator).strip()

    @property
    def vouched_by(self):
        return self.sel.get_text(*self._vouched_by_locator).strip()

    def click_edit_my_profile_button(self):
        self.sel.click(*self._edit_my_profile_button_locator)
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansEditProfilePage(self.testsetup)


class MozilliansEditProfilePage(MozilliansBasePage):

    _cancel_button_locator = (By.CSS_SELECTOR, "#edit_controls a")
    _update_button_locator = (By.CSS_SELECTOR, "#edit_controls button")

    def click_update_button(self):
        self.sel.find_element(*self._update_button_locator).click()
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansProfilePage(self.testsetup)

    def click_cancel_button(self):
        self.sel.find_element(*self._cancel_button_locator).click()

    def go_to_tab(self, tab_name):
        if tab_name is "profile":
            self.sel.find_element(*self._profile_tab).click()
            return self.ProfileTab(self)
        else if tab_name is "skills":
            self.sel.find_element(*self._skills_tab).click()
            return self.SkillsAndGroupsTab(self)
        else if tab_name is "vouches":
            self.sel.find_element(*self._vouches_tab).click()
            return self.VouchesAndInvitesTab(self)
        else if tab_name is "account":
            self.sel.find_element(*self._account_tab).click()
            return self.AccountTab(self)

    class ProfileTab(MozilliansEditProfilePage):

        _first_name_field_locator = (By.ID, 'id_first_name')
        _last_name_field_locator = (By.ID, 'id_last_name')
        _website_field_locator = (By.ID, 'id_website')
        _bio_field_locator = (By.ID, 'id_bio')

        def set_first_name(self, first_name):
            self.sel.type(*self._first_name_field_locator, first_name)

        def set_last_name(self, last_name):
            self.sel.type(*self._last_name_field_locator, last_name)

        def set_bio(self, biography):
            self.sel.type(*self._bio_field_locator, biography)

        def set_irc_nickname(self, irc_nickname):
            self.sel.type(*self._irc_nickname_field_locator, irc_nickname)

    class SkillsAndGroupsTab(MozilliansEditProfilePage):

        _group_field_locator = (By.CSS_SELECTOR, 'ul.tagit:nth-child(1) input')
        _skill_field_locator = (By.CSS_SELECTOR, 'ul.tagit:nth-child(2) input')

        def add_group(self, group_name):
            self.sel.type(*self._group_field_locator, group_name)

        def add_skill(self, skill_name):
            self.sel.type(*self._skill_field_locator, skill_name)

    class VouchesAndInvitesTab(MozilliansEditProfilePage):

        _voucher_name_locator = (By.CSS_SELECTOR, '#vouches .vouched')

        @property
        def vouched_by(self):
            return self.sel.get_text(*self._voucher_name_locator).strip()

    class AccountTab(MozilliansEditProfilePage):

        _username_field_locator = (By.ID, 'id_username')
        _browserid_mail_locator = (By.CSS_SELECTOR, '.control-group:nth-of-type(2) .label-text')
        _delete_profile_button_locator = (By.ID, 'delete-profile')
        _browserid_link_locator = (By.CSS_SELECTOR, 'a[href*=browserid]')

        @property
        def username(self):
            return self.sel.get_text(self._username_field_locator)

        @property
        def browserid_email(self):
            return self.sel.get_text(self._browserid_mail_locator).strip()

        def click_delete_profile_button(self):
            self.sel.find_element(*self._delete_profile_button_locator).click()
            self.sel.wait_for_page_to_load(self.timeout)
            return MozilliansConfirmProfileDeletePage(self.testsetup)

        @property
        def is_browserid_link_present(self):
            return self.sel.is_element_present(*self._browserid_link_locator)

class MozilliansConfirmProfileDeletePage(MozilliansBasePage):

    _delete_button_locator = (By.ID, 'delete-action')
    _cancel_button_locator = (By.ID, 'cancel-action')
    _confirm_profile_delete_text = 'Confirm Profile Deletion'

    @property
    def is_confirm_text_present(self):
        return self.sel.is_text_present(self._confirm_profile_delete_text)

    @property
    def is_delete_button_present(self):
        return self.sel.is_element_present(*self._delete_button_locator)

    @property
    def is_cancel_button_present(self):
        return self.sel.is_element_present(*self._cancel_button_locator)


class MozilliansInvitePage(MozilliansBasePage):

    _recipient_field_locator = (By.ID, 'id_recipient')
    _send_invite_button_locator = (By.CSS_SELECTOR, '#main button')
    _enter_valid_email_address_text = 'Enter a valid e-mail address'
    _field_is_required_text = 'This field is required'

    def invite(self, email):
        self.sel.type(*self._recipient_field_locator, email)
        self.sel.find_element(*self._send_invite_button_locator).click()
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansInviteSuccessPage(self.testsetup)

    @property
    def is_invalid_mail_address_message_present(self):
        return self.sel.is_text_present(self._enter_valid_email_address_text)

    @property
    def is_this_field_is_required_message_present(self):
        return self.sel.is_text_present(self._field_is_required_text)


class MozilliansInviteSuccessPage(MozilliansBasePage):

    _success_message = "Invitation Sent"
    _invite_another_mozillian_link_locator = (By.CSS_SELECTOR, "#main a[href*='invite']")

    def is_mail_address_present(self, address):
        return self.sel.is_text_present(address)

    @property
    def is_success_message_present(self):
        return self.sel.is_text_present(self._success_message)

    @property
    def is_invite_another_mozillian_link_present(self):
        return self.sel.is_element_present(*self._invite_another_mozillian_link_locator)

