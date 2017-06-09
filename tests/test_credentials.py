from spotify_connect_scrobbler import credentials


def test_save(tmpdir):
    creds_file_path = tmpdir.join("creds.json")

    lastfm = credentials.LastfmCredentials("some_key")
    spotify = credentials.SpotifyCredentials(
            "some_access",
            "Bearer",
            "refreshing",
            "scoping")
    creds = credentials.Credentials(lastfm, spotify)
    creds.save(creds_file_path)

    data = creds_file_path.read()
    assert data == ('{"lastfm": {"session_key": "some_key"}, '
                    '"spotify": {"access_token": "some_access", '
                    '"token_type": "Bearer", "refresh_token": "refreshing", '
                    '"scope": "scoping"}}')


def test_load():
    creds = credentials.load('tests/fixtures/credentials.json')

    assert creds.lastfm.session_key == "other_key"
    assert creds.spotify.access_token == "other_access"
    assert creds.spotify.token_type == "Bearer"
    assert creds.spotify.refresh_token == "more refreshing"
    assert creds.spotify.scope == "scoped"
