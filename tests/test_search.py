#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from random import randrange

import pytest
import requests

from pages.home_page import Home
from pages.profile import Profile


class TestSearch:

    @pytest.mark.xfail("'mozillians-dev' in config.getvalue('base_url')",
                       reason="Bug 944101 - Searching by email substring does not return all results")
    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_that_search_returns_results_for_email_substring(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        search_page = home_page.header.search_for(u'@mozilla.com', loggedin=True)
        assert search_page.results_count > 0

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_that_search_returns_results_for_first_name(self, base_url, selenium, vouched_user):
        query = u'Matt'
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        search_page = home_page.header.search_for(query, loggedin=True)
        assert search_page.results_count > 0
        # get random index
        random_profile = randrange(search_page.results_count)
        profile_name = search_page.search_results[random_profile].name
        assert query in profile_name

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_that_search_returns_results_for_irc_nickname(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        home_page.header.search_for(u'mbrandt', loggedin=True)
        profile = Profile(base_url, selenium)
        assert u'Matt Brandt' == profile.name

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_search_for_not_existing_mozillian_when_logged_in(self, base_url, selenium, vouched_user):
        query = u'Qwerty'
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        search_page = home_page.header.search_for(query, loggedin=True)
        assert 0 == search_page.results_count

    @pytest.mark.nondestructive
    def test_search_for_not_existing_mozillian_when_not_logged_in(self, base_url, selenium):
        query = u'Qwerty'
        home_page = Home(base_url, selenium)
        search_page = home_page.header.search_for(query)
        assert 0 == search_page.results_count

    @pytest.mark.nondestructive
    def test_search_for_empty_string_redirects_to_search_page(self, base_url, selenium):
        # Searching for empty string redirects to the Search page
        # with publicly available profiles
        query = u''
        home_page = Home(base_url, selenium)
        search_page = home_page.header.search_for(query)
        assert search_page.results_count > 0

    @pytest.mark.xfail(reason="bug 977424 - API count and actual count do not return the same values")
    @pytest.mark.nondestructive
    def test_vouched_user_count(self, base_url, selenium, variables):
        r = requests.get('https://mozillians-dev.allizom.org/api/v1/users/', params={
            'app_name': variables['api']['application'],
            'app_key': variables['api']['key'],
            'format': 'json',
            'limit': 1,
            'is_vouched': 'true'
        })

        r = r.json()

        api_count = r['meta'].get('total_count')
        home_page = Home(base_url, selenium)
        search_results = home_page.header.search_for('')
        results_on_page = search_results.results_count
        number_of_pages = int(search_results.number_of_pages)
        ui_count = results_on_page * number_of_pages

        assert (ui_count - results_on_page) < api_count < (ui_count + results_on_page), u'API Count = %s : UI Count = %s.' % (api_count, ui_count)
