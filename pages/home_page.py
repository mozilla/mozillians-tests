#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from pages.base import Base

class Home(Base):

    def __init__(self, testsetup, open_url=True):
        Base.__init__(self, testsetup)
        if open_url:
            self.selenium.get(self.base_url)

    def go_to_localized_edit_profile_page(self, non_US):
        self.get_relative_path("/" + non_US + "/user/edit/")
        from pages.edit_profile import EditProfile
        return EditProfile(self.testsetup)
