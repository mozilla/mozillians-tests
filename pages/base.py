# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Page
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.select import Select

from pages.auth0 import Auth0
from tests import conftest


class Base(Page):
    URL_TEMPLATE = '/{locale}'

    _logout_locator = (By.ID, 'nav-logout')

    _pending_approval_locator = (By.ID, 'pending-approval')
    _account_created_successfully_locator = (By.CSS_SELECTOR, 'div.alert:nth-child(2)')

    # Not logged in
    _sign_in_button_locator = (By.ID, 'nav-login')

    def __init__(self, selenium, base_url, locale='en-US', **url_kwargs):
        super(Base, self).__init__(selenium, base_url, locale=locale, **url_kwargs)

    @property
    def page_title(self):
        return self.wait.until(lambda s: self.selenium.title)

    @property
    def is_pending_approval_visible(self):
        return self.is_element_displayed(*self._pending_approval_locator)

    @property
    def was_account_created_successfully(self):
        return self.is_element_displayed(*self._account_created_successfully_locator)

    # Not logged in

    @property
    def is_sign_in_button_present(self):
        return self.is_element_present(*self._sign_in_button_locator)

    @property
    def is_user_loggedin(self):
        return self.is_element_present(*self._logout_locator)

    def click_sign_in_button(self):
        self.find_element(*self._sign_in_button_locator).click()

    def login(self, email):
        self.click_sign_in_button()
        auth0 = Auth0(self.selenium, self.base_url)
        auth0.request_login_link(email)
        login_link = conftest.login_link(email)
        self.selenium.get(login_link)
        self.wait.until(lambda s: self.is_user_loggedin)

    def login_with_github(self, username, password, secret):
        self.click_sign_in_button()
        auth0 = Auth0(self.selenium, self.base_url)
        github = auth0.click_login_with_github()
        github.login_with_github(username, password, secret)

    def create_new_user(self, email):
        self.login(email)
        from pages.register import Register
        return Register(self.selenium, self.base_url).wait_for_page_to_load()

    @property
    def header(self):
        return self.Header(self.selenium, self.base_url)

    @property
    def footer(self):
        return self.Footer(self.selenium, self.base_url)

    class Header(Page):

        _search_box_locator = (By.CSS_SELECTOR, '.search-query')
        _search_box_loggedin_locator = (By.CSS_SELECTOR, '.search-right > form > .search-query')
        _profile_menu_locator = (By.CSS_SELECTOR, '#nav-main > a.dropdown-toggle i')

        # menu items
        _dropdown_menu_locator = (By.CSS_SELECTOR, 'ul.dropdown-menu')
        _view_profile_menu_item_locator = (By.ID, 'nav-profile')
        _groups_menu_item_locator = (By.ID, 'nav-groups')
        _invite_menu_item_locator = (By.ID, 'nav-invite')
        _settings_menu_item_locator = (By.ID, 'nav-edit-profile')
        _logout_menu_item_locator = (By.ID, 'nav-logout')

        @property
        def is_search_box_present(self):
            return self.is_element_present(*self._search_box_locator)

        def search_for(self, search_term, loggedin=False):
            if loggedin:
                search_field = self.find_element(*self._search_box_loggedin_locator)
            else:
                search_field = self.find_element(*self._search_box_locator)
            search_field.send_keys(search_term)
            search_field.send_keys(Keys.RETURN)
            from pages.search import Search
            return Search(self.selenium, self.base_url).wait_for_page_to_load()

        def click_options(self):
            self.wait.until(expected.visibility_of_element_located(
                self._profile_menu_locator)).click()
            self.wait.until(expected.visibility_of_element_located(
                self._dropdown_menu_locator))

        @property
        def is_logout_menu_item_present(self):
            return self.is_element_present(*self._logout_menu_item_locator)

        @property
        def is_groups_menu_item_present(self):
            return self.is_element_present(*self._groups_menu_item_locator)

        # menu items
        def click_view_profile_menu_item(self):
            self.click_options()
            self.find_element(*self._view_profile_menu_item_locator).click()
            from pages.profile import Profile
            return Profile(self.selenium, self.base_url).wait_for_page_to_load()

        def click_invite_menu_item(self):
            self.click_options()
            self.find_element(*self._invite_menu_item_locator).click()
            from pages.invite import Invite
            return Invite(self.selenium, self.base_url)

        def click_settings_menu_item(self):
            self.click_options()
            self.find_element(*self._settings_menu_item_locator).click()
            from pages.settings import Settings
            return Settings(self.selenium, self.base_url)

        def click_logout_menu_item(self):
            self.click_options()
            self.find_element(*self._logout_menu_item_locator).click()
            self.wait.until(lambda s: not self.is_logout_menu_item_present)

        def click_groups_menu_item(self):
            self.click_options()
            self.find_element(*self._groups_menu_item_locator).click()
            from pages.groups_page import GroupsPage
            return GroupsPage(self.selenium, self.base_url)

    class Footer(Page):

        _about_mozillians_link_locator = (By.CSS_SELECTOR, '.footer-nav.details > li:nth-child(1) > a')
        _language_selector_locator = (By.ID, 'language')
        _language_selection_ok_button = (By.CSS_SELECTOR, '#language-switcher button')

        def click_about_link(self):
            self.find_element(*self._about_mozillians_link_locator).click()
            from pages.about import About
            return About(self.selenium, self.base_url)

        def select_language(self, lang_code):
            element = self.find_element(*self._language_selector_locator)
            select = Select(element)
            select.select_by_value(lang_code)
