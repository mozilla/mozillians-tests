#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.mozillians_page import MozilliansStartPage
from unittestzero import Assert
import pytest
xfail = pytest.mark.xfail


class TestInvite:

    @pytest.mark.nondestructive
    def test_inviting_an_invalid_email_address(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        login_page.log_in()
        home_page.open_profile_menu()
        invite_page = home_page.click_invite_menu_item()
        invite_page.invite("invalidmail")
        Assert.true(invite_page.is_invalid_mail_address_message_present)

    @pytest.mark.nondestructive
    def test_invite(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        login_page.log_in()
        home_page.open_profile_menu()
        invite_page = home_page.click_invite_menu_item()
        Assert.true(invite_page.is_csrf_token_present)
        mail_address = "validuser@example.com"
        invite_success_page = invite_page.invite(mail_address)
        Assert.true(invite_success_page.is_mail_address_present(mail_address))
        Assert.true(invite_success_page.is_success_message_present)
        Assert.true(invite_success_page.is_invite_another_mozillian_link_present)
