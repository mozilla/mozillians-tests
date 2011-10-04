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
# The Original Code is Crash Tests Selenium Tests.
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

from mozillians_page import MozilliansBasePage
from mozillians_page import MozilliansStartPage
from unittestzero import Assert
import pytest

class TestAccount:

    def test_login_with_invalid_credentials(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        login_page.log_in("username@invalid.tld", "invalidpass")
        Assert.true(login_page.is_invalid_credentials_text_present)

    def test_login_with_invalid_ldap_credentials(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        login_page.log_in("username@mozilla.com", "invalidpass")
        Assert.true(login_page.is_invalid_credentials_text_present)

    def test_reset_password(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        password_reset_page = login_page.click_forgot_password_link()
        Assert.true(password_reset_page.is_reset_password_button_present)
        Assert.true(password_reset_page.is_email_field_present)
        password_reset_page.reset_password()
        Assert.true(password_reset_page.is_password_reset_sent_text_present)

    def test_profile_deletion_confirmation(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        login_page.log_in()
        profile_page = home_page.click_profile_link()
        edit_profile_page = profile_page.click_edit_my_profile_button()
        confirm_profile_delete_page = edit_profile_page.click_delete_profile_button()
        Assert.true(confirm_profile_delete_page.is_confirm_text_present)
        Assert.true(confirm_profile_delete_page.is_cancel_button_present)
        Assert.true(confirm_profile_delete_page.is_delete_button_present)
