#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.home_page import Home
from unittestzero import Assert
import pytest


class TestInvite:

    @pytest.mark.nondestructive
    def test_inviting_an_invalid_email_address(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        invite_page = home_page.header.click_invite_menu_item()
        invite_page.invite("invalidmail")
        Assert.equal('Enter a valid e-mail address.', invite_page.error_text_message)

    @pytest.mark.nondestructive
    def test_invite(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        invite_page = home_page.header.click_invite_menu_item()
        Assert.true(invite_page.is_csrf_token_present)
        mail_address = "validuser@example.com"
        invite_success_page = invite_page.invite(mail_address)
        Assert.contains(mail_address, invite_success_page.success_message_body)
        Assert.equal('Invitation Sent!', invite_success_page.success_message_header)
        Assert.true(invite_success_page.is_invite_another_mozillian_link_present)
