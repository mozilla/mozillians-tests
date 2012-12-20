#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.home_page import Home
from pages.profile import Profile


@pytest.mark.xfail(reason="Bug 822543 - No search results on Mozillians dev")
# https://bugzilla.mozilla.org/show_bug.cgi?id=822543
class TestSearch:
    @pytest.mark.nondestructive
    def test_that_search_returns_results_for_city(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        search_page = home_page.header.search_for("Mountain View")
        Assert.true(search_page.results_count > 0)

    @pytest.mark.nondestructive
    def test_that_search_returns_results_for_country(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        search_page = home_page.header.search_for("Romania")
        Assert.true(search_page.results_count > 0)

    @pytest.mark.nondestructive
    def test_that_search_returns_results_for_email_substring(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        search_page = home_page.header.search_for("@mozilla.com")
        Assert.true(search_page.results_count > 0)

    @pytest.mark.nondestructive
    def test_that_search_returns_results_for_first_name(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        search_page = home_page.header.search_for("Paul")
        Assert.true(search_page.results_count > 0)

    @pytest.mark.nondestructive
    def test_that_search_returns_results_for_irc_nickname(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        home_page.header.search_for("stephend")
        profile = Profile(mozwebqa)
        Assert.equal("Stephen Donner", profile.name)

    @pytest.mark.nondestructive
    def test_that_search_returns_results_for_region(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        search_page = home_page.header.search_for("California")
        Assert.true(search_page.results_count > 0)

    @pytest.mark.nondestructive
    def test_search_function_only_present_for_vouched_users(self, mozwebqa):
        home_page = Home(mozwebqa)
        Assert.false(home_page.header.is_search_box_present)
        home_page.login()
        Assert.true(home_page.header.is_search_box_present)

    @pytest.mark.nondestructive
    def test_search_for_no_results(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        search_page = home_page.header.search_for(",")
        Assert.contains('Sorry, we cannot find a group or person related to ",".', search_page.no_results_message_head)  # changed '.' => to ',' as workaround for selenium issue 4608
        Assert.equal("Maybe they're not a Mozillian yet? Invite this person to create a profile.", search_page.no_results_message_body)
