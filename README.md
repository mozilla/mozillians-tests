Web QA Tests for mozillians.org
===============================

A community phonebook for core contributors
-------------------------------------------

Thank you for checking out Mozilla's Mozillians test suite! Mozilla and the Web
QA team are grateful for the help and hard work of many contributors like yourself.
The following contributors have submitted pull requests to mozillians-tests:

https://github.com/mozilla/mozillians-tests/contributors

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

How to setup and run Mozillians tests locally
---------------------------------------------
This repository contains Selenium tests used to test:

* development: http://mozillians-dev.allizom.org
* staging: http://mozillians.allizom.org
* production: http://mozillian.org

Mozilla maintains a guide to running Automated tests on our QMO website:

https://quality.mozilla.org/docs/webqa/running-webqa-automated-tests/

This wiki page has some advanced instructions specific to Windows:

https://wiki.mozilla.org/QA_SoftVision_Team/WebQA_Automation


###You will need to install the following:

#### Git
If you have cloned this project already then you can skip this!
GitHub has excellent guides for [Windows][GitWin], [MacOSX][GitMacOSX], and
[Linux][GitLinux].

#### Python
Before you will be able to run these tests you will need to have
[Python 2.6][Python] installed.
[Python]: http://www.python.org/download/releases/2.6.6/

####Virtualenv and Virtualenvwrapper (Optional/Intermediate level)
While most of us have had some experience using virtual machines, 
[virtualenv][venv] is something else entirely.  It's used to keep libraries
that you install from clashing and messing up your local environment.  After
installing virtualenv, installing [virtualenvwrapper][wrapper] will give you
some nice commands to use with virtualenvwrapper. [virtualenv][venv] will allow
you to install Python modules and run your tests in a sandboxed environment. 

__note__

This is not necessary but is really helpful if you are working on multiple
Python projects that use different versions of modules.

Run

    easy_install pip

followed by

    sudo pip install -r requirements/mozwebqa.txt

#### Submodules
Be sure to retrieve and initialize the git submodules:

    git submodule update --init

__note__

If you are running on Ubuntu/Debian you will need to do following first

    sudo apt-get install python-setuptools

to install the required Python libraries.

#### Credentials
Some of the tests in mozillians-tests require accounts for 
https://mozillians.allizom.org. You'll need to create three sets of credentials
with varying privilege levels.

1. Create three username and password combinations on https://mozillians.allizom.org
2. Join #commtools and ask for one of these users to be vouched (or ask someone on #mozwebqa to do this for you)
3. Copy mozillians-tests/credentials.yaml to a location outside of mozillians-tests. Update the 'user', 'unvouched', and 'unconfirmed' users in credentials.yaml with those credentials

#### Running tests locally
Before each test run, clean up the repo:
    find . \( -name 'results*' -or -name '*.pyc' \) -print0 | xargs -0 rm -Rf

To run tests locally it is as simple as calling <code>py.test</code> with
several flags. To run testcases that do not modify or delete data:

    py.test --driver=firefox --baseurl=http://mozillians.allizom.org --credentials=/full/path/to/credentials.yaml .

To run testcases that are known to change or delete account data use the
<code>--destructive</code> flag:

    py.test --driver=firefox --baseurl=http://mozillians.allizom.org --destructive --credentials=/full/path/to/credentials.yaml .

__Output__

Output of a test run should look something like this:

    ============================= test session starts ==============================
    collected 15 items 

    tests/test_about_page.py ..
    tests/test_account.py ..
    tests/test_invite.py ..
    tests/test_profile.py ...x.x
    tests/test_search.py ...
    ==================== 13 passed, 2 xpassed in 172.03 seconds ====================

__Note__
"~" will not resolve to the home directory when used in the py.test command line.

Some options for py.test are pre-specified by the file mozillians-tests/mozwebqa.cfg

The mozwebqa plugin has advanced command line options for reporting and using
browsers. See the documentation on [davehunt's pytest mozwebqa github][pymozwebqa].
[pymozwebqa]: https://github.com/davehunt/pytest-mozwebqa

__Troubleshooting__

If the test run hangs with Firefox open but no URL gets entered in the address
box, some combination of the Firefox version, and the python Selenium bindings
version may not be compatible. Upgrading each of them to latest should fix it.

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
[GitHub Templates]: https://github.com/mozilla/mozwebqa-test-templates
[Style Guide]: https://wiki.mozilla.org/QA/Execution/Web_Testing/Docs/Automation/StyleGuide
[MPL]: http://www.mozilla.org/MPL/2.0/
