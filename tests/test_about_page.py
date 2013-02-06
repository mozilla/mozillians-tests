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

        links = [a['href'] for a in parsed_html.find(id='main').findAll('a')]
        for link in links:
            r = requests.get(link)
            Assert.true(
                r.status_code == requests.codes.ok,
                'request to %s returned %s code' % (r.url, r.status_code))
