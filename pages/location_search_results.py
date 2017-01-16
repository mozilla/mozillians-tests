#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from random import randrange

from selenium.webdriver.common.by import By

from pages.base import Base
from pages.page import PageRegion


class LocationSearchResults(Base):

    _results_title_locator = (By.CSS_SELECTOR, '#main > h2')
    _result_item_locator = (By.CSS_SELECTOR, 'div.row > div.result')

    @property
    def title(self):
        return self.selenium.find_element(*self._results_title_locator).text

    @property
    def results_count(self):
        return len(self.selenium.find_elements(*self._result_item_locator))

    @property
    def search_results(self):
        return [self.SearchResult(self.base_url, self.selenium, el) for el in
                self.selenium.find_elements(*self._result_item_locator)]

    def get_random_profile(self):
        random_index = randrange(self.results_count)
        return self.search_results[random_index].open_profile_page()

    class SearchResult(PageRegion):

        _profile_page_link_locator = (By.CSS_SELECTOR, 'img')

        def open_profile_page(self):
            self._root_element.find_element(*self._profile_page_link_locator).click()
            from pages.profile import Profile
            return Profile(self.base_url, self.selenium)
