# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import uuid
from urlparse import urlparse

import pytest


@pytest.fixture(scope='session')
def session_capabilities(pytestconfig, session_capabilities):
    if pytestconfig.getoption('driver') == 'SauceLabs':
        session_capabilities.setdefault('tags', []).append('mozillians')
    return session_capabilities


@pytest.fixture
def capabilities(request, capabilities):
    driver = request.config.getoption('driver')
    if capabilities.get('browserName', driver).lower() == 'firefox':
        capabilities['marionette'] = True
    return capabilities


@pytest.fixture
def new_email():
    return 'mozillians_{0}@restmail.net'.format(uuid.uuid1())


@pytest.fixture
def new_user(new_email):
    return {'email': new_email}


@pytest.fixture(scope='session')
def stored_users(base_url, variables):
    return variables[urlparse(base_url).hostname]['users']


@pytest.fixture(scope='function')
def vouched_user(request, stored_users):
    slave_id = getattr(request.config, 'slaveinput', {}).get('slaveid', 'gw0')
    return stored_users['vouched'][int(slave_id[2:])]


@pytest.fixture(scope='session')
def private_user(stored_users):
    return stored_users['private']


@pytest.fixture(scope='session')
def unvouched_user(stored_users):
    return stored_users['unvouched']


@pytest.fixture(scope='session')
def github_non_nda_user(stored_users):
    return stored_users['github_non_nda']
