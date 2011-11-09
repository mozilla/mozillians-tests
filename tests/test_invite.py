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
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Alin Trif <alin.trif@softvision.ro>
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

from pages.mozillians_page import MozilliansStartPage
from unittestzero import Assert
import pytest
xfail = pytest.mark.xfail


class TestInvite:

    def test_inviting_an_invalid_email_address(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        login_page.log_in()
        invite_page = home_page.click_invite_link()
        invite_page.invite("invalidmail")
        Assert.true(invite_page.is_invalid_mail_address_message_present)

    def test_invite(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        login_page.log_in()
        invite_page = home_page.click_invite_link()
        Assert.true(invite_page.is_csrf_token_present)
        mail_address = "validuser@example.com"
        invite_success_page = invite_page.invite(mail_address)
        Assert.true(invite_success_page.is_mail_address_present(mail_address))
        Assert.true(invite_success_page.is_success_message_present)
        Assert.true(invite_success_page.is_invite_another_mozillian_link_present)
