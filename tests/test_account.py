#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.home_page import Home
from pages.link_crawler import LinkCrawler


class TestAccount:

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_login_logout(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        assert home_page.header.is_logout_menu_item_present
        home_page.header.click_logout_menu_item()
        assert home_page.is_sign_in_button_present

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_logout_verify_bid(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        assert home_page.header.is_logout_menu_item_present
        home_page.logout_using_url()

        home_page.wait_for_user_login()
        assert home_page.is_sign_in_button_present

    @pytest.mark.nondestructive
    def test_that_links_in_footer_return_200_code(self, base_url):
        crawler = LinkCrawler(base_url)
        urls = crawler.collect_links('/', name='footer')
        bad_urls = []

        assert len(urls) > 0

        for url in urls:
            check_result = crawler.verify_status_code_is_ok(url)
            if check_result is not True:
                bad_urls.append(check_result)

        assert 0 == len(bad_urls), u'%s bad links found. ' % len(bad_urls) + ', '.join(bad_urls)
