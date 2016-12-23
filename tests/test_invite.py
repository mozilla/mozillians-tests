#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.home_page import Home


class TestInvite:

    @pytest.mark.credentials
    def test_inviting_an_invalid_email_address(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        invite_page = home_page.header.click_invite_menu_item()
        invite_page.invite("invalidmail")
        assert 'Enter a valid email address.' == invite_page.error_text_message

    @pytest.mark.credentials
    def test_invite(self, base_url, selenium, vouched_user):
        home_page = Home(base_url, selenium)
        home_page.login(vouched_user['email'])
        invite_page = home_page.header.click_invite_menu_item()
        email_address = "user@example.com"
        invite_success_page = invite_page.invite(email_address, 'Just a bot sending a test invite to a test account.')
        assert "%s has been invited to Mozillians. They'll receive an email with instructions on how to join.\
 You can invite another Mozillian if you like." % email_address == invite_success_page.success_message
