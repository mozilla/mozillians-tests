#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests
from unittestzero import Assert


xfail = pytest.mark.xfail


@pytest.mark.skip_selenium
class TestRedirects:

    _urls = ['/es/country/us/',
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

    #@pytest.mark.xfail(reason='Disabled until Bug 846039 is fixed')
    @pytest.mark.skip_selenium
    @pytest.mark.nondestructive
    def test_302_redirect_for_anonomous_users(self, mozwebqa):
        error_list = []
        for resource in self._urls:
            url = mozwebqa.base_url + resource

            # prevent redirects - we only want to check the value of the
            # firest HTTP code.
            response = requests.get(url, allow_redirects=False)
            if response.status_code != requests.codes.found:
                error_list.append('Expected 302 but got %s. %s' %
                                  (response.status_code, response.url))

        Assert.equal(0, len(error_list), error_list)
