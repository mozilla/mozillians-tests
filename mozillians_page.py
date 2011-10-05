#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Mozilla WebQA Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

from selenium import selenium
import re
import time
import base64
from page import Page

class MozilliansBasePage(Page):

    _header_locator = 'id=header'
    _profile_link_locator = 'id=profile'
    _invite_link_locator = 'id=invite'
    _join_us_link_locator = 'id=register'
    _login_link_locator = 'id=login'
    _logout_link_locator = 'id=logout'
    _search_box_locator = 'id=q'
    _search_btn_locator = 'id=quick-search-btn'
    _about_link_locator = 'css=#footer-links a[href*=about]'
    _csrf_token_locator = 'css=input[name="csrfmiddlewaretoken"]'

    def __init__(self, testsetup):
        Page.__init__(self, testsetup)
        self.sel = self.selenium
        
    @property
    def page_title(self):
        return self.sel.get_title()

    def click_invite_link(self):
        self.sel.click(self._invite_link_locator)
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansInvitePage(self.testsetup)

    def click_join_us_link(self):
        self.sel.click(self._join_us_link_locator)
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansCreateProfilePage(self.testsetup)

    def click_login_link(self):
        self.sel.click(self._login_link_locator)
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansLoginPage(self.testsetup)

    @property
    def is_login_link_present(self):
        return self.sel.is_element_present(self._login_link_locator)

    def click_logout_link(self):
        self.sel.click(self._logout_link_locator)
        self.sel.wait_for_page_to_load(self.timeout)

    @property
    def is_logout_link_present(self):
        return self.sel.is_element_present(self._logout_link_locator)

    @property
    def is_csrf_token_present(self):
        return self.sel.is_element_present(self._csrf_token_locator)

    def click_profile_link(self):
        self.sel.click(self._profile_link_locator)
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansProfilePage(self.testsetup)

    def click_about_link(self):
        self.sel.click(self._about_link_locator)
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansAboutPage(self.testsetup)

    def search_for(self, search_term):
        self.sel.type(self._search_box_locator, search_term)
        self.sel.click(self._search_btn_locator)
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansSearchPage(self.testsetup)

    @property
    def is_search_box_present(self):
        return self.sel.is_element_present(self._search_box_locator)

    def select_language(self, lang_code):
        self.sel.select(self._language_selector_locator, lang_code)
        self.sel.wait_for_page_to_load(self.timeout)


class MozilliansStartPage(MozilliansBasePage):

    _create_profile_button_locator = 'css=#call-to-action a'

    def __init__(self, testsetup):
       MozilliansBasePage.__init__(self, testsetup)
       self.sel.open('/')

    def click_create_profile_button(self):
        self.sel.click(self._create_profile_button_locator)
        self.sel.wait_for_page_to_load(self.timeout)


class MozilliansSearchPage(MozilliansBasePage):

    _result_locator = 'css=#main-content .result'

    def __init__(self, testsetup):
        MozilliansBasePage.__init__(self, testsetup)

    @property
    def results_count(self):
        return self.sel.get_css_count(self._result_locator)

    @property
    def too_many_results_message_shown(self):
        return self.sel.is_text_present("Too Many Search Results")


class MozilliansAboutPage(MozilliansBasePage):

    _privacy_section_locator = 'id=privacy'
    _get_involved_section_locator = 'id=get-involved'

    def __init__(self, testsetup):
        MozilliansBasePage.__init__(self, testsetup)

    @property
    def is_privacy_section_present(self):
        return self.sel.is_element_present(self._privacy_section_locator)

    @property
    def is_get_involved_section_present(self):
        return self.sel.is_element_present(self._get_involved_section_locator)


class MozilliansLoginPage(MozilliansBasePage):

    _username_box_locator = 'id=id_username'
    _password_box_locator = 'id=id_password'
    _log_in_button_locator = 'id=submit'
    _forgot_password_link_locator = 'css=#fyp-container a'
    _invalid_credentials_text = 'Please enter a correct username and password'

    def log_in(self, email = None, password = None):
        credentials = self.testsetup.credentials['user']

        if email is None:
            self.sel.type(self._username_box_locator, credentials['email'])
        else:
            self.sel.type(self._username_box_locator, email)

        if password is None:
            self.sel.type(self._password_box_locator, credentials['password'])
        else:
            self.sel.type(self._password_box_locator, password)

        self.sel.click(self._log_in_button_locator)
        self.sel.wait_for_page_to_load(self.timeout)

    @property
    def is_invalid_credentials_text_present(self):
        return self.sel.is_text_present(self._invalid_credentials_text)

    def click_forgot_password_link(self):
        self.sel.click(self._forgot_password_link_locator)
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansResetPasswordPage(self.testsetup)

class MozilliansResetPasswordPage(MozilliansBasePage):

    _reset_password_button_locator = 'id=submit'
    _email_field_locator = 'id=id_email'

    def __init__(self, testsetup):
        MozilliansBasePage.__init__(self, testsetup)

    @property
    def is_reset_password_button_present(self):
        return self.sel.is_element_present(self._reset_password_button_locator)

    @property
    def is_email_field_present(self):
        return self.sel.is_element_present(self._email_field_locator)

    def reset_password(self, email = None):
        credentials = self.testsetup.credentials['user']

        if email is None:
            self.sel.type(self._email_field_locator, credentials['email'])
        else:
            self.sel.type(self._email_field_locator, email)

        self.sel.click(self._reset_password_button_locator)
        self.sel.wait_for_page_to_load(self.timeout)

    @property
    def is_password_reset_sent_text_present(self):
        return self.sel.is_text_present("Password Reset Sent")

