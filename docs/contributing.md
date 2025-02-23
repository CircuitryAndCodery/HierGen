# How to Contribute

The code lives at https://github/CircuitryAndCodery/HierGen

There are 2 ways to contribute but they both start with creating an issue.

Feature requests and bugfixes are the 2 types of issues that I accept. Please create
an issue in github with the one that is more appropriate. If you can provide a snippet
of code with an expected outcome and an expected outcome, that would be ideal.

## As a User

Found a bug? Want a feature? Create an bug or feature request issue.

### Bug Reporting

The best way to report a bug is to show:

* indicate:
    * the version of the package
    * the version of python
    * the name and version of the operating system
* some minimal code that is expected to run correctly
* what the expected result is
* what the actual result is--include any error messages

## As a Developer

Is there a bug or issue you would like to work on? Clone the repo, fix or implement it
and start a pull request. Ensure that you write tests that adequately test the new code. Use the coverage tool to either ensure 100% coverage or explain why it's not 100% (e.g. there is normally unreachable code that asserts or raises a developer exception). Also ensure that the documentation is adjusted accordingly. This includes docstrings and
the user documentation.

This repo uses [git flow workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow).

All branches must be named with one of the following prefixes:

    * `feature/`
    * `bugfix/`
    * `process/`
    * `test/`
    * `release/`

Pull requests are typically merged into `develop` but can be merged
into other branches. Only `feature/*`, `bugfix/*`, and `process/*` branches
can be merged into `develop`.
The `test/*` branches can be created but not merged into any branch.
Only `release/v[0-9]+\.[0-9]+\.[0-9]+` branches can be merged into `main`.

This repo uses rebase merge to merge into `develop`.

### Breaking Changes and Deprecation

This project uses semantic versioning in the form of `major.minor.patch`. The `major` version bumps when there is a breaking change that can cause existing users to change their usage
when the change takes effect. The `minor` version is used when there are new changes that
won't break existing usages. The `patch` version is uses for fixes that don't affect the
current usage or available features. When creating a pull request, please indicate if the
change is major, minor or patch level. All `major` changes must be introduced after a
a new minor change that has a deprecation warning. The time between the minor change with
the deprecation warning and the major change must be atleast 30 days.
