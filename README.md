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

The scrobbler requires access tokens to the Spotify web API and Last.fm API.
You authenticate your account with

  ```
  SPOTIFY_CLIENT_ID=<Your app ID> \
  SPOTIFY_CLIENT_SECRET=<Your app secret> \
  spotify <path to credentials file>

  LASTFM_API_KEY=<Your app key> \
  LASTFM_API_SECRET=<Your app secret>
  lastfm <path to credentials file>
  ```

After you've followed the instructions the access tokens are saved to the
credentials file you've specified.

# Build Instructions

We use tox for building and testing. Just install and run tox

  ```
  pip install tox
  tox
  ```
