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

from mozillians_page import MozilliansStartPage
from unittestzero import Assert
import pytest
xfail = pytest.mark.xfail

class TestSearch:

    def test_search_function_only_present_for_vouched_users(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        Assert.false(home_page.is_search_box_present)
        login_page = home_page.click_login_link()
        login_page.log_in()
        Assert.true(home_page.is_search_box_present)

    def test_that_search_returns_results_for_first_name(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        login_page.log_in()
        search_page = home_page.search_for("Paul")
        Assert.true(search_page.results_count > 0)

    def test_that_search_returns_results_for_email_substring(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        login_page.log_in()
        search_page = home_page.search_for("@mozilla.com")
        Assert.true(search_page.results_count > 0)

    @xfail(reason="Searching by email field is currently unsupported, see Bug 690551")
    def test_that_search_returns_results_for_email_substring(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        login_page.log_in()
        search_page = home_page.search_for("stephend")
        Assert.true(search_page.results_count > 0)

    @xfail(reason="Too few accounts on stage and trunk to be triggering this message")
    def test_search_for_too_many_results(self, mozwebqa):
        home_page = MozilliansStartPage(mozwebqa)
        login_page = home_page.click_login_link()
        login_page.log_in()
        search_page = home_page.search_for(".")
        Assert.true(search_page.too_many_results_message_shown)
