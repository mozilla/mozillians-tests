#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.home_page import Home
from unittestzero import Assert
import pytest


class TestSearch:

    @pytest.mark.nondestructive
    def test_search_function_only_present_for_vouched_users(self, mozwebqa):
        home_page = Home(mozwebqa)
        Assert.false(home_page.header.is_search_box_present)
        home_page.login()
        Assert.true(home_page.header.is_search_box_present)

    @pytest.mark.nondestructive
    def test_that_search_returns_results_for_first_name(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        search_page = home_page.header.search_for("Paul")
        Assert.true(search_page.results_count > 0)

    @pytest.mark.nondestructive
    def test_that_search_returns_results_for_email_substring(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        search_page = home_page.header.search_for("@mozilla.com")
        Assert.true(search_page.results_count > 0)

    @pytest.mark.nondestructive
    @pytest.mark.xfail(reason="github issue #20")
    def test_that_search_returns_results_for_irc_nickname(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        search_page = home_page.header.search_for("stephend")
        Assert.true(search_page.results_count > 0)

    @pytest.mark.nondestructive
    def test_search_for_no_results(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        search_page = home_page.header.search_for(",")
        Assert.contains('Sorry, we cannot find a group or person related to ",".', search_page.no_results_message_head)
        Assert.equal("Maybe they're not a Mozillian yet? Invite this person to create a profile.", search_page.no_results_message_body)
