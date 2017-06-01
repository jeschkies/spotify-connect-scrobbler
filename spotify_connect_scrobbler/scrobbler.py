#!/usr/bin/env python
import click
import dateutil.parser
from dateutil.tz import tzutc
import json
import os

from .lastfm import LastfmClient
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
    SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
    SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
    LASTFM_API_KEY = os.environ['LASTFM_API_KEY']
    LASTFM_API_SECRET = os.environ['LASTFM_API_SECRET']

    config = json.load(config_file)

    client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    response = client.recently_played_tracks(config['spotify'])
    tracks = [convert_to_lastfm(item) for item in response['items']]
    print(tracks)

    fmclient = LastfmClient(LASTFM_API_KEY, LASTFM_API_SECRET)
    scrobbles = fmclient.scrobble(tracks, config['lastfm']['session']['key'])
    print(scrobbles)


if __name__ == "__main__":
    main()
