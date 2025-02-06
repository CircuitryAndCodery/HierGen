# How to Contribute

The code lives at https://github/CircuitryAndCodery/HierGen.git

There are 2 ways to contribute but they both start with creating an issue.

Feature requests and bugfixes are the 2 types of issues that I accept. Please create
an issue in github with the one that is more appropriate. If you can provide a snippet
of code with an expected outcome and an expected outcome, that would be ideal.

## As a User

Found a bug? Want a feature? Create an bug or feature request issue.

### Bug Reporting

The best way to report a bug is to show:

* indicate the version of the package and the version of python
* some minimal code that should run
* what the expected result is
* what the actual result is

## As a Developer

Is there a bug or issue you would like to work on? Clone the repo, fix or implement it
and start a pull request. Ensure that you write tests that adequately test the new code. Use the coverage tool to either ensure 100% coverage or explain why it's not 100% (e.g. there is normally unreachable code that asserts or raises a developer exception). Also ensure that the documentation is adjusted accordingly. This includes docstrings and
the user documentation.

### Breaking Changes and Deprecation

This project uses semantic versioning in the form of `major.minor.patch`. The `major` version bumps when there is a breaking change that can cause existing users to change their usage
when the change takes effect. The `minor` version is used when there are new changes that
won't break existing usages. The `patch` version is uses for fixes that don't affect the
current usage or available features. When creating a pull request, please indicate if the
change is major, minor or patch level. All `major` changes must be introduced after a
a new minor change that has a deprecation warning. The time between the minor change with
the deprecation warning and the major change must be atleast 30 days.
