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

    * `feature/cchg-[issue #]-[short-description]`
    * `bugfix/cchg-[issue #]-[short-description]`
    * `process/*`
    * `test/*`
    * `release/v[M].[m].[p]`

Pull requests are typically merged into `develop` but can be merged
into other branches. Only `feature/*`, `bugfix/*`, and `process/*` branches
can be merged into `develop`.
The `test/*` branches can be created but not merged into any branch.
Only `release/[0-9]+\.[0-9]+\.[0-9]+` branches can be merged into `main`.

This repo uses rebase merge to merge into `develop`.

Once the repo is cloned, run:

``` bash
$ make sync precommit
```

### Release Process

To make a release, examine the release note lines in README.md that are in the `unreleased` section. These should have an issue followed by major|minor|patch. Find the most severe one to determine the next version, create a section with that version, and copy these to (minus the major|minor|patch) to that section.

Create a branch called `release/{major}.{minor}.{patch}` off develop, bump the version in version.py, and adjust the test/version_test.py. Ensure that all test pass.

Start two pull requests to merge into both `main` and develop.

Once merged, tag the commit in main to `v{major}.{minor}.{patch}` and push the tag. This will push the changes to `pypi` and a stable `readthedocs.io`.


### Breaking Changes and Deprecation

This project uses semantic versioning in the form of `major.minor.patch`. The `major` version bumps when there is a breaking change that can cause existing users to change their usage
when the change takes effect. The `minor` version is used when there are new changes that
won't break existing usages. The `patch` version is uses for fixes that don't affect the
current usage or available features. When creating a pull request, please indicate if the
change is major, minor or patch level. All `major` changes must be introduced after a
a new minor change that has a deprecation warning. The time between the minor change with
the deprecation warning and the major change must be atleast 30 days.

### Pushing a branch

Use the precommit hooks to ensure that the tests all pass. They can
also be run with:

``` bash
$ make check-pre-commit
```

### Starting a Pull Request

Ensure that the README.md `Release Notes` section has a short
description in the `- unreleased` list. These will be copied to
a release tag in the release branch. They should be in the format:

```
# Release Notes
## unreleased
  - IssueNumber major|minor|patch Description of change
## 0.0.3
  - Initial commit
```

## GitHub Actions

This repo uses github actions to validate the code and manage releases.

### On Push Branch

Pushing a branch starts all of the usual tests. They don't need to pass,
but they can be used to direct further work on the branch. It is, nevertheless
recommended that the user run `make check-pre-commit` when getting ready to
push work that is expected to be in good condition.

### On Push Tag

Pushing a tag is generally how releases are made. The tag name is verified by
ensuring its format and then the major minor patch are compared against the
__version__.py. If all is well, the push to testpypi and pypi begin.

### On Pull Request

Starting a pull request starts the same tests as pushing a branch if it's
pushing into develop, a release, or support branch. It also
ensures that the branch being merged into is not main. It is always
allowed to do a pull request for merging into a feature or bugfix branch.
