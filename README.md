Mozillians Tests
===================

Automated tests for the Mozillians web application.
The following contributors have submitted pull requests to Addon-Tests:

https://github.com/mozilla/mozillians-tests/contributors

Running Tests
-------------

### Java
You will need a version of the [Java Runtime Environment][JRE] installed

[JRE]: http://www.oracle.com/technetwork/java/javase/downloads/index.html

### Python
Before you will be able to run these tests, you will need to have Python 2.6 installed (or a newer, stable version).

Run

    easy_install pip

followed by

    sudo pip install -r requirements/mozwebqa.txt

__note__

If you are running on Ubuntu/Debian you will need to do following first


    sudo apt-get install python-setuptools

to install the required Python libraries.

### Selenium
Once this is all set up, you will need to download and start a Selenium server. You can download the latest Selenium server from [here][Selenium Downloads]. The filename will be something like 'selenium-server-standalone-x.x.x.jar'

To start the Selenium server run the following command:

    java -jar ~/Downloads/selenium-server-standalone-x.x.x.jar

Change the path/name to the downloaded Selenium server file.

[Selenium Downloads]: http://code.google.com/p/selenium/downloads/list

### Running tests locally

To run tests locally, it's a simple case of calling py.test from the Mozillians-tests directory
<br />You should specify the following argument for the Selenium rc: --api=rc
<br />The base URL should be a valid instance of mozillians-dev: --baseurl=http://mozillians-dev.allizom.org

    py.test --credentials=~/credentials.yaml

For other instructions type py.test --help .


Writing Tests
-------------
If you want to get involved and add more tests then there's just a few things
we'd like to ask you to do:

1. Use the [template files][GitHub Templates] for all new tests and page objects
2. Follow our simple [style guide][Style Guide]
3. Fork this project with your own GitHub account
4. Make sure all tests are passing, and submit a pull request with your changes

[GitHub Templates]: https://github.com/mozilla/mozwebqa-test-templates
[Style Guide]: https://wiki.mozilla.org/QA/Execution/Web_Testing/Docs/Automation/StyleGuide

License
-------
This software is licensed under the [MPL] 2.0:

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.

[MPL]: http://www.mozilla.org/MPL/2.0/