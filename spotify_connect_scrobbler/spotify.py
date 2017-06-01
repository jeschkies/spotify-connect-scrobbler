#!/usr/bin/env python
import base64
import os
import requests
import secrets
import sys
import urllib


class SpotifyClient:
    """ A simple client for the Spotify Web API."""

    def __init__(self, client_id, client_secret):
        """Create Spotify client.

        Args:
            client_id (str): Identifies the client and the app.
            client_secret (str): API secret.
        """
        self.__client_id = client_id
        self.__client_secret = client_secret

    def _make_authorization_headers(self):
        auth = "{}:{}".format(self.__client_id, self.__client_secret)
        auth_base64 = base64.b64encode(auth.encode('utf-8')).decode('utf-8')
        return {'Authorization': "Basic {}".format(auth_base64)}

    def request_authorization(self):
        """Returns an URL the user has to follow to authorize this app."""

        # Requests authorization
        request_secret = secrets.token_hex()
        payload = {
            'client_id': self.__client_id,
            'response_type': 'code',
            'redirect_uri': 'https://localhost:4000/steps/2',
            'scope': 'user-read-recently-played',
            'state': request_secret
        }
        params = ("{}={}".format(param, value)
                  for param, value
                  in payload.items())
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
            'client_id': self.__client_id,
            'client_secret': self.__client_secret
        }
        return requests.post(
                'https://accounts.spotify.com/api/token', data=payload).json()

    def refresh_access_token(self, refresh_token):
        """ Returns the access token for Spotify Web API using a refresh token.

        Args:
            refresh_token (string): The token has been returned by the access
            token request.

        Returns:
            dict: The response from Spotify.
        """
        # Get new auth token
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        headers = self._make_authorization_headers()
        return requests.post(
            'https://accounts.spotify.com/api/token',
            data=payload,
            headers=headers
        ).json()

    def recently_played_tracks(self, auth):
        """Query Spotify for the recently played tracks of user.

        Args:
            auth (dict): The authentication dictionary returned by Spotify.

        Returns:
            dict: A dictionary including tracks and metadata.
        """
        payload = {}
        token = "{} {}".format(auth['token_type'], auth['access_token'])
        headers = {'Authorization': token}
        response = requests.get(
            'https://api.spotify.com/v1/me/player/recently-played?limit=50',
            data=payload,
            headers=headers
        )
        if response.ok:
            return response.json()
        elif response.status_code == 401:
            print("Spotify access token expired")
            auth = self.refresh_access_token(auth['refresh_token'])
            print(auth)
            # Retry
            return self.recently_played_tracks(auth)
        else:
            print(response.text)
            sys.exit(1)


if __name__ == "__main__":
    SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
    SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']

    client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    auth_url = client.request_authorization()
    print('Go to:')
    print(auth_url)

    # Simulate redirect
    redirect_url = input('Enter the redirect URL:')
    response = urllib.parse.urlparse(redirect_url)
    query = urllib.parse.parse_qs(response.query)

    access_token = client.request_access_token(query['code'])
    print(access_token)
