#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

import pytest
from selenium.webdriver.common.by import By

from pages.home_page import Home
from pages.link_crawler import LinkCrawler


class TestProfile:

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_profile_deletion_confirmation(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        settings = home_page.header.click_settings_menu_item()

        delete_form = settings.profile.delete_account

        assert not delete_form.is_delete_button_enabled

        delete_form.check_acknowledgement()

        assert delete_form.is_delete_button_enabled

        confirm_profile_delete_page = delete_form.click_delete_profile()
        assert confirm_profile_delete_page.is_confirm_text_present
        assert confirm_profile_delete_page.is_cancel_button_present
        assert confirm_profile_delete_page.is_delete_button_present

    @pytest.mark.credentials
    def test_edit_profile_information(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        settings = home_page.header.click_settings_menu_item()
        current_time = str(time.time()).split('.')[0]

        # New profile data
        new_full_name = "Updated Mozillians User %s" % current_time
        new_biography = "Hello, I'm new here and trying stuff out. Oh, and by the way: I'm a robot, run in a cronjob, most likely, run at %s" % current_time

        profile_basic_info = settings.profile.basic_information

        # Update the profile fields
        profile_basic_info.set_full_name(new_full_name)
        profile_basic_info.set_bio(new_biography)
        profile_basic_info.click_update()

        profile_page = home_page.header.click_view_profile_menu_item()

        # Check that everything was updated
        assert new_full_name == profile_page.name
        assert new_biography == profile_page.biography

    @pytest.mark.credentials
    def test_skill_addition(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])

        settings = home_page.header.click_settings_menu_item()
        skills_form = settings.profile.skills
        skills_form.add_skill("Hello World")
        skills_form.click_update()

        profile_page = home_page.header.click_view_profile_menu_item()

        assert profile_page.is_skills_present
        skills = profile_page.skills
        assert skills.find("hello world") >= 0

    @pytest.mark.credentials
    def test_skill_deletion(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])

        settings = home_page.header.click_settings_menu_item()
        skills_form = settings.profile.skills
        skills_form.add_skill("Hello World")
        skills_form.click_update()

        settings = home_page.header.click_settings_menu_item()
        skills_form = settings.profile.skills
        skills = skills_form.skills

        skill_delete_buttons = skills_form.delete_skill_buttons
        skill_delete_buttons[skills.index("hello world")].click()
        skills_form.click_update()

        profile_page = home_page.header.click_view_profile_menu_item()

        if profile_page.is_skills_present:
            skills = profile_page.skills
            assert -1 == skills.find("hello world")

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_that_filter_by_city_works(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])

        profile_page = home_page.open_user_profile(u'Mozillians.User')
        city = profile_page.city
        country = profile_page.country

        search_results_page = profile_page.click_profile_city_filter()
        expected_results_title = u'Mozillians in %s, %s' % (city, country)
        actual_results_title = search_results_page.title

        assert expected_results_title == actual_results_title

        random_profile = search_results_page.get_random_profile()
        assert city == random_profile.city

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_that_filter_by_region_works(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])

        profile_page = home_page.open_user_profile(u'Mozillians.User')
        region = profile_page.region
        country = profile_page.country
        search_results_page = profile_page.click_profile_region_filter()
        expected_results_title = u'Mozillians in %s, %s' % (region, country)
        actual_results_title = search_results_page.title

        assert expected_results_title == actual_results_title

        random_profile = search_results_page.get_random_profile()
        assert region == random_profile.region

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_that_filter_by_country_works(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])

        profile_page = home_page.open_user_profile(u'Mozillians.User')
        country = profile_page.country
        search_results_page = profile_page.click_profile_country_filter()
        expected_results_title = u'Mozillians in %s' % country
        actual_results_title = search_results_page.title

        assert expected_results_title == actual_results_title

        random_profile = search_results_page.get_random_profile()
        assert country == random_profile.country

    @pytest.mark.credentials
    def test_that_non_us_user_can_set_get_involved_date(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        settings = home_page.go_to_localized_settings_page("es")
        contributions = settings.you_and_mozilla.contributions
        selected_date = contributions.month + contributions.year
        contributions.select_random_month()
        contributions.select_random_year()
        contributions.click_update()

        profile_page = home_page.header.click_view_profile_menu_item()

        assert "Tu perfil" == profile_page.profile_message
        settings = home_page.go_to_localized_settings_page("es")
        contributions = settings.you_and_mozilla.contributions
        assert selected_date != contributions.month + contributions.year

    @pytest.mark.credentials
    def test_that_user_can_create_and_delete_group(self, base_url, selenium, vouched_user):
        group_name = (time.strftime('%x-%X'))

        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        settings = home_page.header.click_settings_menu_item()
        groups = settings.groups.click_find_group_link()
        create_group = groups.click_create_group_main_button()
        create_group.create_group_name(group_name)
        create_group.click_create_group_submit()

        search_listings = create_group.header.search_for(group_name)

        assert search_listings.is_element_present(By.LINK_TEXT, group_name)

        group_info = search_listings.open_group(group_name)
        groups_page = group_info.delete_group()
        groups_page.wait_for_alert_message()

        home_page.header.click_settings_menu_item()

        assert not search_listings.is_element_present(By.LINK_TEXT, group_name)

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_private_groups_field_as_public_when_logged_in(self, base_url, selenium, private_user):
        # User has certain fields preset to values to run the test properly
        # groups - private
        # belongs to at least one group
        home_page = Home(base_url, selenium)
        home_page.login(private_user['email'])

        profile_page = home_page.header.click_view_profile_menu_item()
        profile_page.view_profile_as('Public')
        assert not profile_page.is_groups_present

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_private_groups_field_when_not_logged_in(self, base_url, selenium, private_user):
        home_page = Home(base_url, selenium)
        profile_page = home_page.open_user_profile(private_user['name'])
        assert not profile_page.is_groups_present

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_that_links_in_the_services_page_return_200_code(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])

        settings = home_page.header.click_settings_menu_item()
        developer = settings.developer
        crawler = LinkCrawler(base_url)
        urls = developer.get_services_urls()
        bad_urls = []

        assert len(urls) > 0

        for url in urls:
            check_result = crawler.verify_status_code_is_ok(url)
            if check_result is not True:
                bad_urls.append(check_result)

        assert 0 == len(bad_urls), u'%s bad links found. ' % len(bad_urls) + ', '.join(bad_urls)

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_that_user_can_view_external_accounts(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        settings = home_page.header.click_settings_menu_item()

        assert settings.external_accounts.irc_form.is_displayed
        assert settings.external_accounts.external_accounts_form.is_displayed

    @pytest.mark.credentials
    def test_that_user_can_add_external_account(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        settings = home_page.header.click_settings_menu_item()

        external_accounts_form = settings.external_accounts.external_accounts_form
        cnt_external_accounts = external_accounts_form.count_external_accounts()
        external_accounts_form.click_add_account()
        new_cnt_external_accounts = external_accounts_form.count_external_accounts()
        assert (cnt_external_accounts + 1) == new_cnt_external_accounts

    @pytest.mark.credentials
    def test_that_user_can_modify_external_accounts_irc_nickname(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        settings = home_page.header.click_settings_menu_item()

        irc_form = settings.external_accounts.irc_form
        old_nickname = irc_form.nickname
        new_nickname = old_nickname + '_'
        irc_form.update_nickname(new_nickname)
        irc_form.click_update()

        profile_page = home_page.header.click_view_profile_menu_item()
        assert new_nickname == profile_page.irc_nickname

        settings = home_page.header.click_settings_menu_item()
        irc_form = settings.external_accounts.irc_form
        irc_form.update_nickname(old_nickname)
        irc_form.click_update()

        profile_page = home_page.header.click_view_profile_menu_item()
        assert old_nickname == profile_page.irc_nickname

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_new_user_cannot_see_groups_or_functional_areas(self, base_url, selenium, unvouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(unvouched_user['email'])

        assert not home_page.header.is_groups_menu_item_present
        assert not home_page.is_groups_link_visible
        assert not home_page.is_functional_areas_link_visible

        settings = home_page.header.click_settings_menu_item()
        assert not settings.groups.is_find_group_link_visible
