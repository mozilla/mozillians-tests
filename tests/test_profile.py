#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
import pytest
from unittestzero import Assert

from pages.home_page import Home
from tests.base_test import BaseTest


class TestProfile(BaseTest):

    @pytest.mark.nondestructive
    def test_profile_deletion_confirmation(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        edit_profile_page = home_page.header.click_edit_profile_menu_item()
        confirm_profile_delete_page = edit_profile_page.click_delete_profile_button()
        Assert.true(confirm_profile_delete_page.is_csrf_token_present)
        Assert.true(confirm_profile_delete_page.is_confirm_text_present)
        Assert.true(confirm_profile_delete_page.is_cancel_button_present)
        Assert.true(confirm_profile_delete_page.is_delete_button_present)

    def test_edit_profile_information(self, mozwebqa):
        home_page = Home(mozwebqa)

        home_page.login()

        profile_page = home_page.header.click_view_profile_menu_item()
        edit_profile_page = home_page.header.click_edit_profile_menu_item()
        Assert.true(edit_profile_page.is_csrf_token_present)
        current_time = str(time.time()).split('.')[0]

        # New profile data
        new_full_name = "Updated Mozillians User %s" % current_time
        new_biography = "Hello, I'm new here and trying stuff out. Oh, and by the way: I'm a robot, run in a cronjob, most likely, run at %s" % current_time
        new_website = "http://%s.com/" % current_time

        # Update the profile fields
        edit_profile_page.set_full_name(new_full_name)
        edit_profile_page.set_website(new_website)
        edit_profile_page.set_bio(new_biography)
        edit_profile_page.click_update_button()

        # Get the current data of profile fields
        name = profile_page.name
        biography = profile_page.biography
        website = profile_page.website

        # Check that everything was updated
        Assert.equal(name, new_full_name)
        Assert.equal(biography, new_biography)
        Assert.equal(website, new_website)

    def test_creating_profile_without_checking_privacy_policy_checkbox(self, mozwebqa):
        user = self.get_new_user()

        home_page = Home(mozwebqa)

        profile = home_page.create_new_user(user)

        profile.set_full_name("User that doesn't like policy")
        profile.set_bio("Hello, I'm new here and trying stuff out. Oh, and by the way: I'm a robot, run in a cronjob, and will not check accept the privacy policy")

        # Skills
        profile.add_skill('test')
        profile.add_language('english')

        # Location
        profile.select_country('us')
        profile.set_state('California')
        profile.set_city('Mountain View')

        profile.click_create_profile_button()

        Assert.equal('Please correct the errors below.', profile.error_message)

    def test_profile_creation(self, mozwebqa):
        user = self.get_new_user()

        home_page = Home(mozwebqa)

        profile = home_page.create_new_user(user)

        profile.set_full_name("New MozilliansUser")
        profile.set_bio("Hello, I'm new here and trying stuff out. Oh, and by the way: I'm a robot, run in a cronjob, most likely")

        # Skills
        profile.add_skill('test')
        profile.add_language('english')

        # Location
        profile.select_country('us')
        profile.set_state('California')
        profile.set_city('Mountain View')
        profile.check_privacy()

        profile_page = profile.click_create_profile_button()

        Assert.true(profile_page.was_account_created_successfully)
        Assert.true(profile_page.is_pending_approval_visible)

        Assert.equal('New MozilliansUser', profile_page.name)
        Assert.equal(user['email'], profile_page.email)
        Assert.equal("Hello, I'm new here and trying stuff out. Oh, and by the way: I'm a robot, run in a cronjob, most likely", profile_page.biography)
        Assert.equal('test', profile_page.skills)
        Assert.equal('english', profile_page.languages)
        Assert.equal('Mountain View, California, United States', profile_page.location)

    @pytest.mark.xfail(reason="Bug   - Error adding groups / skills / or languages with non-latin chars.")
    def test_non_ascii_characters_are_allowed_in_profile_information(self, mozwebqa):
        user = self.get_new_user()

        home_page = Home(mozwebqa)
        profile = home_page.create_new_user(user)

        profile.set_full_name("New MozilliansUser")
        profile.set_bio("Hello, I'm new here and trying stuff out. Oh, and by the way: I'm a robot, run in a cronjob, most likely")

        # Skills
        profile.add_skill(u'\u0394\u03D4\u03D5\u03D7\u03C7\u03C9\u03CA\u03E2')
        profile.add_language(u'\u0394\u03D4\u03D5\u03D7\u03C7\u03C9\u03CA\u03E2')

        # Location
        profile.select_country('gr')
        profile.set_state('Greece')
        profile.set_city('Athens')
        profile.check_privacy()

        profile_page = profile.click_create_profile_button()

        Assert.true(profile_page.was_account_created_successfully)
        Assert.true(profile_page.is_pending_approval_visible)

        Assert.equal('New MozilliansUser', profile_page.name)
        Assert.equal(user['email'], profile_page.email)
        Assert.equal("Hello, I'm new here and trying stuff out. Oh, and by the way: I'm a robot, run in a cronjob, most likely", profile_page.biography)
        Assert.equal(u'\u0394\u03D4\u03D5\u03D7\u03C7\u03C9\u03CA\u03E2', profile_page.skills)
        Assert.equal(u'\u0394\u03D4\u03D5\u03D7\u03C7\u03C9\u03CA\u03E2', profile_page.languages)
        Assert.equal('Athenes, Greece, Greece', profile_page.location)

    @pytest.mark.nondestructive
    def test_that_filter_by_city_works(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()

        profile_page = home_page.open_user_profile(u'Mozillians.User')
        city = profile_page.city
        country = profile_page.country
        search_results_page = profile_page.click_city_name(city=city, country=country)
        expected_results_title = u'Mozillians in %s, %s' % (city, country)
        actual_results_title = search_results_page.title

        Assert.true(search_results_page.is_the_current_page)
        Assert.equal(
            expected_results_title, actual_results_title,
            u'''Search results title is incorrect.
                Expected: %s, but got: %s''' % (expected_results_title, actual_results_title))

        random_profile = search_results_page.get_random_profile()
        random_profile_city = random_profile.city

        Assert.equal(
            city, random_profile_city,
            u'Expected city: %s, but got: %s' % (city, random_profile_city))

    @pytest.mark.nondestructive
    def test_that_filter_by_region_works(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()

        profile_page = home_page.open_user_profile(u'Mozillians.User')
        region = profile_page.region
        country = profile_page.country
        search_results_page = profile_page.click_region_name(region=region, country=country)
        expected_results_title = u'Mozillians in %s, %s' % (region, country)
        actual_results_title = search_results_page.title

        Assert.true(search_results_page.is_the_current_page)
        Assert.equal(
            expected_results_title, actual_results_title,
            u'''Search results title is incorrect.
                Expected: %s, but got: %s''' % (expected_results_title, actual_results_title))

        random_profile = search_results_page.get_random_profile()
        random_profile_region = random_profile.region

        Assert.equal(
            region, random_profile_region,
            u'Expected region: %s, but got: %s' % (region, random_profile_region))

    @pytest.mark.nondestructive
    def test_that_filter_by_county_works(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()

        profile_page = home_page.open_user_profile(u'Mozillians.User')
        country = profile_page.country
        search_results_page = profile_page.click_country_name(country=country)
        expected_results_title = u'Mozillians in %s' % country
        actual_results_title = search_results_page.title

        Assert.true(search_results_page.is_the_current_page)
        Assert.equal(
            expected_results_title, actual_results_title,
            u'''Search results title is incorrect.
                Expected: %s, but got: %s''' % (expected_results_title, actual_results_title))

        random_profile = search_results_page.get_random_profile()
        random_profile_country = random_profile.country

        Assert.equal(
            country, random_profile_country,
            u'Expected country: %s, but got: %s' % (country, random_profile_country))
