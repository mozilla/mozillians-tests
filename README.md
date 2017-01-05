Web QA Tests for mozillians.org
===============================

A community phonebook for core contributors
-------------------------------------------

Thank you for checking out Mozilla's Mozillians test suite! Mozilla and the Web
QA team are grateful for the help and hard work of many contributors like yourself.
The following contributors have submitted pull requests to mozillians-tests:

https://github.com/mozilla/mozillians-tests/contributors

[![license](https://img.shields.io/badge/license-MPL%202.0-blue.svg)](https://github.com/mozilla/mozillians-tests/tree/master#license)
[![travis](https://img.shields.io/travis/mozilla/mozillians-tests.svg?label=travis)](http://travis-ci.org/mozilla/mozillians-tests/)
[![dev](https://img.shields.io/jenkins/s/https/webqa-ci.mozilla.com/mozillians.dev.svg?label=dev)](https://webqa-ci.mozilla.com/job/mozillians.dev/)
[![stage](https://img.shields.io/jenkins/s/https/webqa-ci.mozilla.com/mozillians.stage.svg?label=stage)](https://webqa-ci.mozilla.com/job/mozillians.stage/)
[![prod](https://img.shields.io/jenkins/s/https/webqa-ci.mozilla.com/mozillians.prod.svg?label=prod)](https://webqa-ci.mozilla.com/job/mozillians.prod/)
[![updates](https://pyup.io/repos/github/mozilla/mozillians-tests/shield.svg)](https://pyup.io/repos/github/mozilla/mozillians-tests/)
[![Python 3](https://pyup.io/repos/github/mozilla/mozillians-tests/python-3-shield.svg)](https://pyup.io/repos/github/mozilla/mozillians-tests/)

Getting involved as a contributor
---------------------------------

We love working with contributors to improve the Selenium test coverage for
mozillians-tests but it does require a few skills.  You will need to be familiar
with Python, Selenium, and have a working knowledge of GitHub.

If you are comfortable with Python, it's worth having a look at the Selenium
framework to understand the basic concepts of browser-based testing and the
page objects pattern.

If you need to brush up on programming but are eager to start contributing
immediately, please consider helping out by doing manual testing.  You can
help find bugs in Mozilla [Firefox][firefox] or find bugs in the Mozilla web
sites tested by the [Web QA][webqa] team.  We have many projects that would be
thrilled to have your help!

To brush up on Python skills before engaging with us, [Dive Into Python][dive]
is an excellent resource.  MIT also has [lecture notes on Python][mit] available
through their open courseware.  The programming concepts you will need to know
include functions, working with classes, and the basics of object-oriented
programming.

Questions are always welcome
----------------------------
While we take great pains to keep our documentation updated, the best source of
information is those of us who work on the project.  Don't be afraid to join us
in irc.mozilla.org #mozwebqa to ask questions about our Selenium tests.  Mozilla
also hosts the #mozillians chat room to answer your general questions about
contributing to Mozilla.

How to set up and run Mozillians tests locally
---------------------------------------------
This repository contains Selenium tests used to test:

* development: http://mozillians-dev.allizom.org
* staging: http://mozillians.allizom.org
* production: http://mozillians.org

Mozilla maintains a guide to running Automated tests on our QMO website:

https://wiki.mozilla.org/QA/Execution/Web_Testing/Docs/Automation/

###You will need to install the following:

#### Git
If you have cloned this project already then you can skip this!
GitHub has excellent guides for [Windows][GitWin], [Mac OS X][GitMacOSX], and
[Linux][GitLinux].

#### Python
Before you will be able to run these tests you will need to have
[Python 2.6.8+][Python] installed.
[Python]: http://www.python.org/download/releases/2.6.8/

### Running tests locally

#### Credentials
Some of the tests in mozillians-tests require accounts for
https://mozillians.allizom.org. You'll need to create three sets of credentials
with varying privilege levels.

1. Create three username and password combinations on https://mozillians.allizom.org
2. Join #commtools and ask for two of these users to be vouched (or ask someone on #mozwebqa to do this for you)
3. In one of the vouched users' profiles, join at least one group and mark groups as private
4. Copy mozillians-tests/variables.json to a location outside of mozillians-tests. Update the 'vouched', 'private', and 'unvouched' users in variables.json with those credentials

* [Install Tox](https://tox.readthedocs.io/en/latest/install.html)
* Run `PYTEST_ADDOPTS="--variables=/path/to/variables.json" tox`

Writing Tests
-------------

If you want to get involved and add more tests, then there's just a few things
we'd like to ask you to do:

1. Use the [template files][GitHub Templates] for all new tests and page objects
2. Follow our simple [style guide][Style Guide]
3. Fork this project with your own GitHub account
4. Make sure all tests are passing, and submit a pull request with your changes
5. Always feel free to reach out to us and ask questions. We'll do our best to help get you started and unstuck

License
-------
This software is licensed under the [MPL] 2.0:

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.


[mit]: http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-189-a-gentle-introduction-to-programming-using-python-january-iap-2011/
[dive]: http://www.diveintopython.net/toc/index.html
[webqa]: http://quality.mozilla.org/teams/web-qa/
[firefox]: http://quality.mozilla.org/teams/desktop-firefox/
[webdriver]: http://seleniumhq.org/docs/03_webdriver.html
[mozwebqa]:http://02.chat.mibbit.com/?server=irc.mozilla.org&channel=#mozwebqa
[GitWin]: http://help.github.com/win-set-up-git/
[GitMacOSX]: http://help.github.com/mac-set-up-git/
[GitLinux]: http://help.github.com/linux-set-up-git/
[mozillians]:http://02.chat.mibbit.com/?server=irc.mozilla.org&channel=#mozillians
[venv]: http://pypi.python.org/pypi/virtualenv
[wrapper]: http://www.doughellmann.com/projects/virtualenvwrapper/
[GitHub Templates]: https://github.com/mozilla/mozwebqa-examples
[Style Guide]: https://wiki.mozilla.org/QA/Execution/Web_Testing/Docs/Automation/StyleGuide
[MPL]: http://www.mozilla.org/MPL/2.0/
