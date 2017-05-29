from datetime import datetime
from dateutil.tz import tzutc
from spotify_connect_scrobbler.scrobbler import to_posix_timestamp

def test_datetime_conversion():
    dt = datetime(2015, 3, 14, 9, 26, 53, tzinfo=tzutc())
    ts = to_posix_timestamp(dt)
    assert ts == 1426325213
