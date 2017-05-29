import dateutil.parser
from dateutil.tz import tzutc

def to_posix_timestamp(dt):
    """Converts dt to POSIX timestamp.

    Args:
        dt (datetime): The datetime object that is converted.

    Returns:
        int: The POSIX timestamp.
    """
    return int(dt.replace(tzinfo=tzutc()).timestamp())

def convert_to_lastfm(item):
    """Converts Spotify items to Last.fm tracks."""
    track = item['track']['name']
    artists = [ a['name'] for a in item['track']['artists'] ]
    played_at = to_posix_timestamp(dateutil.parser.parse(item['played_at']))

    return {'name': track, 'artists': artists, 'played_at': played_at}
