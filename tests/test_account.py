#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.mozillians_page import MozilliansStartPage
from unittestzero import Assert


class TestAccount:

    @pytest.mark.nondestructive
    def test_login_logout(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        Assert.true(login_page.is_csrf_token_present)
        login_page.log_in()
        Assert.true(home_page.is_logout_link_present)
        login_page.click_logout_link()
        Assert.true(home_page.is_login_link_present)
