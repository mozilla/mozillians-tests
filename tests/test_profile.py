#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from pages.home_page import Home
from unittestzero import Assert
import pytest


class TestProfile:

    @pytest.mark.nondestructive
    def test_profile_deletion_confirmation(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        profile_page = home_page.header.click_view_profile_menu_item()
        edit_profile_page = profile_page.click_edit_my_profile_button()
        account_tab = edit_profile_page.go_to_tab("account")
        confirm_profile_delete_page = account_tab.click_delete_profile_button()
        Assert.true(confirm_profile_delete_page.is_csrf_token_present)
        Assert.true(confirm_profile_delete_page.is_confirm_text_present)
        Assert.true(confirm_profile_delete_page.is_cancel_button_present)
        Assert.true(confirm_profile_delete_page.is_delete_button_present)

    @pytest.mark.xfail(reason="Bug 794035 - Editing profile URL with http://1348571949.com returns a invalid url")
    def test_edit_profile_information(self, mozwebqa):
        home_page = Home(mozwebqa)

        home_page.login()

        profile_page = home_page.header.click_view_profile_menu_item()
        edit_profile_page = profile_page.click_edit_my_profile_button()
        profile_tab = edit_profile_page.go_to_tab("profile")
        Assert.true(edit_profile_page.is_csrf_token_present)
        current_time = str(time.time()).split('.')[0]
        new_first_name = "Updated %s" % current_time
        new_last_name = "Mozillians User %s" % current_time
        new_biography = "Hello, I'm new here and trying stuff out. Oh, and by the way: I'm a robot, run in a cronjob, most likely, run at %s" % current_time
        new_website = "http://%s.com" % current_time
        profile_tab.set_first_name(new_first_name)
        profile_tab.set_last_name(new_last_name)
        profile_tab.set_website(new_website)
        profile_tab.set_bio(new_biography)
        profile_tab.click_update_button()
        name = profile_page.name
        biography = profile_page.biography
        website = profile_page.website
        Assert.equal(name, new_first_name + " " + new_last_name)
        Assert.equal(biography, new_biography)
        Assert.equal(website, new_website)

    @pytest.mark.nondestructive
    def test_browserid_link_present(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        profile_page = home_page.header.click_view_profile_menu_item()
        edit_profile_page = profile_page.click_edit_my_profile_button()
        account_tab = edit_profile_page.go_to_tab("account")
        Assert.true(account_tab.is_browserid_link_present)

    @pytest.mark.xfail(reason="Needs to be updated for browserid")
    def test_creating_profile_with_invalid_email_address(self, mozwebqa):
        home_page = Home(mozwebqa)
        register_page = home_page.click_join_us_link()
        register_page.set_email("invalidmail")
        register_page.set_password("validpassword")
        register_page.set_first_name("userwith")
        register_page.set_last_name("invalidmail")
        register_page.check_privacy_policy_checkbox()
        register_page.click_create_account_button()
        Assert.true(register_page.is_invalid_email_message_present)

    @pytest.mark.xfail(reason="Shouldn't be needed anymore with browserid")
    def test_creating_profile_with_non_matching_passwords(self, mozwebqa):
        home_page = Home(mozwebqa)
        register_page = home_page.click_join_us_link()
        register_page.set_email("invalidpassword@example.com")
        register_page.set_password("passwords", "dontmatch")
        register_page.set_first_name("userwith")
        register_page.set_last_name("invalidpassword")
        register_page.check_privacy_policy_checkbox()
        register_page.click_create_account_button()
        Assert.true(register_page.is_non_matching_passwords_message_present)

    @pytest.mark.xfail(reason="Needs to be updated for browserid")
    def test_creating_profile_without_checking_privacy_policy_checkbox(self, mozwebqa):
        home_page = Home(mozwebqa)
        register_page = home_page.click_join_us_link()
        register_page.set_email("newvaliduser@example.com")
        register_page.set_password("newpassword")
        register_page.set_first_name("NewUser")
        register_page.set_last_name("DoesNotCheckBox")
        register_page.click_create_account_button()
        Assert.true(register_page.is_optin_required)

    @pytest.mark.xfail(reason="needs to be updated for browserid")
    def test_profile_creation(self, mozwebqa):
        home_page = Home(mozwebqa)
        register_page = home_page.click_join_us_link()
        register_page.set_email("newvaliduserwith@example.com")
        register_page.set_password("newpassword")
        register_page.set_first_name("New")
        register_page.set_last_name("MozilliansUser")
        register_page.check_privacy_policy_checkbox()
        login_page = register_page.click_create_account_button()
        Assert.true(login_page.is_account_needs_verification_message_present)
