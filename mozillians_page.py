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
# The Original Code is Crash Tests Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2010
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
    _login_link_locator = 'id=login'
    _logout_link_locator = 'id=logout'
    _search_box_locator = 'id=q'
    _search_btn_locator = 'id=quick-search-btn'
    _about_link_locator = 'css=#footer-links a[href*=about]'

    def __init__(self, testsetup):
        Page.__init__(self, testsetup)
        self.sel = self.selenium
        
    @property
    def page_title(self):
        return self.sel.get_title()

    def click_login_link(self):
        self.sel.click(self._login_link_locator)
        self.sel.wait_for_page_to_load(self.timeout)
        return MozilliansLoginPage(self.testsetup)

    def click_logout_link(self):
        self.sel.click(self._logout_link_locator)
        self.sel.wait_for_page_to_load(self.timeout)

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

    def log_in(self):
        credentials = self.testsetup.credentials['user']

        self.sel.type(self._username_box_locator, credentials['name'])
        self.sel.type(self._password_box_locator, credentials['password'])
        self.sel.click(self._log_in_button_locator)
        self.sel.wait_for_page_to_load(self.timeout)
