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
# Contributor(s): Bebe <florin.strugariu@softvision.ro>
#                 Teodosia Pop <teodosia.pop@softvision.ro>
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


from page import Page

class BrowserID(Page):

    _pop_up_id = '_mozid_signin'
    _email_locator = 'id=email'
    _password_locator = 'id=password'

    _log_in_button_locator = 'css=button.returning'
    _next_button_locator = 'css=button.start'
    _sign_in_locator = 'id=signInButton'

    def __init__(self, testsetup):
        Page.__init__(self, testsetup)
        self.selenium.wait_for_pop_up(self._pop_up_id, self.timeout)
        self.selenium.select_pop_up(self._pop_up_id)

    def login_browser_id(self, credentials):
        self.wait_for_element_visible(self._email_locator)

        self.selenium.type(self._email_locator, credentials['email'])
        self.selenium.click(self._next_button_locator)
        self.wait_for_element_visible(self._password_locator)

        self.selenium.type(self._password_locator, credentials['password'])
        self.selenium.click(self._log_in_button_locator)

    def sign_in(self):
        self.wait_for_element_visible(self._sign_in_locator)
        self.selenium.click(self._sign_in_locator)

        self.selenium.deselect_pop_up()
