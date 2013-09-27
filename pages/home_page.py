#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.support.ui import WebDriverWait
from pages.base import Base


class Home(Base):

    def __init__(self, testsetup, open_url=True):
        Base.__init__(self, testsetup)
        self.maximize_window()
        if open_url:
            self.selenium.get(self.base_url)

    def wait_for_user_login(self):
        # waits to see if user gets logged back in
        # if not then all ok
        try:
            WebDriverWait(self.selenium, 20).until(lambda s: self.is_user_loggedin)
        except Exception:
            pass
