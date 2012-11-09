#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
import pytest
from unittestzero import Assert

from pages.home_page import Home
from pages.register import ProfileTab
from tests.base_test import BaseTest


class TestProfile(BaseTest):

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
        new_website = "http://%s.com/" % current_time
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

    @pytest.mark.xfail(reason="Bug 797790 - Create Your Profile page privacy policy error message is ambiguous")
    def test_creating_profile_without_checking_privacy_policy_checkbox(self, mozwebqa):
        user = self.get_new_user()

        home_page = Home(mozwebqa)

        profile = home_page.create_new_user(user)

        profile.set_first_name("User that doesn't like policy")
        profile.set_last_name("MozilliansUser")
        profile.set_bio("Hello, I'm new here and trying stuff out. Oh, and by the way: I'm a robot, run in a cronjob, and will not check accept the privacy policy")

        skills = profile.click_next_button()
        skills.add_skill('test')
        skills.add_language('english')

        location = skills.click_next_button()
        location.select_country('United States')
        location.set_state('California')
        location.set_city('Mountain View')

        location.click_create_profile_button()

        profile = ProfileTab(mozwebqa)

        Assert.equal('new error message', profile.error_message)
        location = profile.go_to_tab('location')
        Assert.equal('This field is required.', location.privacy_error_message)

    def test_profile_creation(self, mozwebqa):
        user = self.get_new_user()

        home_page = Home(mozwebqa)

        profile = home_page.create_new_user(user)

        profile.set_first_name("New")
        profile.set_last_name("MozilliansUser")
        profile.set_bio("Hello, I'm new here and trying stuff out. Oh, and by the way: I'm a robot, run in a cronjob, most likely")

        skills = profile.click_next_button()
        skills.add_skill('test')
        skills.add_language('english')

        location = skills.click_next_button()
        location.select_country('us')
        location.set_state('California')
        location.set_city('Mountain View')
        location.check_privacy()

        profile_page = location.click_create_profile_button()

        Assert.true(profile_page.was_account_created_successfully)
        Assert.true(profile_page.is_pending_approval_visible)

        Assert.equal('New MozilliansUser', profile_page.name)
        Assert.equal(user['email'], profile_page.email)
        Assert.equal("Hello, I'm new here and trying stuff out. Oh, and by the way: I'm a robot, run in a cronjob, most likely", profile_page.biography)
        Assert.equal('test', profile_page.skills)
        Assert.equal('english', profile_page.languages)
        Assert.equal('Mountain View, California\nUnited States', profile_page.location)
