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
        login_page = home_page.click_browserid_link()
        Assert.true(login_page.is_csrf_token_present)
        login_page.login()
        Assert.true(home_page.is_logout_link_present)
        home_page.click_logout_menu_item()
        Assert.true(home_page.is_login_link_present)
