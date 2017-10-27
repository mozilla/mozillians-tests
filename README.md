# Tests for mozillians.org

Thank you for checking out our Mozillians test suite! This repository contains
tests for [Mozillians](https://mozillians.org/) - a community phonebook for
core contributors.

[![license](https://img.shields.io/badge/license-MPL%202.0-blue.svg)](https://github.com/mozilla/mozillians-tests/blob/master/LICENSE.txt)
[![travis](https://img.shields.io/travis/mozilla/mozillians-tests.svg?label=travis)](http://travis-ci.org/mozilla/mozillians-tests/)
[![updates](https://pyup.io/repos/github/mozilla/mozillians-tests/shield.svg)](https://pyup.io/repos/github/mozilla/mozillians-tests/)
[![Python 3](https://pyup.io/repos/github/mozilla/mozillians-tests/python-3-shield.svg)](https://pyup.io/repos/github/mozilla/mozillians-tests/)

## Table of contents:

* [Getting involved](#getting-involved)
* [How to run the tests](#how-to-run-the-tests)
* [Writing tests](#writing-tests)

## Getting involved

We love working with contributors to improve test coverage our projects, but it
does require a few skills. By contributing to our test suite you will have an
opportunity to learn and/or improve your skills with Python, Selenium
WebDriver, GitHub, virtual environments, the Page Object Model, and more.

Our [new contributor guide][guide] should help you to get started, and will
also point you in the right direction if you need to ask questions.

## How to run the tests

### Clone the repository

If you have cloned this project already then you can skip this, otherwise
you'll need to clone this repo using Git. If you do not know how to clone a
GitHub repository, check out this [help page][git clone] from GitHub.

If you think you would like to contribute to the tests by writing or
maintaining them in the future, it would be a good idea to create a fork of
this repository first, and then clone that. GitHub also has great instructions
for [forking a repository][git fork].

### Create test variables files

Some of the tests require credentials associated with account with specific
access levels. Create three username and password combinations on [staging][].

Join #commtools on IRC and ask for two of these users to be vouched (or ask
someone on #fx-test to do this for you). In one of the vouched users' profiles,
join at least one group and mark groups as private.

Create a file outside of the project (to avoid accidentally exposing the
credentials) with the following format. You will reference this file when
running the tests using the `--variables` command line option.

```json
{
  "users": {
    "vouched": {
      "email": "vouched@example.com",
      "password": "password",
      "name": "Vouched User"
    },
    "unvouched": {
      "email": "unvouced@example.com",
      "password": "password",
      "name": "Unvouched User"
    },
    "private": {
      "email": "private@example.com",
      "password": "password",
      "name": "Private User"
    }
  }
}
```

### Run the tests

You will need to [install tox][] and then set the path to your variables file
by adding it to the `PYTEST_ADDOPTS` environment variable:

```sh
$ PYTEST_ADDOPTS="--variables=/path/to/variables.json"
```

Then you can run the tests using:

```sh
$ tox
```

## Writing tests

If you want to get involved and add more tests, then there are just a few
things we'd like to ask you to do:

1. Follow our simple [style guide][].
2. Fork this project with your own GitHub account.
3. Make sure all tests are passing, and submit a pull request.
4. Always feel free to reach out to us and ask questions.

[guide]: http://firefox-test-engineering.readthedocs.io/en/latest/guide/index.html
[git clone]: https://help.github.com/articles/cloning-a-repository/
[git fork]: https://help.github.com/articles/fork-a-repo/
[staging]: https://web-mozillians-staging.production.paas.mozilla.community/
[install tox]: https://tox.readthedocs.io/en/latest/install.html
[style guide]: https://wiki.mozilla.org/QA/Execution/Web_Testing/Docs/Automation/StyleGuide
