#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.home_page import Home


class TestAccount:

    @pytest.mark.nondestructive
    def test_login_logout(self, mozwebqa):
        home_page = Home(mozwebqa)
        Assert.true(home_page.is_csrf_token_present)
        home_page.login()
        Assert.true(home_page.header.is_logout_menu_item_present)
        home_page.header.click_logout_menu_item()
        Assert.true(home_page.is_browserid_link_present)
