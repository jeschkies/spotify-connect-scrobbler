from datetime import datetime
from dateutil.tz import tzutc
import json
import pytest
from spotify_connect_scrobbler.scrobbler import to_posix_timestamp, convert_to_lastfm

@pytest.fixture
def recently_played_response():
    """JSON response object from Spotify recently-played call."""
    with open('tests/fixtures/recently_played.json', 'r') as f:
        yield json.load(f)

def test_datetime_conversion():
    dt = datetime(2015, 3, 14, 9, 26, 53, tzinfo=tzutc())
    ts = to_posix_timestamp(dt)
    assert ts == 1426325213

def test_convert_to_lastfm(recently_played_response):
    tracks = [ convert_to_lastfm(i) for i in recently_played_response['items'] ]

    assert tracks[0]['name'] == "Disciples"
    assert tracks[0]['artists'] == ["Tame Impala"]
    assert tracks[0]['played_at'] == 1481661844

    assert tracks[1]['name'] == "Let It Happen"
    assert tracks[1]['artists'] == ["Tame Impala"]
    assert tracks[1]['played_at'] == 1481661737
