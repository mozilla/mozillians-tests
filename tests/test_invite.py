#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert

from pages.home_page import Home


class TestInvite:

    def test_inviting_an_invalid_email_address(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        invite_page = home_page.header.click_invite_menu_item()
        invite_page.invite("invalidmail")
        Assert.equal('Enter a valid e-mail address.', invite_page.error_text_message)

    def test_invite(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        invite_page = home_page.header.click_invite_menu_item()
        Assert.true(invite_page.is_csrf_token_present)
        mail_address = "validuser@example.com"
        invite_success_page = invite_page.invite(mail_address)
        Assert.equal("%s has been invited to Mozillians. They'll receive an email with instructions on how to join. You can invite another Mozillian if you like." % mail_address, invite_success_page.success_message)
