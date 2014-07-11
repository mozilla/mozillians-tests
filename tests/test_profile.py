#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import time

from unittestzero import Assert
from selenium.webdriver.common.by import By
from pages.home_page import Home
from pages.link_crawler import LinkCrawler
from tests.base_test import BaseTest


class TestProfile(BaseTest):

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_profile_deletion_confirmation(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        edit_profile_page = home_page.header.click_edit_profile_menu_item()
        confirm_profile_delete_page = edit_profile_page.click_delete_profile_button()
        Assert.true(confirm_profile_delete_page.is_confirm_text_present)
        Assert.true(confirm_profile_delete_page.is_cancel_button_present)
        Assert.true(confirm_profile_delete_page.is_delete_button_present)

    @pytest.mark.credentials
    def test_edit_profile_information(self, mozwebqa):
        home_page = Home(mozwebqa)

        home_page.login()

        profile_page = home_page.header.click_view_profile_menu_item()
        edit_profile_page = home_page.header.click_edit_profile_menu_item()
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

    @pytest.mark.xfail("'allizom' in config.getvalue('base_url')",
                       reason="Bug 938184 - Users should not create, join, or leave groups from the profile create/edit screens")
    @pytest.mark.credentials
    def test_group_addition(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()

        edit_profile_page = home_page.header.click_edit_profile_menu_item()
        edit_profile_page.add_group("Hello World")
        profile_page = edit_profile_page.click_update_button()

        Assert.true(profile_page.is_groups_present, "No groups added to profile.")
        groups = profile_page.groups
        Assert.greater(groups.find("hello world"), -1, "Group 'Hello World' not added to profile.")

    @pytest.mark.xfail("'allizom' in config.getvalue('base_url')",
                       reason="Bug 938184 - Users should not create, join, or leave groups from the profile create/edit screens")
    @pytest.mark.credentials
    def test_group_deletion(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()

        edit_profile_page = home_page.header.click_edit_profile_menu_item()
        edit_profile_page.add_group("Hello World")
        profile_page = edit_profile_page.click_update_button()
        edit_profile_page = profile_page.header.click_edit_profile_menu_item()

        groups = edit_profile_page.groups
        group_delete_buttons = edit_profile_page.delete_group_buttons
        group_delete_buttons[groups.index("hello world")].click()
        profile_page = edit_profile_page.click_update_button()

        if profile_page.is_groups_present:
            groups = profile_page.groups
            Assert.equal(groups.find("hello world"), -1, "Group 'hello world' not deleted.")

    @pytest.mark.credentials
    def test_skill_addition(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()

        edit_profile_page = home_page.header.click_edit_profile_menu_item()
        edit_profile_page.add_skill("Hello World")
        profile_page = edit_profile_page.click_update_button()

        Assert.true(profile_page.is_skills_present, "No skills added to profile.")
        skills = profile_page.skills
        Assert.greater(skills.find("hello world"), -1, "Skill 'hello world' not added to profile.")

    @pytest.mark.credentials
    def test_skill_deletion(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()

        edit_profile_page = home_page.header.click_edit_profile_menu_item()
        edit_profile_page.add_skill("Hello World")
        profile_page = edit_profile_page.click_update_button()
        edit_profile_page = profile_page.header.click_edit_profile_menu_item()

        skills = edit_profile_page.skills
        skill_delete_buttons = edit_profile_page.delete_skill_buttons
        skill_delete_buttons[skills.index("hello world")].click()

        if profile_page.is_skills_present:
            skills = profile_page.skills
            Assert.equal(skills.find("hello world"), -1, "Skill 'hello world' not deleted.")

    def test_creating_profile_without_checking_privacy_policy_checkbox(self, mozwebqa):
        user = self.get_new_user()

        home_page = Home(mozwebqa)

        profile = home_page.create_new_user(user)

        profile.set_full_name("User that doesn't like policy")
        profile.set_bio("Hello, I'm new here and trying stuff out. Oh, and by the way: I'm a robot, run in a cronjob, and will not check accept the privacy policy")

        # Skills
        profile.add_skill('test')
        profile.select_language('en')

        # Location
        profile.set_location('Durango, Colorado')

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
        profile.select_language('en')

        # Location
        profile.set_location('Mountain View, California')

        # agreed to privacy policy
        profile.check_privacy()

        profile_page = profile.click_create_profile_button()

        Assert.true(profile_page.was_account_created_successfully)
        Assert.true(profile_page.is_pending_approval_visible)

        Assert.equal('New MozilliansUser', profile_page.name)
        Assert.equal(user['email'], profile_page.email)
        Assert.equal("Hello, I'm new here and trying stuff out. Oh, and by the way: I'm a robot, run in a cronjob, most likely", profile_page.biography)
        Assert.equal('test', profile_page.skills)
        Assert.equal('English', profile_page.languages)
        Assert.equal('Mountain View, California, United States', profile_page.location)

    @pytest.mark.xfail(reason="Bug 835318 - Error adding groups / skills / or languages with non-latin chars.")
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
        profile.set_location('Athens, Greece')

        # agreed to privacy policy
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

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_that_filter_by_city_works(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()

        profile_page = home_page.open_user_profile(u'Mozillians.User')
        city = profile_page.city
        country = profile_page.country

        search_results_page = profile_page.click_profile_city_filter()
        expected_results_title = u'Mozillians in %s, %s' % (city, country)
        actual_results_title = search_results_page.title

        Assert.equal(
            expected_results_title, actual_results_title,
            u'''Search results title is incorrect.
                Expected: %s, but got: %s''' % (expected_results_title, actual_results_title))

        random_profile = search_results_page.get_random_profile()
        random_profile_city = random_profile.city

        Assert.equal(
            city, random_profile_city,
            u'Expected city: %s, but got: %s' % (city, random_profile_city))

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_that_filter_by_region_works(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()

        profile_page = home_page.open_user_profile(u'Mozillians.User')
        region = profile_page.region
        country = profile_page.country
        search_results_page = profile_page.click_profile_region_filter()
        expected_results_title = u'Mozillians in %s, %s' % (region, country)
        actual_results_title = search_results_page.title

        Assert.equal(
            expected_results_title, actual_results_title,
            u'''Search results title is incorrect.
                Expected: %s, but got: %s''' % (expected_results_title, actual_results_title))

        random_profile = search_results_page.get_random_profile()
        random_profile_region = random_profile.region

        Assert.equal(
            region, random_profile_region,
            u'Expected region: %s, but got: %s' % (region, random_profile_region))

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_that_filter_by_country_works(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()

        profile_page = home_page.open_user_profile(u'Mozillians.User')
        country = profile_page.country
        search_results_page = profile_page.click_profile_country_filter()
        expected_results_title = u'Mozillians in %s' % country
        actual_results_title = search_results_page.title

        Assert.equal(
            expected_results_title, actual_results_title,
            u'''Search results title is incorrect.
                Expected: %s, but got: %s''' % (expected_results_title, actual_results_title))

        random_profile = search_results_page.get_random_profile()
        random_profile_country = random_profile.country

        Assert.equal(
            country, random_profile_country,
            u'Expected country: %s, but got: %s' % (country, random_profile_country))

    @pytest.mark.credentials
    def test_that_non_US_user_can_set_get_involved_date(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        edit_page = home_page.go_to_localized_edit_profile_page("es")
        selected_date = edit_page.month + edit_page.year
        edit_page.select_random_month()
        edit_page.select_random_year()
        profile_page = edit_page.click_update_button()
        Assert.equal(profile_page.profile_message, "Tu perfil")
        edit_page = profile_page.header.click_edit_profile_menu_item()
        Assert.not_equal(selected_date, edit_page.month + edit_page.year, "The date is not changed")

    @pytest.mark.credentials
    def test_that_user_can_create_and_delete_group(self, mozwebqa):
        current_time = time.strftime("%x"+"-"+"%X")
        group_name = ('qa_test' + ' ' + current_time)

        home_page = Home(mozwebqa)
        home_page.login()
        edit_page = home_page.header.click_edit_profile_menu_item()
        groups = edit_page.click_find_group_link()
        create_group = groups.click_create_group_main_button()
        create_group.create_group_name(group_name)
        create_group.click_create_group_submit()

        search_listings = create_group.header.search_for(group_name)

        Assert.true(search_listings.is_element_present(By.LINK_TEXT, group_name))

        group_info = search_listings.open_group(group_name)
        groups_page = group_info.delete_group()
        groups_page.wait_for_alert_message()

        home_page.header.click_edit_profile_menu_item()

        Assert.false(search_listings.is_element_present(By.LINK_TEXT, group_name))

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_private_groups_field_as_public_when_logged_in(self, mozwebqa):
        home_page = Home(mozwebqa)
        # User has certain fields preset to values to run the test properly
            # groups - private
            # belongs to at least one group
        credentials = mozwebqa.credentials['vouched_with_private_fields']

        home_page.login('vouched_with_private_fields')
        profile_page = home_page.header.click_view_profile_menu_item()
        profile_page.view_profile_as('Public')

        Assert.false(profile_page.is_groups_present,
                     u'Profile: ' + profile_page.get_url_current_page())

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_private_groups_field_when_not_logged_in(self, mozwebqa):
        credentials = mozwebqa.credentials['vouched_with_private_fields']
        home_page = Home(mozwebqa)
        profile_page = home_page.open_user_profile(credentials['name'])

        Assert.false(profile_page.is_groups_present,
                     u'Profile: ' + profile_page.get_url_current_page())

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_that_links_in_the_services_page_return_200_code(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()

        edit_profile_page = home_page.header.click_edit_profile_menu_item()
        crawler = LinkCrawler(mozwebqa)
        urls = edit_profile_page.get_services_urls()
        bad_urls = []

        Assert.greater(
            len(urls), 0, u'something went wrong. no links found.')

        for url in urls:
            check_result = crawler.verify_status_code_is_ok(url)
            if check_result is not True:
                bad_urls.append(check_result)

        Assert.equal(
            0, len(bad_urls),
            u'%s bad links found. ' % len(bad_urls) + ', '.join(bad_urls))
