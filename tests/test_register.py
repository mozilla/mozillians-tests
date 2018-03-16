# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.home_page import Home


class TestRegister:

    def test_profile_creation(self, base_url, selenium, new_user):
        home_page = Home(selenium, base_url).open()
        profile = home_page.create_new_user(new_user['email'])

        # Click recaptcha box
        profile.check_recaptcha()

        # Full name
        profile.set_full_name("New MozilliansUser")

        # Location
        profile.select_country("United States")
        profile.select_region("California")
        profile.select_city("Mountain View")

        # Agree to privacy policy
        profile.check_privacy()

        profile_page = profile.click_create_profile_button()

        assert profile_page.was_account_created_successfully
        assert profile_page.is_pending_approval_visible

        assert 'New MozilliansUser' == profile_page.name
        assert new_user['email'] == profile_page.email
        assert 'Mountain View, California, United States' == profile_page.location

    def test_creating_profile_without_checking_privacy_policy_checkbox(self, base_url, selenium, new_user):
        home_page = Home(selenium, base_url).open()
        profile = home_page.create_new_user(new_user['email'])

        profile.set_full_name("User that doesn't like policy")

        # Location
        profile.select_country("United States")
        profile.select_region("Colorado")
        profile.select_city("Durango")

        # Click recaptcha box
        profile.check_recaptcha()

        profile = profile.click_create_profile_button(leavepage=False)
        assert 'Please check this box if you want to proceed.' == profile.privacy_error_message
