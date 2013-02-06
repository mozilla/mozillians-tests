#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.home_page import Home


class TestAboutPage:

    @pytest.mark.nondestructive
    def test_about_page(self, mozwebqa):
        home_page = Home(mozwebqa)
        about_mozillians_page = home_page.footer.click_about_link()
        Assert.true(about_mozillians_page.is_privacy_section_present)
        Assert.true(about_mozillians_page.is_get_involved_section_present)

    @pytest.mark.skip_selenium
    @pytest.mark.nondestructive
    def test_that_links_in_the_about_page_return_200_code(self, mozwebqa):
        import requests
        from BeautifulSoup import BeautifulSoup

        url = mozwebqa.base_url
        about_page = requests.get(url + '/about')
        parsed_html = BeautifulSoup(about_page.text)

        bad_urls = []
        urls = [anchor['href'] for anchor in parsed_html.find(id='main').findAll('a')]

        for url in urls:
            r = requests.get(url)
            if r.status_code != requests.codes.ok:
                bad_urls.append('request to %s returned %s code' % (r.url, r.status_code))
        Assert.equal(0, len(bad_urls), '%s bad links found: ' % len(bad_urls) + ', '.join(bad_urls))