class MozilliansProfilePage(MozilliansBasePage):

    _edit_my_profile_button_locator = 'id=edit-profile'
    _name_locator = 'css=#profile-info h2'
    _irc_nickname_locator = 'css=#profile-info .nickname'
    _email_locator = 'css=#profile-info a[href*="mailto:"]'
    _vouched_by_locator = 'css=#profile-info .vouched'
    _biography_locator = 'id=bio'

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
    _cancel_link_locator = 'id=cancel'
    _update_button_locator = 'id=submit'
    _first_name_field_locator = 'id=id_first_name'
    _last_name_field_locator = 'id=id_last_name'
    _biography_field_locator = 'id=id_biography'
    _irc_nickname_field_locator = 'id=id_irc_nickname'
    _email_locator = 'css=#email-container dd'

    def click_update_button(self):
        self.sel.click(self._update_button_locator)
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansProfilePage(self.testsetup)

    def click_delete_profile_button(self):
        self.sel.click(self._delete_profile_button_locator)
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansConfirmProfileDeletePage(self.testsetup)

    def set_first_name(self, first_name):
        self.sel.type(self._first_name_field_locator, first_name)

    def set_last_name(self, last_name):
        self.sel.type(self._last_name_field_locator, last_name)

    def set_biography(self, biography):
        self.sel.type(self._biography_field_locator, biography)

    def set_irc_nickname(self, irc_nickname):
        self.sel.type(self._irc_nickname_field_locator, irc_nickname)

    @property
    def email(self):
        return self.sel.get_text(self._email_locator)

class MozilliansConfirmProfileDeletePage(MozilliansBasePage):

    _delete_button_locator = 'id=delete-action'
    _cancel_button_locator = 'id=cancel-action'
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

    _recipient_field_locator = 'id=id_recipient'
    _send_invite_button_locator = 'css=#main-content button'
    _enter_valid_email_address_text = 'Enter a valid e-mail address'

    def invite(self, email):
        self.sel.type(self._recipient_field_locator, email)
        self.sel.click(self._send_invite_button_locator)
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansInviteSuccessPage(self.testsetup)

    @property
    def is_invalid_mail_address_message_present(self):
        return self.sel.is_text_present(self._enter_valid_email_address_text)

class MozilliansInviteSuccessPage(MozilliansBasePage):

    _success_message = "Invitation Sent"
    _invite_another_mozillian_link_locator = "css=#main-content a[href*='invite']"

    def is_mail_address_present(self, address):
        return self.sel.is_text_present(address)

    @property
    def is_success_message_present(self):
        return self.sel.is_text_present(self._success_message)

    @property
    def is_invite_another_mozillian_link_present(self):
        return self.sel.is_element_present(self._invite_another_mozillian_link_locator)

class MozilliansCreateProfilePage(MozilliansBasePage):

    _email_field_locator = 'id=id_email'
    _password_field_locator = 'id=id_password'
    _confirm_password_field_locator = 'id=id_confirmp'
    _first_name_field_locator = 'id=id_first_name'
    _last_name_field_locator = 'id=id_last_name'
    _privacy_policy_checkbox_locator = 'id=id_optin'
    _create_account_button_locator = 'id=submit'
    _invalid_email_string = 'Enter a valid e-mail address'
    _non_matching_passwords_string = 'The passwords did not match'
    _email_container_locator = 'id=email-container'
    _password_container_locator = 'id=password-container'
    _confirm_password_container_locator = 'id=confirmp-container'
    _last_name_container_locator = 'id=last_name-container'
    _optin_container_locator = 'id=optin-container'
    _error_list_locator = ' .errorlist'

    def has_form_error(self, container_id):
        return self.sel.is_element_present(container_id + self._error_list_locator) and self.sel.is_element_present(container_id + ".error")

    def set_email(self, email_string):
        self.sel.type(self._email_field_locator, email_string)

    def set_password(self, password, confirmpassword=None):
        self.sel.type(self._password_field_locator, password)
        if confirmpassword is None:
            self.sel.type(self._confirm_password_field_locator, password)
        else:
            self.sel.type(self._confirm_password_field_locator, confirmpassword)

    def set_first_name(self, first_name):
        self.sel.type(self._first_name_field_locator, first_name)

    def set_last_name(self, last_name):
        self.sel.type(self._last_name_field_locator, last_name)

    def check_privacy_policy_checkbox(self):
        self.sel.check(self._privacy_policy_checkbox_locator)

    def click_create_account_button(self):
        self.sel.click(self._create_account_button_locator)
        self.sel.wait_for_page_to_load(self.timeout)

    @property
    def is_primary_email_required(self):
        return self.has_form_error(self._email_container_locator)

    @property
    def is_password_required(self):
        return self.has_form_error(self._password_container_locator)

    @property
    def is_confirm_password_required(self):
        return self.has_form_error(self._confirm_password_container_locator)

    @property
    def is_last_name_required(self):
        return self.has_form_error(self._last_name_container_locator)

    @property
    def is_optin_required(self):
        return self.has_form_error(self._optin_container_locator)

    @property
    def is_invalid_email_message_present(self):
        return self.sel.is_text_present(self._invalid_email_string)

    @property
    def is_non_matching_passwords_message_present(self):
        return self.sel.is_text_present(self._non_matching_passwords_string)
