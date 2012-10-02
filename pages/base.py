#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page


class Base(Page):

    _csrf_token_locator = (By.NAME, 'csrfmiddlewaretoken')
    _logged_in_marker_locator = (By.CSS_SELECTOR, "body[class~='auth']")

    _pending_approval_locator = (By.ID, 'pending-approval')
    _account_created_successfully_locator = (By.CSS_SELECTOR, 'div.alert:nth-child(2)')

    # Not logged in
    _browserid_login_locator = (By.CSS_SELECTOR, 'a.browser_id_login > img')

    @property
    def page_title(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        return self.selenium.title

    @property
    def is_csrf_token_present(self):
        return self.is_element_present(*self._csrf_token_locator)

    @property
    def is_pending_approval_visible(self):
        return self.is_element_visible(*self._pending_approval_locator)

    @property
    def was_account_created_successfully(self):
        return self.is_element_visible(*self._account_created_successfully_locator)

    #Not logged in
    def click_browserid_login(self):
        self.selenium.find_element(*self._browserid_login_locator).click()

    @property
    def is_browserid_link_present(self):
        return self.is_element_present(*self._browserid_login_locator)

    @property
    def is_user_loggedin(self):
        return self.is_element_present(*self._logged_in_marker_locator)

    def login(self, user='user'):
        self.click_browserid_login()
        credentials = self.testsetup.credentials[user]

        from browserid import BrowserID
        pop_up = BrowserID(self.selenium, self.timeout)
        pop_up.sign_in(credentials['email'], credentials['password'])
        WebDriverWait(self.selenium, 20).until(lambda s: self.is_user_loggedin)

    def create_new_user(self, user):
        self.click_browserid_login()
        from browserid import BrowserID
        pop_up = BrowserID(self.selenium, self.timeout)
        pop_up.sign_in(user['email'], user['password'])

        WebDriverWait(self.selenium, 20).until(lambda s: self.is_user_loggedin)
        from pages.register import ProfileTab
        return ProfileTab(self.testsetup)

    #Logged in

    @property
    def header(self):
        return self.Header(self.testsetup)

    @property
    def footer(self):
        return self.Footer(self.testsetup)

    class Header(Page):

        _search_box_locator = (By.NAME, 'q')
        _profile_menu_locator = (By.CSS_SELECTOR, '#profile_menu > a.dropdown-toggle')

        #menu items
        _dropdown_menu_locator = (By.CSS_SELECTOR, 'ul.dropdown-menu')
        _view_profile_menu_item_locator = (By.ID, 'profile')
        _invite_menu_item_locator = (By.ID, 'invite')
        _settings_menu_item_locator = (By.ID, 'edit_profile')
        _logout_menu_item_locator = (By.ID, 'logout')

        @property
        def is_search_box_present(self):
            return self.is_element_present(*self._search_box_locator)

        def search_for(self, search_term):
            term = self.selenium.find_element(*self._search_box_locator)
            term.send_keys(search_term)
            term.send_keys(Keys.RETURN)
            from pages.search import Search
            return Search(self.testsetup)

        def click_options(self):
            self.selenium.find_element(*self._profile_menu_locator).click()
            WebDriverWait(self.selenium, self.timeout).until(lambda s: self.selenium.find_element(*self._dropdown_menu_locator))

        #menu items
        def click_view_profile_menu_item(self):
            self.click_options()
            self.selenium.find_element(*self._view_profile_menu_item_locator).click()
            from pages.profile import Profile
            return Profile(self.testsetup)

        def click_invite_menu_item(self):
            self.click_options()
            self.selenium.find_element(*self._invite_menu_item_locator).click()
            from pages.invite import Invite
            return Invite(self.testsetup)

        def click_settings_menu_item(self):
            self.click_options()
            self.selenium.find_element(*self._settings_menu_item_locator).click()

        def click_logout_menu_item(self):
            self.click_options()
            self.selenium.find_element(*self._logout_menu_item_locator).click()

        @property
        def is_logout_menu_item_present(self):
            return self.is_element_present(*self._logout_menu_item_locator)

    class Footer(Page):

        _about_mozillians_link_locator = (By.CSS_SELECTOR, '#footer-links a:nth-child(1)')
        _language_selector_locator = (By.ID, 'language')
        _language_selection_ok_button = (By.CSS_SELECTOR, '#language-switcher button')

        def click_about_link(self):
            self.selenium.find_element(*self._about_mozillians_link_locator).click()
            from pages.about import About
            return About(self.testsetup)

        def select_language(self, lang_code):
            element = self.selenium.find_element(*self._language_selector_locator)
            select = Select(element)
            select.select_by_value(lang_code)
