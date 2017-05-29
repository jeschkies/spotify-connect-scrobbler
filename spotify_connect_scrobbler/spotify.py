#!/usr/bin/env python
import os
import requests
import secrets
import urllib

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']

class SpotifyClient:
    """ A simple client for the Spotify Web API."""

    def request_authorization(self):
        """Returns an URL the user has to follow to authorize this app."""

        # Requests authorization
        request_secret = secrets.token_hex()
        payload = {
            'client_id': SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': 'https://localhost:4000/steps/2',
            'scope': 'user-read-recently-played',
            'state': request_secret
        }
        params = ("{}={}".format(param, value) for param, value in payload.items())
        auth_url = 'https://accounts.spotify.com/authorize?{}'.format(
                '&'.join(params))
        return auth_url


    def request_access_token(self, code):
        """ Returns the access token for Spotify Web API.

        Args:
            code (string): The code passed by the authorization redirect.

        Returns:
            dict: The response from Spotify.
        """

        # Get auth token
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'https://localhost:4000/steps/2',
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET
        }
        return requests.post(
                'https://accounts.spotify.com/api/token', data=payload).json()


    def recently_played_tracks():
        # Query Spotify for the recently played tracks of user.
        payload = {}
        headers = {'Authorization': '<ACCESS TOKEN>'}
        response = requests.get(
                'https://api.spotify.com/v1/me/player/recently-played',
                data=payload, headers=headers).json()
        for item in response['items']:
            track = item['track']['name']
            artists = [ a['name'] for a in item['track']['artists'] ]
            played_at = int(dateutil.parser.parse(item['played_at']).replace(tzinfo=tzutc()).timestamp())
            print("{} by {} at {} ".format(track, ', '.join(artists), played_at))


if __name__ == "__main__":
    client = SpotifyClient()
    auth_url = client.request_authorization()
    print('Go to:')
    print(auth_url)

    # Simulate redirect
    redirect_url = input('Enter the redirect URL:')
    response = urllib.parse.urlparse(redirect_url)
    query = urllib.parse.parse_qs(response.query)

    access_token = client.request_access_token(query['code'])
    print(access_token)
