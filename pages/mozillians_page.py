#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page


class MozilliansBasePage(Page):

    _header_locator = (By.ID, 'header')
    _view_profile_menu_item_locator = (By.ID, 'profile')
    _invite_link_locator = (By.ID, 'invite')
    _join_us_link_locator = (By.ID, 'register')
    _login_link_locator = (By.CSS_SELECTOR,'#create_profile .signin')
    _logout_menu_item_locator = (By.ID, 'logout')
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

    def click_invite_link(self):
        self.sel.find_element(*self._invite_link_locator).click()
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansInvitePage(self.testsetup)

    def click_login_link(self):
        self.sel.find_element(*self._login_link_locator).click()
        return MozilliansLoginPage(self.testsetup)

    @property
    def is_login_link_present(self):
        return self.sel.is_element_present(self._login_link_locator)

    def click_logout_menu_item(self):
        self.sel.find_element(*self._logout_menu_item_locator).click()
        self.sel.wait_for_page_to_load(self.timeout)

    @property
    def is_logout_menu_item_present(self):
        return self.is_element_present(*self._logout_menu_item_locator)

    @property
    def is_csrf_token_present(self):
        return self.is_element_present(*self._csrf_token_locator)

    def click_view_profile_item(self):
        self.sel.find_element(*self._view_profile_menu_item_locator).click()
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansProfilePage(self.testsetup)

    def click_about_link(self):
        self.sel.find_element(*self._about_link_locator).click()
        return MozilliansAboutPage(self.testsetup)

    def search_for(self, search_term):
        self.sel.type(self._search_box_locator, search_term)
        self.sel.click(self._search_btn_locator)
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansSearchPage(self.testsetup)

    @property
    def is_search_box_present(self):
        return self.sel.is_element_present(*self._search_box_locator)

    def select_language(self, lang_code):
        self.sel.select(self._language_selector_locator, lang_code)
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

    def __init__(self, testsetup):
        MozilliansBasePage.__init__(self, testsetup)

    @property
    def results_count(self):
        return self.sel.get_css_count(*self._result_locator)

    @property
    def too_many_results_message_shown(self):
        return self.sel.is_text_present("Too Many Search Results")


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
        return self.sel.get_text(self._name_locator).strip()

    @property
    def biography(self):
        return self.sel.get_text(self._biography_locator).strip()

    @property
    def email(self):
        return self.sel.get_text(self._email_locator).strip()

    @property
    def vouched_by(self):
        return self.sel.get_text(self._vouched_by_locator).strip()

    def click_edit_my_profile_button(self):
        self.sel.click(self._edit_my_profile_button_locator)
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansEditProfilePage(self.testsetup)


class MozilliansEditProfilePage(MozilliansBasePage):

    _delete_profile_button_locator = 'id=delete-profile'
    _cancel_button_locator = (By.CSS_SELECTOR, "#edit_controls a")
    _update_button_locator = (By.CSS_SELECTOR, "#edit_controls button")
    _first_name_field_locator = (By.ID, 'id_first_name')
    _last_name_field_locator = (By.ID, 'id_last_name')
    _website_field_locator = (By.ID, 'id_website')
    _bio_field_locator = (By.ID, 'id_bio')

    def click_update_button(self):
        self.sel.find_element(*self._update_button_locator).click()
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansProfilePage(self.testsetup)

    def click_delete_profile_button(self):
        self.sel.find_element(*self._delete_profile_button_locator).click()
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansConfirmProfileDeletePage(self.testsetup)

    def set_first_name(self, first_name):
        self.sel.type(self._first_name_field_locator, first_name)

    def set_last_name(self, last_name):
        self.sel.type(self._last_name_field_locator, last_name)

    def set_bio(self, biography):
        self.sel.type(self._bio_field_locator, biography)

    def set_irc_nickname(self, irc_nickname):
        self.sel.type(self._irc_nickname_field_locator, irc_nickname)

    @property
    def email(self):
        return self.sel.get_text(self._email_locator)


class MozilliansConfirmProfileDeletePage(MozilliansBasePage):

    _delete_button_locator = (By.ID, 'delete-action')
    _cancel_button_locator = (By.ID, 'cancel-action')
    _confirm_profile_delete_text = 'Confirm Profile Deletion'

    @property
    def is_confirm_text_present(self):
        return self.sel.is_text_present(self._confirm_profile_delete_text)

    @property
    def is_delete_button_present(self):
        return self.sel.is_element_present(self._delete_button_locator)

    @property
    def is_cancel_button_present(self):
        return self.sel.is_element_present(self._cancel_button_locator)


class MozilliansInvitePage(MozilliansBasePage):

    _recipient_field_locator = (By.ID, 'id_recipient')
    _send_invite_button_locator = (By.CSS_SELECTOR, '#main button')
    _enter_valid_email_address_text = 'Enter a valid e-mail address'
    _field_is_required_text = 'This field is required'

    def invite(self, email):
        self.sel.type(self._recipient_field_locator, email)
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
        return self.sel.is_element_present(self._invite_another_mozillian_link_locator)

