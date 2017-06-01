from spotify_connect_scrobbler.spotify import SpotifyClient


def test_make_authorization_headers():
    client = SpotifyClient("some_id", "very_secret")
    headers = client._make_authorization_headers()
    assert headers['Authorization'] == "Basic c29tZV9pZDp2ZXJ5X3NlY3JldA=="
