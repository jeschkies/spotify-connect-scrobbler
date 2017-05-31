#!/usr/bin/env python
import click
import dateutil.parser
from dateutil.tz import tzutc
import json

from .spotify import SpotifyClient

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


@click.command()
@click.argument('config_file', type=click.File('r'))
def main(config_file):
    """Retrieves recently played tracks from Spotify and scrobbles them to
       Last.fm.
    """
    config = json.load(config_file)

    client = SpotifyClient()
    response = client.recently_played_tracks(config['spotify'])
    tracks = [convert_to_lastfm(item) for item in response['items']]

    print(tracks)


if __name__ == "__main__":
    main()
