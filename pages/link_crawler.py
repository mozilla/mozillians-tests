# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
from BeautifulSoup import BeautifulSoup


class LinkCrawler(object):

    def __init__(self, base_url):
        self.base_url = base_url

    def collect_links(self, url, relative=True, name=True, **kwargs):
        """Collects links for given page URL.

        If name is True, then links will be collected for whole page.
        Use name argument to pass tag name of element.
        Use kwargs to pass id of element or its class name.
        Because 'class' is a reserved keyword in Python,
        you need to pass class as: **{'class': 'container row'}.

        Read more about searching elements with BeautifulSoup.
        See: http://goo.gl/85BuZ
        """

        # support for relative URLs
        if relative:
            url = '%s%s' % (self.base_url, url)

        # get the page and verify status code is OK
        r = requests.get(url)
        assert requests.codes.ok == r.status_code

        # collect links
        parsed_html = BeautifulSoup(r.text)
        urls = [anchor['href'] for anchor in
                parsed_html.find(name, attrs=kwargs).findAll('a')]

        # prepend base_url to relative links
        return map(
            lambda u: u if u.startswith('http') else '%s%s' % (self.base_url, u), urls)

    def verify_status_code_is_ok(self, url):
        r = requests.get(url, verify=False)
        if not r.status_code == requests.codes.ok:
            return u'{0.url} returned: {0.status_code} {0.reason}'.format(r)
        else:
            return True
