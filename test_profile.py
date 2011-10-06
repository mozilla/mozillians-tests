#!/usr/bin/env python
#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Mozilla WebQA Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

import time

from mozillians_page import MozilliansBasePage
from mozillians_page import MozilliansStartPage
from unittestzero import Assert
import pytest
xfail = pytest.mark.xfail

class TestProfile:

    def test_profile_deletion_confirmation(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        login_page.log_in()
        profile_page = home_page.click_profile_link()
        edit_profile_page = profile_page.click_edit_my_profile_button()
        confirm_profile_delete_page = edit_profile_page.click_delete_profile_button()
        Assert.true(confirm_profile_delete_page.is_csrf_token_present)
        Assert.true(confirm_profile_delete_page.is_confirm_text_present)
        Assert.true(confirm_profile_delete_page.is_cancel_button_present)
        Assert.true(confirm_profile_delete_page.is_delete_button_present)

    def test_edit_profile_information(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        login_page.log_in()
        profile_page = home_page.click_profile_link()
        edit_profile_page = profile_page.click_edit_my_profile_button()
        Assert.true(edit_profile_page.is_csrf_token_present)
        current_time = str(time.time()).split('.')[0]
        new_first_name = "Updated %s" % current_time
        new_last_name = "Mozillians User %s" % current_time
        new_biography = "Hello, I'm new here and trying stuff out. Oh, and by the way: I'm a robot, run in a cronjob, most likely, run at %s" % current_time
        new_email = edit_profile_page.email
        edit_profile_page.set_first_name(new_first_name)
        edit_profile_page.set_last_name(new_last_name)
        edit_profile_page.set_biography(new_biography)
        edit_profile_page.click_update_button()
        name = profile_page.name
        biography = profile_page.biography
        email = profile_page.email
        Assert.equal(name, new_first_name + " " + new_last_name)
        Assert.equal(biography, new_biography)
        Assert.equal(new_email, email)

    @xfail(reason="Bug 692271 - Registration with invalid form data redirects to login page in some cases")
    def test_creating_profile_with_invalid_email_address(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        register_page = home_page.click_join_us_link()
        register_page.set_email("invalidmail")
        register_page.set_password("validpassword")
        register_page.set_first_name("userwith")
        register_page.set_last_name("invalidmail")
        register_page.check_privacy_policy_checkbox()
        register_page.click_create_account_button()
        Assert.true(register_page.is_invalid_email_message_present)

    @xfail(reason="Bug 692271 - Registration with invalid form data redirects to login page in some cases")
    def test_creating_profile_with_non_matching_passwords(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        register_page = home_page.click_join_us_link()
        register_page.set_email("invalidpassword@example.com")
        register_page.set_password("passwords", "dontmatch")
        register_page.set_first_name("userwith")
        register_page.set_last_name("invalidpassword")
        register_page.check_privacy_policy_checkbox()
        register_page.click_create_account_button()
        Assert.true(register_page.is_non_matching_passwords_message_present)

    @xfail(reason="Bug 692271 - Registration with invalid form data redirects to login page in some cases")
    def test_creating_profile_without_checking_privacy_policy_checkbox(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        register_page = home_page.click_join_us_link()
        register_page.set_email("newvaliduser@example.com")
        register_page.set_password("newpassword")
        register_page.set_first_name("NewUser")
        register_page.set_last_name("DoesNotCheckBox")
        register_page.click_create_account_button()
        Assert.true(register_page.is_optin_required)