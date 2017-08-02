#!/usr/bin/env python
import click
import os
import urllib

from .credentials import Credentials
from .lastfm import LastfmClient
from .spotify import SpotifyClient


@click.command()
@click.argument('credentials_file', type=click.Path(exists=False))
def main(credentials_file):
    """Authenticates with Spotify and Last.fm APIs.

    The authentication credentials are saved to the credentials file.
    """
    SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
    SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
    LASTFM_API_KEY = os.environ['LASTFM_API_KEY']
    LASTFM_API_SECRET = os.environ['LASTFM_API_SECRET']

    # Direct user to authentication Spotify URL.
    spotify_client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    auth_url = spotify_client.request_authorization(
            'https://localhost:4000/steps/2')
    click.echo('Go to: {}'.format(auth_url))

    # Simulate redirect
    redirect_url = click.prompt('Enter the redirect URL', type=str)
    response = urllib.parse.urlparse(redirect_url)
    query = urllib.parse.parse_qs(response.query)

    # Retrieve credentials.
    spotify_credentials = spotify_client.request_access_token(
            query['code'], 'https://localhost:4000/steps/2')

    # Direct user to authentication Spotify URL.
    lastfm_client = LastfmClient(LASTFM_API_KEY, LASTFM_API_SECRET)
    auth_url = lastfm_client.request_authorization(
            'https://localhost:4000/steps/3')
    click.echo('Go to: {}'.format(auth_url))

    # Simulate redirect
    redirect_url = click.prompt('Enter the redirect URL', type=str)
    response = urllib.parse.urlparse(redirect_url)
    query = urllib.parse.parse_qs(response.query)

    # Retrieve credentials.
    lastfm_credentials = lastfm_client.request_access_token(query['token'][0])

    # Save credentials
    credentials = Credentials(lastfm_credentials, spotify_credentials)
    credentials.save(credentials_file)
    click.echo('Saved authentication to {}'.format(credentials_file))


if __name__ == "__main__":
    main()
