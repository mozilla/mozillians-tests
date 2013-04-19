#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests
from unittestzero import Assert


@pytest.mark.skip_selenium
class TestRedirects:

    _paths = ['/es/country/us/',
             '/sq/country/doesnotexist/',
             '/ar/country/us/region/California/',
             '/pl/country/us/city/',
             '/zh-TW/group/webqa/',
             '/zh-CN/group/258-l10n/toggle/',
             '/sl/group/doesnotexit/',
             '/rl/u/MozilliansUser/',
             '/pt-BR/u/moz.mozillians.unvouched/',
             '/ca/u/UserDoesNotExist',
             '/nl/logout/',
             '/lt/user/edit/',
             '/en-US/invite/']

    @pytest.mark.xfail(reason='Disabled until Bug 846039 is fixed')
    @pytest.mark.nondestructive
    def test_302_redirect_for_anonomous_users(self, mozwebqa):
        urls = self.make_absolute_paths(mozwebqa.base_url, self._paths)
        error_list = self.verify_http_response_codes(urls, 302)

        Assert.equal(0, len(error_list), error_list)

    @pytest.mark.xfail(reason='Bug 846039 - Create additional authorization-state-specific routing rules')
    @pytest.mark.nondestructive
    def test_200_for_anonymous_users(self, mozwebqa):
        paths = ['/pl/opensearch.xml', '/nl/u/MozilliansUser/']
        urls = self.make_absolute_paths(mozwebqa.base_url, paths)
        error_list = self.verify_http_response_codes(urls, 200)

        Assert.equal(len(error_list), 0, error_list)

    def make_absolute_paths(self, url, paths):
        urls = []
        for path in paths:
            urls.append(url + path)
        return urls

    def verify_http_response_codes(self, urls, expected_http_value):
        error_list = []
        for url in urls:
            # prevent redirects, we only want the value of the 1st HTTP status
            response = requests.get(url, allow_redirects=False)
            http_status = response.status_code
            if http_status != expected_http_value:
                error_list.append('Expected %s but got %s. %s' %
                                  (expected_http_value, http_status, url))
        return error_list
