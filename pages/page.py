# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException


class Page(object):

    def __init__(self, base_url, selenium):
        self.base_url = base_url
        self.selenium = selenium
        self.timeout = 60

    @property
    def is_the_current_page(self):
        if self._page_title:
            WebDriverWait(self.selenium, self.timeout).until(lambda s: s.title)

        assert self._page_title == self.selenium.title
        return True

    def get_url_current_page(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: s.title)
        return self.selenium.current_url

    def is_element_present(self, *locator):
        self.selenium.implicitly_wait(0)
        try:
            self.selenium.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(10)

    def wait_for_element_visible(self, *locator):
        count = 0
        while not self.is_element_visible(*locator):
            time.sleep(1)
            count += 1
            if count == self.timeout:
                raise Exception(':'.join(locator) + " is not visible")

    def wait_for_element_not_visible(self, *locator):
        count = 0
        while self.is_element_visible(*locator):
            time.sleep(1)
            count += 1
            if count == self.timeout:
                raise Exception(':'.join(locator) + " is still visible")

    def wait_for_element_present(self, *locator):
        """Wait for an element to become present."""
        self.selenium.implicitly_wait(0)
        try:
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(*locator))
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(10)

    def wait_for_element_not_present(self, *locator):
        """Wait for an element to become not present."""
        self.selenium.implicitly_wait(0)
        try:
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: len(s.find_elements(*locator)) < 1)
            return True
        except TimeoutException:
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(10)

    def is_element_visible(self, *locator):
        try:
            return self.selenium.find_element(*locator).is_displayed()
        except (NoSuchElementException, ElementNotVisibleException):
            return False

    def return_to_previous_page(self):
        self.selenium.back()

    def get_relative_path(self, url):
        self.selenium.get(u'%s%s' % (self.base_url, url))


class PageRegion(Page):

    def __init__(self, base_url, selenium, root_element):
        Page.__init__(self, base_url, selenium)
        self._root_element = root_element
