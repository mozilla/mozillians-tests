#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert
from pages.home_page import Home


class TestRegister:

    @pytest.mark.xfail("'mozillians.allizom' in config.getvalue('base_url')",
                       reason="Bug 1129848 - Registration UI redesign not yet deployed on stage")
    def test_profile_creation(self, base_url, selenium, new_user):
        home_page = Home(base_url, selenium)
        profile = home_page.create_new_user(new_user['email'], new_user['password'])

        profile.set_full_name("New MozilliansUser")

        # Location
        profile.set_location('Mountain View, 94041, California')

        # agreed to privacy policy
        profile.check_privacy()

        profile_page = profile.click_create_profile_button()

        Assert.true(profile_page.was_account_created_successfully)
        Assert.true(profile_page.is_pending_approval_visible)

        Assert.equal('New MozilliansUser', profile_page.name)
        Assert.equal(new_user['email'], profile_page.email)
        Assert.equal('Mountain View, California, United States', profile_page.location)

    @pytest.mark.xfail("'mozillians.allizom' in config.getvalue('base_url')",
                       reason="Bug 1129848 - Registration UI redesign not yet deployed on stage")
    def test_creating_profile_without_checking_privacy_policy_checkbox(self, base_url, selenium, new_user):
        home_page = Home(base_url, selenium)
        profile = home_page.create_new_user(new_user['email'], new_user['password'])

        profile.set_full_name("User that doesn't like policy")

        # Location
        profile.set_location('Durango, Colorado')

        profile.click_create_profile_button()

        Assert.equal('Please correct the errors below.', profile.error_message)
