# A Spotify Connect Scrobbler

[![Build Status](https://travis-ci.org/jeschkies/spotify-connect-scrobbler.svg?branch=master)](https://travis-ci.org/jeschkies/spotify-connect-scrobbler) [![codecov](https://codecov.io/gh/jeschkies/spotify-connect-scrobbler/branch/master/graph/badge.svg)](https://codecov.io/gh/jeschkies/spotify-connect-scrobbler)

A Small Webservice That Scrobbles Spotify Connect Plays

# Setup

The best way to run this scrobbler is with [virtualenv](https://virtualenv.pypa.io).
Assuming you have already virtualenv and Python 3.6 installed, create a new environment

  ```bash
  virtualenv <path to env> --python=python3.6
  ```

Activate the environment and install the scrobbler from git:

  ```bash
  cd <path to env>
  source bin/activate
  pip install git+https://github.com/jeschkies/spotify-connect-scrobbler.git
  ```

Verify that the scrobbler is avialable:

  ```bash
  scrobbler --help
  ```

Call `deactivate` to deactivate the environment.

# Build Instructions

We use tox for building and testing. Just install and run tox

  ```
  pip install tox
  tox
  ```
