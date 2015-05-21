# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests


@pytest.fixture
def persona_test_user():
    return requests.get('http://personatestuser.org/email/').json()


@pytest.fixture
def new_user(persona_test_user):
    user = {'email': persona_test_user['email'],
            'password': persona_test_user['pass']}
    return user


@pytest.fixture
def stored_users(variables):
    return variables['users']


@pytest.fixture
def vouched_user(stored_users):
    return stored_users['vouched']


@pytest.fixture
def private_user(stored_users):
    return stored_users['private']
