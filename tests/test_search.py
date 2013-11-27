#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from random import randrange

import pytest
from unittestzero import Assert

from pages.home_page import Home
from pages.profile import Profile


class TestSearch:

    @pytest.mark.nondestructive
    @pytest.mark.xfail("config.getvalue('base_url') == 'https://mozillians-dev.allizom.org'")
    # uncovered on dev - bug 944101 - Searching by email substring does not return all results
    def test_that_search_returns_results_for_email_substring(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        search_page = home_page.header.search_for(u'@mozilla.com')
        Assert.true(search_page.results_count > 0)

    @pytest.mark.nondestructive
    def test_that_search_returns_results_for_first_name(self, mozwebqa):
        query = u'Matt'
        home_page = Home(mozwebqa)
        home_page.login()
        search_page = home_page.header.search_for(query)
        Assert.true(search_page.results_count > 0)
        #get random index
        random_profile = randrange(search_page.results_count)
        profile_name = search_page.search_results[random_profile].name
        Assert.contains(query, profile_name)

    @pytest.mark.nondestructive
    def test_that_search_returns_results_for_irc_nickname(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        home_page.header.search_for(u'Mozillians.User')
        profile = Profile(mozwebqa)
        Assert.equal(u'Mozillians.User', profile.name)

    @pytest.mark.nondestructive
    def test_search_for_not_existing_mozillian_when_logged_in(self, mozwebqa):
        query = u'Qwerty'
        home_page = Home(mozwebqa)
        home_page.login()
        search_page = home_page.header.search_for(query)
        Assert.equal(search_page.results_count, 0)

    @pytest.mark.nondestructive
    def test_search_for_not_existing_mozillian_when_not_logged_in(self,
                                                                  mozwebqa):
        query = u'Qwerty'
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for(query)
        Assert.equal(search_page.results_count, 0)

    @pytest.mark.nondestructive
    def test_search_for_empty_string_redirects_to_search_page(self, mozwebqa):
        # Searching for empty string redirects to the Search page
        # with publicly available profiles
        query = u''
        home_page = Home(mozwebqa)
        search_page = home_page.header.search_for(query)
        Assert.true(search_page.results_count > 0)
