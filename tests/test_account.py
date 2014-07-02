#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.home_page import Home
from pages.link_crawler import LinkCrawler


class TestAccount:

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_login_logout(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        Assert.true(home_page.header.is_logout_menu_item_present)
        home_page.header.click_logout_menu_item()
        Assert.true(home_page.is_browserid_link_present)

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_logout_verify_bid(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        Assert.true(home_page.header.is_logout_menu_item_present)
        home_page.logout_using_url()

        home_page.wait_for_user_login()
        Assert.true(home_page.is_browserid_link_present)

    @pytest.mark.skip_selenium
    @pytest.mark.nondestructive
    def test_that_links_in_footer_return_200_code(self, mozwebqa):
        crawler = LinkCrawler(mozwebqa)
        urls = crawler.collect_links('/', name='footer')
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
