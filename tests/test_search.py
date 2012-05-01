#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.mozillians_page import MozilliansStartPage
from unittestzero import Assert
import pytest
xfail = pytest.mark.xfail


class TestSearch:

    @pytest.mark.nondestructive
    def test_search_function_only_present_for_vouched_users(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        Assert.false(home_page.is_search_box_present)
        login_page = home_page.click_login_link()
        login_page.log_in()
        Assert.true(home_page.is_search_box_present)

    @pytest.mark.nondestructive
    def test_that_search_returns_results_for_first_name(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        login_page.log_in()
        search_page = home_page.search_for("Paul")
        Assert.true(search_page.results_count > 0)

    @pytest.mark.nondestructive
    def test_that_search_returns_results_for_email_substring(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        login_page.log_in()
        search_page = home_page.search_for("@mozilla.com")
        Assert.true(search_page.results_count > 0)

    @pytest.mark.nondestructive
    def test_that_search_returns_results_for_irc_nickname(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        login_page.log_in()
        search_page = home_page.search_for("stephend")
        Assert.true(search_page.results_count > 0)

    @pytest.mark.nondestructive
    def test_search_for_no_results(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        login_page.log_in()
        search_page = home_page.search_for(".")
        Assert.true(search_page.no_results_message_shown)
